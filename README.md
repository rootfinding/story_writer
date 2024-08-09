# Story Writer - Aventura en el Bosque Mágico

Este proyecto es una aplicación interactiva que genera historias de aventuras personalizadas utilizando IA. El usuario proporciona el nombre de un héroe y su caramelo favorito, y la aplicación crea una historia única con desafíos del Mago Blanco que el héroe debe superar.

## Requisitos Previos

- Python 3.9+
- Docker y Docker Compose (para ejecución con Docker)
- Cuenta de OpenAI y API Key

## Configuración

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/story-writer.git
   cd story-writer
   ```

2. Crea un archivo `.env` en el directorio raíz del proyecto y añade tu API Key de OpenAI:
   ```
   OPENAI_API_KEY=tu_api_key_aqui
   ```

## Ejecución

### Con Docker

1. Construye la imagen de Docker:
   ```
   docker-compose build
   ```

2. Inicia los servicios:
   ```
   docker-compose up
   ```

3. La aplicación estará disponible en `http://localhost:8000`

### Sin Docker (Entorno Local)

1. Crea un entorno virtual e instala las dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Ejecuta la aplicación:
   ```
   python -m intro_writer.main
   ```

## Uso de LangChain Studio

Para visualizar y interactuar con el grafo de la aplicación en LangChain Studio:

1. Inicia el servidor de LangGraph:
   ```
   langgraph up
   ```

2. Abre tu navegador y ve a:
   [https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123)

3. En LangChain Studio, podrás ver una representación visual del flujo de la aplicación y probar diferentes entradas.

## Estructura del Proyecto

- `intro_writer/`: Contiene los módulos principales de la aplicación.
  - `main.py`: Punto de entrada de la aplicación.
  - `flow_graph.py`: Define el flujo de la historia usando LangGraph.
  - `agents_def.py`: Define los tipos de datos utilizados en el estado de la aplicación.
  - `mago_blanco.py`: Implementa la lógica del Mago Blanco y sus desafíos.
  - `human_interaction.py`: Maneja la interacción con el usuario.
  - `evaluator.py`: Evalúa las respuestas del usuario a los desafíos.
  - `scenary.py`: Genera escenarios aleatorios para la historia.
  - `intro_gen.py`: Genera la introducción de la historia.
- `Dockerfile` y `docker-compose.yml`: Configuración para ejecución con Docker.
- `requirements.txt`: Lista de dependencias de Python.
- `langgraph.json`: Configuración para LangGraph.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de hacer un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.