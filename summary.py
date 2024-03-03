from flask import Flask, render_template, request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from docx import Document
from sumy.summarizers.lex_rank import LexRankSummarizer


app = Flask(__name__, static_url_path='/static')


def summarize_text(file_path, num_sentences):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs]
        text = '\n'.join(paragraphs)
    else:
        return "Unsupported file format."

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)

    lex_summary = []

    for sentence in summary:
        lex_summary.append(str(sentence))

    return lex_summary


@app.route('/')
def index():
    return render_template('index.html', lex_summary='')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    num_sentences = 12  # Replace with the desired number of sentences in the summary

    if file:
        file_path = file.filename
        file.save(file_path)
        lex_summary = summarize_text(file_path, num_sentences)
        return render_template('index.html', lex_summary=lex_summary, file_name=file.filename)  # Pass file name to template
    else:
        return render_template('index.html', lex_summary='No file uploaded.', file_name='')  # Pass an empty file name



if __name__ == '__main__':
    app.run()