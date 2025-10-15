"""
Flask Application Factory

Deze module bevat de application factory pattern voor de Flask MQTT PDF demo applicatie.
De applicatie ontvangt MQTT berichten en genereert automatisch PDF documenten.
"""
from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    
    # Configureer Flask applicatie met custom template en static directories
    # Template folder: ../templates (relatief ten opzichte van app/ directory)
    # Static folder: ../static (relatief ten opzichte van app/ directory)
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')

    # === APPLICATIE CONFIGURATIE ===
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-key')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # PDF directory configuratie - zorg voor absoluut pad
    pdf_dir = os.getenv('PDF_DIR', 'generated')
    if not os.path.isabs(pdf_dir):
        # Converteer relatief pad naar absoluut pad relatief ten opzichte van project root
        # __file__ is app/__init__.py, dus twee niveaus omhoog naar project root
        app.config['PDF_DIR'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), pdf_dir)
    else:
        app.config['PDF_DIR'] = pdf_dir

    # === BLUEPRINT REGISTRATIE ===
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Zorg ervoor dat de PDF directory bestaat
    os.makedirs(app.config['PDF_DIR'], exist_ok=True)

    # === MQTT CLIENT INITIALISATIE ===
    # Initialiseer MQTT alleen in productie of in het hoofdprocess van de development server
    # Dit voorkomt dubbele initialisatie bij Flask's auto-reload functionaliteit
    from app.services.mqtt_client import init_mqtt
    if not app.config.get('DEBUG') or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print(os.environ.get('WERKZEUG_RUN_MAIN'))
        init_mqtt(app)

    return app
