# 📜 DOCUMENTACIÓN COMPLETA: BLUESKY ENERGY V2.2 PREMIUM MOBILE
### "Manual Maestro de Ingeniería y Diseño"

---

## 📑 CONTENIDO ACTUALIZADO (V2.2)
1. **Nivel Niños/Principiantes:** El Mapa del Tesoro 3D y el Menú de Celular.
2. **Nivel Intermedio:** El Cerebro (Flask) y los "Cables" Mobile-Nav.
3. **Nivel Datos:** La Nube Blindada (Firebase).
4. **Nivel Constructor:** Cómo escalar el sistema y mantener la estética.
5. **Nivel Experto:** Arquitectura de Producción (Docker + Render).

---

## 🏛️ 1. EL ECOSISTEMA UNIFICADO (UI V2.2)
El sistema ha alcanzado su madurez visual con un diseño **imponente y responsivo**.

- **Navegación Híbrida:** 
  - **PC:** Sidebar lateral con efecto de cristal y expansión al pasar el mouse.
  - **Móvil:** Barra de navegación inferior (Bottom Nav) inspirada en aplicaciones nativas premium.
- **Escala Gigante:** Letra base de **18px/20px** para evitar la fatiga visual y proyectar robustez.
- **Fondo Energético:** Cada página renderiza un canvas de `Three.js` con una red eléctrica interactiva.

---

## 🧠 2. EL CEREBRO Y LOS FILTROS (Backend)
- **Rutas Pro:** Se corrigieron las rutas de `app.py` para asegurar que el logo PNG 1.2 se incluya en el PDF.
- **JavaScript Blindado:** El archivo `main.js` ahora inyecta estilos oscuros (`#121520`) directamente en los inputs de la tabla, eliminando errores de contraste en cualquier navegador.

---

## 📓 3. EL DIARIO DE DATOS (Firebase Firestore)
Los datos están centralizados:
- **`clientes`**: Lista maestra con contadores automáticos de cotizaciones.
- **`cotizaciones`**: Almacenamiento seguro de documentos con estados dinámicos.
- **`counters`**: Control de numeración único por documento.

---

## 🦸 4. CÓMO AGREGAR SUPERPODERES (Mantenimiento)
Para mantener la armonía del sistema:
1. **Inputs:** Deben llevar siempre `background-color: rgba(255,255,255,0.05)` y letra blanca.
2. **Responsividad:** Si agregas una sección, usa `@media (max-width: 768px)` para ocultar el Sidebar y mostrar la navegación móvil.
3. **Fuentes:** Títulos en `Bebas Neue`, resto en `Outfit`.

---

## 🐳 5. DE LA PC AL MUNDO (Docker)
El despliegue en Render usa una imagen `python:3.11-slim` que incluye:
- Librerías de sistema para WeasyPrint (Cairo, Pango).
- Configuración de puerto dinámico (`$PORT`).
- Secret Files para la llave de Firebase.

---

## 🛠️ 6. ESTADO DEL PROYECTO
*   **Finalizado:** Ecosistema 3D, Unificación total de páginas, Adaptabilidad Móvil Pro, Escala de Fuente Pro.
*   **Siguiente Etapa:** Sistema de Login (Auth), Envío de Emails y Firma Digital.

---
**Desarrollado por StartDev Systems & Gemini CLI.**
