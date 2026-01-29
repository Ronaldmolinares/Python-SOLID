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


### 5. D - Dependency Inversion Principle (Principio de Inversión de Dependencias)
**Los módulos de alto nivel no deben depender de los módulos de bajo nivel. Ambos deben depender de abstracciones**

- **Módulos de alto nivel:** Contienen la lógica de negocio
- **Módulos de bajo nivel:** Manejan detalles específicos

Reglas clave:
✦ Las abstracciones no deben depender de los detalles
✦ Los detalles deben depender de las abstracciones
✦ Usar interfaces o clases abstractas en lugar de clases concretas


### Patrones de Diseño
**Soluciones reutilizables para problemas comunes en el diseño de software**

Hay tres categorías principales:
1. **Patrones Creacionales:** Se centran en la creación de objetos.
   - Ejemplos: Singleton, Factory Method, Abstract Factory, Builder, Prototype.

2. **Patrones Estructurales:** Se ocupan de la composición de clases y objetos.
   - Ejemplos: Adapter, Composite, Proxy, Flyweight, Facade, Bridge, Decorator.

3. **Patrones de Comportamiento:** Se enfocan en mejorar la comunicación y asignación de responsabilidades entre objetos.
   - Ejemplos: Observer, Strategy, Command, Chain of Responsibility, Mediator, State, Visitor, Template Method, Iterator, Memento.


#### Patrones Usados:
1. **Strategy**:
Para implementarlo se definió una interfaz `NotifierProtocol` y varias implementaciones concretas (`EmailNotifier`, `SMSNotifier`, `LogOnlyNotifier`). La selección del notificador se realiza en tiempo de ejecución según la información de contacto del cliente.

**Para usar el patrón Strategy se debe:**
✦ Definir una interfaz común (Protocol) que todas las estrategias implementen
✦ Crear implementaciones concretas de cada estrategia
✦ Crear un método selector que escoja la estrategia apropiada
✦ Permitir el cambio de estrategia en tiempo de ejecución

2. **Factory Pattern**
El patrón Factory en Python se caracteriza por:

1. Abstracción: Crea objetos sin especificar la clase exacta, utilizando interfaces o abstracciones.
2. Encapsulamiento: Centraliza la lógica de creación de objetos, simplificando la instancia de clases.
3. Flexibilidad: Permite añadir nuevos tipos de objetos sin modificar el código existente.

**Cuándo aplicarlo:**
- Cuando hay múltiples clases que comparten una interfaz.
- Cuando la creación de objetos requiere lógica compleja.

**Cómo aplicarlo:**
- Crea una clase Factory con un método que instancie objetos basados en parámetros. Usa el Factory donde se requieran instancias, facilitando cambios futuros.