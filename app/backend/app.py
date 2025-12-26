from dotenv import load_dotenv
import os

# Load environment variables before importing model (which relies on them)
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

import model

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    mode = data.get('mode', 'extractive') # extractive, abstractive, hybrid
    
    # Valid params
    try:
        ratio = float(data.get('ratio', 0.4))
    except ValueError:
        ratio = 0.4

    summary = ""
    summary_type = mode

    try:
        if mode == 'extractive':
            summary = model.summarize_text(text, ratio=ratio)
        elif mode == 'abstractive':
            summary = model.bart_summarize(text)
        elif mode == 'hybrid':
            summary = model.hybrid_summarize(text, ratio=ratio)
        else:
            return jsonify({'error': 'Invalid mode'}), 400
            
        return jsonify({'summary': summary, 'type': summary_type})
    except Exception as e:
        print(f"Error during summarization: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
