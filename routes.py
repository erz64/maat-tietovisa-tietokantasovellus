from crypt import methods
from app import app
from flask import redirect, render_template, request
import trivia

@app.route("/")
def index():
    return render_template("frontpage.html")  

@app.route("/paakaupungit")
def capitals_quiz():
    question_data = trivia.get_random_question(1)
    return render_template("trivia.html", question=question_data[0], image=question_data[1], correct = question_data[2])

@app.route("/paakaupungit", methods=["post"])
def answer():
    answer = request.form["answer"].strip()
    correct = request.form["correct"].strip()
    url = "/paakaupungit"
    return render_template("result.html", answer=answer, correct=correct, url=url)

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/send",methods=["POST"])
def send():
    file = request.files["file"]
    name = file.filename
    question = request.form["question"]
    question_answer = request.form["question_answer"]
    id = request.form["id"]
    if not name.endswith(".jpg"):
        return "Virheellinen tiedostonimi"
    data = file.read()
    if len(data) > 2000*2000:
        return "Liian iso tiedosto"
    response = trivia.upload_images_and_questions(name, question_answer, id, data, question)
    return response


    
if __name__ == "__main__":
    app.run(debug=True)



