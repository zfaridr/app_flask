from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

articles_app = Blueprint("articles_app", __name__)
ARTICLES = {
    1: "New thoughts",
    2: "My life",
    3: "Family",
}

@articles_app.route('/', endpoint='list')
def articles_list():
    return render_template('articles/list.html', articles=ARTICLES)


@articles_app.route("/<int:article_id>/", endpoint='details')
def articles_details(article_id: int):
    try:
        article_name = ARTICLES[article_id]
    except KeyError:
        raise NotFound(f"Article #{article_id} doesn't exist")
    return render_template('articles/details.html', article_id = article_id, article_name = article_name)
