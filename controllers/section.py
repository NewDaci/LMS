from app import app, db
from models.model import Book, Sections
from flask import session
from flask import render_template
from flask import request,flash
from flask import redirect
from datetime import date



################## CRUD on Section ##############
@app.route("/category")
def category():

    sec = Sections.query.all()
    l=[]

    for i in sec:
       l.append((i, Book.query.filter_by(section=i.id).count()))

    return render_template("admin/category.html", sec=l)


@app.route("/add-section", methods=["GET", "POST"])
def add_section():
    if request.method == "GET":
        return render_template("admin/add-section.html")
    
    elif request.method == "POST":
        name = request.form.get("name")
        datee = request.form.get("date")
        description = request.form.get("description")

        try:
            a = datee.split("-")
            b = date(int(a[0]), int(a[1]), int(a[2]))
        except:
            flash("Invalid Date!")
            return redirect("category")
        
        alr_ex_sec = Sections.query.filter_by(name=name).first()
        if alr_ex_sec:
            flash("Name already exists! Please provide unique name")
            return redirect("category")
        

        sec = Sections(name=name, date_created=b, description=description)
        db.session.add(sec)
        db.session.commit()
        flash("Section Added Successfully!")
        return redirect("category")

@app.route("/delete-section/<int:id>")
def delete_section(id):

    se = Sections.query.filter_by(id=id).first()
    books = Book.query.filter_by(section=id).all()
    for i in books:
        i.section = 1
    db.session.commit()
    db.session.delete(se)
    db.session.commit()
    flash("Section Deleted Successfully!")
    return redirect("/category")

@app.route("/update-section/<int:id>", methods=["GET", "POST"])
def update_section(id):
    if request.method == "GET":

        sec = Sections.query.filter_by(id=id).first()
        return render_template("section/<int:id>.html", sec=sec)
    
    elif request.method == "POST":
        name = request.form.get("name")
        datee = request.form.get("date")
        a = datee.split("-")
        b = date(int(a[0]), int(a[1]), int(a[2]))

        description = request.form.get("description")

        sec = Sections.query.filter_by(id=id).first()
        sec.name = name
        sec.date_created = b
        sec.description = description

        db.session.commit()
        flash("Section Updated Successfully!")
        return redirect("/category")
    
    
##################  ##############


@app.route("/view-section/<int:id>")
def view_section(id):

    sec = Sections.query.filter_by(id=id).first()
    books = Book.query.filter_by(section=id).all()
    return render_template("section/view/<int:id>.html", books=books, name=sec.name)

# add book to that particular section
@app.route("/new-book/<int:id>", methods=["GET", "POST"])
def new_book_to_sec(id):

    if request.method == "GET":
        
        sec = Sections.query.filter_by(id=id).first()
        return render_template("admin/new_book.html", sec=[sec])

    return redirect("category")
