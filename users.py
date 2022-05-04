import os
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, session, abort


def check_username(username):
    sql = "SELECT username FROM users WHERE username =:username"
    user = db.session.execute(sql, {"username": username}).fetchone()
    if not user:
        return False
    return True


def login_sql(username, password):
    if not check_username(username):
        return False
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username": username}).fetchone()
    hash_value = user.password
    if not check_password_hash(hash_value, password):
        return False
    session["username"] = username
    session["role"] = user[2]
    session["user_id"] = user[0]
    session["csrf_token"] = os.urandom(16).hex()
    return True


def register(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)"
    db.session.execute(
        sql, {"username": username, "password": hash_value, "admin": 0})
    db.session.commit()


def admin_role_required(role):
    if role != session.get("role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)