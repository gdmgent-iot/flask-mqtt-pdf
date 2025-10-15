"""
PDF Generation Service

Deze module verzorgt het genereren van PDF documenten uit MQTT bericht content.
Gebruikt ReportLab voor PDF creatie met een eenvoudige layout.

Features:
- Automatische directory creatie
- Timestamped bestandsnamen
- A4 pagina formaat met professionele layout
- UTF-8 text handling
- Multi-line content support
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def generate_pdf(pdf_dir: str, payload: str) -> str:
    ensure_dir(pdf_dir)
    
    # Genereer timestamp met microseconden voor unieke bestandsnamen
    ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    filename = f"message-{ts}.pdf"
    fullpath = os.path.join(pdf_dir, filename)

    # Initialiseer PDF canvas met A4 formaat
    c = canvas.Canvas(fullpath, pagesize=A4)
    w, h = A4

    # === PDF CONTENT LAYOUT ===
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, h - 72, "MQTT Message Receipt")  # 72pt = 1 inch margin

    c.setFont("Helvetica", 10)
    c.drawString(72, h - 100, f"Timestamp: {ts}")
    c.drawString(72, h - 115, "Topic payload:")

    text = c.beginText(72, h - 135)
    text.setFont("Helvetica", 12)
    
    # Verwerk elke regel van de payload, behandel lege payload
    content_lines = str(payload).splitlines() if payload else ["<empty>"]
    for line in content_lines:
        text.textLine(line)  # textLine() voegt automatisch regeleindes toe
    
    c.drawText(text)

    # Finaliseer PDF
    c.showPage()  # Voltooi huidige pagina
    c.save()      # Sla PDF op naar bestand
    
    return fullpath
