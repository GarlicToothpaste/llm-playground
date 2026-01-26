import assemblyai as aai
import os 
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

audio_file = "https://assembly.ai/wildfires.mp3"

transcript = aai.Transcriber().transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

print(transcript.text)
