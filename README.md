# ASCII Видео Плеер и Конвертер

Данный скрипт на Python позволяет конвертировать видеофайлы (mp4, gif и др.) в цветное ASCII-арт видео и воспроизводить их в отдельном окне или сохранять как цветной ASCII GIF.

---

## Возможности\условия

- Снижение FPS до 10 для более комфортного ASCII-воспроизведения  
- Сохранение оригинального соотношения сторон видео (без обрезки)  
- Конвертация кадров в цветной ASCII-арт  
- Воспроизведение ASCII-видео в отдельном окне поверх других окон  
- Сохранение результата в цветной GIF с анимацией  

---

## Требования

- Python 3.6+  
- Библиотеки:  
  - opencv-python  
  - pillow  
  - numpy  
  - imageio  

Установить библиотеки можно командой:

```bash
pip install opencv-python pillow numpy imageio
```

---

## Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/GeniusofAB/video-to-uscii-gif
cd video-to-uscii-gif
```

2. Запустите скрипт, указав путь к видеофайлу:

```bash
python video_ascii.py "путь/к/видео.mp4"
```

3. Выберите действие, которое хотите выполнить:

```
1 - Открыть окно проигрывателя  
2 - Сохранить ASCII GIF
```

---

## Пример

```bash
python main.py "D:/videos/sample.mp4"
```

---

## Лицензия

MIT License

© 2025 GeniusofAB

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
