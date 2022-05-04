from random import randint
from flask import session
from db import db


def upload_images_and_questions(name, question_answer, id, data, question):
    sql_question = "INSERT INTO questions (question_id, question, answer) VALUES (:question_id, :question, :question_answer)"
    sql_image = "INSERT INTO images (question_id,question_answer,name,data) VALUES (:question_id,:question_answer,:name,:data)"
    db.session.execute(sql_question, {
                       "question_id": id, "question": question, "question_answer": question_answer})
    db.session.execute(sql_image, {
                       "question_id": id, "question_answer": question_answer, "name": name, "data": data})
    db.session.commit()
    return "Kuva ja kysymys tallennettu onnistuneesti"


def get_picture(question_answer, question_id):
    sql = "SELECT encode(data, 'base64') FROM images WHERE question_answer =:question_answer AND question_id =:question_id"
    result = db.session.execute(sql, {"question_answer": question_answer, "question_id": question_id})
    data = result.fetchone()[0]
    return data


def get_random_question(question_id):
    amount_sql = "SELECT COUNT(*) FROM questions WHERE question_id =:question_id"
    amount = db.session.execute(
        amount_sql, {"question_id": question_id}).fetchone()[0]
    while True:
        position = randint(0, amount-1)
        answer_sql = "SELECT answer FROM questions WHERE question_id =:question_id LIMIT 1 OFFSET :position"
        answer = db.session.execute(
            answer_sql, {"question_id": question_id, "position": position}).fetchone()[0]
        if answer in session['asked']:
            continue
        else:
            question_sql = "SELECT question FROM questions WHERE question_id =:question_id LIMIT 1 OFFSET :position"
            question = db.session.execute(
                question_sql, {"question_id": question_id, "position": position}).fetchone()[0]
            asked = session['asked']
            asked.append(answer)
            session['asked'] = asked
            break
    image = get_picture(answer, question_id)
    return (question, image, answer, question_id)
