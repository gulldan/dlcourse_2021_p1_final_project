from dataclasses import dataclass
from emoji import emojize


@dataclass(frozen=True)
class Messages:
    test: str = "Привет {name}. Работаю..."
    btn_online: str = "Онлайн"
    btn_config: str = "Настройки"
    start_new_user: str = "Привет. Я могу сообщать тебе результаты матчей online."
    start_current_user: str = "Привет. {name} " \
                              "Используй команды или меню внизу для продолжения."
    help: str = "Этот бот получает два изображения и переносит стиль со второго изображения на первое." \
    " Бот создан в учебных целях, в рамках итогового проекта - https://stepik.org/course/91157"

    btn_save: str = "Сохранить"
    config_btn_edit: str = "Изменить"
    main: str = "Что будем делать?"
    db_saved: str = "Настройки сохранены"
    cb_limit: str = "Превышен лимит. Падажи"
    cb_updated: str = "Готово"
    unknown_text: str = "Ничего не понятно, но очень интересно.\nПопробуй команду /help"
