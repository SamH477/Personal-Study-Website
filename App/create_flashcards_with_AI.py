from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

# Load the Jinja environment
env = Environment(loader=FileSystemLoader('/templates'))
template = env.get_template('process_pdf.html')

# Render the template to HTML
html_content = template.render(text="Your PDF Text")

# Parse the rendered HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the paragraph tag containing the 'text' value
paragraph_tag = soup.find('p')

# Extract the text content from the paragraph tag
text = paragraph_tag.text

# Print the extracted text
print("Extracted text:", text)