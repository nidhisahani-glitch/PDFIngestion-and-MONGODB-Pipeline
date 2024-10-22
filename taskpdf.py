import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pymongo import MongoClient
from transformers import pipeline
from keybert import KeyBERT

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize MongoDB client
client = MongoClient('mongodb+srv://TestUser:nidhisahani@myfirstcluster.jgfeu.mongodb.net/admin')  # My MongoDB connection string
db = client['TestUser']  # My database name
collection = db['Collection Name']  # My collection name

# Summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
kw_model = KeyBERT()

def summarize_text(text):
    """Summarize the input text using a pretrained model."""
    try:
        input_length = len(text.split())
        max_length = min(130, input_length - 5)
        min_length = min(30, input_length // 2)

        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error summarizing text: {e}")
        return ""

# Extract Keywords
def extract_keywords(text):
    """Extract keywords from the input text using KeyBERT."""
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
    return [kw[0] for kw in keywords]

# Update Document
def update_or_create_document(text, document_id):
    """Update an existing document or create a new one in MongoDB."""
    summary = summarize_text(text)
    keywords = extract_keywords(text)

    # Make the update query
    update_query = {
        'summary': summary,
        'keywords': keywords
    }

    # We Check if the document exists
    existing_document = collection.find_one({'_id': document_id})

    if existing_document:
        # Document exists, perform the update
        result = collection.update_one({'_id': document_id}, {'$set': update_query})
        if result.modified_count > 0:
            logging.info(f"Document {document_id} updated successfully.")
        else:
            logging.info(f"No changes made to document {document_id}.")
    else:
        # Document does not exist, insert a new document
        new_document = {
            '_id': document_id,
            'summary': summary,
            'keywords': keywords
        }
        collection.insert_one(new_document)
        logging.info(f"New document {document_id} created successfully.")

def process_pdf(file_path):
    """Mock implementation of PDF processing. Replace with actual PDF reading logic."""
    try:
        # Simulate reading from a PDF
        return {
            'text': "This is a sample text extracted from the PDF.",
            'id': os.path.basename(file_path).replace(".pdf", "")  
        }
    except Exception as e:
        logging.error(f"Error processing PDF {file_path}: {e}")
        return None


# Performance Metrics  & Error Handling
def process_with_timing(file_path):
    """Process a PDF file and log the processing time."""
    start_time = time.time()
    doc_metadata = process_pdf(file_path)
    
    if doc_metadata:
        text = doc_metadata['text']
        document_id = doc_metadata['id']  # Extract the ID from the metadata
        update_or_create_document(text, document_id)
    
    end_time = time.time()
    logging.info(f"Processed {file_path} in {end_time - start_time:.2f} seconds")

# Concurrency(running multiple pdf simuntaneously)
def process_all_pdfs_in_folder(folder_path):
    """Process all PDF files in a specified folder using ThreadPoolExecutor."""
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]  # List all PDF files

    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust the number of workers as  we needed
        futures = {executor.submit(process_with_timing, os.path.join(folder_path, file_name)): file_name for file_name in pdf_files}
        
        for future in as_completed(futures):
            file_name = futures[future]
            try:
                future.result()  # Wait to complete and check for exceptions
            except Exception as e:
                logging.error(f"Error in processing PDF file {file_name}: {e}")

# My Example
folder_path = "ALL PDF FOLDER"  # Path to my PDF folder
process_all_pdfs_in_folder(folder_path)
