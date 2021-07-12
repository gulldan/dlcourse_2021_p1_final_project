# Style-Transfer-Telegram-Bot
**Style Transfer Telegram Bot based on GAN**

What is Style Transfer Telegram Bot?
------------------------------------
Style Transfer Telegram Bot - финальный проект по курсу [Deep Learning School by MIPT](https://en.dlschool.org/).

The goal was to create a telegram bot based on a GAN network that can transfer the style from one image to another prechoosen styles. It was also necessary to deploy the bot to the server, so that the bot could run smoothly and not fall asleep.

The Bot itself: `@mk_usefull_bot` (Telegram), now disable


Network
-------
Я использовал готовые сконвертированные модели [onnx](https://github.com/microsoft/onnxruntime) для ускорения инфиеренса моделей. Также была выбрана сеть [GANsNRoses](https://github.com/mchong6/GANsNRoses) от [mchong6](https://github.com/mchong6) для переноса стиля видео. Модель и веса оригиналные. 
Всего используется 6 моделей - 5 для изображений [отсюда](https://github.com/onnx/models/tree/master/vision/style_transfer/fast_neural_style/model), 1 для видео [GANsNRoses](https://github.com/mchong6/GANsNRoses). 


Bot
---
Используемый фреймворк [aiogram](https://docs.aiogram.dev/en/latest/index.html) и к нему добавлен antiflood, сохранение картинок в кэш (redis).    

Существует два сценария работы бота.
1) Работа с изображение (в меню надо выбрать Изображение), асинхранные режим.
1.1) Присылается картинка
1.2) бот предлагает выбрать стиль из заданные и ожидает ответа
1.3) бот присылает измененную картинку.

2) Работа с видео (в меню надо выбрать Видео)
2.1) Бот предлагает прислать ссылку на видео (например с тиктока) Важно!!! чтобы на видео было лицо. Синхранные режим, через лок.
2.2) Бот скачивает видео.
2.3) Бот обрабатывает и присылает обработанное видео.

Для второго режима ограничено количество кадров ~20сек при 30 кадрах в секунду. Время обработки занимает около минуты. Возможности обработки и скачивание видео ограничины возможностями youtube-dl. 

Пример сслыки тикток:

https://vm.tiktok.com/ZMe1HQ3vE/

или

https://v.douyin.com/3vn57r/

или

https://www.tiktok.com/@philandmore/video/6805867805452324102

или

https://m.tiktok.com/v/6805867805452324102.html

Примеры результата работы в папке [sample](samples/output9.mp4).


Setup and manual
----------------
I set up the bot via `@BotFather`, and there I got a unique token for my bot.
Thanks to BotFather's capabilities, I was able to create a more comfortable environment for working with the bot. Here's what it looks like:

сделать гифку
http://zulko.github.io/blog/2014/01/23/making-animated-gifs-from-video-files-with-python/

**Before running my code, make sure that you get your own token from BotFather and specify it in the file main.py.**

Deploy
------
Для работы бота необходимо сначало поднять redis. И потом запустить бота.

Я неуспел завернуть все это дело в docker. Причина следующая. Для работы с видео нужна библиотека aubio и ffmpeg. Версии PyPI низкие, соответственно необходимо ставить из conda forge.
Но в conda forge нет остальных пакетов.
Надейное решение следующие. Сначало необходимо создать conda env, туда поставить 

# start redis
docker run --name redis --rm -p 6379:6379 -d redis:alpine

### Services
Поскольку была выбрана достаточна тяжелая модель для бесплатного хостинга, бот запущен на локальном хосте. Развернуло два контейнера: redis, и сам бот.
Dockerfile доступен в корне
