from app import bot
from .sqlighter import SQLighter
import datetime
import math
import os


dir_path = os.path.dirname(os.path.abspath(__file__))
db_name = 'schedule.db'
db_path = os.path.join(dir_path, db_name)


def format_lesson(db, lesson):
    l_name = db.subject_name(lesson[0])
    l_teacher = db.teacher_full_name(lesson[1])
    l_aud = lesson[2]

    # черная магия со временем
    current_time = datetime.datetime.now()
    current_date = current_time.date()
    finish_hour, finish_minute = [int(n) for n in lesson[4].split(':')]
    finish_time = datetime.time(hour=finish_hour, minute=finish_minute)
    finish_dt = datetime.datetime.combine(current_date, finish_time)
    remaining_time = finish_dt - current_time

    l_left = math.ceil(remaining_time.total_seconds() / 60)

    return ('Предмет: {name}\n'
            'Аудитория: {aud}\n'
            'Препод: {teacher}\n'
            'До конца пары осталось {left} минут').format(name=l_name,
                                                          aud=l_aud,
                                                          teacher=l_teacher,
                                                          left=l_left)


@bot.message_handler(commands=["rasp"])
def get_current_lesson(message):
    db = SQLighter(db_path)

    msg = ""
    lessons = db.current_lesson()

    if len(lessons) == 0:
        msg += 'Сейчас пары нет'

    elif len(lessons) == 1:
        msg += format_lesson(db, lessons[0])

    else:
        msg += '[!] Произошла ошибка'

    db.close()
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["next"])
def get_next_lesson(message):
    db = SQLighter(db_path)
    msg = "Следующая пара"
    db.close()
    bot.send_message(message.chat.id, msg)


print("Schedule plugin loaded.")
