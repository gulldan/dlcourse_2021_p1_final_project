from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    test: str = "Привет {name}. Работаю..."
    btn_online: str = "Описание"
    btn_video: str = "Видео"
    btn_image: str = "Изображения"
    start_current_user: str = "Привет. {name} " \
                              "Используй команды или меню внизу для продолжения."
    help: str = "Этот бот получает изображение и изменяет стиль, доступно пять стилей." \
    " Бот создан в учебных целях, в рамках итогового проекта - https://stepik.org/course/91157"

    main: str = "Что будем делать?"
    cb_limit: str = "Превышен лимит. Подождите"
    cb_updated: str = "Готово"
    unknown_text: str = "Ничего не понятно, но очень интересно.\nПопробуй команду /help"
    cancel: str = "Действие отменено"

    style_1: str = "1"
    style_2: str = "2"
    style_3: str = "3"
    style_4: str = "4"
    style_5: str = "5"
