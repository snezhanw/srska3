import streamlit as st
from crewai import Crew
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI

from agents import create_agents
from tasks import create_tasks
from tools import parse_file, count_words, check_topic
from helpers import load_knowledge

# =====================
# ENV
# =====================
load_dotenv()

os.environ["OTEL_SDK_DISABLED"] = "true"

# =====================
# GEMINI LLM 💜
# =====================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# =====================
# UI
# =====================
st.set_page_config(page_title="Проверка тезисов", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #6a0dad, #ffffff); }
h1, h2 { color: #4b0082; }
.stButton>button { background-color: #7b2cbf; color: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("📄 Ассистент проверки научных тезисов")

# =====================
# INPUT
# =====================
st.header("⚙️ Настройка")
tracks = st.text_area("Тематики конференции", "AI, Data Science, Cybersecurity")

st.header("📥 Загрузка данных")
file = st.file_uploader("Загрузите файл", type=["txt", "pdf", "docx"])

# =====================
# RUN
# =====================
if st.button("🚀 Запустить анализ"):

    if file is None:
        st.error("Загрузите файл!")
        st.stop()

    text = parse_file(file)
    word_val = count_words(text)

    st.info(f"Количество слов: {word_val}")

    # =====================
    # KNOWLEDGE
    # =====================
    knowledge_content = load_knowledge()
    content_source = StringKnowledgeSource(content=knowledge_content)

    # =====================
    # AGENTS (С LLM 💜)
    # =====================
    formatting, topic, editor, decision = create_agents(llm)

    # =====================
    # CONDITIONAL LOGIC
    # =====================
    topic_ok = check_topic(text, tracks)
    need_editor = (word_val < 300 or word_val > 500) or not topic_ok

    if need_editor:
        st.warning("⚠️ Сработал Conditional Task (редактор подключен)")

    # =====================
    # TASKS
    # =====================
    tasks = create_tasks(
        formatting,
        topic,
        editor,
        decision,
        text,
        knowledge_content,
        tracks,
        need_editor
    )

    # =====================
    # CREW
    # =====================
    crew = Crew(
        agents=[formatting, topic, editor, decision],
        tasks=tasks,
        process="sequential",
        memory=True,
        verbose=True
    )

    # =====================
    # RUN
    # =====================
    with st.spinner("🤖 Анализ выполняется..."):
        result = crew.kickoff()

    # =====================
    # OUTPUT
    # =====================
    st.success("✅ Анализ завершён!")
    st.subheader("📄 Отчёт системы:")
    st.write(result.raw)

    # =====================
    # HITL
    # =====================
    st.divider()
    st.header("👤 Человеческое подтверждение (HITL)")

    decision_user = st.radio("Подтвердить результат?", ["Да", "Нет"])

    if decision_user == "Да":
        st.success("✔ Решение подтверждено человеком")
    else:
        st.error("✏️ Требуется доработка")