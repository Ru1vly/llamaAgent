import os
from video_utils import detect_silence, cut_video
from transcription_utils import transcribe_audio, save_transcript_as_srt
from video_utils import burn_in_subtitles

def main():
    input_video = "input.mp4"  # Kullanıcıdan alınacak
    trimmed_video = "trimmed_output.mp4"
    subtitle_file = "subtitles.srt"

    print("1. Sessiz bölgeleri tespit ediliyor...")
    silent_chunks = detect_silence(input_video)

    print(f"Tespit edilen sessiz bölge sayısı: {len(silent_chunks)}")

    print("2. Videonun sessiz bölümleri kırpılıyor...")
    cut_video(input_video, trimmed_video, silent_chunks)

    print("3. Whisper ile konuşmalar yazıya dökülüyor...")
    transcription_result = transcribe_audio(trimmed_video)

    print("4. SRT altyazı dosyası oluşturuluyor...")
    save_transcript_as_srt(transcription_result, subtitle_file)

    print("İşlem tamamlandı!")

    print("5. Altyazılar videoya gömülüyor...")
    final_output_video = "final_output_with_subs.mp4"
    burn_in_subtitles(trimmed_video, subtitle_file, final_output_video)

    print("Tüm işlemler başarıyla tamamlandı! 🎉")


if __name__ == "__main__":
    main()
