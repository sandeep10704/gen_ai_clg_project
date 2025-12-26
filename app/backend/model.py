import os
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from dotenv import load_dotenv

load_dotenv()


nltk.download("punkt")
nltk.download("stopwords")


# EXTRACTIVE SUMMARIZATION 
def summarize_text(text: str, ratio: float = 0.4):
    sentences = sent_tokenize(text)
    if not sentences:
        return ""

    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    filtered_words = [w for w in words if w.isalnum() and w not in stop_words]

    freq_table = {}
    for word in filtered_words:
        freq_table[word] = freq_table.get(word, 0) + 1

    sentence_scores = {}

    for i, sentence in enumerate(sentences):
        tokens = word_tokenize(sentence.lower())
        sentence_len = len(tokens)

        if sentence_len < 5 or sentence_len > 100:
            continue

        score = 0
        for word in tokens:
            if word in freq_table:
                score += freq_table[word]

        # Normalize by length
        score /= sentence_len

        # Positional importance
        if i == 0:
            score *= 1.4
        elif i == len(sentences) - 1:
            score *= 1.2

        sentence_scores[sentence] = score

    top_k = max(1, int(len(sentences) * ratio))
    top_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:top_k]

    # Keep original order
    summary = [s for s in sentences if s in top_sentences]
    return " ".join(summary)

# ABSTRACTIVE SUMMARIZATION 
API_URL = os.environ.get("HF_URL")
headers = {
    "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"
}

def bart_summarize(text):
    word_count = len(text.split())

    # Skip abstractive if too short
    if word_count < 50:
        return text

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max(60, int(word_count * 0.6)),
            "min_length": max(30, int(word_count * 0.3)),
            "length_penalty": 2.0,
            "do_sample": False
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    try:
        return response.json()[0]["summary_text"]
    except Exception:
        print("Abstractive error:", response.text)
        return text


# HYBRID SUMMARIZATION

def hybrid_summarize(text, ratio=0.4):
    extractive_summary = summarize_text(text, ratio=ratio)
    final_summary = bart_summarize(extractive_summary)
    return final_summary


# EXAMPLE USAGE
if __name__ == "__main__":
    input_text = """
    In today’s rapidly evolving business environment, organizations are constantly seeking ways
    to gain a competitive advantage by improving operational efficiency and making data-driven
    decisions. One of the major challenges faced by business analysts is dealing with the
    overwhelming amount of textual information available from various sources.

    Industry trends change at a fast pace, and manually analyzing large volumes of data is
    time-consuming. Automated summarization provides an efficient solution by condensing documents
    into meaningful summaries that highlight key information.

    Competitor analysis, customer feedback, and market intelligence further increase the need for
    intelligent summarization tools that support faster and more accurate decision-making.
    """
    summary = hybrid_summarize(input_text, ratio=0.4)
    print(summary)