# Principios SOLID en Python

Curso de Principios SOLID y Patrones de Diseño en Python.

## Requisitos

- Python 3.12 o superior
- [uv](https://github.com/astral-sh/uv) (gestor de paquetes)

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Ronaldmolinares/Python-SOLID.git
   cd Python-SOLID
   ```

2. **Crear y activar el entorno virtual**
   ```bash
   uv venv
   ```
   - **Windows PowerShell:**
     ```powershell
     .venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source .venv/bin/activate
     ```

3. **Instalar dependencias**
   ```bash
   uv sync
   ```

4. **Configurar variables de entorno**
   
   Si vas a usar el procesador de pagos, crea un archivo `.env`:
   ```bash
   STRIPE_API_KEY=tu_clave_de_stripe
   ```

## Principios SOLID

### 1. S - Single Responsibility Principle (Responsabilidad Única)
**Una clase solo debe tener una razón para cambiar/ejecutar**

Cumplir con este principio permite:
✦ Reutilizar código
✦ Mayor velocidad en Testing
✦ Mejor Mantenibilidad
✦ Mayor Escalabilidad

Al tener una sola responsabilidad se logra **alta cohesión** y **bajo acoplamiento**.

### 2. O - Open-Closed Principle (Principio Abierto/Cerrado)
**Las entidades de software deben estar abiertas para extensión, pero cerradas para modificación**

Cumplir con este principio permite:
✦ Agregar nuevas funcionalidades sin modificar código existente
✦ Reducir el riesgo de introducir bugs en código que ya funciona
✦ Mayor flexibilidad y extensibilidad del sistema
✦ Facilitar el mantenimiento a largo plazo

Se logra mediante **abstracción** (clases abstractas, interfaces) y **polimorfismo**, permitiendo que el código sea **extensible sin ser modificable**.

### 3. L - Liskov Substitution Principle (Principio de Sustitución de Liskov)
**Las subclases deben ser sustituibles por sus clases base**

Cumplir con este principio garantiza **Coherencia, interoperabilidad y evita comportamientos inesperados.** 

Para cumplirlo se debe:
✦ Mantener firma de métodos: mismos parámetros y orden.
✦ Mantener el tipo de retorno acordado.
✦ Conservar las reglas de uso: precondiciones y postcondiciones.
✦ Evitar agregar requisitos nuevos para invocar un método.


### 4. I - Interface Segregation Principle (Principio de Segregación de Interfaces)
**Los clientes no deben verse obligados a depender de interfaces que no utilizan**

Implementarlo significa:
✦ Mejor cohesion y reducción del acoplamiento
✦ Reutilizar componentes
✦ Cambios en una interfaz no afectan a otras clases

Se aplica cuando:
- Las interfaces tienen múltiples métodos que no todas las clases necesitan
- Los cambios en una interfaz fuerzan modificaciones en clases que no usan esa funcionalidad

**Solución**: Dividir interfaces grandes en interfaces más pequeñas y específicas, permitiendo que cada cliente dependa solo de los métodos que realmente utiliza.
