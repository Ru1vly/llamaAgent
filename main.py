import os
from video_utils import detect_silence, cut_video
from transcription_utils import transcribe_audio, save_transcript_as_srt
import extract_audio, cut_silent_parts, burn_in_subtitles
from caption_generator import generate_caption_and_hashtags_from_video


def main(video_path):
    # 1. Videodan sessiz kısımları kes
    print("▶️ Sessiz kısımlar kesiliyor...")
    edited_video_path = "outputs/edited_video.mp4"
    cut_silent_parts(video_path, edited_video_path)

    # 2. Videodan sesi çıkar
    print("🔊 Ses çıkarılıyor...")
    audio_path = extract_audio(edited_video_path)

    # 3. Ses dosyasından transcript oluştur
    print("✍️ Konuşmalar yazıya dökülüyor...")
    transcript_text = transcribe_audio(audio_path)

    # 4. Videoya altyazıları göm
    print("🎞️ Altyazılar videoya gömülüyor...")
    subtitles_path = "outputs/subtitles.srt"
    with open(subtitles_path, "w", encoding="utf-8") as f:
        # Basit bir SRT oluşturuyoruz (daha gelişmiş SRT generator ister misin?)
        lines = transcript_text.split('. ')
        for idx, line in enumerate(lines):
            start_time = f"00:00:{idx:02d},000"
            end_time = f"00:00:{(idx+1):02d},000"
            f.write(f"{idx+1}\n{start_time} --> {end_time}\n{line.strip()}\n\n")

    final_video_path = "outputs/final_output_with_subs.mp4"
    burn_in_subtitles(edited_video_path, subtitles_path, final_video_path)

    # 5. Videodan viral caption ve hashtagler oluştur
    print("🧠 Viral açıklama ve hashtagler oluşturuluyor...")
    viral_content = generate_caption_and_hashtags_from_video(final_video_path)

    # 6. Çıktıları kaydet
    print("💾 Çıktılar kaydediliyor...")
    os.makedirs("outputs", exist_ok=True)
    
    # Caption ve hashtagleri dosyaya yaz
    with open("outputs/caption_and_hashtags.txt", "w", encoding="utf-8") as f:
        f.write(viral_content)

    print("\n✅ Video düzenlendi ve viral içerik hazır!")
    print("🎬 Final Video: ", final_video_path)
    print("📝 Viral Caption ve Hashtagler: outputs/caption_and_hashtags.txt")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Kullanım: python main.py <video_dosyasi_yolu>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    main(video_path)
