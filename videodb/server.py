
import yaml

import flask

from videodb import scheduler
from videodb import tmdb

with open('config.yaml') as f:
    config = yaml.load(f)

tmdb.configure(config['tmdb']['api_key'])

app = flask.Flask('videodb')

@app.teardown_request
def shutdown_seesion(exception=None):
    from videodb.db import db_session
    
    db_session.commit()
    db_session.remove()

from videodb import db, pages

db.init_db()
pages.init_routing(app)

if __name__ == "__main__":
    host = config['host']
    debug = config['debug']
    
    app.run(host=host, debug=debug)