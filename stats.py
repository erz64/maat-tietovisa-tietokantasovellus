from db import db


def get_highscores_all(question):
    sql = "SELECT username, MAX(score) FROM SCORES WHERE question=:question GROUP BY username ORDER BY MAX(SCORE) DESC LIMIT 10"
    highscores = db.session.execute(sql, {"question": question}).fetchall()
    return highscores


def insert_into_scores(user_id, question, username, score):
    sql = "INSERT INTO SCORES (user_id, question, username, score) VALUES (:user_id, :question, :username, :score)"
    db.session.execute(sql, {
                       "user_id": user_id, "question": question, "username": username, "score": score})
    db.session.commit()
