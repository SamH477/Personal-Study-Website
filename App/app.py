# jsonify unused in line below (9-1-24)
from flask import Flask, render_template, request, redirect, url_for, session
from openai import OpenAI
from api_config.api_config import OPENAI_API_KEY, key
from PyPDF2 import PdfReader
# import re (not used: 9-1-24)
import os
import moviepy.editor as mp
import speech_recognition as sr
from urllib.parse import unquote

client = OpenAI(api_key=OPENAI_API_KEY)

# Create a Flask app
app = Flask(__name__, static_folder='../Site/static',
            template_folder='../Site/templates')

app.secret_key = key


# Define a route for the homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')


# Define a route for the AI Sites page
@app.route('/aisites')
def aisites():
    return render_template('aisites.html')


# Define a route for uploading a pdf file
@app.route('/pdf_upload')
def pdf_upload():
    return render_template('pdf_upload.html')


# Define a route for uploading a video file
@app.route('/video_upload')
def video_upload():
    return render_template('video_upload.html')


# Define a route for processing pdf files
@app.route('/upload', methods=["POST"])
def process_pdf():
    pdf_file = request.files['file']
    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    text = page.extract_text()

    # Generate Flashcards for Study Guide Terms using AI
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": text},
                  {"role": "user", "content": "Generate one sentence \
                   definitions for each term from this study guide in\
                   this format: term1:definition term2:definition etc\
                   . Make sure that each term and its corresponding  \
                   definition is seperated by a colon."}])

    response = str(completion.choices[0].message)

    response = response.replace("', role='assistant', function_call= \
                                None, tool_calls=None)", ' ')

    response = response.replace("\\n", '*')

    response = response.replace("ChatCompletionMessage(content='", ' ')

    terms_list = response.split(sep="*")

    del terms_list[-1]

    # print(response)

    return render_template('process_pdf.html', text=text, terms=terms_list)


@app.route('/upload2', methods=["POST"])
def process_video():
    # Get the video file from the form
    video_file = request.files['file2']

    # Save the video file to a temporary location
    video_file.save("test_docs", "temp_video.mp4")              # Edit #1!!!

    # Load the video from the temporary location
    video = mp.VideoFileClip("test_docs", "temp_video.mp4")     # Edit #2!!!

    # Extract the audio from the video
    audio_file = video.audio

    # Generate the filename for the audio file                  # Edit #3!!!
    audio_filename = "{}.wav".format(os.path.join("test_docs", "temp_video").split('.')[0])

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

    response = response.replace("', role='assistant', function_call=None, \
                                tool_calls=None)", ' ')

    response = response.replace("\\n", '*')

    response = response.replace("ChatCompletionMessage(content='", ' ')

    terms_list = response.split(sep="*")

    del terms_list[-1]

    # print(text)

    # print(response)

    return render_template('process_video.html', text=text, terms=terms_list)

    # Remove the temporary video file                           # Edit #4!!!
    # os.remove(os.path.join("test_docs", "temp_video.mp4"))

    # Remove the temporary audio file
    # os.remove(audio_filename)


@app.route('/save_flashcards', methods=["POST"])
def save_flashcards():
    link = request.form.get('link')
    name = request.form.get('name')
    session['link'] = link
    session['name'] = name
    return redirect(url_for('my_flashcards'))


@app.route('/my_flashcards')
def my_flashcards():
    link = session.get('link')
    name = session.get('name')
    return render_template('my_flashcards.html', url=link, name=name)


@app.route('/view_flashcards')
def view_flashcards():
    terms = request.args.get('data')  # Get the terms from the URL query parameters
    decoded_terms = unquote(terms)  # Decode the encoded terms
    terms_list = eval(decoded_terms)  # Convert the decoded string to a list
    return render_template('view_flashcards.html', terms=terms_list)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=15000)
