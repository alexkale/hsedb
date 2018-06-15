import shelve as sh

fields = ['Title', 'Genre', 'Director', 'Country', 'Budget, $ million', 'Year']

def dict_from_list(entries):
    """
    Создает словарь БД из списка записей\n
    Входные параметры:\n
        entries – список с записями БД\n
    Выходные параметры:\n
        dictionary – словарь с записями БД
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    dictionary = dict()
    for idx in range(len(entries)):
        dictionary[idx] = dict(zip(fields, entries[idx]))
    return dictionary

def db_from_dict(entries, db_path):
    """
    Создает файл БД из словаря\n
    Входные параметры:\n
        entries – словарь с записями БД\n
        db_path – путь к файлу БД
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    db = sh.open(db_path)
    db.clear()
    for key, item in entries.items():
        db[str(key)] = item
    db.close()
    
def dict_from_db_file(db_path):
    """
    Создает словарь с записями из файла БД\n
    Входные параметры:\n
        db_path – путь к файлу БД\n
    Выходные параметры:\n
        dictionary – словарь с записями БД
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    dictionary = {}
    db = sh.open(db_path)
    for key, item in db.items():
        dictionary[str(key)] = item
    db.close()
    return dictionary