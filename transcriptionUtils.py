import whisper
import os

def transcribe_audio(input_video_path, model_size="small"):
    """
    Videodaki sesi yazıya döker.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(input_video_path)
    return result

def save_transcript_as_srt(transcription_result, output_path):
    """
    Altyazı dosyası (SRT) oluşturur.
    """
    segments = transcription_result['segments']
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(segments):
            start = segment['start']
            end = segment['end']
            text = segment['text']

            f.write(f"{idx+1}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(f"{text.strip()}\n\n")

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
