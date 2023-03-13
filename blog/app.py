from flask import Flask, render_template, Blueprint, url_for
from flask import request
from flask import g
from time import time
from werkzeug.exceptions import BadRequest
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.views.blog import blog_app
from blog.models.database import db
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from blog.views.authors import authors_app

cfg_name = os.environ.get("CONFIG_NAME") or "TestingConfig"

app = Flask(__name__)

app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
app.register_blueprint(blog_app, url_prefix="/")
app.register_blueprint(authors_app, url_prefix="/authors")

app.config["SECRET_KEY"] = "5207"
app.register_blueprint(auth_app, url_prefix="/auth")
login_manager.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.config.from_object(f"blog.configs.{cfg_name}")
migrate = Migrate(app, db, compare_type=True)

flask_bcrypt.init_app(app)

@app.route('/')
def index():
    render_template('index.html')

@app.route('/user/')
def read_user():
    name = request.args.get('name')
    surname = request.args.get('surname')
    return f"User {name or '[no name]'} {surname or '[no surname]'}"

@app.route("/status/", methods=["GET", "POST"])
def custom_status_code():
    if request.method == "GET":
        return """\
        To get response with custom...
        """
    print("raw bytes data:", request.data)

    if request.form and "code" in request.form:
        return "code from form", request.form["code"]
    
    if request.json and "code" in request.json:
        return "code from json", request.json["code"]
    
    return "", 204

@app.before_request
def process_before_request():
    g.start_time = time()

@app.after_request
def process_after_request(response):
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time
    
    return response

@app.route("/power/")
def power_value():
    x = request.args.get("x") or ""
    y = request.args.get("y") or ""
    if not (x.isdigit() and y.isdigit()):
        app.logger.info("invalid values for power: x=%r and y=%r", x, y)  
        raise BadRequest("please pass integer in 'x' and 'y' query params")
    
    x = int(x)
    y = int(y)
    result = x ** y
    app.logger.debug("%s **v %s = %s", x, y, result)
    return str(result)

@app.route("/divide_by_zero")
def do_zero_division():
    return 1 / 0

@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(error):
    print(error)
    app.logger.exception("Here's traceback for zero division error")
    return "Never divide by zero!", 400

# @app.cli.command("init-db")
# def init_db():
#     """
#     Run in your terminal:
#     flask init-db
#     """
#     db.create_all()
#     print("done!")

@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    from blog.models import user
    admin = user(username="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)
