from app.nlp.extractive_summarizer import summarize_text

class NLPService:
    def extractive_summary(self, text: str):
        return summarize_text(text)
