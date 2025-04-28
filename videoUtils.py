import ffmpeg
import whisper
import numpy as np
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips


def detect_silence(input_path, silence_threshold=-35, chunk_duration=0.5):
    """
    Sessiz bölümleri tespit eder (dB cinsinden).
    """
    try:
        probe = ffmpeg.probe(input_path)
        duration = float(probe['format']['duration'])
    except Exception as e:
        print(f"Error probing video: {e}")
        return []

    command = (
        ffmpeg
        .input(input_path)
        .output('pipe:', format='wav', acodec='pcm_s16le', ac=1, ar='16000')
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    import wave
    import io

    out, _ = command.communicate()
    wav_file = wave.open(io.BytesIO(out), 'rb')

    frame_rate = wav_file.getframerate()
    frames = wav_file.readframes(wav_file.getnframes())
    audio = np.frombuffer(frames, dtype=np.int16)
    audio = audio / np.iinfo(np.int16).max

    chunk_samples = int(chunk_duration * frame_rate)
    silent_chunks = []
    for i in range(0, len(audio), chunk_samples):
        chunk = audio[i:i+chunk_samples]
        rms = np.sqrt(np.mean(chunk**2))
        db = 20 * np.log10(rms + 1e-6)
        if db < silence_threshold:
            silent_chunks.append((i/frame_rate, (i+chunk_samples)/frame_rate))

    return silent_chunks

def cut_video(input_path, output_path, silence_chunks, min_duration=2.0):
    """
    Sessiz bölgeleri atlayarak videoyu keser.
    """
    video = VideoFileClip(input_path)

    segments = []
    last_end = 0
    for start, end in silence_chunks:
        if start - last_end > min_duration:
            segments.append(video.subclip(last_end, start))
        last_end = end

    if video.duration - last_end > min_duration:
        segments.append(video.subclip(last_end, video.duration))

    final = concatenate_videoclips(segments)
    final.write_videofile(output_path, codec="libx264")

def burn_in_subtitles(input_video_path, subtitles_path, output_video_path, font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
    """
    SRT altyazı dosyasını videoya gömer (stil ile birlikte).
    """
    # FFmpeg komutu
    try:
        (
            ffmpeg
            .input(input_video_path)
            .output(
                output_video_path,
                vf=f"subtitles={subtitles_path}:force_style='FontName=DejaVu Sans,FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1'",
                codec="libx264",
                crf=23,
                preset="medium"
            )
            .overwrite_output()
            .run()
        )
        print("Altyazılar başarıyla videoya gömüldü!")
    except ffmpeg.Error as e:
        print("FFmpeg altyazı gömme hatası:", e)

def extract_audio(video_path, output_audio_path="temp_audio.wav"):
    """
    Videodan sesi çıkarır ve .wav dosyasına kaydeder.
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_audio_path, acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run()
        )
        return output_audio_path
    except ffmpeg.Error as e:
        print("FFmpeg ses çıkarma hatası:", e)
        return None
        
def transcribe_audio(audio_path):
    """
    Ses dosyasını transkripte çevirir.
    """
    model = whisper.load_model("small")  # whisper'ın küçük modeli hızlı ve yeterli
    result = model.transcribe(audio_path)
    return result["text"]
