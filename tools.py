import PyPDF2
import docx
from crewai.tools import tool

def parse_file(file):
    name = file.name.lower()
    if name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

def count_words_logic(text: str):
    return len(text.split())

def check_topic_logic(text: str, tracks: str):
    return any(track.strip().lower() in text.lower() for track in tracks.split(","))

@tool("word_counter")
def count_words(text: str):
    """Считает количество слов в тексте."""
    return count_words_logic(text)

@tool("topic_checker")
def check_topic(text: str, tracks: str):
    """Проверяет соответствие текста научным направлениям."""
    return check_topic_logic(text, tracks)