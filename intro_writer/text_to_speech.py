from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from intro_writer.agents_def import AgentState
from openai import OpenAI
from dotenv import load_dotenv
import os
import platform
import subprocess

def generate_speech(text, output_file="output.mp3", voice="alloy"):
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text,
    )
    response.stream_to_file(output_file)
    return output_file

import os
import platform
import subprocess

import os
import platform
import subprocess

def play_speech(file_path):
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["afplay", file_path])
        elif system == "Linux":
            # Check if we're in WSL
            if "microsoft" in platform.uname().release.lower():
                # Convert the WSL path to a Windows path
                windows_path = subprocess.check_output(["wslpath", "-w", file_path]).strip().decode()
                # Open the file with the default program
                subprocess.run(["powershell.exe", "-c", f"Invoke-Item '{windows_path}'"])
            else:
                # For non-WSL Linux, you might want to use a command-line audio player like 'aplay'
                subprocess.run(["aplay", file_path])
        elif system == "Windows":
            os.startfile(file_path)
        else:
            print(f"Unsupported operating system: {system}")
    except Exception as e:
        print(f"Error playing audio: {e}")