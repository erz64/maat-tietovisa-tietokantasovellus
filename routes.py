from app import app
from flask import redirect, render_template, request, session
from os import getenv
import trivia
import users
import stats

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("frontpage.html")  

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login_sql(username,password):
        return render_template("errors.html", error = "Väärä käyttäjätunnus tai salasana")
    return redirect("/")

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("errors.html", error = "Salasanat eivät ole samat")
        if len(password1) < 3:
            return render_template("errors.html", error = "Salasanassa pitää olla vähintään 3 merkkiä")
        if len(password1) > 30:
            return render_template("errors.html", error = "Salasanassa saa olla enintään 30 merkkiä")
        users.register(username, password1)
        return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/paakaupungit")
def capitals_quiz_start():
    session['asked'] = []
    highscores = stats.get_highscores_all("Minkä maan pääkaupunki?")
    question_data = trivia.get_random_question(1)
    return render_template("trivia.html",question=question_data[0], image=question_data[1], correct=question_data[2], right_answers=0, counter=0, highscores=highscores)

@app.route("/paakaupungit/result", methods=["post"])
def answer():
    answer = request.form["answer"].strip()
    correct = request.form["correct"].strip()
    right_answers = int(request.form["right_answers"])
    counter = int(request.form["counter"])
    url = "/paakaupungit/1"
    counter += 1
    if counter >= 10:
        if answer.lower() == correct.lower():
            right_answers +=1
        stats.insert_into_scores(session["user_id"], "Minkä maan pääkaupunki?", session["username"], right_answers)
        del session['asked']
        if 0 <= right_answers <= 3:
            return render_template("total_result_bad.html", correct=correct, right_answers=right_answers, counter=counter)
        if 4 <= right_answers <= 7:
            return render_template("total_result_ok.html", correct=correct, right_answers=right_answers, counter=counter)
        else:
            return render_template("total_result_good.html", correct=correct, right_answers=right_answers, counter=counter)
    if answer.lower() == correct.lower():
        right_answers += 1
        return render_template("correct_result.html", url=url, right_answers=right_answers, counter=counter)
    return render_template("wrong_result.html",correct=correct, url=url, right_answers=right_answers, counter=counter)

@app.route("/paakaupungit/1", methods = ["POST"])
def capitals_quiz():
    highscores = stats.get_highscores_all("Minkä maan pääkaupunki?")
    right_answers = int(request.form["right_answers"])
    counter = int(request.form["counter"])
    question_data = trivia.get_random_question(1)
    return render_template("trivia.html", question=question_data[0], image=question_data[1], correct=question_data[2], right_answers=right_answers, counter=counter, highscores=highscores)

@app.route("/form")
def form():
    users.admin_role_required(1)
    return render_template("form.html")

@app.route("/send",methods=["POST"])
def send():
    file = request.files["file"]
    name = file.filename
    question = request.form["question"]
    question_answer = request.form["question_answer"]
    if question == "" or question_answer == "":
        return "Kysymys tai vastaus eivät voi olla tyhjiä"
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



