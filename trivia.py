from random import randint
from flask import make_response
from db import db


def upload_images_and_questions(name, question_answer, id, data, question):
    sql_question = "INSERT INTO questions (question_id, question, answer) VALUES (:question_id, :question, :question_answer)"
    sql_image = "INSERT INTO images (question_id,question_answer,name,data) VALUES (:question_id,:question_answer,:name,:data)"
    db.session.execute(sql_question,{"question_id":id,"question":question,"question_answer":question_answer})
    db.session.execute(sql_image,{"question_id":id,"question_answer":question_answer,"name":name,"data":data})
    db.session.commit()
    return "Kuva ja kysymys tallennettu onnistuneesti"

def get_picture(question_answer):
    sql = "SELECT encode(data, 'base64') FROM images WHERE question_answer LIKE :question_answer"
    result = db.session.execute(sql, {"question_answer":question_answer})
    data = result.fetchone()[0]
    return data

def get_random_question(question_id):
    amount_sql = "SELECT COUNT(*) FROM questions WHERE question_id =:question_id"
    amount = db.session.execute(amount_sql, {"question_id":question_id}).fetchone()[0]
    position = randint(0, amount-1)
    question_sql = "SELECT question FROM questions WHERE question_id =:question_id LIMIT 1 OFFSET :position"
    question = db.session.execute(question_sql, {"question_id":question_id,"position":position}).fetchone()[0]
    answer_sql = "SELECT answer FROM questions WHERE question_id =:question_id LIMIT 1 OFFSET :position"
    answer = db.session.execute(answer_sql, {"question_id":question_id,"position":position}).fetchone()[0]
    image = get_picture(answer)
    return (question, image, answer)