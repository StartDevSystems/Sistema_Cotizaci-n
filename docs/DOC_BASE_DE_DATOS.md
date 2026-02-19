# Documentación de Base de Datos (Firestore)

## Modelo NoSQL
El sistema utiliza una estructura orientada a documentos.

### 1. Colección: `clientes`
- `nombre` (string): Nombre completo (Key única de búsqueda).
- `empresa` (string): Nombre de la empresa.
- `email` (string): Correo electrónico.
- `telefono` (string): Número de contacto.
- `total_cotizaciones` (int): Contador acumulativo de documentos generados para este cliente.

### 2. Colección: `cotizaciones`
- `quote_number` (int): Número secuencial único (ej: 005).
- `cliente` (string): Referencia al nombre del cliente.
- `fecha` (string): Fecha en formato YYYY-MM-DD.
- `estado` (string): Pendiente, Aprobada, Rechazada, En Revisión.
- `total` (string): Monto total formateado (ej: $1,200.00).
- `items` (array): Lista de objetos con `descripcion`, `cantidad` y `precio`.
- `timestamp` (timestamp): Hora exacta de creación en el servidor.

### 3. Colección: `counters`
- Documento: `cotizaciones_counter`
- Campo: `current_number` (int): Último número utilizado para garantizar la secuencia.
