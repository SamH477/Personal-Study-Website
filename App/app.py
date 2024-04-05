from flask import Flask, render_template, request
from openai import OpenAI
from api_config.api_config import OPENAI_API_KEY
from PyPDF2 import PdfReader
import re
import os
import moviepy.editor as mp
import speech_recognition as sr

client = OpenAI(api_key=OPENAI_API_KEY)

# Create a Flask app
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Define a route for uploading a pdf file
@app.route('/aisites')
def aisites():
    return render_template('aisites.html')

# Define a route for uploading a pdf file
@app.route('/youtube')
def youtube():
    return render_template('youtube.html')

# Define a route for uploading a pdf file
@app.route('/pdf_upload')
def pdf_upload():
    return render_template('pdf_upload.html')

# Define a route for uploading a video file
@app.route('/video_upload')
def video_upload():
    return render_template('video_upload.html')

# Define a route for processing pdf files
@app.route('/upload', methods = ["POST"])
def process_pdf():
    pdf_file = request.files['file']
    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    text = page.extract_text()

    # Generate Flashcards for Study Guide Terms using AI
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": text},
    {"role": "user", "content": "Generate one sentence definitions for each term from this study guide in this format: term1:definition term2:definition etc. Make sure that each term and its corresponding definition is seperated by a colon."}
    ])

    response = str(completion.choices[0].message)

    response = response.replace("', role='assistant', function_call=None, tool_calls=None)", ' ')

    response = response.replace("\\n", '   ')

    response = response.replace("ChatCompletionMessage(content='", ' ')

    terms_list = response.split(sep = "  ")

    del terms_list[-1]

    print(response)

    return render_template('process_pdf.html', text=text, terms=terms_list)

@app.route('/upload2', methods = ["POST"])
def process_video():
    # Get the video file from the form
    video_file = request.files['file2']
    
    # Save the video file to a temporary location
    video_file.save("temp_video.mp4")
    
    # Load the video from the temporary location
    video = mp.VideoFileClip("temp_video.mp4")
    
    # Extract the audio from the video
    audio_file = video.audio
    
    # Generate the filename for the audio file
    audio_filename = "{}.wav".format("temp_video.mp4".split('.')[0])
    
    # Write the audio file
    audio_file.write_audiofile(audio_filename)
    
    # Initialize recognizer
    r = sr.Recognizer()
    
    # Load the audio file
    with sr.AudioFile(audio_filename) as source:
        data = r.record(source)
    
    # Convert speech to text
    text = r.recognize_google(data)
    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": text},
    {"role": "user", "content": "Generate one sentence definitions for each term from this video transcription text in this format: term1:definition term2:definition etc. Make sure that each term and its corresponding definition is seperated by a colon."}
    ])

    response = str(completion.choices[0].message)

    response = response.replace("', role='assistant', function_call=None, tool_calls=None)", ' ')

    response = response.replace("\\n", '  ')

    response = response.replace("ChatCompletionMessage(content='", ' ')

    terms_list = response.split(sep = "   ")

    # del terms_list[-1]

    print(text)

    print(response)

    return render_template('process_video.html', text=text, terms=terms_list)
    
    # Remove the temporary video file
    # os.remove("temp_video.mp4")

# Define a route so users can see their flashcards
@app.route('/my_flashcards')
def my_flashcards():
    return render_template('my_flashcards.html')

@app.route('/view_flashcards')
def view_flashcards():
    return render_template('view_flashcards.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port = 15000)