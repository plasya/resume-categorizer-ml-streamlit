# Import necessary libraries for file handling, text processing, and machine learning
import os
import pandas as pd
import pickle
from pypdf import PdfReader  # To read PDF files
import re
import streamlit as st
from docx import Document  # To read Word (.docx) files

# Load the pre-trained models (TF-IDF vectorizer and machine learning classifier)
tfidf_vectorizer = pickle.load(open(r"../Weights/tfidf.pkl", "rb"))
model = pickle.load(open(r"../Weights/model.pkl", "rb"))

# Function to clean the resume text
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)  
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

# Dictionary that maps numerical prediction output to actual job categories
category_mapping = {
    15: "Java Developer",
    23: "Testing",
    8: "DevOps Engineer",
    20: "Python Developer",
    24: "Web Designing",
    12: "HR",
    13: "Hadoop",
    3: "Blockchain",
    10: "ETL Developer",
    18: "Operations Manager",
    6: "Data Science",
    22: "Sales",
    16: "Mechanical Engineer",
    1: "Arts",
    7: "Database",
    11: "Electrical Engineering",
    14: "Health and fitness",
    19: "PMO",
    4: "Business Analyst",
    9: "DotNet Developer",
    2: "Automation Testing",
    17: "Network Security Engineer",
    21: "SAP Developer",
    5: "Civil Engineer",
    0: "Advocate",
}

# Function to extract text from .docx files
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to categorize resumes into job categories and save them into corresponding folders
def categorize_resumes(uploaded_files, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    results = []  # List to store results for each file
    
    # Iterate through each uploaded file
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith('.pdf'):  # Handle PDF files
            reader = PdfReader(uploaded_file)
            page = reader.pages[0]
            text = page.extract_text()  # Extract the resume text from the PDF
        elif uploaded_file.name.endswith('.docx'):  # Handle .docx files
            text = extract_text_from_docx(uploaded_file)  # Extract the resume text from the Word file
        else:
            st.warning(f"Unsupported file format: {uploaded_file.name}")
            continue
        
        # Clean the extracted resume text
        cleaned_resume = cleanResume(text)

        # Convert the cleaned resume into numerical features using TF-IDF
        input_features = tfidf_vectorizer.transform([cleaned_resume])
        
        # Predict the job category based on the resume
        prediction_id = model.predict(input_features)[0]
        
        # Map the predicted category ID to the actual category name
        category_name = category_mapping.get(prediction_id, "Unknown")
        
        # Create a folder for the predicted category if it doesn't exist
        category_folder = os.path.join(output_directory, category_name)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)
        
        # Save the uploaded file into the category folder
        target_path = os.path.join(category_folder, uploaded_file.name)
        with open(target_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Append the result (filename and category) to the results list
        results.append({'filename': uploaded_file.name, 'category': category_name})
    
    # Convert the results list to a DataFrame for better visualization and download
    results_df = pd.DataFrame(results)
    return results_df

# Streamlit app interface
st.title("Resume Classifier Application")
st.subheader("Categorize Resumes Based on Job Roles using Machine Learning")

# Allow both .pdf and .docx files to be uploaded
uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX format)", type=["pdf", "docx"], accept_multiple_files=True)

# Input for specifying the output directory where the categorized resumes will be saved
output_directory = st.text_input("Specify Output Directory", "categorized_resumes")

# Button to trigger the categorization process
if st.button("Start Categorization"):
    if uploaded_files and output_directory:
        # Call the categorize_resumes function and display the results
        results_df = categorize_resumes(uploaded_files, output_directory)
        st.write(results_df)  # Display the categorization results in a table
        
        # Provide a CSV download option for the categorization results
        results_csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Categorization Results as CSV",
            data=results_csv,
            file_name='categorized_resumes.csv',
            mime='text/csv',
        )
        st.success("Resumes categorization and processing completed.")
    else:
        st.error("Please upload files and specify the output directory.")

# Use streamlit run application.py to run the application