from crewai import Task

def create_tasks(formatting, topic, editor, decision, text, knowledge, tracks):
    t1 = Task(
        description=f"Проверь оформление и структуру:\n{text}\nТребования:\n{knowledge}",
        expected_output="Список ошибок оформления",
        agent=formatting
    )

    t2 = Task(
        description=f"Определи соответствие тематике:\n{text}\nТемы:\n{tracks}",
        expected_output="Подходит ли тема и к какому треку",
        agent=topic
    )

    t3 = ConditionalTask(
        description=f"На основе отчетов t1 и t2, исправь текст или предложи правки:\n{text}",
        expected_output="Исправленный текст или детальные рекомендации",
        condition=lambda output: "ошибок" in output.raw.lower() or "не подходит" in output.raw.lower(),
        agent=editor
    )

    t4 = Task(
        description="Сделай финальный вывод на основе всех предыдущих этапов: Принять / Доработать / Отклонить",
        expected_output="Итоговое решение (Decision Memo)",
        agent=decision,
        human_input=True 
    )

    return [t1, t2, t3, t4]