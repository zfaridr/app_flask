from flask import Flask, render_template, Blueprint
from flask import request
from flask import g
from time import time
from werkzeug.exceptions import BadRequest
from blog.views.users import users_app
from blog.views.articles import articles_app

app = Flask(__name__)

app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")

@app.route('/')
def index:
    render_template('index.html')

@app.route('/<data>')
def index(data: str):
    return f'Hello!, {data}'

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
