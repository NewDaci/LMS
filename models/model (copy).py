from app import db

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    author = db.Column(db.String)
    section = db.Column(db.Integer, db.ForeignKey("section.id"), nullable=False)
    issuedate = db.Column(db.Date)
    returndate = db.Column(db.Date)
    enrollments = db.relationship("Enrollment", back_populates="book")

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    enrollments = db.relationship("Enrollment", back_populates="user")
    
    
class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.Date)
    detail = db.Column(db.String)

class Book_req(db.Model):
    __tablename__ = "book_req"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    u_id = db.Column(db.Integer,nullable=False)
    u_name = db.Column(db.String,nullable=False)
    b_id = db.Column(db.Integer,nullable=False)
    b_name = db.Column(db.String,nullable=False)
   
   
class Enrollment(db.Model):
    __tablename__ = "enrollment"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    b_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user = db.relationship("User", back_populates="enrollments")
    book = db.relationship("Book", back_populates="enrollments")


