import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Transcribe the audio file
result = model.transcribe("/Users/joellim/iCloud Drive (Archive)/Desktop/tiktok-search-improvement/project/audio transcribing/wav files/5.wav")

# Print the transcription
print(result["text"])