from app import app, db
from models.model import Book,Enrollments, Rating, Sections, Feedback, Status
from flask import render_template,session, redirect, request
from datetime import date
from fpdf import FPDF
from flask import send_file, flash


@app.route("/show/<int:id>")
def show(id):

    book = Book.query.filter_by(id=id).first()
    feedbacks = Feedback.query.filter_by(book_id=id).all()
    return render_template("show/<int:id>.html", book=book, feedbacks=feedbacks)


@app.route("/book-id/<int:id>")
def read_book(id):

    #get book contents
    book = Book.query.filter_by(id=id).first()
    curr_date = date.today()
    return render_template("/book_id/<int:id>.html",book=book, curr_date=curr_date)


@app.route("/my-book")
def my_book():

    curr_date = date.today()
    user_id = session.get("user_id")

    enrolls = Enrollments.query.filter_by(user_id=user_id).all()
    valid_books = []
    not_valid = []
    for i in enrolls:
        if curr_date < i.return_date:
            valid_books.append(i)
        else:
            not_valid.append(i)


    # for completed books
    comp_books = Status.query.filter_by(user_id=session.get('user_id')).all()
    books = []
    for i in comp_books:
        book = Book.query.get(i.book_id)
        books.append(book)

    return render_template("mybook.html", enrolls=valid_books, curr_date=curr_date, books=books, revoked=not_valid)

@app.route("/genre")
def genre():

    sections = Sections.query.all()
    data = [ (sec, Book.query.filter_by(section=sec.id).all()) for sec in sections ]
    return render_template("genre.html", data=data)


@app.route("/author")
def author():

    all_books = Book.query.all()

    #get all author names:
    authors = []
    for book in all_books:
        if book.author_name not in authors:
            authors.append(book.author_name)
    return render_template("author.html",all_books=all_books, authors=authors)

@app.route("/language")
def language():

    all_books = Book.query.all()

    #get all author names:
    languages = []
    for book in all_books:
        if book.language not in languages:
            languages.append(book.language)
    return render_template("language.html",all_books=all_books, languages=languages)


@app.route("/rating/<int:book_id>/<int:rate>")
def rating(book_id, rate):

    book = Book.query.filter_by(id=book_id).first()

    if book.rating is None:
        book.rating = rate
        rat_ob = Rating(book_id=book_id, total=rate, count=1)
        db.session.add(rat_ob)
    else:
        rating = Rating.query.filter_by(book_id=book.id).first()
        rating.total += rate
        rating.count += 1
        book.rating = rating.total//rating.count

    db.session.commit()
    return redirect("/book-id/"+str(book_id))


@app.route("/return_feedback/<int:book_id>/<int:enroll_id>", methods=["GET", "POST"])
def feedback(book_id, enroll_id):

    if request.method == "POST":
        feedback = request.form.get("feedback")
        read_value = request.form.get("read_val")

        if read_value == "Yes":
            status = Status(book_id=book_id, user_id=session.get('user_id'))
            db.session.add(status)

        if feedback != '':
            feed = Feedback(book_id=book_id, feedback=feedback)
            db.session.add(feed)

        enrollment = Enrollments.query.filter_by(id=enroll_id).first()
        db.session.delete(enrollment)

        db.session.commit()
    return redirect("/my-book")




@app.route("/download/<int:id>", methods=["GET", "POST"])
def download(id):

    if request.method == "POST":

        book = Book.query.filter_by(id=id).first()
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        paragraphs = book.content.split("\n\n")

        for paragraph in paragraphs:
            pdf.cell(200, 20, txt=paragraph.encode('latin-1', 'replace').decode('latin-1'), ln=1, align='C')

        temp_file = f"/home/daci/vscodez/mad1/library/download/{book.name}.pdf"
        pdf.output(temp_file)

        # Return the file to the user for download
        flash("Book Purchased Successfully! Check Downloads. <a href='/my-book'>Go Back</a>")
        return send_file(temp_file, as_attachment=True, mimetype="application/pdf")
    
    elif request.method == "GET":
        return render_template("download.html", id=id)


