# Hero Journey Writer

## Descripción
Hero Journey Writer es una aplicación interactiva de narración basada en el concepto del "Viaje del Héroe" de Joseph Campbell. Utiliza modelos de lenguaje de IA y bases de datos vectoriales para crear una experiencia de juego de rol dinámica y personalizada.

## Características
- Generación de historia basada en IA
- Interacciones dinámicas con personajes
- Toma de decisiones que afectan el curso de la historia
- Memoria persistente de personajes utilizando bases de datos vectoriales
- Eventos aleatorios que añaden variedad a la narrativa

## Estructura del Proyecto
```bash
hero-journey-writer/
├── src/
│   ├── main.py
│   ├── graph/
│   │   └── hero_journey_graph.py
│   ├── utils/
│   │   ├── option_generator.py
│   │   ├── decision_evaluator.py
│   │   ├── character_encounters.py
│   │   ├── dynamic_events.py
│   │   └── story_generator.py
│   ├── models/
│   │   └── character.py
│   └── database/
│       └── vector_store.py
├── .env
└── README.md
```

## Diagrama de Funcionamiento
```bash
graph TD
    A[Inicio] --> B[Crear Grafo del Viaje del Héroe]
    B --> C[Inicializar Estado del Juego]
    C --> D[Generar Segmento de Historia]
    D --> E{Evento Aleatorio}
    E -->|Sí| F[Manejar Evento Dinámico]
    E -->|No| G[Encuentro con Personaje]
    F --> H[Manejar Elección del Jugador]
    G --> H
    H --> I[Evaluar Decisión]
    I --> J[Actualizar Estado]
    J --> K{Fin del Viaje?}
    K -->|No| D
    K -->|Sí| L[Fin]
```

## Requisitos
- Python 3.10+
- Bibliotecas: langgraph, langchain, langchain_anthropic, langchain_openai, pinecone-client, python-dotenv

## Configuración
1. Clona el repositorio:
```bash
   git clone https://github.com/tu-usuario/hero-journey-writer.git
   cd hero-journey-writer
```

2. Instala las dependencias:
```bash
   pip install -r requirements.txt
```

3. Configura las variables de entorno en un archivo `.env`:
```bash
   ANTHROPIC_API_KEY=tu_clave_api_de_anthropic
   OPENAI_API_KEY=tu_clave_api_de_openai
   PINECONE_API_KEY=tu_clave_api_de_pinecone
   PINECONE_ENVIRONMENT=tu_entorno_de_pinecone
```

## Ejecución
Para iniciar el juego, ejecuta:
```bash
python -m src.main
```

## Cómo Funciona
1. El juego inicia creando un grafo que representa las etapas del Viaje del Héroe.
2. Se genera un segmento de historia para la etapa actual.
3. Aleatoriamente, se presenta un evento dinámico o un encuentro con un personaje.
4. El jugador toma decisiones que afectan el curso de la historia.
5. Las decisiones son evaluadas y el estado del juego se actualiza.
6. El proceso se repite hasta que se alcanza la etapa final del viaje.
7. Durante todo el proceso, se utiliza una base de datos vectorial para mantener la memoria de los personajes y sus interacciones.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de enviar un pull request.

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)
