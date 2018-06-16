import sys
sys.path.insert(0, '..')
import gui as gui
import settings as settings
import Library.db_helper as db_helper



db_list = [['Криминальное чтиво', 'криминал, комедия, триллер', 'Квентин Тарантино', 'США', 8.0, 1994],
  ['Бешеные псы', 'криминал, триллер, драма', 'Квентин Тарантино', 'США', 1.2, 1991], 
  ['Джанго Освобожденный', 'драма, вестерн, приключения', 'Квентин Тарантино', 'США', 100.0, 2012], 
  ['Омерзительная восьмерка', 'драма, криминал, детектив, вестерн', 'Квентин Тарантино', 'США', 44.0, 2015], 
  ['Престиж', 'фантастика, триллер, драма, детектив', 'Кристофер Нолан', 'США, Великобритания', 40.0, 2006], 
  ['Начало', 'фантастика, боевик, триллер', 'Кристофер Нолан', 'США, Великобритания', 160.0, 2010], 
  ['Интерстеллар', 'фантастика, драма, приключения', 'Кристофер Нолан', 'США, Великобритания', 165.0, 2014], 
  ['Большой куш', 'криминал, комедия, боевик', 'Гай Ричи', 'Великобритания, США', 10.0, 2000], 
  ['Карты, деньги, два ствола', 'комедия, криминал', 'Гай Ричи', 'Великобритания', 0.96, 1998], 
  ['Бутч Кэссиди и Санденс Кид', 'вестерн', 'Джордж Рой Хилл', 'США', 6.0, 1969], 
  ['Мечтатели', 'эротическая драма', 'Бернардо Бертолуччи', 'Италия', 15.0, 2003], 
  ['Последнее танго в Париже', 'эротическая мелодрама', 'Бернардо Бертолуччи', 'Италия, Франция', 1.25, 1972], 
  ['Париж, Техас', 'драматическое роуд-муви', 'Вим Вендерс', 'США', 1.16, 1984], 
  ['Выживут только любовники', 'фэнтези, драма', 'Джим Джармуш', 'Великобритания', 7.0, 2013], 
  ['Кофе и сигареты', 'комедия, драма', 'Джим Джармуш', 'США', 0.0, 2003], 
  ['Рэмбо: первая кровь', 'боевик', 'Тед Котчефф', 'США', 15.0, 1982], 
  ['Рэмбо: первая кровь 2', 'боевик', 'Джордж Косматос', 'США', 44.0, 1985], 
  ['Субмарина', 'комедия, драма', 'Ричард Айоади', 'Великобритания, США', 1.5, 2010],
  ['Вечное сияние чистого разума', 'мелодрама, фантастика, комедия', 'Мишель Гондри', 'США', 20.0, 2004],
  ['Наука сна', 'романтическая комедия', 'Мишель Гондри', 'Франция', 6.0, 2006]
]

def reset_base():
    """
    Возвращает базу данных к исходному виду (из списка записей)\n
    Входные параметры:
        –
    Выходные параметры:
        –
    Автор: Калентьев А.А.
    """
    db = db_helper.dict_from_list(db_list)
    db_helper.db_from_dict(db, settings.DB_PATH)

def main():
    """
    Точка входа в приложение.\n
    Проверяет параметры командной строки и при необходимости вызывает функцию 
    сброса данных БД\n
    Запускает приложение и вызывает функцию создания GUI\n
    Входные параметры:
        –
    Выходные параметры:
        –
    Автор: Калентьев А.А.
    """
    if 'reset' in sys.argv:
        reset_base()
    gui.setup_db()
    gui.main_window()

if __name__ == '__main__':
    main()

