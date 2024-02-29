from openai import OpenAI
from api_config import OPENAI_API_KEY
from flask import Flask, render_template, request
from PyPDF2 import PdfReader

# Create a Flask app
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Define a route for uploading a pdf file
@app.route('/pdf_upload')
def pdf_upload():
    return render_template('pdf_upload.html')

# Define a route for processing pdf files
@app.route('/upload', methods = ["POST"])
def process_pdf():
    pdf_file = request.files['file']
    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    text = page.extract_text()
    
    return render_template('process_pdf.html', text=text)

# Define a route so users can see their flashcards
@app.route('/my_flashcards')
def my_flashcards():
    return render_template('my_flashcards.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
