import operator
import shelve as sh

def inrange(val, boundaries): 
    if val >= boundaries[0] and val <= boundaries[1]:
        return True
    return False

def contains(val, request):
    """
    Проверяет вхождение подстроки в строку\n
    Входные параметры:\n
        val – строка для проверки\n
        request – подстрока, наличие которой необходимо проверить\n
    Выходные параметры:\n
        True, если строка удовлетворяет условию\n
        False в ином случае\n
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    if val.lower().find(request.lower()) != -1:
        return True
    return False

operators = { '<' : operator.lt, '<=' : operator.le, '=' : operator.eq,
             '>' : operator.gt, '>=' : operator.ge, '!=' : operator.ne,
             'contains' : contains, 'inrange' : inrange }

def db_select(db, conditions):
    """
    Выбирает из базы данных элементы, удовлетворяющие заданным условиям\n
    Входные параметры:\n
        db – объект базы данных\n
        conditions – словарь с условиями выборки\n
    Выходные параметры:\n
        keys – список ключей, соответствующих удовлетворяющим условиям элементам
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    keys = list()
    for key, entry in db.items():
        add = True
        for field, condition in conditions.items():
            if operators[condition['operation']](entry.get(field), condition['values']) == False:
                add = False
                break
        if add:
            keys.append(key)
    return keys

def db_sort_by_id(entries, reverse):
    """
    Сортирует записи в БД по ID\n
    Входные параметры:\n
        entries – объект с запиями БД (словарь словарей)\n
        reverse – определяет направление сортировки\n
    Выходные параметры:\n
        d – отсортированная БД
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    d = dict()
    for key, value in sorted(entries.items(), key=lambda kv: int(kv[0]), 
                             reverse=reverse):
        d[key] = value
    return d

def db_sort_by_field(entries, field, reverse):
    """
    Сортирует записи в БД по заданному полю\n
    Входные параметры:\n
        entries – объект с запиями БД (словарь словарей)\n
        field – поле, по которому необходимо произвести сортировку\n
        reverse – определяет направление сортировки\n
    Выходные параметры:\n
        d – отсортированная БД
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    d = dict()
    for key, value in sorted(entries.items(),key=lambda kv: kv[1][field], 
                             reverse=reverse):
        d[key] = value
    return d

def db_add(db_path, new_entry):
    """
    Добавляет запись в БД\n
    Входные параметры:\n
        db_path – путь к файлу БД\n
        new_entry – словарь с данными новой записи\n
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    db = sh.open(db_path)
    last_key = int(sorted(list(db.keys()),key=lambda x: int(x))[-1])
    last_key += 1
    db[str(last_key)] = new_entry
    db.close()

def db_edit(db_path, key, values):
    """
    Изменяет существующую запись в БД\n
    Входные параметры:\n
        db_path – путь к файлу БД\n
        key – ключ записи, которую необходимо изменить\n
        values – новые значения полей записи\n
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    db = sh.open(db_path)
    db[key] = values
    db.close()

def db_delete(db_path, key):
    """
    Удаляет запись из БД\n
    Входные параметры:\n
        db_path – путь к файлу БД\n
        key – ключ записи, которую необходимо удалить\n
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    db = sh.open(db_path)
    if key in db:
        del db[key]
    db.close()

def db_stats(db):
    """
    Вычисляет статистику по элементам БД\n
    Входные параметры:\n
        db – объект БД\n
    Выходные параметры:\n
        stats – словарь с данными о статистике
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    stats = dict()
    budgets = list()
    years = list()
    sum_budget = 0.0
    for key, entry in db.items():
        budgets.append(entry['Budget, $ million'])
        sum_budget += entry['Budget, $ million']
        years.append(entry['Year'])
    stats['min_budget'] = min(budgets)
    stats['max_budget'] = max(budgets)
    stats['avg_budget'] = sum(budgets)/len(budgets)
    stats['min_year'] = min(years)
    stats['max_year'] = max(years)
    stats['entries'] = len(db)
    return stats