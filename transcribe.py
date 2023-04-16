import os
import openai
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe_audio(audio_path, output_path):
    if not os.path.exists(output_path):
        perform_transcription(audio_path, output_path)


def load_transcription(output_path):
    with open(output_path, "r") as f:
        transcription = f.read()
        print(f"Transcription loaded from {output_path}")
    return transcription


def perform_transcription(audio_path, output_path):
    with open(audio_path, "rb") as f:
        try:
            transcription = openai.Audio.transcribe("whisper-1", f)
            save_transcription(transcription, output_path)
        except Exception as e:
            print(f"Error transcribing {audio_path}: {e}")
            transcription = None
    return transcription


def save_transcription(transcription, output_path):
    with open(output_path, "w") as f:
        f.write(transcription.text)
        print(f"Transcription saved to {output_path}")


def find_audio_files(directory="./audios"):
    audio_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                audio_path = os.path.join(root, file)
                audio_files.append(audio_path)
    return audio_files


def split_audio(audio_path, max_duration_minutes=20):
    audio = AudioSegment.from_mp3(audio_path)
    audio_duration = audio.duration_seconds / 60

    split_audio_paths = []

    if audio_duration > max_duration_minutes:
        chunk_duration = max_duration_minutes * 60 * 1000  # milliseconds
        num_chunks = int(audio.duration_seconds // (max_duration_minutes * 60)) + 1
        base_name = os.path.splitext(audio_path)[0]

        for i in range(num_chunks):
            start_time = i * chunk_duration
            end_time = min((i + 1) * chunk_duration, audio.duration_seconds * 1000)

            chunk_audio = audio[start_time:end_time]
            chunk_audio_path = f"{base_name}_part{i + 1}.mp3"
            chunk_audio.export(chunk_audio_path, format="mp3")

            split_audio_paths.append(chunk_audio_path)
    else:
        split_audio_paths.append(audio_path)

    return split_audio_paths


def main():
    os.makedirs("transcript", exist_ok=True)

    audio_files = find_audio_files()
    for audio_path in audio_files:
        split_audio_paths = split_audio(audio_path)

        for split_audio_path in split_audio_paths:
            output_filename = (
                os.path.basename(os.path.splitext(split_audio_path)[0]) + ".txt"
            )
            output_path = os.path.join("transcript", output_filename)

            if not os.path.exists(output_path):
                transcribe_audio(split_audio_path, output_path)
                print(f"Transcription saved to {output_path}")
            else:
                print(f"{output_path} already exists, skipping transcription")


if __name__ == "__main__":
    main()
