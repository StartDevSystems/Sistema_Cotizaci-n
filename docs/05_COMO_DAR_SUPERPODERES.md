# 🦸 05. CÓMO DAR SUPERPODERES (Nuevas Funciones)

Si quieres agregar algo nuevo, sigue estos 3 pasos mágicos. Digamos que quieres agregar un campo llamado "Vendedor":

## Paso 1: El Formulario (HTML)
Ve a `templates/index.html` y agrega un cuadrito (input) para escribir el nombre del vendedor.
```html
<input type="text" id="vendedor">
```

## Paso 2: El Mensajero (JS)
Ve a `static/js/main.js`. Busca donde se guardan los datos y agrega:
`vendedor: document.getElementById('vendedor').value`

## Paso 3: El Almacén (Python)
En `app.py`, asegúrate de que cuando recibas la cotización, guardes ese campo en Firebase. 

¡Y listo! Ya tienes una nueva función. ¡No olvides agregarla también al `cotizacion_pdf.html` para que salga en el PDF!
