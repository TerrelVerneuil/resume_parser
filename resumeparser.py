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
import PyPDF2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize, word_tokenize

from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
model = SentenceTransformer('all-MiniLM-L6-v2')
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

#extract the text from the pdf and make it a new file
if __name__ == "__main__":
    for i in range(1, 10):
        #realistically this should be an input section
        #or a file upload section
        #but that will be implemented later :D

        #if upload box has no files input
        #it shouldn't run convert to pdf
        pdf_path = 'resume_' + str(i) + '.pdf'
        output_txt = 'resume_'+ str(i) + '.txt'
        pdf_to_text(pdf_path, output_txt)

    # print("PDF converted to text successfully!")

#this is the first step in the process
#parse the text to get the most relevant information

#text to string
def text_to_string(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    # Join the sentences into a single string
    text = ' '.join(sentences)
    return text
token_resumes = []
word_token = []
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
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
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
# print("Enter the job qualifications: ")

job_description = '''Requirements

Pursuing a degree in UI/UX design, interaction design, graphic design, or a related field
Proficiency in design tools such as Figma, Adobe Creative Suite, Sketch, or simliar
Strong portfolio showcasing user-centered design projects and problem-solving skills
Familiarity with responsive design principles and mobile-first design
Experience designing mobile app interfaces and responsive web designs is essential
Excellent communication skills and the ability to articulate design decisions
Passion for fashion, sustainability, and user-centered design
'''
qualifications = ""
qualifications += job_description + "\n"  # Append the input line to qualifications with a newline

# Tokenize the qualifications input
qualifications = job_description.strip()
qualifications_embeddings = get_use_embeddings(qualifications)
job_keywords = extract_keywords(job_description)
# print(job_keywords)
# print(qualifications_tokenized)
# # Loop through each resume
candidate_scores = defaultdict(dict)
    
for resume_text, resume_tokenized, resume_embeddings in resumes:
        skills_text = extract_skills_section(resume_text)
        if skills_text:
            skills_embedding = get_use_embeddings(skills_text)
            similarity = cosine_similarity([skills_embedding], [qualifications_embeddings])[0][0]
        else:
            similarity = 0
        
        resume_keywords = extract_keywords(resume_text)
        keyword_score = len(job_keywords.intersection(resume_keywords)) / len(job_keywords)

        combined_score = (0.7 * similarity + 0.3 * keyword_score)

        name = resume_text.split('\n')[0]  # Assuming the name is at the top of the resume
        candidate_scores[name] = {
            "similarity": similarity,
            "keyword_score": keyword_score,
            "combined_score": combined_score
        }

sorted_candidates = sorted(candidate_scores.items(), key=lambda x: x[1]['combined_score'], reverse=True)
    
print("Best candidates for the position:")
for candidate, scores in sorted_candidates[:5]:
    print(f"Candidate: {candidate}")
    print(f"Combined Score: {scores['combined_score']:.2f}, Similarity: {scores['similarity']:.2f}, Keyword Score: {scores['keyword_score']:.2f}")
    print()