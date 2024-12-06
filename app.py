from flask import Flask
import random
from flask import request


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

about_me = {
"name": "Владимир",
"surname": "Рогачев",
"email": "vladimir.rogachev@ford-nn.com"
}

quotes_all = [
{
"id": 3,
"author": "Rick Cook",
"text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы большей и лучшей идиотоустойчивостью, и вселенной, котораяпытается создать больше отборных идиотов. Пока вселеннаяпобеждает."
},
{
"id": 5,
"author": "Waldi Ravens",
"text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
},
{
"id": 6,
"author": "Mosher’s Law of Software Engineering",
"text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
},
{
"id": 8,
"author": "Yoggi Berra",
"text": "В теории, теория и практика неразделимы. На практике это не так."
},
]



@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/about")
def about():
    return about_me

@app.route("/quotes")
def quotes():
    return quotes_all
       
@app.route("/quotes/<int:id>")
def quotes_id(id):   
    for num_id in quotes_all:
        if num_id["id"] == id:
            return num_id
    return f"Quote with id={id} not found", 404

@app.route("/quotes/count")
def quotes_count():
    return { "count" : len(quotes_all) }

@app.route("/quotes/random_url")
def random_url():
    return random.choice(quotes_all)

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