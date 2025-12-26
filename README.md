# Text Summarizer

A web application that provides text summarization functionality, built with a Python backend and a simple HTML/CSS/JavaScript frontend.

## Features
- Text summarization using advanced NLP techniques and Hugging face API
- Clean and responsive user interface
- Easy-to-use API endpoints

## Project Structure
```
app/
├── backend/           # Backend server and ML model
│   ├── app.py        # Flask application
│   ├── model.py      # Text summarization model
│   └── requirements.txt  # Python dependencies
├── frontend/         # Frontend files
│   ├── index.html    # Main page
│   ├── styles.css    # Styling
│   └── script.js     # Frontend logic
└── .gitignore        # Git ignore file

```
## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```cmd
   cd backend
   ```

2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with your configuration.

4. Run the backend server:
   ```cmd
   python app.py
   ```

### Frontend Setup
1. Open `frontend/index.html` in your web browser
2. The application will be accessible at `http://127.0.0.1:5000` after starting the backend

## Usage
1. Enter or paste your text into the input area
2. Click the "Summarize" button
3. Select type of  Summarization you need from List(Abstarctive, Extractive, Hybrid)
4. View the generated summary

## API Endpoints
- `POST /summarize` - Accepts text and returns a summary
  - Request body: `{"text": "Your long text here..."}`
  - Response: `{"summary": "Summarized text..."}`

