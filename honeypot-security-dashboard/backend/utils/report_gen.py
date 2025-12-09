from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from models.log_entry import AttackLog
import os
from datetime import datetime

def generate_pdf_report(filename="report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Honeypot Attack Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fetch stats
    total_attacks = AttackLog.query.count()
    c.drawString(50, height - 120, f"Total Attacks Recorded: {total_attacks}")
    
    # Recent Attacks
    c.drawString(50, height - 150, "Recent Attacks:")
    recent_logs = AttackLog.query.order_by(AttackLog.timestamp.desc()).limit(10).all()
    
    y = height - 170
    for log in recent_logs:
        text = f"{log.timestamp} - {log.ip_address} ({log.country}) - {log.attack_type}"
        c.drawString(70, y, text)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
            
    c.save()
    return filename
