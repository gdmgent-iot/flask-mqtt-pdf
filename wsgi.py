"""
WSGI Application Entry Point

Dit is het hoofdbestand voor het starten van de Flask MQTT PDF demo applicatie.
Kan worden gebruikt voor zowel development als production deployment.

Voor development:
    python wsgi.py

Voor production (met gunicorn):
    gunicorn wsgi:app

Environment Variables:
    HOST: Server bind address (standaard: 127.0.0.1)
    PORT: Server poort (standaard: 5000)
    
Auteur: Demo Project
Datum: 15 oktober 2025
"""

from app import create_app
import os

# Creëer Flask applicatie instance via application factory
app = create_app()

if __name__ == '__main__':
    # Development server configuratie
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5000'))
    
    print(f"Starting development server on {host}:{port}")
    print("Press CTRL+C to quit")
    
    # Start Flask development server
    # Voor production gebruik een WSGI server zoals gunicorn
    app.run(host=host, port=port)
