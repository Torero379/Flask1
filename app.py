from flask import Flask, jsonify, abort, request
import random
import sqlite3
from flask import request
from pathlib import Path
from werkzeug.exceptions import HTTPException
### импорт для SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

BASE_DIR = Path(__file__).parent
path_to_db = BASE_DIR / "store.db"  # <- тутпутькБД

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(model_class=Base)
db.init_app(app)


class QuoteModel(db.Model):
    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(32))
    text: Mapped[str] = mapped_column(String(255))
    rating: Mapped[int] ###= mapped_column(default=1)

    def __init__(self, author, text):
        self.author = author
        self.text  = text
        self.rating = rating


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


### Функция для перехвата ошибок HTTP и возврата в виде JSON###

@app.errorhandler(HTTPException)
def handle_exeption(e):
    return jsonify({"massage": e.description}), e.code









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

# @app.route("/quotes/count")
# def quotes_count():
#     return { "count" : len(quotes_all) }



@app.route("/quotes", methods=['POST'])
def create_quote():
    data = request.json
    
    # select_quotes = f"INSERT INTO quotes (author, text) VALUES ({data['author']},{data['text']}) " ### не понял почему не могу так записать 
    # и ниже использовать cursor.execute(select_quotes) выдает ошибку OperationalError sqlite3.OperationalError: near "quote": syntax error
    
    select_quotes = "INSERT INTO quotes (author, text) VALUES(?,?)"
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    cursor.execute(select_quotes,(data["author"],data["text"]))
    data_id = cursor.lastrowid
    connection.commit() 
    cursor.close()
    connection.close()
    data["id"] = data_id
    return jsonify(data),201

    # last_id = quotes_all[-1].get("id") + 1
    # data = request.json
    # data["id"] = last_id
    # quotes_all.append(data)
    # return data, 201


@app.route("/quotes/<id>", methods=['PUT'])
def edit_quote(id):
    new_data= request.json
    new_data["id"] = int(id)
    if new_data.get("author") is not None:
        select_quotes = "UPDATE quotes SET author=(?) WHERE id=(?)"
        connection = sqlite3.connect("store.db")
        cursor = connection.cursor()
        cursor.execute(select_quotes,(new_data["author"],new_data["id"])) 
        connection.commit() 
        cursor.close()
        connection.close()
    if new_data.get("text") is not None:
        select_quotes = f"UPDATE quotes  SET text=?  WHERE id=?"
        connection = sqlite3.connect("store.db")
        cursor = connection.cursor()
        cursor.execute(select_quotes, (new_data["text"],new_data["id"]))  
        connection.commit() 
        cursor.close()
        connection.close()
    
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
       
   
#     for num_id in quotes_all:
#         if num_id["id"] == new_data["id"]:
#             if new_data.get("author") is not None :
#                 num_id["author"] = new_data["author"]                   
#             if new_data.get("text") is not None :
#                 num_id["text"] = new_data["text"]
#             return num_id
#     return f"Quote with id={id} not found", 404


@app.route("/quotes/<id>", methods=['DELETE'])
def delete(id):
    select_quotes = f"DELETE FROM quotes WHERE id={id} "
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()
    cursor.execute(select_quotes)   
    del_quotes= cursor.rowcount
    if del_quotes is not None:
        connection.commit() 
        cursor.close()
        connection.close()
        return f"Quote with id {id} is deleted.", 200
    else: return f"Quote with id={id} not found", 404
#   
# 
#     ind=0
#     for num_id in quotes_all:
#         if num_id["id"] == int(id):
#             del quotes_all[ind]
#             return f"Quote with id {id} is deleted.", 200
#         ind= ind+1
        
if __name__ == "__main__":
    app.run(debug=True)