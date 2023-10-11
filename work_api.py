from datetime import *
import requests

class API:
    def __init__(self):
        """
        Инициализация объекта API.

        Этот метод инициализирует объект API с начальной датой (self.start) и вызывает метод regenerate() для получения расписания.

        Параметры:
        - Нет параметров.

        Возвращает:
        - Ничего не возвращает.
        """
        self.start = datetime(2023, 8, 28) # в начале следующего семестра эту дату нужно будет поменять
        self.regenerate()

    def regenerate(self):
        """
        Получение расписания из API.

        Этот метод отправляет GET-запрос к API университета и сохраняет результат в self.req.

        Параметры:
        - Нет параметров.

        Возвращает:
        - Если запрос прошел успешно, возвращает True и 'ok'.
        - Если в запросе были ошибки, возвращает False и сообщение об ошибке.
        """
        self.req = requests.get("https://timetable.mirea.ru/api/groups/name/%D0%98%D0%9A%D0%91%D0%9E-20-23").json()
        if 'errors' in self.req.keys():
            return False, self.req['errors']
        return True, 'ok'

    def get_today(self):
        """
        Получение расписания на текущий день.

        Этот метод анализирует расписание, полученное из API, и возвращает список занятий на текущий день.

        Параметры:
        - Нет параметров.

        Возвращает:
        - Список занятий на текущий день. Каждый элемент списка представляет собой список с названием дисциплины и временем начала занятия.
        """
        self.day = []
        now = datetime.now()
        week, now_day = (now - self.start).days // 7 + 1, now.weekday() + 1
        print(week)
        for lesson in self.req['lessons']:
            if week in lesson['weeks'] and now_day == lesson['weekday']:
                self.day.append([lesson['discipline']['name'], lesson['calls']['time_start']])
        return self.day

if __name__ == '__main__':
    a = API()
    print(a.get_today())