from crewai import Agent

def create_agents(llm):

    formatting = Agent(
        role="Аналитик оформления",
        goal="Проверить структуру и оформление",
        backstory="Эксперт по научным текстам",
        llm=llm
    )

    topic = Agent(
        role="Эксперт по тематике",
        goal="Проверить соответствие теме",
        backstory="Член конференции",
        llm=llm
    )

    editor = Agent(
        role="Редактор",
        goal="Исправить ошибки",
        backstory="Научный редактор",
        llm=llm
    )

    decision = Agent(
        role="Финальное решение",
        goal="Принять итоговое решение",
        backstory="Председатель комиссии",
        llm=llm
    )

    return formatting, topic, editor, decision