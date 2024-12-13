import sqlite3

select_quotes = "SELECT * from quotes"
# ПодключениевБД
connection = sqlite3.connect("store.db")
# Создаем cursor, он позволяет делать SQL-запросы
cursor = connection.cursor()
# Выполняемзапрос:
cursor.execute(select_quotes)

# Извлекаем результаты запроса
quotes = cursor.fetchall()
print(f"{quotes=}")

# Закрыть курсор:
cursor.close()
# Закрыть соединение:
connection.close()
