# Documentación Técnica - BlueSky Energy

Este documento detalla la arquitectura, el modelo de datos y la configuración del sistema de cotizaciones.

## 🏛️ Arquitectura del Sistema

La aplicación sigue un patrón de arquitectura **Cliente-Servidor**:

- **Servidor (Backend):** Flask maneja la lógica de negocio, autenticación de base de datos y generación de documentos pesados (PDF/Excel).
- **Cliente (Frontend):** Interfaz SPA (Single Page Application) basada en JavaScript que consume una API REST propia.
- **Persistencia:** Firebase Firestore proporciona una base de datos en tiempo real y escalable.

## 🗄️ Modelo de Datos (Firebase Firestore)

### 1. Colección: `clientes`
Almacena la información de contacto de los clientes.
- `nombre`: string (ID visual)
- `empresa`: string
- `email`: string
- `telefono`: string
- `total_cotizaciones`: number (contador acumulativo)
- `created_at`: timestamp

### 2. Colección: `cotizaciones`
Almacena el detalle de cada oferta económica.
- `quote_number`: number (ID secuencial)
- `cliente`: string (Referencia al nombre del cliente)
- `fecha`: string (YYYY-MM-DD)
- `estado`: enum ['Pendiente', 'Aprobada', 'Rechazada', 'En Revisión']
- `items`: array de objetos [{descripcion, cantidad, precio}]
- `total`: string (Formato moneda)
- `timestamp`: serverTimestamp

### 3. Colección: `counters`
Controla la secuencia numérica de las cotizaciones.
- Documento: `cotizaciones_counter` -> `{ current_number: X }`

## 🔌 API Endpoints

### Clientes
- `GET /api/clientes`: Lista todos los clientes.
- `POST /api/clientes`: Crea un nuevo cliente.

### Cotizaciones
- `GET /api/cotizaciones`: Obtiene todas las cotizaciones (orden descendente).
- `GET /api/cotizaciones/<id>`: Obtiene el detalle de una cotización específica.
- `POST /guardar-cotizacion`: Crea una nueva cotización y aumenta el contador.
- `PUT /api/cotizaciones/<id>`: Actualiza estado o datos.
- `DELETE /api/cotizaciones/<id>`: Elimina el registro.
- `POST /api/cotizaciones/<id>/duplicar`: Clona una cotización existente.

### Otros
- `GET /api/estadisticas`: Procesa datos para las gráficas del Dashboard.
- `GET /descargar-pdf/<id>`: Genera y retorna un archivo PDF.
- `GET /descargar-excel/<id>`: Genera y retorna un archivo Excel.

## 🐳 Docker y Producción

El archivo `Dockerfile` utiliza una imagen base de `python:3.11-slim` e instala las siguientes librerías de sistema esenciales para `WeasyPrint`:
- `libpango`, `libcairo`, `libgdk-pixbuf`: Necesarias para renderizar fuentes y gráficos en el PDF.
- `shared-mime-info`: Para la detección de tipos de archivos.

## 🛡️ Seguridad

1. **Variables de Entorno:** El puerto y los logs se configuran vía `PORT` y `PYTHON_UNBUFFERED`.
2. **Secret Files:** Las credenciales de Firebase se manejan como archivos secretos en Render, nunca se suben a GitHub.
3. **Validación:** Se recomienda en futuras versiones añadir un sistema de Login (Firebase Auth).

---
*Ultima actualización: Febrero 2026*
