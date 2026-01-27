import assemblyai as aai
import os 
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

current_dir = str(Path.cwd())
audio_file = current_dir+"/gettysburg.mp3"
print(audio_file)
# audio_file = "https://assembly.ai/wildfires.mp3"

# transcript = aai.Transcriber().transcribe(audio_file)

#System will use slam-1 first, but if it cant will switch to univesal
# config = aai.TranscriptionConfig(speech_models=["slam-1", "universal" ])
# config = aai.TranscriptionConfig(speech_model="universal")
# transcript = aai.Transcriber(config=config).transcribe(audio_file)

transcript = aai.Transcriber().transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print(transcript.text)
