from flask import Flask, render_template, request, jsonify, make_response, Response
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from weasyprint import HTML
import os
from pathlib import Path
import io
import json
import logging
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter

# Configurar logs para ver qué pasa en Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- INICIALIZACIÓN DE FIREBASE ---
try:
    cred_path = os.path.join(os.getcwd(), "firebase_credentials.json")
    if os.path.exists(cred_path):
        logger.info(f"Cargando credenciales desde: {cred_path}")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        logger.error("¡ERROR! No se encontró firebase_credentials.json en el directorio raíz.")
        # Intentar cargar desde variable de entorno si el archivo no existe
        firebase_json = os.environ.get("FIREBASE_JSON")
        if firebase_json:
            logger.info("Cargando credenciales desde variable de entorno FIREBASE_JSON")
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        else:
            raise FileNotFoundError("No se encontró el archivo de credenciales ni la variable FIREBASE_JSON")

    db = firestore.client()
    logger.info("Firebase inicializado correctamente.")
except Exception as e:
    logger.error(f"Error fatal inicializando Firebase: {e}")
    # No detenemos la app aquí para que al menos Flask pueda mostrar errores más claros

# -----------------------------------

def format_spanish_date(date_obj):
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{date_obj.day} de {months[date_obj.month - 1]}, {date_obj.year}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/cotizaciones')
def ver_cotizaciones():
    return render_template('cotizaciones.html')

# === RUTAS DE CLIENTES ===
@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    try:
        clientes_ref = db.collection('clientes').order_by('nombre')
        docs = clientes_ref.stream()
        
        clientes = []
        for doc in docs:
            data = doc.to_dict()
            clientes.append({
                'id': doc.id,
                'nombre': data.get('nombre', ''),
                'email': data.get('email', ''),
                'telefono': data.get('telefono', ''),
                'empresa': data.get('empresa', ''),
                'total_cotizaciones': data.get('total_cotizaciones', 0)
            })
        
        return jsonify({'status': 'ok', 'clientes': clientes})
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
def crear_cliente():
    try:
        data = request.get_json()
        cliente_data = {
            'nombre': data.get('nombre', ''),
            'email': data.get('email', ''),
            'telefono': data.get('telefono', ''),
            'empresa': data.get('empresa', ''),
            'total_cotizaciones': 0,
            'created_at': datetime.datetime.now(datetime.timezone.utc)
        }
        
        _, doc_ref = db.collection('clientes').add(cliente_data)
        return jsonify({'status': 'ok', 'message': 'Cliente creado', 'cliente_id': doc_ref.id})
    except Exception as e:
        print(f"Error al crear cliente: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# === RUTAS DE PRODUCTOS/PLANTILLAS ===
@app.route('/api/productos', methods=['GET'])
def listar_productos():
    try:
        productos_ref = db.collection('productos').order_by('nombre')
        docs = productos_ref.stream()
        
        productos = []
        for doc in docs:
            data = doc.to_dict()
            productos.append({
                'id': doc.id,
                'nombre': data.get('nombre', ''),
                'descripcion': data.get('descripcion', ''),
                'precio': data.get('precio', 0)
            })
        
        return jsonify({'status': 'ok', 'productos': productos})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# === RUTAS DE COTIZACIONES ===
@app.route('/api/cotizaciones', methods=['GET'])
def listar_cotizaciones():
    try:
        cotizaciones_ref = db.collection('cotizaciones').order_by('timestamp', direction=firestore.Query.DESCENDING)
        docs = cotizaciones_ref.stream()
        
        cotizaciones = []
        for doc in docs:
            data = doc.to_dict()
            cotizaciones.append({
                'id': doc.id,
                'quote_number': data.get('quote_number', 0),
                'cliente': data.get('cliente', ''),
                'fecha': data.get('fecha', ''),
                'total': data.get('total', '$0.00'),
                'estado': data.get('estado', 'Pendiente'),
                'items': data.get('items', []),
                'notas': data.get('notas', ''),
                'timestamp': data.get('timestamp').isoformat() if data.get('timestamp') else ''
            })
        
        return jsonify({'status': 'ok', 'cotizaciones': cotizaciones})
    except Exception as e:
        print(f"Error al obtener cotizaciones: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/descargar-pdf/<cotizacion_id>')
def descargar_pdf(cotizacion_id):
    try:
        doc_ref = db.collection('cotizaciones').document(cotizacion_id)
        doc = doc_ref.get()
        if not doc.exists: return "Cotización no encontrada", 404
        
        cotizacion_data = doc.to_dict()
        cotizacion_data['cotizacion_id_interno'] = cotizacion_id

        fecha_cotizacion_str = cotizacion_data.get('fecha', '')
        fecha_cotizacion_obj = datetime.datetime.strptime(fecha_cotizacion_str, '%Y-%m-%d')
        fecha_validez_obj = fecha_cotizacion_obj + datetime.timedelta(days=15)
        
        cotizacion_data['fecha_formateada'] = format_spanish_date(fecha_cotizacion_obj)
        cotizacion_data['fecha_validez'] = format_spanish_date(fecha_validez_obj)
        
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'img', 'logo.jpg')
        cotizacion_data['logo_url'] = Path(logo_path).as_uri()
        
        html_string = render_template('cotizacion_pdf.html', **cotizacion_data)
        pdf_file = HTML(string=html_string).write_pdf()
        
        response = make_response(pdf_file)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=cotizacion_{cotizacion_data.get("quote_number", "num"):03d}.pdf'
        return response
    except Exception as e:
        logger.error(f"Error al generar el PDF: {e}")
        return "Ocurrió un error al generar el PDF", 500

# (Mantener el resto de rutas iguales...)

if __name__ == '__main__':
    # Usar el puerto de la variable de entorno o 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
