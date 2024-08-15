import os
from melo.api import TTS
import traceback

def test_tts_connection():
    print("Iniciando prueba de conexión Text-to-Speech con MeloTTS")
    
    try:
        # Configuración
        speed = 1.0
        device = 'cpu'
        language = 'ES'
        
        print(f"Creando modelo TTS para el idioma: {language}")
        model = TTS(language=language, device=device)
        print("Modelo TTS creado exitosamente")
        
        # Preparar la solicitud
        text = "Hola, esta es una prueba de conexión con MeloTTS."
        output_path = "output.wav"
        
        print("Intentando sintetizar voz...")
        speaker_id = model.hps.data.spk2id[language]
        model.tts_to_file(text, speaker_id, output_path, speed=speed)
        
        # Si llegamos aquí, la síntesis fue exitosa
        print("Síntesis de voz exitosa")
        print(f'Contenido de audio escrito en el archivo "{output_path}"')
        
    except Exception as e:
        print(f"Error durante la prueba de conexión: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_tts_connection()