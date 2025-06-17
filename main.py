import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
import locale
import os
import imageio

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

# --- Локализация ---
def get_locale_language():
    try:
        lang, _ = locale.getdefaultlocale()
        if lang and lang.startswith("ru"):
            return "ru"
    except:
        pass
    # Альтернативно — смотрим переменную окружения
    env_lang = os.environ.get("LANG", "").lower()
    if "ru" in env_lang:
        return "ru"
    return "en"

lang = get_locale_language()

MESSAGES = {
    "choose_action": {
        "ru": "\nВыберите действие:\n1. Открыть окно проигрывателя\n2. Сохранить ASCII GIF\nВаш выбор: ",
        "en": "\nChoose action:\n1. Open player window\n2. Save ASCII GIF\nYour choice: "
    },
    "opening_video": {
        "ru": "❌ Ошибка открытия видео.",
        "en": "❌ Error opening video."
    },
    "processing_frames": {
        "ru": "📦 Обработка кадров:",
        "en": "📦 Processing frames:"
    },
    "done": {
        "ru": "✅ Готово.",
        "en": "✅ Done."
    },
    "saving_gif": {
        "ru": "💾 Сохранение ASCII GIF...",
        "en": "💾 Saving ASCII GIF..."
    },
    "choose_filename": {
        "ru": "Введите имя файла для сохранения (например, output.gif): ",
        "en": "Enter filename to save (e.g. output.gif): "
    },
    "start_player": {
        "ru": "▶️ Запуск проигрывателя...",
        "en": "▶️ Starting player..."
    }
}

# --- Обработка видео ---

def resize_preserve_aspect(frame, target_width=100):
    height, width, _ = frame.shape
    aspect_ratio = height / width
    new_width = target_width
    new_height = int(aspect_ratio * new_width * 0.55)  # корректировка высоты символов
    resized = cv2.resize(frame, (new_width, new_height))
    return resized

def frame_to_ascii_colored(image):
    gray = Image.fromarray(image).convert('L')
    color = Image.fromarray(image).convert('RGB')

    gray_pixels = np.array(gray)
    color_pixels = np.array(color)
    ascii_frame = []

    for y in range(gray_pixels.shape[0]):
        row = []
        for x in range(gray_pixels.shape[1]):
            brightness = gray_pixels[y, x]
            char = ASCII_CHARS[brightness * len(ASCII_CHARS) // 256]
            r, g, b = color_pixels[y, x]
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            row.append((char, hex_color))
        ascii_frame.append(row)
    return ascii_frame

def process_video(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(MESSAGES["opening_video"][lang])
        return []

    fps_target = 10
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps <= 0 or original_fps < fps_target:
        frame_interval = 1
    else:
        frame_interval = max(1, int(original_fps // fps_target))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 100
    ascii_frames = []
    frame_count = 0
    saved_count = 0

    print(MESSAGES["processing_frames"][lang])
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            resized = resize_preserve_aspect(frame, target_width=80)
            ascii_frame = frame_to_ascii_colored(resized)
            ascii_frames.append(ascii_frame)
            saved_count += 1
            progress = int((saved_count / total_frames) * 100)
            bar = ('#' * (progress // 5)).ljust(20)
            print(f"\r[{bar}] {saved_count}/{total_frames}", end="")
        frame_count += 1
    cap.release()
    print(f"\n{MESSAGES['done'][lang]}")
    return ascii_frames

# --- GUI player ---

def play_ascii_gui_colored(frames, fps=10):
    root = tk.Tk()
    root.title("🎞 ASCII Player")
    root.configure(bg="black")
    root.attributes('-topmost', True)

    font_size = 6
    font_family = "Courier New"
    char_width = 6
    char_height = 9

    rows = len(frames[0])
    cols = len(frames[0][0])
    canvas_width = cols * char_width
    canvas_height = rows * char_height

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
    canvas.pack()

    text_ids = []

    def draw_frame(index=0):
        nonlocal text_ids
        for tid in text_ids:
            canvas.delete(tid)
        text_ids.clear()

        frame = frames[index]
        for y, row in enumerate(frame):
            for x, (char, color) in enumerate(row):
                tid = canvas.create_text(
                    x * char_width, y * char_height,
                    text=char,
                    fill=color,
                    anchor="nw",
                    font=(font_family, font_size)
                )
                text_ids.append(tid)

        next_index = (index + 1) % len(frames)
        root.after(int(1000 / fps), draw_frame, next_index)

    draw_frame()
    root.mainloop()

# --- Сохранение ASCII GIF (цветного) ---

def ascii_frame_to_image(ascii_frame, font_path=None, font_size=12, bg_color=(0, 0, 0)):
    rows = len(ascii_frame)
    cols = len(ascii_frame[0])
    # Подбираем размер изображения по символам
    image_width = cols * font_size
    image_height = rows * font_size

    img = Image.new("RGB", (image_width, image_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Шрифт моноширинный
    if font_path is None:
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, font_size)

    for y, row in enumerate(ascii_frame):
        for x, (char, color) in enumerate(row):
            draw.text((x * font_size, y * font_size), char, fill=color, font=font)
    return img

def save_ascii_gif(frames, filename):
    print(MESSAGES["saving_gif"][lang])
    pil_frames = []
    for f in frames:
        img = ascii_frame_to_image(f)
        pil_frames.append(img)
    # Сохраняем GIF
    pil_frames[0].save(
        filename,
        save_all=True,
        append_images=pil_frames[1:],
        duration=100,  # мс, соответствует 10 fps
        loop=0
    )
    print(f"✅ GIF сохранён в {filename}")

# --- Основной запуск ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python video_ascii.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    frames = process_video(video_path)
    if not frames:
        sys.exit(1)

    choice = input(MESSAGES["choose_action"][lang])
    if choice == "1":
        print(MESSAGES["start_player"][lang])
        play_ascii_gui_colored(frames)
    elif choice == "2":
        filename = input(MESSAGES["choose_filename"][lang]).strip()
        if not filename:
            filename = "output.gif"
        save_ascii_gif(frames, filename)
    else:
        print("❌ Invalid choice.")
