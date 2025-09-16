from transformers import pipeline
from ..config import settings

if settings.HF_OFFLINE:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    ner = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple")
else:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    ner = pipeline("token-classification", model="Davlan/bert-base-multilingual-cased-ner-hrl", aggregation_strategy="simple")

def summarize_text(text: str) -> str:
    return summarizer(text, max_length=120, min_length=40, do_sample=False)[0]["summary_text"]

def extract_entities(text: str):
    return ner(text)
