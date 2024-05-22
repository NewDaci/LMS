from app import db

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    author_name = db.Column(db.String)
    section = db.Column(db.Integer, db.ForeignKey("sections.id"), nullable=False)
    language = db.Column(db.String)
    date_added = db.Column(db.Date)
    rating = db.Column(db.Integer)
    #till now its independent table

    #here comes the relationship
    enrollments = db.relationship("Enrollments", back_populates="book")
    ratings = db.relationship("Rating", backref="book")
    sections = db.relationship('Sections', backref='books')


class Sections(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date_created = db.Column(db.Date)
    description = db.Column(db.String)




class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    enrollments = db.relationship("Enrollments", back_populates="user")



class Enrollments(db.Model):
    __tablename__ = "enrollments"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    user = db.relationship("User", back_populates="enrollments")
    book = db.relationship("Book", back_populates="enrollments")

    issue_date = db.Column(db.Date)
    return_date = db.Column(db.Date)


    __table_args__ = (db.UniqueConstraint('user_id', 'book_id'),)



class Book_req(db.Model):
    __tablename__ = "book_req"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    user_name = db.Column(db.String,nullable=False)
    book_id = db.Column(db.Integer,nullable=False)
    book_name = db.Column(db.String,nullable=False)
    req_days = db.Column(db.Integer, nullable=False)
    issue_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    __table_args__ = (db.UniqueConstraint('user_id', 'book_id'),)



class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    feedback = db.Column(db.String)




class Rating(db.Model):
    __tablename__ = "rating"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    total = db.Column(db.Integer)
    count = db.Column(db.Integer)



class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)


class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=True)
    message = db.Column(db.String)