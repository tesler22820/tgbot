import telebot

API_TOKEN = "7682939795:AAGsU5W7lSWPqtapZRo7ejRp28tQqbGFTKE"
bot = telebot.TeleBot(API_TOKEN)
tasks = []
@bot.message_handler(commands=['start'])
def start(message):
    welcome_message = (
        "Привет! Я твой личный помощник.\n"
        "Вот что я умею:\n"
        "/add_task - добавить задачу\n"
        "/show_tasks - показать все задачи\n"
        "/delete_task - удалить задачу по номеру\n"
        "/edit_task - редактировать задачу по номеру"
    )
    bot.send_message(message.chat.id, welcome_message)

@bot.message_handler(commands=['add_task'])
def add_task(message):
    task = message.text[10:].strip()
    if task:
        tasks.append(task)
        bot.send_message(message.chat.id, f'Задача добавлена: "{task}"')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите текст задачи.')

@bot.message_handler(commands=['show_tasks'])
def show_tasks(message):
    if tasks:
        task_list = '\n'.join(f"{i + 1}. {task}" for i, task in enumerate(tasks))
        bot.send_message(message.chat.id, f'Ваши задачи:\n{task_list}')
    else:
        bot.send_message(message.chat.id, 'У вас пока нет задач.')

@bot.message_handler(commands=['delete_task'])
def delete_task(message):
    try:
        task_index = int(message.text.split()[1]) - 1
        if 0 <= task_index < len(tasks):
            removed_task = tasks.pop(task_index)
            bot.send_message(message.chat.id, f'Задача удалена: "{removed_task}"')
        else:
            bot.send_message(message.chat.id, 'Неверный номер задачи. Попробуйте еще раз.')
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, 'Используйте: /delete_task НОМЕР_ЗАДАЧИ')

@bot.message_handler(commands=['edit_task'])
def edit_task(message):
    try:
        task_parts = message.text.split()
        task_index = int(task_parts[1]) - 1
        new_task = ' '.join(task_parts[2:])
        if 0 <= task_index < len(tasks) and new_task:
            tasks[task_index] = new_task
            bot.send_message(message.chat.id, f'Задача изменена на: "{new_task}"')
        else:
            bot.send_message(message.chat.id, 'Неверный номер задачи или текст пуст.')
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, 'Используйте: /edit_task НОМЕР_ЗАДАЧИ НОВАЯ_ЗАДАЧА')

bot.polling()