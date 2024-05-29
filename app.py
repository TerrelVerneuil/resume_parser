#this is a machine learning project that will parse resumes

#different types of NLP models

#1. Heuristic-based NLP models
#2. Stastical Machine learning-based NLP models
#3. Neural Network-based NLP models

# this is a resume parser we should look at the
# the most specific information in the resume in
# order to get the most relevant information
# and hire the best candidate for the position based on
# the specifications.
# I should be able to mass import resumes and get the 
# top 5 candidates for the position


#credit to the authors of the book
# Bird, Steven, Edward Loper and Ewan Klein (2009), 
# Natural Language Processing with Python. O’Reilly 
# Media Inc.

# most common ways employers look at is keyword matching.
# many resumes are shortlist because of just keyword matching
# I will make a fair alternative that checks all criteria
from flask import Flask, render_template, request
from collections import defaultdict
import torch
import os
import PyPDF2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize, word_tokenize

from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from werkzeug.utils import secure_filename
from flask import send_from_directory




app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/download/<filename>')
def download_resume(filename):
    folder_name = secure_filename(request.form.get('folder_name', 'default_folder'))
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    return send_from_directory(folder_path, filename)

def get_use_embeddings(text):
    embeddings = model.encode(text)
    return np.array(embeddings)

def preprocess_text(text):
    sentences = sent_tokenize(text)
    tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]
    return tokenized_sentences
#convert the pdf to text

def pdf_to_text(pdf_path, output_txt): 
    # Open the PDF file in read-binary mode
    # should get it directly from
    # the file upload section

    with open(pdf_path, 'rb') as pdf_file:
        #I should use this when woking with files
        #the python with keyword is used when working
        #with unmanaged resources like file streams
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # Initialize an empty string to store the text
        text = ''
        # Loop through each page in the PDF file
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

#this is the first step in the process
#parse the text to get the most relevant information

#text to string
def text_to_string(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    # Join the sentences into a single string
    text = ' '.join(sentences)
    return text
# token_resumes = []
# word_token = []
resumes = []
for i in range(1, 10):
    with open('resume_' + str(i) + '.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        tokenized_text = preprocess_text(text)
        embeddings = get_use_embeddings([text])
        resumes.append((text, tokenized_text, embeddings))


# print(resumes)
#compare the information to the job description
def extract_keywords(text):
    # print("Input text:", repr(text))  # Print the input text
    # Rest of the function code...
    vectorizer = TfidfVectorizer(stop_words='english')
    text_list = [text]
    tfidf_matrix = vectorizer.fit_transform(text_list)
    feature_array = np.array(vectorizer.get_feature_names_out())
    tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
    top_n = feature_array[tfidf_sorting][:10]
    return set(top_n)
# embeddings_np = np.array(embeddings)
# print(embeddings_np)
# dict = {}
# print(token_resumes[0])
def extract_skills_section(text):
    # This function extracts the skills section from the resume text
    skill_keywords = ["skills", "expertise", "proficiencies", "technologies", "competencies"]
    lines = text.split('\n')
    skills_text = ""
    recording = False
    for line in lines:
        if any(keyword in line.lower() for keyword in skill_keywords):
            recording = True
            skills_text += line + " "
        elif recording and line.strip() == "":
            break
        elif recording:
            skills_text += line + " "
    return skills_text.strip()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        job_description = request.form['job_description']
        # print(uploaded_files)
        qualifications_embeddings = get_use_embeddings(job_description)
        job_keywords = extract_keywords(job_description)
        
        folder_name = secure_filename(request.form.get('folder_name', 'default_folder'))
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        os.makedirs(folder_path, exist_ok=True)

        candidate_scores = defaultdict(dict)

        for file in uploaded_files:
            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(folder_path, filename)
                file.save(file_path)

                output_txt = os.path.join(folder_path, filename.replace('.pdf', '.txt'))
                pdf_to_text(file_path, output_txt)

                text = open(output_txt, 'r', encoding='utf-8').read()
                skills_text = extract_skills_section(text)

                if skills_text:
                    skills_embedding = get_use_embeddings(skills_text)
                    similarity = cosine_similarity([skills_embedding], [qualifications_embeddings])[0][0]
                else:
                    similarity = 0

                resume_keywords = extract_keywords(text)
                keyword_score = len(resume_keywords.intersection(job_keywords)) / len(job_keywords)
                
                combined_score = 0.7 * similarity + 0.3 * keyword_score
                
                candidate_name = filename.split('\n')[0]
                candidate_scores[candidate_name] = {
                    "similarity": similarity,
                    "keyword_score": keyword_score,
                    "combined_score": combined_score
                }

        sorted_candidates = sorted(candidate_scores.items(), key=lambda x: x[1]['combined_score'], reverse=True)

        return render_template('results.html', candidates=sorted_candidates[:5])

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)