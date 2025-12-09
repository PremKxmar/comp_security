from flask import Blueprint, jsonify
import pandas as pd
from models.log_entry import AttackLog, db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/stats', methods=['GET'])
def stats():
    total_attacks = AttackLog.query.count()
    
    # Attacks by Country
    country_stats = db.session.query(AttackLog.country, func.count(AttackLog.id)).group_by(AttackLog.country).all()
    
    # Attacks by Type
    type_stats = db.session.query(AttackLog.attack_type, func.count(AttackLog.id)).group_by(AttackLog.attack_type).all()
    
    # Recent Logs
    recent_logs = AttackLog.query.order_by(AttackLog.timestamp.desc()).limit(10).all()
    
    # Attacks over Time (Last 24 Hours) using Pandas
    # We fetch all for now, but in production should limit query
    query = AttackLog.query.statement
    df = pd.read_sql(query, db.session.bind)
    
    attacks_over_time = []
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Group by hour
        hourly_counts = df.resample('H', on='timestamp').size().reset_index(name='count')
        # Format for frontend
        attacks_over_time = hourly_counts.apply(lambda x: {
            "time": x['timestamp'].strftime('%H:%M'),
            "count": x['count']
        }, axis=1).tolist()

    return jsonify({
        "total_attacks": total_attacks,
        "country_stats": dict(country_stats),
        "type_stats": dict(type_stats),
        "recent_logs": [log.to_dict() for log in recent_logs],
        "attacks_over_time": attacks_over_time
    })
