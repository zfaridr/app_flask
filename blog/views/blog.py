from flask import Blueprint, render_template


blog_app = Blueprint("blog_app", __name__)


@blog_app.route('/', endpoint='index')
def blog_l():
    return render_template('index.html')



