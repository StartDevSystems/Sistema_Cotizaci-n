# 🔌 04. CONECTANDO LOS CABLES

¿Cómo sabe la web que tiene que mostrar los clientes? Gracias a los "Cables Invisibles" llamados **Fetch API**.

## 🔄 El ciclo de la información

1. **La Pregunta (Frontend):** En el archivo `main.js`, JavaScript dice: `"Oye servidor, dame la lista de clientes"`.
   ```javascript
   fetch('/api/clientes')
   ```
2. **La Respuesta (Backend):** El cerebro en `app.py` busca en Firebase y le manda una caja llena de datos (JSON).
3. **El Resultado (Frontend):** JavaScript recibe esa caja, la abre y dibuja las filas en la tabla para que tú las veas.

### ¿Cómo se guardan las cosas?
Cuando das clic en "Guardar Cotización", JavaScript recoge todo lo que escribiste en el formulario, lo mete en una caja y se lo manda al servidor usando un método llamado `POST`.
