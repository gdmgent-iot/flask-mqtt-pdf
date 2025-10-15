import os
from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory

# Blueprint voor main routes - groepeer gerelateerde routes
bp = Blueprint('main', __name__)

@bp.get('/')
def index():
    return render_template('index.html',
                           mqtt_topic=os.getenv('MQTT_TOPIC', 'demo/messages'),
                           mqtt_port=int(os.getenv('MQTT_PORT', '9001')),
                           mqtt_host=os.getenv('MQTT_BROKER', ''))

@bp.get('/pdfs')
def list_pdfs():
    pdf_dir = current_app.config['PDF_DIR']
    files = sorted((f for f in os.listdir(pdf_dir) if f.endswith('.pdf')), reverse=True)
    return jsonify(files=files)

@bp.get('/pdfs/<name>')
def download_pdf(name):
    pdf_dir = current_app.config['PDF_DIR']
    # Serveer de PDF om te bekijken in plaats van te downloaden
    return send_from_directory(pdf_dir, name, as_attachment=False)
