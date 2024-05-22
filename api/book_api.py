from app import api,app, db
from flask_restful import Resource
from flask import make_response
from models.model import Book, Sections, Book_req, Feedback, Messages, Status
from flask_restful import fields, marshal, marshal_with
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask_restful import reqparse
from datetime import date
import json

CORS(app)

#marshalling
book_fields={
  "id": fields.Integer,
  "isbn": fields.Integer,
  "name": fields.String,
  "author_name": fields.String,
  "sections.name": fields.String,
  "language": fields.String,
  "content": fields.String,
  'date_added': fields.DateTime(dt_format='iso8601'),
  "rating": fields.Integer
}

#book_parser
book_parser = reqparse.RequestParser()
book_parser.add_argument("isbn")
book_parser.add_argument("name")
book_parser.add_argument("author_name")
book_parser.add_argument("section")
book_parser.add_argument("language")
book_parser.add_argument("content")
book_parser.add_argument("date_added")


class BookNotFound(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class BadReqCodeError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        error = {"error_code": error_code, "error_message": error_message}
        self.response = make_response( json.dumps(error), status_code )




class BookAPI(Resource):

    @marshal_with(book_fields)
    def get(self, book_name):

        try:  
            book = Book.query.filter_by(name=book_name).first()
        except:
            raise BookNotFound(status_code=500)  #internal server error that database throws

        if book is None:
            raise BookNotFound(status_code=404)
        return book,200



    def post(self):

        args = book_parser.parse_args()
        isbn = args.get("isbn", None)
        name = args.get("name", None)
        author_name = args.get("author_name", None)
        section = args.get("section", None)
        language = args.get("language", None)
        content = args.get("content", None)
        date_added = args.get("date_added", None)

        #check for errors 400
        if isbn is None:
            raise BadReqCodeError(status_code=400, error_code="BOOK001", error_message="ISBN No. required")
        if name is None:
            raise BadReqCodeError(status_code=400, error_code="BOOK002", error_message="Name is required")
        if section is None:
            raise BadReqCodeError(status_code=400, error_code="BOOK003", error_message="Section is required")
        if date_added is None:
            raise BadReqCodeError(status_code=400, error_code="BOOK004", error_message="Date is required")
        
        alr_book = Book.query.filter_by(isbn=isbn, name=name).first()
        if alr_book:
            raise BadReqCodeError(status_code=409, error_code="BOOK009", error_message="Book Already Exits")

        try:
            a = date_added.split("-")
            b = date(int(a[0]), int(a[1]), int(a[2]))
        except:
            raise BadReqCodeError(status_code=400, error_code="BOOK005", error_message="Invalid Date Format")

        try:
            section = Sections.query.filter_by(name=section).first()
        except:
            raise BadReqCodeError(status_code=400, error_code="BOOK006", error_message="Section Not Found")

        try:
            new_book = Book(
                isbn=isbn,
                name=name,
                author_name=author_name,
                language=language,
                content=content,
                section=section.id,
                date_added = b
            )
            db.session.add(new_book)
            db.session.commit()
        except:
            raise BookNotFound(status_code=500)
        return marshal(new_book, book_fields), 201
    


        
    def delete(self, book_name):

        try:  
            book = Book.query.filter_by(name=book_name).first()
        except:
            raise BookNotFound(status_code=500)  #internal server error that database throws

        if book:
            try:
                l=[]

                l.append(book.enrollments)
                l.append(book.ratings)
                l.append(Book_req.query.filter_by(book_id=book.id).all())
                l.append(Feedback.query.filter_by(book_id=book.id).all())
                l.append(Messages.query.filter_by(book_id=book.id).all())
                l.append(Status.query.filter_by(book_id=book.id).all())

                for i in l:
                    for j in i:
                        db.session.delete(j)

                db.session.commit() 
                db.session.delete(book)
                db.session.commit()
                return '', 200
            except:
                raise BookNotFound(status_code=500)
            
        #throw error not found
        raise BookNotFound(status_code=404)
    



    def put(self, book_id):

        args = book_parser.parse_args()
        isbn = args.get("isbn", None)
        name = args.get("name", None)
        author_name = args.get("author_name", None)
        section = args.get("section", None)
        language = args.get("language", None)
        content = args.get("content", None)
        date_added = args.get("date_added", None)

        try:
            a = date_added.split("-")
            b = date(int(a[0]), int(a[1]), int(a[2]))
        except:
            raise BadReqCodeError(status_code=400, error_code="BOOK005", error_message="Invalid Date Format")

        try:
            section = Sections.query.filter_by(name=section).first()
        except:
            raise BadReqCodeError(status_code=400, error_code="BOOK006", error_message="Section Not Found")


        try:  
            book = Book.query.filter_by(id=book_id).first()
        except:
            raise BookNotFound(status_code=500)  #internal server error that database throws

        if book:
            try:
                book.isbn = isbn
                book.name = name
                book.author_name = author_name
                book.section = section.id
                book.language = language
                book.date_added = b
                book.content = content
                
                db.session.commit()
                return marshal(book, book_fields),200
            except:
                raise BookNotFound(status_code=500)
            
        #throw error not found
        raise BookNotFound(status_code=404)
    
    



api.add_resource(BookAPI, '/api/book', '/api/book/<book_name>', '/api/book/<int:book_id>')
