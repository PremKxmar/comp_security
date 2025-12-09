from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import time
import json
import threading
from models.log_entry import db
from routes.honeypot import honeypot_bp
from routes.dashboard import dashboard_bp
from routes.reports import reports_bp
from utils.sse import announcer

load_dotenv()

app = Flask(__name__)
# Use SQLite as fallback if DATABASE_URL is not set or is invalid
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Register Blueprints
app.register_blueprint(honeypot_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(reports_bp)

@app.route('/')
def index():
    return "Honeypot Backend Running"

@app.route('/api/stream')
def stream():
    def event_stream():
        messages = announcer.listen()
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
