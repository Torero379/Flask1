from flask import Flask, jsonify, abort, request
from typing import Any
import random
import sqlite3
from flask import request
from pathlib import Path
from werkzeug.exceptions import HTTPException
### импорт для SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, func, ForeignKey
from flask_migrate import Migrate
class Base(DeclarativeBase):
    pass

BASE_DIR = Path(__file__).parent
#path_to_db = BASE_DIR / "store.db"  # <- тутпутькБД

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'quotes.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)




class AuthorModel(db.Model):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(32), index= True, unique=True)
    quotes: Mapped[list['QuoteModel']] = relationship(back_populates='author', lazy='dynamic')
    

    def __init__(self, name):
        self.name = name
    def to_dict(self):
        return{"name": self.name}


class QuoteModel(db.Model):
    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[str] = mapped_column(ForeignKey('authors.id'))
    author: Mapped['AuthorModel'] = relationship(back_populates='quotes')
    text: Mapped[str] = mapped_column(String(255))

    def __init__(self, author, text):
        self.author = author
        self.text  = text

    def to_dict(self):
        return {
            "id" : self.id,
            "author": self.author,
            "text": self.text,
            "rating": self.rating
        }

# app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

about_me = {
"name": "Владимир",
"surname": "Рогачев",
"email": "vladimir.rogachev@ford-nn.com"
}




### Функция для перехвата ошибок HTTP и возврата в виде JSON###

@app.errorhandler(HTTPException)
def handle_exeption(e):
    return jsonify({"massage": e.description}), e.code









@app.route("/quotes")
def quotes()->list[dict[str,Any]]:
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()
    quotes = []
    for quote in quotes_db:
        quotes.append(quote.to_dict())
    return jsonify(quotes), 200



    ###Вывод через select
    # select_quotes = "SELECT * from quotes"
    # # ПодключениевБД
    # connection = sqlite3.connect("store.db")
    # # Создаем cursor, он позволяет делать SQL-запросы
    # cursor = connection.cursor()
    # # Выполняемзапрос:
    # cursor.execute(select_quotes)

    # # Извлекаем результаты запроса
    # quotes_db = cursor.fetchall() #получаем список кортежей list[tuple]
    

    # # Закрыть курсор:
    # cursor.close()
    # # Закрыть соединение:
    # connection.close()
    # # преобразовываем полученные из бд данные
    # # необходимо выполнить преобразование
    # # list[tuple] -> list [dict]
    # keys = ("id", "author", "text")
    # quotes=[]
    # for quote_db in quotes_db:
    #     quote = dict(zip(keys,quote_db))
    #     quotes.append(quote)

    # return jsonify(quotes), 200
       
@app.route("/quotes/<int:id>")
def quotes_id(id):
    quote = db.get_or_404(QuoteModel, id)
    return jsonify(quote.to_dict()),200

    #####################Вывод через select
    # select_quotes = f"SELECT * from quotes where id ={id} "
    # connection = sqlite3.connect("store.db")
    # cursor = connection.cursor()
    # cursor.execute(select_quotes)
    # quotes_db = cursor.fetchone()  
    # cursor.close()
    # connection.close()
    # keys = ("id", "author", "text")
    # if quotes_db is not None:
    #     quote = dict(zip(keys,quotes_db))
    #     return jsonify(quote), 200
    # return f"Quote with id={id} not found", 404

    # for num_id in quotes_all:
    #     if num_id["id"] == id:
    #         return num_id
    # return f"Quote with id={id} not found", 404
######################




@app.route("/quotes", methods=['POST'])
def create_quote():
    data = request.json
    if "rating" in data:
        if 0<int(data["rating"])<6:
            data_raiting = data["rating"]
    else: data_raiting="1"
    quote = QuoteModel (data["author"],data["text"],data_raiting)
    db.session.add(quote)
    db.session.commit()
    return jsonify(quote.to_dict()),200

##########################Вывод через select
    # select_quotes = "INSERT INTO quotes (author, text) VALUES(?,?)"
    # connection = sqlite3.connect("store.db")
    # cursor = connection.cursor()
    # cursor.execute(select_quotes,(data["author"],data["text"]))
    # data_id = cursor.lastrowid
    # connection.commit() 
    # cursor.close()
    # connection.close()
    # data["id"] = data_id
    # return jsonify(data),201
############################
    # last_id = quotes_all[-1].get("id") + 1
    # data = request.json
    # data["id"] = last_id
    # quotes_all.append(data)
    # return data, 201


@app.route("/quotes/<id>", methods=['PUT'])
def edit_quote(id):
    new_data= request.json
    quote = db.get_or_404(QuoteModel, id)

    if "author" in new_data:
        quote.author = new_data["author"]
    if "text" in new_data:
        quote.text = new_data["text"]
    if "rating" in new_data:
        if 0<int(new_data["rating"])<6:
            quote.rating = int(new_data["rating"])
        
    db.session.commit()
    return jsonify(quote.to_dict()),200

    ############################Вывод через select
    # new_data= request.json
    # new_data["id"] = int(id)
    # if new_data.get("author") is not None:
    #     select_quotes = "UPDATE quotes SET author=(?) WHERE id=(?)"
    #     connection = sqlite3.connect("store.db")
    #     cursor = connection.cursor()
    #     cursor.execute(select_quotes,(new_data["author"],new_data["id"])) 
    #     connection.commit() 
    #     cursor.close()
    #     connection.close()
    # if new_data.get("text") is not None:
    #     select_quotes = f"UPDATE quotes  SET text=?  WHERE id=?"
    #     connection = sqlite3.connect("store.db")
    #     cursor = connection.cursor()
    #     cursor.execute(select_quotes, (new_data["text"],new_data["id"]))  
    #     connection.commit() 
    #     cursor.close()
    #     connection.close()
    
    # select_quotes = f"SELECT * from quotes where id ={id} "
    # connection = sqlite3.connect("store.db")
    # cursor = connection.cursor()
    # cursor.execute(select_quotes)
    # quotes_db = cursor.fetchone()  
    # cursor.close()
    # connection.close()
    # keys = ("id", "author", "text")
    # if quotes_db is not None:
    #     quote = dict(zip(keys,quotes_db))
    #     return jsonify(quote), 200
    # return f"Quote with id={id} not found", 404
#################################       
   
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
    quote = db.get_or_404(QuoteModel, id)
    db.session.delete(quote)
    db.session.commit()
    return f"Quote with id {id} is deleted.", 200
    #############################Вывод через select
    # select_quotes = f"DELETE FROM quotes WHERE id={id} "
    # connection = sqlite3.connect("store.db")
    # cursor = connection.cursor()
    # cursor.execute(select_quotes)   
    # del_quotes= cursor.rowcount
    # if del_quotes is not None:
    #     connection.commit() 
    #     cursor.close()
    #     connection.close()
    #     return f"Quote with id {id} is deleted.", 200
    # else: return f"Quote with id={id} not found", 404
############################   
# 
#     ind=0
#     for num_id in quotes_all:
#         if num_id["id"] == int(id):
#             del quotes_all[ind]
#             return f"Quote with id {id} is deleted.", 200
#         ind= ind+1
        
if __name__ == "__main__":
    app.run(debug=True)