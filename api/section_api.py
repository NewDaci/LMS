from app import api, db
from flask_restful import Resource
from flask import make_response
from models.model import Book, Sections
from flask_restful import fields, marshal, marshal_with
from werkzeug.exceptions import HTTPException
from flask_restful import reqparse
from datetime import date
import json


#marshalling
section_fields={
  "id": fields.Integer,
  "name": fields.String,
  'date_created': fields.DateTime(dt_format='iso8601'),
  "description": fields.String
}

#section_parser
section_parser = reqparse.RequestParser()
section_parser.add_argument("name")
section_parser.add_argument("date_created")
section_parser.add_argument("description")


class SectionNotFound(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class BadReqCodeError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        error = {"error_code": error_code, "error_message": error_message}
        self.response = make_response( json.dumps(error), status_code )




class SectionAPI(Resource):

    @marshal_with(section_fields)
    def get(self, section_name):

        try:  
            sec = Sections.query.filter_by(name=section_name).first()
        except:
            raise SectionNotFound(status_code=500)  #internal server error that database throws

        if sec is None:
            raise SectionNotFound(status_code=404)
        return sec,200



    def post(self):

        args = section_parser.parse_args()
        name = args.get("name", None)
        date_created = args.get("date_created", None)
        description = args.get("description", None)

        #check for errors 400
        if name is None:
            raise BadReqCodeError(status_code=400, error_code="SEC001", error_message="Name is required")
        if date_created is None:
            raise BadReqCodeError(status_code=400, error_code="SEC002", error_message="Date is required")
        
        alr_sec = Sections.query.filter_by(name=name).first()
        if alr_sec:
            raise BadReqCodeError(status_code=409, error_code="SEC009", error_message="Section Already Exits")

        try:
            a = date_created.split("-")
            b = date(int(a[0]), int(a[1]), int(a[2]))
        except:
            raise BadReqCodeError(status_code=400, error_code="SEC005", error_message="Invalid Date Format")

        try:
            new_sec = Sections(
                name=name,
                date_created = b,
                description = description
            )
            db.session.add(new_sec)
            db.session.commit()
        except:
            raise SectionNotFound(status_code=500)
        return marshal(new_sec, section_fields), 201
    


        
    def delete(self, section_name):

        try:  
            sec = Sections.query.filter_by(name=section_name).first()
        except:
            raise SectionNotFound(status_code=500)  #internal server error that database throws

        if sec:
            try:
                books = Book.query.filter_by(section=sec.id).all()
                if books:
                    for i in books:
                            i.section = 1
                    db.session.commit()
                db.session.delete(sec)
                db.session.commit()
                return '', 200

            except:
                raise SectionNotFound(status_code=500)  #internal server error that database throws
            
        #throw error not found
        raise SectionNotFound(status_code=404)
    



    def put(self, section_id):

        args = section_parser.parse_args()
        name = args.get("name", None)
        date_created = args.get("date_created", None)
        description = args.get("description", None)

        try:
            a = date_created.split("-")
            b = date(int(a[0]), int(a[1]), int(a[2]))
        except:
            raise BadReqCodeError(status_code=400, error_code="SEC005", error_message="Invalid Date Format")

        try:
            section = Sections.query.filter_by(id=section_id).first()
        except:
            raise SectionNotFound(status_code=500)  #internal server error that database throws
        
        
        if  Sections.query.filter_by(name=name).first():
            raise BadReqCodeError(status_code=400, error_code="SEC006", error_message="Name Already Taken")

        if section:
            try:
                section.name = name
                section.date_created = b
                section.description = description
                db.session.commit()
                return marshal(section, section_fields),200
            except:
                raise SectionNotFound(status_code=500)
            
        #throw error not found
        raise SectionNotFound(status_code=404)


api.add_resource(SectionAPI, '/api/section', '/api/section/<section_name>', '/api/section/<int:section_id>')
