import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download once
nltk.download("punkt")
nltk.download("stopwords")


def summarize_text(text: str, ratio: float = 1.2):
    """
    Simple extractive summarization using NLTK.
    ratio → threshold multiplier for sentence selection
    """

    # Tokenization
    words = word_tokenize(text)

    # Stopwords
    stop_words = set(stopwords.words("english"))

    # Remove stopwords
    filtered_words = [w.lower() for w in words if w.lower() not in stop_words]

    # Frequency table
    freq_table = {}
    for word in filtered_words:
        freq_table[word] = freq_table.get(word, 0) + 1

    # Sentences
    sentences = sent_tokenize(text)
    sentence_value = {}

    for sentence in sentences:
        for word, freq in freq_table.items():
            if word in sentence.lower():
                sentence_value[sentence] = sentence_value.get(sentence, 0) + freq

    # Prevent empty input
    if not sentence_value:
        return ""

    # Calculate average score
    avg_score = sum(sentence_value.values()) / len(sentence_value)

    # Build summary
    summary = " ".join(
        [sentence for sentence in sentences
         if sentence_value.get(sentence, 0) > ratio * avg_score]
    )

    return summary
