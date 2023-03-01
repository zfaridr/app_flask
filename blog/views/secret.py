from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from blog.models import User

secret_app = Blueprint("secret_app", __name__)


@secret_app.route('/', endpoint='data')
def secret():
    {% if current_user.is_authenticated %}
        return render_template('secret/data.html')
    {% else %}
        return render_template('secret/not_allowed.html')
    {% endif %}
    