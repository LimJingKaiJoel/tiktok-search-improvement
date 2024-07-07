import os
import whisper
import pandas as pd
import time

start_time = time.time()

wav_folder = "/Users/joellim/iCloud Drive (Archive)/Desktop/tiktok-search-improvement/project/audio transcribing/wav files"
output_csv = "transcriptions.csv"
model = whisper.load_model("base")

# Initialize a list to store the results
results = []
i = 0

# Process each WAV file in the folder
for file_name in os.listdir(wav_folder):
    if file_name.endswith(".wav"):
        i += 1
        # Construct the full file path
        file_path = os.path.join(wav_folder, file_name)
        
        # Transcribe the audio file
        result = model.transcribe(file_path)
        
        # Extract the file ID (assumes file name is in the format 'ID.wav')
        file_id = os.path.splitext(file_name)[0]
        
        # Append the result to the list
        results.append({"ID": file_id, "Text": result["text"]})

        print(i)
        print(time.time() - start_time)

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Save the DataFrame to a CSV file
df.to_csv(output_csv, index=False)

print(f"Transcriptions saved to {output_csv}")
