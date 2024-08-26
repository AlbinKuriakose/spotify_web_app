from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv
import os
from routes import configure_routes

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('SECRET_KEY')

    app.config['CLIENT_ID'] = os.environ.get('CLIENT_ID')

    app.config['CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET')


    app.config['REDIRECT_URI'] = 'https://127.0.0.1:5555/callback'

    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    app.config['SESSION_COOKIE_SECURE'] = True


    configure_routes(app)

    return app

if __name__ == '__main__':

    app = create_app()

    app.run(host='0.0.0.0', port = 5555, ssl_context = 'adhoc')

