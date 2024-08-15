from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
import soundfile as sf
import numpy as np

class TextToSpeech:
    def __init__(self):
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        self.speaker_embeddings = torch.randn(1, 512)  # Random speaker embedding

    def synthesize_speech(self, text, output_file="output.wav"):
        inputs = self.processor(text=text, return_tensors="pt")
        speech = self.model.generate_speech(inputs["input_ids"], self.speaker_embeddings, vocoder=self.vocoder)
        speech = speech.numpy()
        sf.write(output_file, speech, samplerate=16000)
        return output_file

    def narrator_speech(self, text):
        return self.synthesize_speech(text, "narrator_output.wav")

    def mago_blanco_speech(self, text):
        return self.synthesize_speech(text, "mago_blanco_output.wav")

tts = TextToSpeech()

def speak_text(text, is_mago_blanco=False):
    try:
        if is_mago_blanco:
            file_path = tts.mago_blanco_speech(text)
        else:
            file_path = tts.narrator_speech(text)
        print(f"Audio generado en: {file_path}")
        # Aquí puedes agregar código para reproducir el audio si lo deseas
    except Exception as e:
        print(f"Error en la síntesis de voz: {e}")
        print("Continuando sin audio...")