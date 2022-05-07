from pydoc import render_doc
from app import app
from flask import redirect, render_template, request, session
from os import getenv
import trivia
import users
import stats

app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    stars_capitals = stats.get_reviews_all(1)
    stars_food = stats.get_reviews_all(2)
    stars_flags = stats.get_reviews_all(3)
    return render_template("frontpage.html", stars_capitals=stars_capitals, stars_food=stars_food, stars_flags=stars_flags)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login_sql(username, password):
        return render_template("errors.html", error="Väärä käyttäjätunnus tai salasana")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("errors.html", error="Salasanat eivät ole samat")
        if len(password1) < 3:
            return render_template("errors.html", error="Salasanassa pitää olla vähintään 3 merkkiä")
        if len(password1) > 30:
            return render_template("errors.html", error="Salasanassa saa olla enintään 30 merkkiä")
        users.register(username, password1)
        return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    del session["role"]
    del session["user_id"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/paakaupungit")
def capitals_quiz_start():
    try:
        session["username"]
    except:
        return render_template("errors.html", error = "Sinun pitää kirjautua ensin.")
    session['asked'] = []
    highscores = stats.get_highscores_all("Minkä maan pääkaupunki?")
    question_data = trivia.get_random_question(1)
    url = "/paakaupungit/result"
    title = "Pääkaupungit"
    return render_template("trivia.html", title=title, url=url, question=question_data[0], 
        image=question_data[1], correct=question_data[2], right_answers=0, counter=0, highscores=highscores)


@app.route("/paakaupungit/result", methods=["post"])
def capitals_result():
    users.check_csrf()
    answer = request.form["answer"].strip()
    correct = request.form["correct"].strip()
    right_answers = int(request.form["right_answers"])
    counter = int(request.form["counter"])
    url = "/paakaupungit/1"
    counter += 1
    if counter >= 10:
        if answer.lower() == correct.lower():
            right_answers += 1
        stats.insert_into_scores(
            session["user_id"], "Minkä maan pääkaupunki?", session["username"], right_answers)
        del session['asked']
        if 0 <= right_answers <= 3:
            return render_template("total_result_bad.html", correct=correct, right_answers=right_answers, counter=counter, question_id=1)
        if 4 <= right_answers <= 7:
            return render_template("total_result_ok.html", correct=correct, right_answers=right_answers, counter=counter, question_id=1)
        else:
            return render_template("total_result_good.html", correct=correct, right_answers=right_answers, counter=counter, question_id=1)
    if answer.lower() == correct.lower():
        right_answers += 1
        return render_template("correct_result.html", url=url, right_answers=right_answers, counter=counter)
    return render_template("wrong_result.html", correct=correct, url=url, right_answers=right_answers, counter=counter)


@app.route("/paakaupungit/1", methods=["POST"])
def capitals_quiz():
    users.check_csrf()
    highscores = stats.get_highscores_all("Minkä maan pääkaupunki?")
    right_answers = int(request.form["right_answers"])
    counter = int(request.form["counter"])
    question_data = trivia.get_random_question(1)
    url = "/paakaupungit/result"
    title = "Pääkaupungit"
    return render_template("trivia.html", title=title, url=url, question=question_data[0], image=question_data[1],
        correct=question_data[2], right_answers=right_answers, counter=counter, highscores=highscores)


@app.route("/ruoat")
def food_quiz_start():
    try:
        session["username"]
    except:
        return render_template("errors.html", error = "Sinun pitää kirjautua ensin.")
    session['asked'] = []
    highscores = stats.get_highscores_all("Minkä maan kansallisruoka?")
    question_data = trivia.get_random_question(2)
    url = "/ruoat/result"
    title = "Kansallisruoat"
    return render_template("trivia.html", title=title, url=url, question=question_data[0], image=question_data[1],
        correct=question_data[2], right_answers=0, counter=0, highscores=highscores)


@app.route("/ruoat/result", methods=["post"])
def food_result():
    users.check_csrf()
    answer = request.form["answer"].strip()
    correct = request.form["correct"].strip()
    right_answers = int(request.form["right_answers"])
    counter = int(request.form["counter"])
    url = "/ruoat/1"
    counter += 1
    if counter >= 10:
        if answer.lower() == correct.lower():
            right_answers += 1
        stats.insert_into_scores(
            session["user_id"], "Minkä maan kansallisruoka?", session["username"], right_answers)
        del session['asked']
        if 0 <= right_answers <= 3:
            return render_template("total_result_bad.html", correct=correct, right_answers=right_answers, counter=counter, question_id=2)
        if 4 <= right_answers <= 7:
            return render_template("total_result_ok.html", correct=correct, right_answers=right_answers, counter=counter, question_id=2)
        else:
            return render_template("total_result_good.html", correct=correct, right_answers=right_answers, counter=counter, question_id=2)
    if answer.lower() == correct.lower():
        right_answers += 1
        return render_template("correct_result.html", url=url, right_answers=right_answers, counter=counter)
    return render_template("wrong_result.html", correct=correct, url=url, right_answers=right_answers, counter=counter)


@app.route("/ruoat/1", methods=["POST"])
def food_quiz():
    users.check_csrf()
    highscores = stats.get_highscores_all("Minkä maan kansallisruoka?")
    right_answers = int(request.form["right_answers"])
    counter = int(request.form["counter"])
    question_data = trivia.get_random_question(2)
    url = "/ruoat/result"
    title = "Kansallisruoat"
    return render_template("trivia.html", title=title, url=url, question=question_data[0], image=question_data[1], correct=question_data[2], right_answers=right_answers, counter=counter, highscores=highscores)


@app.route("/liput")
def flags_quiz_start():
    try:
        session["username"]
    except:
        return render_template("errors.html", error = "Sinun pitää kirjautua ensin.")
    session['asked'] = []
    highscores = stats.get_highscores_all("Minkä maan lippu?")
    question_data = trivia.get_random_question(3)
    url = "/liput/result"
    title = "Liput"
    return render_template("trivia.html", title=title, url=url, question=question_data[0], 
        image=question_data[1], correct=question_data[2], right_answers=0, counter=0, highscores=highscores)


@app.route("/liput/result", methods=["post"])
def flags_result():
    users.check_csrf()
    answer = request.form["answer"].strip()
    correct = request.form["correct"].strip()
    right_answers = int(request.form["right_answers"])
    counter = int(request.form["counter"])
    url = "/liput/1"
    counter += 1
    if counter >= 10:
        if answer.lower() == correct.lower():
            right_answers += 1
        stats.insert_into_scores(
            session["user_id"], "Minkä maan lippu?", session["username"], right_answers)
        del session['asked']
        if 0 <= right_answers <= 3:
            return render_template("total_result_bad.html", correct=correct, right_answers=right_answers, counter=counter, question_id=1)
        if 4 <= right_answers <= 7:
            return render_template("total_result_ok.html", correct=correct, right_answers=right_answers, counter=counter, question_id=1)
        else:
            return render_template("total_result_good.html", correct=correct, right_answers=right_answers, counter=counter, question_id=1)
    if answer.lower() == correct.lower():
        right_answers += 1
        return render_template("correct_result.html", url=url, right_answers=right_answers, counter=counter)
    return render_template("wrong_result.html", correct=correct, url=url, right_answers=right_answers, counter=counter)


@app.route("/liput/1", methods=["POST"])
def flags_quiz():
    users.check_csrf()
    highscores = stats.get_highscores_all("Minkä maan lippu?")
    right_answers = int(request.form["right_answers"])
    counter = int(request.form["counter"])
    question_data = trivia.get_random_question(3)
    url = "/liput/result"
    title = "Liput"
    return render_template("trivia.html", title=title, url=url, question=question_data[0], image=question_data[1],
        correct=question_data[2], right_answers=right_answers, counter=counter, highscores=highscores)


@app.route("/review", methods=["post"])
def review():
    users.check_csrf()
    star = request.form["star"]
    question_id = request.form["question_id"]
    stats.insert_into_reviews(session["user_id"], star, question_id)
    return render_template("review.html")


@app.route("/form")
def form():
    users.admin_role_required(1)
    return render_template("form.html")


@app.route("/send", methods=["POST"])
def send():
    users.check_csrf()
    file = request.files["file"]
    name = file.filename
    question = request.form["question"]
    question_answer = request.form["question_answer"]
    if question == "" or question_answer == "":
        return "Kysymys tai vastaus eivät voi olla tyhjiä"
    id = request.form["id"]
    if not name.endswith(".jpg") and not name.endswith(".png"):
        return "Virheellinen tiedostonimi"
    data = file.read()
    if len(data) > 2000*2000:
        return "Liian iso tiedosto"
    response = trivia.upload_images_and_questions(
        name, question_answer, id, data, question)
    return response


if __name__ == "__main__":
    app.run(debug=True)
