# 📜 DOCUMENTACIÓN COMPLETA: BLUESKY ENERGY V2 PREMIUM
### "Manual Maestro del Sistema de Gestión Energética"

---

## 📑 CONTENIDO ACTUALIZADO (FEBRERO 2026)
1. **Nivel Niños/Principiantes:** El Mapa 3D y las Habitaciones.
2. **Nivel Intermedio:** El Cerebro (Flask) y las Animaciones (GSAP).
3. **Nivel Datos:** La Nube de Notas (Firebase).
4. **Nivel Constructor:** Cómo escalar el sistema.
5. **Nivel Experto:** Render, Docker y Manejo de Versiones.

---

## 🏛️ 1. EL NUEVO MAPA DEL PROYECTO (UI V2)
El sistema ha evolucionado de una web estática a un **entorno 3D interactivo**.

- **Fondo 3D (`Three.js`):** Ubicado en `three-canvas`. Es una red de energía que simboliza la conectividad de BlueSky.
- **Diseño Glassmorphism:** Las tarjetas ya no son opacas; ahora son de cristal transparente con desenfoque (`backdrop-filter`).
- **Navegación Sidebar:** Se ha movido el menú a la izquierda para una experiencia tipo Software as a Service (SaaS) profesional.

---

## 🧠 2. EL CEREBRO Y LAS ANIMACIONES (Backend y Visuales)
El cerebro sigue siendo **Flask**, pero ahora tiene compañeros de lujo:

- **GSAP:** Encargado de que los números no aparezcan de golpe, sino que "cuenten" del 0 al total.
- **Branding PNG:** Se migró todo el sistema de `logo.jpg` a `logo 1.2.png` para soportar transparencias en el diseño oscuro.

---

## 📓 3. EL DIARIO DE DATOS (Firebase Firestore)
Los datos están blindados en la nube.
- **Colección Clientes:** Información de contacto y volumen de compra.
- **Colección Cotizaciones:** El historial completo de ventas.
- **Seguridad:** Las llaves están en `/etc/secrets/firebase_credentials.json` en el servidor de Render.

---

## 🦸 4. CÓMO AGREGAR SUPERPODERES (Guía de Desarrollo)
Para agregar un campo nuevo en la V2:
1. **HTML:** Usa las clases `.form-control` y `.form-select`.
2. **CSS:** Asegúrate de que el fondo sea `rgba(255,255,255,0.05)` para mantener el estilo oscuro.
3. **JS:** Usa `gsap.from()` para que el nuevo elemento entre con estilo.

---

## 🐳 5. INFRAESTRUCTURA Y VERSIONES
- **Manejo de Ramas:** 
  - `main`: Versión estable (V1).
  - `v2-premium-visuals`: El futuro del sistema (Lo que estás viendo ahora).
- **Docker:** El archivo `Dockerfile` instala las librerías `libpango` y `libcairo` para que los PDFs salgan perfectos en Linux.

---

## 🛠️ 6. ROADMAP DE MANTENIMIENTO
*   **Finalizado:** Dashboard 3D, Nueva Cotización Premium, Cambio de Logo PNG.
*   **Pendiente:** Unificar diseño en página de Clientes, agregar login de seguridad, envío automático de correos.

---
**Desarrollado por StartDev Systems en colaboración con la IA de Gemini CLI.**
