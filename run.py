#!flask/bin/python
import sys
from flask import Flask
import extensions
from main import views, users, fruits, vegetables, gasoline, consumerprice, exchangerates, weather, herbs, nuts, ornamentals, commodities
import utils as utl
from flask import jsonify
from flask_cors import CORS
import emails

# @TODO: add this as a command line tool
debug_config = False

def register_blueprints(app):
    app.register_blueprint(views.blueprint)
    app.register_blueprint(users.blueprint)
    app.register_blueprint(fruits.blueprint)
    app.register_blueprint(vegetables.blueprint)
    app.register_blueprint(gasoline.blueprint)
    app.register_blueprint(consumerprice.blueprint)
    app.register_blueprint(exchangerates.blueprint)
    app.register_blueprint(weather.blueprint)
    app.register_blueprint(herbs.blueprint)
    app.register_blueprint(nuts.blueprint)
    app.register_blueprint(ornamentals.blueprint)
    app.register_blueprint(commodities.blueprint)
    return None


def create_app(config_object="prod"):
    app = Flask(__name__)
    app.config.from_object('config_debug' if debug_config else 'config')
    extensions.db.init_app(app)
    emails.mail.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.login_manager.session_protection = 'strong'
    extensions.login_manager.login_view = "/login"
    register_blueprints(app)
    return app


app = create_app("prod")
CORS(app)


@app.errorhandler(403)
def error_403(e):
    return (jsonify({'response_status': "ERROR"},
                    {'response_message': "Coming Soon"}), 200)


@app.errorhandler(404)
def error_404(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "Coming Soon"}), 200)


@app.errorhandler(405)
def error_405(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "METHOD NOT ALLOWED"}), 200)


@app.errorhandler(500)
def error_500(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "Internal Server Error"}), 200)


if __name__ == '__main__':
    # @Todo: Convert logger to module specific
    logger = utl.logging

    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', debug=True, port=port)

