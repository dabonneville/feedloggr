
import datetime
import feedparser

from flask import Blueprint, render_template

from .models import *

######################################################################

feedloggr = Blueprint(
    'feedloggr',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/feedloggr',
)

@feedloggr.route('/')
@feedloggr.route('/<int:year>-<int:month>-<int:day>')
def index(year=None, month=None, day=None):
    try:
        date = datetime.date(year, month, day)
    except (ValueError, TypeError):
        date = datetime.date.today()

    news = []
    date = Date.get_or_create(date = date) # TODO: deprecated func
    if date:
        for feed in Feed.select().order_by(Feed.title.desc()):
            items = Entry.select().where(
                Entry.feed == feed,
                Entry.date == date
            )

            if items.count() > 0:
                news.append({
                    'title': feed.title,
                    'link': feed.link,
                    'items': items,
                })

    delta = datetime.timedelta(days=1)
    context = {
        'news': news,
        'date': str(date.date),
        'next_day': str(date.date + delta),
        'prev_day': str(date.date - delta),
    }
    return render_template('index.html', **context)

