from flask import Flask, render_template, request, jsonify, make_response, Response
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from weasyprint import HTML
import os
from pathlib import Path
import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter

# --- INICIALIZACIÓN DE FIREBASE ---
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
# -----------------------------------

app = Flask(__name__)

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

@app.route('/api/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.get_json()
        producto_data = {
            'nombre': data.get('nombre', ''),
            'descripcion': data.get('descripcion', ''),
            'precio': float(data.get('precio', 0))
        }
        
        _, doc_ref = db.collection('productos').add(producto_data)
        return jsonify({'status': 'ok', 'message': 'Producto creado', 'producto_id': doc_ref.id})
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

@app.route('/api/cotizaciones/<cotizacion_id>', methods=['GET'])
def obtener_cotizacion(cotizacion_id):
    try:
        doc_ref = db.collection('cotizaciones').document(cotizacion_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'status': 'error', 'message': 'Cotización no encontrada'}), 404
        
        data = doc.to_dict()
        data['id'] = doc.id
        return jsonify({'status': 'ok', 'cotizacion': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/guardar-cotizacion', methods=['POST'])
def guardar_cotizacion():
    try:
        data = request.get_json()
        counter_ref = db.collection('counters').document('cotizaciones_counter')
        
        @firestore.transactional
        def update_in_transaction(transaction, ref):
            snapshot = ref.get(transaction=transaction)
            current_number = snapshot.get('current_number')
            new_number = current_number + 1
            transaction.update(ref, {'current_number': new_number})
            return new_number

        transaction = db.transaction()
        new_quote_number = update_in_transaction(transaction, counter_ref)
        
        data['quote_number'] = new_quote_number
        data['timestamp'] = datetime.datetime.now(datetime.timezone.utc)
        data['estado'] = data.get('estado', 'Pendiente')
        data['notas'] = data.get('notas', '')
        
        cotizaciones_ref = db.collection('cotizaciones')
        timestamp, doc_ref = cotizaciones_ref.add(data)

        # Actualizar contador de cotizaciones del cliente
        cliente_nombre = data.get('cliente', '')
        if cliente_nombre:
            clientes_ref = db.collection('clientes').where('nombre', '==', cliente_nombre).limit(1)
            clientes = list(clientes_ref.stream())
            if clientes:
                cliente_doc = clientes[0]
                cliente_ref = db.collection('clientes').document(cliente_doc.id)
                cliente_data = cliente_doc.to_dict()
                cliente_ref.update({
                    'total_cotizaciones': cliente_data.get('total_cotizaciones', 0) + 1
                })

        return jsonify({
            'status': 'ok', 
            'message': f'Cotización Nº {new_quote_number:03d} guardada',
            'cotizacion_id': doc_ref.id
        })
    except Exception as e:
        print(f"Error al guardar en Firebase: {e}")
        return jsonify({'status': 'error', 'message': 'Ocurrió un error al guardar'}), 500

@app.route('/api/cotizaciones/<cotizacion_id>', methods=['PUT'])
def actualizar_cotizacion(cotizacion_id):
    try:
        data = request.get_json()
        doc_ref = db.collection('cotizaciones').document(cotizacion_id)
        
        update_data = {}
        if 'estado' in data:
            update_data['estado'] = data['estado']
        if 'notas' in data:
            update_data['notas'] = data['notas']
        if 'items' in data:
            update_data['items'] = data['items']
        if 'total' in data:
            update_data['total'] = data['total']
        if 'cliente' in data:
            update_data['cliente'] = data['cliente']
        
        update_data['updated_at'] = datetime.datetime.now(datetime.timezone.utc)
        
        doc_ref.update(update_data)
        return jsonify({'status': 'ok', 'message': 'Cotización actualizada'})
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/cotizaciones/<cotizacion_id>', methods=['DELETE'])
def eliminar_cotizacion(cotizacion_id):
    try:
        db.collection('cotizaciones').document(cotizacion_id).delete()
        return jsonify({'status': 'ok', 'message': 'Cotización eliminada'})
    except Exception as e:
        print(f"Error al eliminar: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/cotizaciones/<cotizacion_id>/duplicar', methods=['POST'])
def duplicar_cotizacion(cotizacion_id):
    try:
        doc_ref = db.collection('cotizaciones').document(cotizacion_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'status': 'error', 'message': 'Cotización no encontrada'}), 404
        
        data = doc.to_dict()
        
        # Obtener nuevo número
        counter_ref = db.collection('counters').document('cotizaciones_counter')
        @firestore.transactional
        def update_in_transaction(transaction, ref):
            snapshot = ref.get(transaction=transaction)
            current_number = snapshot.get('current_number')
            new_number = current_number + 1
            transaction.update(ref, {'current_number': new_number})
            return new_number

        transaction = db.transaction()
        new_quote_number = update_in_transaction(transaction, counter_ref)
        
        # Crear nueva cotización
        nueva_data = {
            'quote_number': new_quote_number,
            'cliente': data.get('cliente', ''),
            'fecha': datetime.datetime.now().strftime('%Y-%m-%d'),
            'items': data.get('items', []),
            'total': data.get('total', '$0.00'),
            'estado': 'Pendiente',
            'notas': f"Duplicada de cotización #{data.get('quote_number', 0):03d}",
            'timestamp': datetime.datetime.now(datetime.timezone.utc)
        }
        
        _, new_doc_ref = db.collection('cotizaciones').add(nueva_data)
        
        return jsonify({
            'status': 'ok',
            'message': f'Cotización duplicada. Nueva cotización #{new_quote_number:03d}',
            'cotizacion_id': new_doc_ref.id
        })
    except Exception as e:
        print(f"Error al duplicar: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# === RUTA DE ESTADÍSTICAS PARA DASHBOARD ===
@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    try:
        cotizaciones_ref = db.collection('cotizaciones')
        docs = list(cotizaciones_ref.stream())
        
        total = len(docs)
        monto_total = 0
        por_estado = {'Pendiente': 0, 'Aprobada': 0, 'Rechazada': 0, 'En Revisión': 0}
        por_mes = {}
        
        for doc in docs:
            data = doc.to_dict()
            
            # Monto total
            total_str = data.get('total', '$0.00')
            monto = float(total_str.replace('$', '').replace(',', ''))
            monto_total += monto
            
            # Por estado
            estado = data.get('estado', 'Pendiente')
            por_estado[estado] = por_estado.get(estado, 0) + 1
            
            # Por mes
            fecha = data.get('fecha', '')
            if fecha:
                mes = fecha[:7]  # YYYY-MM
                por_mes[mes] = por_mes.get(mes, 0) + 1
        
        return jsonify({
            'status': 'ok',
            'total_cotizaciones': total,
            'monto_total': monto_total,
            'promedio': monto_total / total if total > 0 else 0,
            'por_estado': por_estado,
            'por_mes': dict(sorted(por_mes.items())[-6:])  # Últimos 6 meses
        })
    except Exception as e:
        print(f"Error en estadísticas: {e}")
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
        print(f"Error al generar el PDF: {e}")
        return "Ocurrió un error al generar el PDF", 500

@app.route('/descargar-excel/<cotizacion_id>')
def descargar_excel(cotizacion_id):
    try:
        doc_ref = db.collection('cotizaciones').document(cotizacion_id)
        doc = doc_ref.get()
        if not doc.exists: return "Cotización no encontrada", 404
        cotizacion_data = doc.to_dict()

        wb = Workbook()
        ws = wb.active
        ws.title = "Cotización"

        header_font = Font(bold=True, color="FFFFFF", size=12)
        header_fill = PatternFill(start_color="0D2A42", end_color="0D2A42", fill_type="solid")
        title_font = Font(bold=True, size=16)
        bold_font = Font(bold=True)
        currency_format = '$#,##0.00'
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'img', 'logo.jpg')
        img = Image(logo_path)
        img.height = 80
        img.width = 210
        ws.add_image(img, 'A1')

        ws.merge_cells('A5:D5')
        ws['A5'] = f"COTIZACIÓN Nº {cotizacion_data.get('quote_number', ''):03d}"
        ws['A5'].font = title_font
        ws['A5'].alignment = Alignment(horizontal='center')

        ws['A7'] = 'Cliente:'
        ws['A7'].font = bold_font
        ws['B7'] = cotizacion_data.get('cliente', '')
        ws['A8'] = 'Fecha:'
        ws['A8'].font = bold_font
        ws['B8'] = cotizacion_data.get('fecha', '')

        headers = ['Descripción', 'Cantidad', 'Precio Unitario', 'Total']
        ws.append([])
        header_row = 10
        for col_num, header_title in enumerate(headers, 1):
            cell = ws.cell(row=header_row, column=col_num, value=header_title)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = thin_border

        current_row = header_row + 1
        for item in cotizacion_data.get('items', []):
            total_item = item.get('cantidad', 0) * item.get('precio', 0)
            ws.cell(row=current_row, column=1, value=item.get('descripcion', '')).border = thin_border
            ws.cell(row=current_row, column=2, value=item.get('cantidad', 0)).border = thin_border
            cell_price = ws.cell(row=current_row, column=3, value=item.get('precio', 0))
            cell_price.number_format = currency_format
            cell_price.border = thin_border
            cell_total = ws.cell(row=current_row, column=4, value=total_item)
            cell_total.number_format = currency_format
            cell_total.border = thin_border
            current_row += 1
        
        ws.cell(row=current_row, column=3, value='Total General:').font = bold_font
        ws.cell(row=current_row, column=3, value='Total General:').alignment = Alignment(horizontal='right')
        
        total_str = cotizacion_data.get('total', '$0.00')
        total_numerico = float(total_str.replace('$', '').replace(',', ''))
        
        total_cell = ws.cell(row=current_row, column=4, value=total_numerico)
        total_cell.font = bold_font
        total_cell.number_format = currency_format
        total_cell.border = thin_border

        ws.column_dimensions['A'].width = 60
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['D'].width = 20

        virtual_workbook = io.BytesIO()
        wb.save(virtual_workbook)
        virtual_workbook.seek(0)

        return Response(
            virtual_workbook,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment;filename=cotizacion_{cotizacion_data.get("quote_number", "num"):03d}.xlsx'}
        )
    except Exception as e:
        print(f"Error al generar el Excel: {e}")
        return "Ocurrió un error al generar el Excel", 500


if __name__ == '__main__':
    app.run(debug=True)