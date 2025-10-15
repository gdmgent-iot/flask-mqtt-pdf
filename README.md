# Flask MQTT PDF Demo

Een demonstratie applicatie die MQTT berichten ontvangt en automatisch PDF documenten genereert.

## 📋 Overzicht

Deze Flask applicatie biedt:
- **Web interface** voor het versturen van MQTT berichten
- **Automatische PDF generatie** bij ontvangst van MQTT berichten  
- **PDF lijst en weergave** via web interface
- **Real-time MQTT communicatie** via WebSocket

## 🚀 Quick Start

### 1. Omgeving voorbereiden

```bash
# Virtual environment aanmaken
python -m venv venv

# Virtual environment activeren
source venv/bin/activate  # macOS/Linux
# of
venv\Scripts\activate     # Windows

# Dependencies installeren
pip install -r requirements.txt
```

### 2. Configuratie

Kopieer `.env.example` naar `.env` en pas de instellingen aan:

```bash
cp .env.example .env
```

Belangrijke environment variables:
```env
# Flask configuratie
HOST=0.0.0.0
PORT=5555
DEBUG=True
SECRET_KEY=change-me

# MQTT configuratie  
MQTT_BROKER=localhost
MQTT_TCP_PORT=1883
MQTT_PORT=9001
MQTT_TOPIC=demo/messages

# PDF configuratie
PDF_DIR=generated
```

### 3. MQTT Broker

Voor lokale development heb je een MQTT broker nodig met WebSocket support:

```bash
# Met Docker
docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto

# Of installeer Mosquitto lokaal en configureer WebSocket support
```

### 4. Applicatie starten

```bash
python wsgi.py
```

De applicatie is nu beschikbaar op: http://localhost:5555

## 📁 Project Structuur

```
flask_demo_mqtt_pdf/
├── app/                    # Flask applicatie package
│   ├── __init__.py        # Application factory
│   ├── routes/            # HTTP route handlers
│   │   ├── __init__.py
│   │   └── main.py        # Hoofdroutes (/, /pdfs, /pdfs/<name>)
│   └── services/          # Business logic services
│       ├── __init__.py
│       ├── mqtt_client.py # MQTT client en message handling
│       └── pdf.py         # PDF generatie service
├── templates/             # Jinja2 HTML templates
│   └── index.html        # Hoofdpagina met MQTT interface
├── static/               # Statische bestanden (CSS, JS, images)
│   └── app.css          # Applicatie styling
├── generated/           # Gegenereerde PDF bestanden
├── requirements.txt     # Python dependencies
├── wsgi.py             # WSGI entry point
├── .env               # Environment configuratie
└── README.md         # Deze documentatie
```

## 🔧 API Endpoints

### Web Interface
- `GET /` - Hoofdpagina met MQTT interface

### API Endpoints  
- `GET /pdfs` - JSON lijst van alle PDF bestanden
- `GET /pdfs/<name>` - Specifiek PDF bestand serveren

## 🔄 Workflow

1. **Gebruiker verzendt bericht** via web interface
2. **MQTT client publiceert** bericht naar broker
3. **MQTT subscriber ontvangt** bericht  
4. **PDF wordt gegenereerd** met bericht inhoud
5. **PDF wordt opgeslagen** in configured directory
6. **Gebruiker kan PDF bekijken** via web interface

## 🛠️ Development

### Code Organisatie

- **Application Factory Pattern**: Flask app wordt gecreëerd via `create_app()` functie
- **Blueprint Structuur**: Routes zijn georganiseerd in blueprints
- **Service Layer**: Business logic is gescheiden in service modules
- **Environment Configuration**: Alle configuratie via environment variables

### Logging

De applicatie logt belangrijke events naar console:
- MQTT verbindingsstatus
- PDF generatie resultaten  
- Error handling

### Testing

Voor development testing:
1. Start de applicatie (`python wsgi.py`)
2. Open web interface in browser
3. Verstuur testberichten via MQTT interface
4. Controleer gegenereerde PDF's

## 📦 Dependencies

Zie `requirements.txt` voor volledige lijst:
- **Flask**: Web framework
- **python-dotenv**: Environment variable management
- **paho-mqtt**: MQTT client library
- **reportlab**: PDF generatie

## 🚀 Production Deployment

Voor production gebruik een WSGI server:

```bash
# Met gunicorn
pip install gunicorn
gunicorn wsgi:app

# Met configuratie
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:app
```

## 🔒 Beveiliging

- Verander `SECRET_KEY` in production
- Configureer MQTT broker authenticatie
- Valideer en sanitize user input
- Gebruik HTTPS in production
- Monitor disk space voor PDF directory

## 📝 Licentie

Demo project - vrij te gebruiken voor educatieve doeleinden.

## 👥 Auteurs

Demo Project - 15 oktober 2025