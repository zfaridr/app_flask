from flask import Blueprint, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


blog_app = Blueprint("blog_app", __name__)


@blog_app.route('/', endpoint='index')
def blog_l():
    return render_template('index.html')



