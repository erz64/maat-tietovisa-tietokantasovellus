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


def get_reviews_all(question_id):
    sql = "SELECT AVG(star) FROM reviews WHERE question_id=:question_id"
    stars = db.session.execute(sql, {"question_id": question_id}).fetchone()[0]
    rounded_stars = round(stars)
    return rounded_stars


def insert_into_reviews(user_id, star, question_id):
    sql = "INSERT INTO reviews (user_id, star, question_id) SELECT :user_id, :star, :question_id WHERE NOT EXISTS (SELECT user_id FROM reviews WHERE user_id=:user_id AND question_id=:question_id)"
    db.session.execute(
        sql, {"user_id": user_id, "star": star, "question_id": question_id})
    db.session.commit()
