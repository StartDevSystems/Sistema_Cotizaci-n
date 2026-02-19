# 🧠 02. EL CEREBRO DE LA APP (Backend)

El archivo `app.py` es el cerebro. Está escrito en **Python** y usa un sistema llamado **Flask**.

## ⚙️ ¿Qué hace el cerebro?

1. **Recibe peticiones:** Cuando alguien entra a la web, el cerebro dice: "¡Ah! quieres ver la página de clientes, aquí la tienes".
2. **Habla con Firebase:** El cerebro tiene las llaves (`firebase_credentials.json`) para abrir el cuaderno de notas (la base de datos) y leer o escribir en él.
3. **Hace Magia (PDF y Excel):**
   - Usa **WeasyPrint** para transformar una página HTML en un PDF profesional.
   - Usa **OpenPyxl** para crear tablas de Excel.

## 📍 Rutas Importantes
- `@app.route('/')`: La entrada principal (Nueva Cotización).
- `@app.route('/api/...')`: Rutas que solo envían datos (números y letras), no páginas completas.

**Regla de Oro:** Si vas a tocar el cerebro, asegúrate de no borrar las líneas de `import`, porque son las herramientas que Python necesita para trabajar.
