# 📓 03. EL DIARIO DE DATOS (Base de Datos)

Usamos **Firebase Firestore**. Imagina que es un cuaderno con muchas páginas. Cada página es un "Documento" y cada cuaderno es una "Colección".

## 📚 Nuestros Cuadernos (Colecciones)

1. **Cuaderno `clientes`**:
   - Aquí anotamos el nombre, correo y empresa de cada persona.
   - Cada vez que hacemos una cotización, le sumamos +1 a su contador.

2. **Cuaderno `cotizaciones`**:
   - Aquí anotamos los detalles: ¿Qué compró? ¿Cuánto costó? ¿Está aprobada?
   - Guardamos una lista llamada `items` con los productos.

3. **Cuaderno `counters`**:
   - Es un cuaderno especial que solo tiene un número. Lo usamos para saber cuál es el siguiente número de cotización (001, 002, 003...).

### ☁️ ¿Dónde están los datos?
Estan en la nube de Google. Para verlos, puedes entrar a la consola de Firebase. El servidor se conecta usando el archivo secreto `firebase_credentials.json`.
