# Guía del Desarrollador y Mantenimiento

## 🚀 Correr en Desarrollo (Local)
1. Activar entorno virtual: `.\venv\Scripts\activate`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Tener GTK+ instalado en Windows.
4. Ejecutar: `python app.py`

## 🌍 Despliegue en Producción (Render)
1. El despliegue es automático mediante el `Dockerfile`.
2. Las credenciales de Firebase deben estar en la sección "Secret Files" de Render con el nombre `firebase_credentials.json`.
3. El puerto se configura automáticamente mediante la variable de entorno `PORT`.

## ➕ Cómo agregar una nueva funcionalidad
### Ejemplo: Agregar un campo "Vendedor"
1. **Frontend:** Añadir el input en `index.html` y capturarlo en `main.js`.
2. **Backend:** Recibir el campo en `app.py` dentro de la función `guardar_cotizacion`.
3. **PDF:** Agregar el campo en la plantilla `cotizacion_pdf.html`.

## 🛠️ Mantenimiento y Escalabilidad
- **Escalabilidad:** El sistema puede crecer agregando más colecciones en Firebase sin afectar el código existente.
- **Mantenimiento:** Se recomienda revisar los logs de Render semanalmente para detectar posibles errores de conexión con Firebase o con la generación de PDFs.
