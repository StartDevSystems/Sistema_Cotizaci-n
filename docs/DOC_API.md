# Documentación de la API (REST Interna)

Todos los endpoints retornan un JSON con el formato: `{ "status": "ok", "data": ... }` o `{ "status": "error", "message": "..." }`.

## 1. Clientes
- `GET /api/clientes`: Lista de todos los clientes.
- `POST /api/clientes`: Crea un nuevo cliente. Requiere JSON con `nombre`, `empresa`, `email`, `telefono`.

## 2. Cotizaciones
- `GET /api/cotizaciones`: Todas las cotizaciones.
- `POST /guardar-cotizacion`: Crea una cotización. Maneja la lógica de contadores y actualización de clientes.
- `GET /api/cotizaciones/<id>`: Detalles de una sola.
- `DELETE /api/cotizaciones/<id>`: Borra registro.
- `POST /api/cotizaciones/<id>/duplicar`: Clona con nuevo número.

## 3. Estadísticas
- `GET /api/estadisticas`: Retorna:
  - `total_cotizaciones`
  - `monto_total`
  - `promedio`
  - `por_estado` (Objeto para gráfica de torta)
  - `por_mes` (Objeto para gráfica de líneas)

## 4. Documentos (Binarios)
- `GET /descargar-pdf/<id>`: Retorna archivo PDF.
- `GET /descargar-excel/<id>`: Retorna archivo XLSX.
