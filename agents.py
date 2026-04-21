from crewai import Agent

def create_agents(llm):
    model_id = "gemini-2.5-flash-lite"

    formatting = Agent(
        role="Аналитик оформления",
        goal="Проверить структуру и оформление научного текста",
        backstory="Вы эксперт по стандартам научных публикаций и конференций.",
        llm=model_id,
        allow_delegation=False
    )

    topic = Agent(
        role="Эксперт по тематике",
        goal="Определить соответствие текста тематическим направлениям",
        backstory="Вы ученый с многолетним стажем в области IT и AI.",
        llm=model_id,
        allow_delegation=False
    )

    editor = Agent(
        role="Редактор",
        goal="Исправить стилистические и смысловые ошибки",
        backstory="Вы профессиональный академический редактор.",
        llm=model_id,
        allow_delegation=False
    )

    decision = Agent(
        role="Финальное решение",
        goal="Сформировать итоговый вердикт: Принять или Отклонить",
        backstory="Вы председатель программного комитета конференции.",
        llm=model_id,
        allow_delegation=False
    )

    return formatting, topic, editor, decision