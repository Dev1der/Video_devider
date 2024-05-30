import os
import moviepy.editor as mp
import speech_recognition as sr

# Константы для путей
TEXT_DIR = "resources/text"
AUDIO_DIR = "resources/audio"
VIDEO_DIR = "resources/video"

# Создание директорий, если их нет
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


def extract_audio_from_video(video_path, audio_path):
    # Извлекаем аудио из видео и сохраняем его.
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
    except Exception as e:
        print(f"Ошибка при извлечении аудио: {e}")


def extract_text_from_audio(audio_path, text_path):
    # Извлекаем текст из аудио и сохраняем его.
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)

    with audio_file as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        with open(text_path, 'w') as file:
            file.write(text)
    except sr.UnknownValueError:
        print("Код не смог распознать аудио")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи; {e}")


def save_video(video_path, output_path):
    # Сохраняем видео в указанную директорию.
    try:
        video = mp.VideoFileClip(video_path)
        video.write_videofile(output_path)
    except Exception as e:
        print(f"Ошибка при сохранении видео: {e}")


def process_video(video_path):
    # Основная функция для обработки видео.
    base_name = os.path.basename(video_path).split('.')[0]
    audio_path = os.path.join(AUDIO_DIR, f"{base_name}.wav")
    text_path = os.path.join(TEXT_DIR, f"{base_name}.txt")
    video_output_path = os.path.join(VIDEO_DIR, f"{base_name}.mp4")

    # Извлечение и сохранение аудио
    extract_audio_from_video(video_path, audio_path)

    # Извлечение и сохранение текста
    extract_text_from_audio(audio_path, text_path)

    # Сохранение видео
    save_video(video_path, video_output_path)


# Пример использования
video_file_path = "resources/video/это_фиаско_братан.mp4"
process_video(video_file_path)
