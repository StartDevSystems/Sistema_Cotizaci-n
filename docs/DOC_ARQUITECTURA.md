# Documento de Arquitectura - BlueSky Energy

## 1. Visión General
El sistema BlueSky Energy está diseñado como una aplicación web monolítica ligera que utiliza servicios en la nube para escalabilidad y persistencia de datos.

## 2. Tecnologías Core
- **Backend:** Flask (Python 3.11) - Maneja el enrutamiento y la lógica de negocio.
- **Base de Datos:** Firebase Firestore - Base de datos NoSQL de documentos.
- **Generación de PDF:** WeasyPrint - Renderiza HTML/CSS a PDF.
- **Infraestructura:** Docker - Empaqueta la aplicación con sus dependencias de sistema.

## 3. Capas del Sistema
- **Capa de Presentación:** Plantillas Jinja2 y Bootstrap 5.
- **Capa de Servicio (API):** Controladores en Flask que retornan JSON.
- **Capa de Datos:** Integración directa con el SDK de Firebase Admin.

## 4. Flujo de Datos
1. El usuario interactúa con la UI (JavaScript).
2. JS realiza peticiones `fetch()` a los endpoints de Flask.
3. Flask procesa la solicitud, consulta/guarda en Firebase.
4. Flask retorna la respuesta al frontend o genera un archivo binario (PDF/Excel).
