from .configs import configs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# =====
# DB
db = SQLAlchemy()

# =====
# App factory \0o0/
def build_app(config_name):

    app = Flask(__name__)
    app.config.from_object( configs[config_name] )

    # CORS
    CORS(app)

    # DB
    db.init_app(app)

    # Blueprints
    from .docs import docs as docs_blueprint
    app.register_blueprint(docs_blueprint) 

    from .word import word as word_blueprint
    app.register_blueprint(word_blueprint, url_prefix="/word") 

    from .game import game as game_blueprint
    app.register_blueprint(game_blueprint, url_prefix="/game") 

    from .leaderboard import leaderboard as leaderboard_blueprint
    app.register_blueprint(leaderboard_blueprint, url_prefix="/leaderboard")
    return app

