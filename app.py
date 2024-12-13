from flask import Flask, jsonify
import random
import sqlite3
from flask import request
from pathlib import Path


BASE_DIR = Path(__file__).parent
path_to_db = BASE_DIR / "store.db"  # <- тутпутькБД



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

about_me = {
"name": "Владимир",
"surname": "Рогачев",
"email": "vladimir.rogachev@ford-nn.com"
}

# quotes_all = [
# {
# "id": 3,
# "author": "Rick Cook",
# "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы большей и лучшей идиотоустойчивостью, и вселенной, котораяпытается создать больше отборных идиотов. Пока вселеннаяпобеждает."
# },
# {
# "id": 5,
# "author": "Waldi Ravens",
# "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
# },
# {
# "id": 6,
# "author": "Mosher’s Law of Software Engineering",
# "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
# },
# {
# "id": 8,
# "author": "Yoggi Berra",
# "text": "В теории, теория и практика неразделимы. На практике это не так."
# },
# ]


@app.route("/quotes")
def quotes():
    select_quotes = "SELECT * from quotes"
    # ПодключениевБД
    connection = sqlite3.connect("store.db")
    # Создаем cursor, он позволяет делать SQL-запросы
    cursor = connection.cursor()
    # Выполняемзапрос:
    cursor.execute(select_quotes)

    # Извлекаем результаты запроса
    quotes_db = cursor.fetchall() #получаем список кортежей list[tuple]
    

    # Закрыть курсор:
    cursor.close()
    # Закрыть соединение:
    connection.close()
    # преобразовываем полученные из бд данные
    # необходимо выполнить преобразование
    # list[tuple] -> list [dict]
    keys = ("id", "author", "text")
    quotes=[]
    for quote_db in quotes_db:
        quote = dict(zip(keys,quote_db))
        quotes.append(quote)

    return jsonify(quotes), 200
       
@app.route("/quotes/<int:id>")
def quotes_id(id): 
    select_quotes = f"SELECT * from quotes where id ={id} "
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchone()  
    cursor.close()
    connection.close()
    keys = ("id", "author", "text")
    if quotes_db is not None:
        quote = dict(zip(keys,quotes_db))
        return jsonify(quote), 200
    return f"Quote with id={id} not found", 404

    # for num_id in quotes_all:
    #     if num_id["id"] == id:
    #         return num_id
    # return f"Quote with id={id} not found", 404

@app.route("/quotes/count")
def quotes_count():
    return { "count" : len(quotes_all) }



@app.route("/quotes", methods=['POST'])
def create_quote():
    last_id = quotes_all[-1].get("id") + 1
    data = request.json
    data["id"] = last_id
    quotes_all.append(data)
    return data, 201


@app.route("/quotes/<id>", methods=['PUT'])
def edit_quote(id):
    new_data= request.json
    new_data["id"] = int(id)
    for num_id in quotes_all:
        if num_id["id"] == new_data["id"]:
            if new_data.get("author") is not None :
                num_id["author"] = new_data["author"]                   
            if new_data.get("text") is not None :
                num_id["text"] = new_data["text"]
            return num_id
    return f"Quote with id={id} not found", 404


@app.route("/quotes/<id>", methods=['DELETE'])
def delete(id):
    ind=0
    for num_id in quotes_all:
        if num_id["id"] == int(id):
            del quotes_all[ind]
            return f"Quote with id {id} is deleted.", 200
        ind= ind+1
        
if __name__ == "__main__":
    app.run(debug=True)