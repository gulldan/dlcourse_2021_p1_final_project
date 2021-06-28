from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    image = State()  # Will be represented in storage as 'Form:image'
    image_hash = State() # Will be represented in storage as 'Form:image_hash'
    style = State()  # Will be represented in storage as 'Form:style'
    user = State()  # Will be represented in storage as 'Form:user'

