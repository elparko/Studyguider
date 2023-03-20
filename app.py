from flask import Flask, render_template, request, redirect, url_for
import pdfplumber
import os
import openai

app = Flask(__name__)

# Configure your OpenAI API key
openai.api_key = "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"
def generate_gpt3_response(syllabus_text):
    prompt = (
        f"You are a digital tutor, Please look for class topics within the syllabus provided, ignore entries that are not class topics, and please create a practice test using the topics and activities from the following syllabus content:\n\n"
        f"{syllabus_text}\n\n"
        f"Study Guide:"
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['syllabus']
        if file:
            # Process the uploaded file and generate study guide or test
            # Save the file temporarily
            file.save("temp_syllabus.pdf")

            # Extract text from PDF
            with pdfplumber.open("temp_syllabus.pdf") as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages)

            # Remove the temporary file
            os.remove("temp_syllabus.pdf")

            # Send the extracted text to GPT-3 API
            gpt3_response = generate_gpt3_response(text)

            return render_template('result.html', content=gpt3_response)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
