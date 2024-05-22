from app import app, db
from models.model import Book, User, Book_req, Messages
from flask import session
from flask import render_template
from flask import request
from flask import redirect, url_for

@app.context_processor
def inject_admin():
    admin1 = 1
    admin0 = 0

    req = Book_req.query.all()
    msg = Messages.query.filter_by(user_id=session.get('user_id')).all()

    return dict(admin1=admin1, admin0=admin0, req=len(req), msg=len(msg))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404page.html"),404


@app.route("/", methods=["GET", "POST"])
def main():

    # else render login.html for "GET" method
    if request.method == "GET":
        return render_template("first_page.html")

    # render pages based on user or admin click "POST" method
    elif request.method == "POST":
        if "user_login" in request.form:
            return redirect(url_for("user_login"))
        elif "admin_login" in request.form:
            return redirect(url_for("admin_login"))


@app.route("/index")
def index():
    
    all_books = Book.query.all()
    latest = Book.query.order_by(Book.date_added.desc()).limit(6).all()
    trend = Book.query.order_by(Book.rating.desc()).limit(6).all()
    return render_template("index.html", all_books=all_books, latest=latest, trend=trend)

    

@app.route("/logout/<int:val>")
def logout(val):

    if val == 0:
        session.pop('user_id', None)
        return redirect(url_for('user_login'))
    
    else:
        session.pop('admin', None)
        return redirect(url_for("admin_login"))