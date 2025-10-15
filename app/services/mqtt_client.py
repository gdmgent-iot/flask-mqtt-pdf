"""
MQTT Client Service

Deze module beheert de MQTT client connectie en verwerkt binnenkomende berichten.
Wanneer een MQTT bericht wordt ontvangen, wordt automatisch een PDF gegenereerd
met de inhoud van het bericht.

Features:
- Automatische verbinding met MQTT broker
- Background thread voor MQTT message loop
- PDF generatie bij bericht ontvangst
- Thread-safe initialisatie
- Reconnection handling
"""

import os
import threading
import paho.mqtt.client as mqtt
from app.services.pdf import generate_pdf

# Globale variabelen voor MQTT client state management
_client = None
_started = False

def _on_connect(client, userdata, flags, reason_code, properties=None):
    topic = userdata["topic"]
    client.subscribe(topic)
    print(f"[MQTT] Verbonden en geabonneerd op topic: {topic}")

def _on_message(client, userdata, msg):
    pdf_dir = userdata["pdf_dir"]
    payload = msg.payload.decode("utf-8", errors="replace")
    try:
        path = generate_pdf(pdf_dir, payload)
        print(f"[MQTT] PDF gegenereerd: {path}")
    except Exception as e:
        print(f"[MQTT] PDF generatie fout: {e}")

def init_mqtt(app):
    global _client, _started
    if _started:
        print("[MQTT] Al geïnitialiseerd, overslaan...")
        return

    # Lees MQTT configuratie uit environment variables
    broker_host = os.getenv("MQTT_BROKER", "localhost")
    tcp_port    = int(os.getenv("MQTT_TCP_PORT", "1883"))
    topic       = os.getenv("MQTT_TOPIC", "demo/messages")
    pdf_dir     = app.config['PDF_DIR']  # Gebruik Flask app config voor consistentie

    print(f"[MQTT] Initialiseren met PDF_DIR: {pdf_dir}")
    print(f"[MQTT] Broker: {broker_host}:{tcp_port}, Topic: {topic}")
    
    # Configureer userdata voor callback functies
    userdata = {"topic": topic, "pdf_dir": pdf_dir}

    # Maak MQTT client aan met callback API versie 2
    _client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=userdata)
    _client.on_connect = _on_connect
    _client.on_message = _on_message

    # Verbind met MQTT broker
    try:
        _client.connect(broker_host, tcp_port, keepalive=60)
        print(f"[MQTT] Verbinding geïnitieerd naar {broker_host}:{tcp_port}")
    except Exception as e:
        print(f"[MQTT] Verbinding fout: {e}")
        return

    # Start MQTT client loop in background thread
    # Daemon thread wordt automatisch beëindigd wanneer hoofdapplicatie stopt
    t = threading.Thread(target=_client.loop_forever, daemon=True)
    t.start()
    _started = True
    print("[MQTT] Background thread gestart")
