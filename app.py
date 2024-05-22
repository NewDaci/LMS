from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify, request 
from flask_restful import Resource, Api 
from flask_bcrypt import Bcrypt


app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

app.secret_key = b'verysecretpass'
app.config['SESSION_PERMANENT'] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.sqlite3"
db = SQLAlchemy()
migrate = Migrate(app, db)


db.init_app(app)
app.app_context().push()


#import Controllers
from controllers.books import *
from controllers.index import *
from controllers.user import *
from controllers.admin import *
from controllers.issue_book import *
from controllers.section import *
from controllers.enrollments import *
from api.book_api import *
from api.section_api import *


if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run()
