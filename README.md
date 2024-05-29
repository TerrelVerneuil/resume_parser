# resume_parser
# Resume Parser

## Overview
This project is a web application designed to parse and evaluate resumes to help employers identify the best candidates for a job position. It leverages Natural Language Processing (NLP) techniques to extract and analyze relevant information from resumes and match them against a job description. The application supports mass import of resumes and ranks the top 5 candidates based on their relevance to the job specifications.

## Objectives
- Extract specific information from resumes to identify the best candidates.
- Provide a fair alternative to traditional keyword matching by evaluating multiple criteria.
- Enable mass import of resumes and ranking of the top 5 candidates based on their relevance to the job description.

## Technologies Used
- **Flask**: For building the web application.
- **PyPDF2**: For extracting text from PDF resumes.
- **NLTK**: For text tokenization and preprocessing.
- **SentenceTransformers**: For generating sentence embeddings.
- **TensorFlow**: For neural network operations.
- **scikit-learn**: For TF-IDF vectorization and cosine similarity calculations.

## How It Works
1. **Upload Resumes**: Users can upload multiple PDF resumes through the web interface.
2. **Job Description Input**: Users input the job description against which the resumes will be evaluated.
3. **Text Extraction**: PDF resumes are converted to text using PyPDF2.
4. **Text Preprocessing**: Tokenization and text normalization using NLTK.
5. **Keyword Extraction**: Extracts top keywords from the job description using TF-IDF.
6. **Skills Extraction**: Identifies the skills section in each resume.
7. **Embedding Generation**: Generates embeddings for the job description and resume skills using SentenceTransformers.
8. **Similarity Calculation**: Computes cosine similarity between job description embeddings and resume embeddings.
9. **Scoring**: Combines similarity scores and keyword matching scores to rank candidates.
10. **Results Display**: Displays the top 5 candidates based on their combined scores.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-parser.git
   cd resume-parser


pip install -r requirements.txt

python app.py

Usage

Open your web browser and navigate to http://127.0.0.1:5000/.
Upload PDF resumes and enter the job description.
Click the "Submit" button to process the resumes.
View the top 5 candidates on the results page.
Credit

This project is inspired by the book "Natural Language Processing with Python" by Steven Bird, Edward Loper, and Ewan Klein (2009), O’Reilly Media Inc.

License

This project is licensed under the MIT License. See the LICENSE file for details.
