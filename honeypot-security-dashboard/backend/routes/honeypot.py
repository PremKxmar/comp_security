from flask import Blueprint, request, jsonify, Response
from models.log_entry import db, AttackLog
from models.ml_model import AttackClassifier
from utils.geoip import get_location
from utils.sse import announcer
import json

honeypot_bp = Blueprint('honeypot', __name__)
classifier = AttackClassifier()

def log_attack(endpoint, method, payload=None):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    country, city = get_location(ip)
    
    # Classify attack
    attack_type = classifier.predict(payload)
    
    log = AttackLog(
        ip_address=ip,
        country=country,
        city=city,
        endpoint=endpoint,
        method=method,
        payload=payload,
        user_agent=user_agent,
        attack_type=attack_type
    )
    db.session.add(log)
    db.session.commit()
    
    # Notify SSE stream
    announcer.announce(f"data: {json.dumps(log.to_dict())}\n\n")

@honeypot_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        username = data.get('username')
        password = data.get('password')
        payload = f"User: {username}, Pass: {password}"
        log_attack('/login', 'POST', payload)
        return jsonify({"error": "Invalid credentials"}), 401
    
    log_attack('/login', 'GET')
    return jsonify({"message": "Login required"}), 200

@honeypot_bp.route('/api/admin', methods=['GET'])
def admin_api():
    log_attack('/api/admin', 'GET')
    return jsonify({"error": "Unauthorized"}), 403

@honeypot_bp.route('/wp-admin', methods=['GET'])
def wp_admin():
    log_attack('/wp-admin', 'GET')
    return "Not Found", 404

@honeypot_bp.route('/admin', methods=['GET', 'POST'])
@honeypot_bp.route('/administrator', methods=['GET', 'POST'])
def fake_admin():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        username = data.get('username')
        password = data.get('password')
        payload = f"Admin Attempt - User: {username}, Pass: {password}"
        log_attack(request.path, 'POST', payload)
        return jsonify({"error": "Invalid credentials"}), 401
    
    log_attack(request.path, 'GET')
    return jsonify({"message": "Admin Login Required"}), 200

@honeypot_bp.route('/backup', methods=['GET'])
@honeypot_bp.route('/database.sql', methods=['GET'])
def fake_backup():
    log_attack(request.path, 'GET', "Attempted to download database backup")
    # Return a fake SQL dump
    fake_sql = "-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)\n--\n-- Host: localhost    Database: sensitive_data\n-- ------------------------------------------------------\n\nDROP TABLE IF EXISTS `users`;\nCREATE TABLE `users` (\n  `id` int NOT NULL AUTO_INCREMENT,\n  `username` varchar(255) NOT NULL,\n  `password` varchar(255) NOT NULL,\n  PRIMARY KEY (`id`)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n-- Dumping data for table `users`\n-- (Fake data to trick attacker)\nINSERT INTO `users` VALUES (1,'admin','5f4dcc3b5aa765d61d8327deb882cf99');"
    return Response(fake_sql, mimetype='text/plain')

@honeypot_bp.route('/.env', methods=['GET'])
@honeypot_bp.route('/config.php', methods=['GET'])
def fake_env():
    log_attack(request.path, 'GET', "Attempted to access sensitive config file")
    fake_env_content = "DB_HOST=localhost\nDB_USER=root\nDB_PASS=password123\nSECRET_KEY=supersecretkey"
    return Response(fake_env_content, mimetype='text/plain')
