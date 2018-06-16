import tkinter as tk
import Library.db_helper as db_helper
import Library.db_operations as db_operations
import Scripts.settings as settings

root = object()
entries_table = object()
canvas = object()
db = dict()
conditions = dict()

def setup_db():
    """
    Загружает БД из файла и устанавливает объект БД\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    db = db_helper.dict_from_db_file(settings.DB_PATH)
    db = db_operations.db_sort_by_id(db, False)

def popup_error():
    """
    Создает всплывающее окно с сообщением об ошибке\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    win = tk.Toplevel()
    win.wm_title('Ошибка')

    l = tk.Label(win, text='Неверный формат данных.\n\
Проверьте введенные данные на соответствие типам полей\n и попробуйте снова.')
    l.pack()

    b = tk.Button(win, text='Закрыть', command=win.destroy, 
                  **settings.button_options)
    b.pack()
    
def edit_entry(key, values):
    """
    Изменяет запись в БД.\n
    Проверяет корректность введенных значений и записывает изменения в БД\n
    Входные параметры:\n
        key – ключ записи, которую необходимо изменить\n
        values – словарь с новыми значениями записи\n
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    entry = dict()
    for field,value in values.items():
        try:
            if settings.field_types[field] == 'string':
                entry[field] = str(value.get())
            elif settings.field_types[field] == 'int':
                entry[field] = int(value.get())
            elif settings.field_types[field] == 'float':
                entry[field] = float(value.get())
        except ValueError:
            popup_error()
            return
    db_operations.db_edit(settings.DB_PATH, key, entry)    
    db = db_helper.dict_from_db_file(settings.DB_PATH)
    db = db_operations.db_sort_by_id(db, False)
    update_canvas()
    
def edit_entry_window(key): 
    """
    Создает всплывающее окно для редактирования записи\n
    Входные параметры:\n
        key – ключ записи, которую необходимо изменить\n
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    win = tk.Toplevel()
    win.wm_title('Изменение записи')
    edit_frame = tk.Frame(win, width = 800, height = 600, padx=20, pady=20)
    btn_frame = tk.Frame(win, pady=20)

    values = dict()

    row = 0
    for field in db_helper.fields:
        field_name = tk.Label(edit_frame, text=field, anchor = 'w')
        value = tk.Entry(edit_frame)
        value.insert(0, db[key].get(field))
        field_name.grid(row=row,column=0)
        value.grid(row=row,column=1)
        values[field] = value
        row += 1
    edit_btn = tk.Button(btn_frame, text = 'Изменить', 
                           command=lambda key=key, 
                           values=values: edit_entry(key, values), 
                           **settings.button_options)
    edit_frame.pack()
    edit_btn.pack()
    btn_frame.pack()
    
def add_entry(values):
    """
    Добавляет запись в БД.\n
    Проверяет корректность введенных значений и записывает изменения в БД\n
    Входные параметры:\n
        values – словарь со значениями записи\n
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    entry = dict()
    for field,value in values.items():
        try:
            if settings.field_types[field] == 'string':
                entry[field] = str(value.get())
            elif settings.field_types[field] == 'int':
                entry[field] = int(value.get())
            elif settings.field_types[field] == 'float':
                entry[field] = float(value.get())
        except ValueError:
            popup_error()
            return
    db_operations.db_add(settings.DB_PATH, entry)
    db = db_helper.dict_from_db_file(settings.DB_PATH)
    db = db_operations.db_sort_by_id(db, False)
    update_canvas()
    
def add_entry_window():
    """
    Создает всплывающее окно для добавления записи\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    win = tk.Toplevel()
    win.wm_title('Добавление записи')
    add_frame = tk.Frame(win, width = 800, height = 600, padx=20, pady=20)
    btn_frame = tk.Frame(win, pady=20)

    values = dict()

    row = 0
    for field in db_helper.fields:
        field_name = tk.Label(add_frame, text=field, anchor = 'w')
        value = tk.Entry(add_frame)
        field_name.grid(row=row,column=0)
        value.grid(row=row,column=1)
        values[field] = value
        row += 1
    add_btn = tk.Button(btn_frame, text = 'Добавить', 
                           command=lambda values=values: add_entry(values), 
                           **settings.button_options)
    add_frame.pack()
    add_btn.pack()
    btn_frame.pack()

def do_search():
    """
    Проверяет верность введенных данных, создает на основе этих данных запрос,
    выполняет поиск в базе данных и обновляет таблицу с записями
    с результатами\n
    Автор: Калентьев А.А.
    """
    global entries_table, db
    request = dict()
    for field, condition in conditions.items():
        if len(condition['values'].get()) != 0:
            try:
                if settings.field_types[field] == 'string':
                    request[field] = {
                                'operation' : settings.string_operations[condition['operation'].get()],
                                 'values' : condition['values'].get()}
                else:
                    request[field] = {'operation' : settings.number_operations[condition['operation'].get()],
                              'values' : float(condition['values'].get())}
            except ValueError:
                popup_error()
                return
    keys = db_operations.db_select(db, request)
    db = {key: value for (key, value) in db.items() if key in keys}
    update_canvas()

def show_selection():
    """
    Создает всплывающее окно для ввода параметров фильтрации записей\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    win = tk.Toplevel()
    win.wm_title('Поиск записей')
    filter_frame = tk.Frame(win, width = 800, height = 600, padx=20, pady=20)
    btn_frame = tk.Frame(win, pady=20)
    #Заголовок таблицы
    title_header = tk.Label(filter_frame, text = 'Поле', anchor = 'w', 
                            bg = '#afbacc')
    operation_header = tk.Label(filter_frame, text = 'Операция сравнения', 
                                anchor = 'w', bg = '#afbacc')
    value_header = tk.Label(filter_frame, text = 'Значение', anchor = 'w',
                            bg = '#afbacc')
    
    title_header.grid(row=0, column=0, sticky='nsew')
    operation_header.grid(row=0, column=1, sticky='nsew')
    value_header.grid(row=0, column=2, sticky='nsew')

    row = 1
    for field in db_helper.fields:
        field_name = tk.Label(filter_frame, text=field, anchor = 'w')
        search_type = tk.StringVar(filter_frame)
        if settings.field_types[field] == 'string':
            search_type.set('Полное совпадение')
            search_type_box = tk.OptionMenu(filter_frame, search_type,
                                        *settings.string_operations)
        else:
            search_type.set('=')
            search_type_box = tk.OptionMenu(filter_frame, search_type,
                                        *settings.number_operations)
        value = tk.Entry(filter_frame)
        conditions[field] = {'operation':search_type,'values':value}
        field_name.grid(row=row,column=0, sticky='nsew')
        search_type_box.grid(row=row,column=1, sticky='nsew')
        value.grid(row=row,column=2, sticky='nsew')
        row += 1
    search_btn = tk.Button(btn_frame, text = 'Отфильтровать', 
                           command=do_search, **settings.button_options)
    filter_frame.pack()
    search_btn.pack()
    btn_frame.pack()

def save_db():
    """
    Записывает изменения в БД\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    db_helper.db_from_dict(db)

def create_table_from_entries(entries, parent):
    """
    Создает таблицу с записями для GUI\n
    Параметры:
        \tentries – словарь с записями (словарями) для вывода\n
        \tparent - родительское окно
    Возвращает объект класса tkinter.Frame\n
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    icon = tk.PhotoImage(file='../Graphics/edit.gif')
    table_frame = tk.Frame(parent, width=800)
    c = tk.Label(table_frame, bg = '#f7f3c5', text = 'ID', font='Arial 12')
    c.grid(row = 0,column = 0, sticky = tk.NSEW)
    col = 1
    for field in db_helper.fields:
        c = tk.Label(table_frame, bg = '#f7f3c5', 
                     text = field, font='Arial 12')
        c.grid(row = 0,column = col, sticky = tk.NSEW)
        col += 1
    row = 1
    for key, item in entries.items():
        c = tk.Label(table_frame, bg = '#e0dfd0', text = key, font='Arial 12')
        c.grid(row = row,column = 0, sticky = tk.NSEW)
        col = 1
        for field_key, field_value in item.items():
            c = tk.Label(table_frame, bg = '#e0dfd0', 
                         text = field_value, anchor='w', font='Arial 12')
            c.grid(row = row, column = col, sticky = tk.NSEW)
            col += 1
        edit_btn = tk.Button(table_frame, text = 'Изменить', height=2,
                             image = icon,
                             command=lambda key=key: edit_entry_window(key))
        edit_btn.image = icon
        del_btn = tk.Button(table_frame, text = 'X', fg='#ff0505', width=2,
                            height=2,
                            command=lambda key=key: delete_entry(key))
        edit_btn.grid(row = row, column = col)
        del_btn.grid(row = row, column = col + 1)
        row += 1
    return table_frame
    
def show_stats():
    """
    Создает всплывающее окно со статистикой для текущей выборки, 
    сохраняет статистику в файл\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    main_frame = tk.Frame(tk.Toplevel(), padx=20, pady=20)
    stats = db_operations.db_stats(db)
    
    title = tk.Label(main_frame, text='Статистика выборки', bg='#f7f3c5')
    min_budget = tk.Label(main_frame, text='Минимальный бюджет: {0}, $ млн.'
                                      .format(stats['min_budget']))
    max_budget = tk.Label(main_frame, text='Максимальный бюджет: {0}, $ млн.'
                                      .format(stats['max_budget']))
    avg_budget = tk.Label(main_frame, text='Средний бюджет: {0}, $ млн.'
                                      .format(round(stats['avg_budget'],1)))
    avg_budget = tk.Label(main_frame, 
                    text='Выборочная дисперсия бюджета в выборке: {0}'
                                      .format(round(stats['budget_variance'],2)))
    min_year = tk.Label(main_frame, text='Самая ранняя дата выхода: {0}'
                                      .format(stats['min_year']))
    max_year = tk.Label(main_frame, text='Самая поздняя дата выхода: {0}'
                                      .format(stats['max_year']))
    count = tk.Label(main_frame, text='Количество записей: {0}'
                                      .format(stats['entries']))
    title.pack(fill='x')
    min_budget.pack()
    max_budget.pack()   
    avg_budget.pack()
    min_year.pack()
    max_year.pack()
    count.pack()
    
    main_frame.pack()
    
    with open('../Output/stats.txt','w+') as f:
        stats = 'Статистика для последней выборки:\n\tМинимальный бюджет: {0}, $ млн.\n\
        Максимальный бюджет: {1}, $ млн.\n\
        Средний бюджет: {2}, $ млн.\n\
        Выборочная дисперсия бюджета в выборке: {3}\n\
        Самая ранняя дата выхода: {4}\n\
        Самая поздняя дата выхода: {5}\n\
        Количество записей в выборке: {6}'.format(stats['min_budget'],
                stats['max_budget'],round(stats['avg_budget'],2),
                round(stats['budget_variance'],2),stats['min_year'],
                stats['max_year'],stats['entries'])
        f.write(stats)

def do_sort(sort_field, reverse):
    """
    Сортирует записи БД по заданному полю\n
    Входные параметры:\n
        ksort_field – поле, по которому производится сортировка\n
        reverse – направление сортировки
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    if sort_field.get() == 'ID':
        entries = db_operations.db_sort_by_id(db, reverse.get())
    else:
        entries = db_operations.db_sort_by_field(db, 
                                 settings.sort_options[sort_field.get()], 
                                 reverse.get())
    db = entries
    update_canvas()

def sort_window():
    """
    Создает всплывающее окно для выбора параметров сортировки\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    main_frame = tk.Frame(tk.Toplevel(), padx=20, pady=20)
    c = tk.Label(main_frame, 
             text = 'Выберите поле, которому необходимо отсортировать записи')
    c.pack()
    sort_field = tk.StringVar(main_frame)
    sort_field.set('Title')
    sort_field_box = tk.OptionMenu(main_frame, sort_field,
                                        *settings.sort_options)
    sort_field_box.pack()
    reverse = tk.BooleanVar()
    checkbox = tk.Checkbutton(main_frame, 
              text='Изменить направление сортировки (сортировать по убыванию)', 
              variable = reverse)
    checkbox.pack()
    sort_btn = tk.Button(main_frame, text = 'Отсортировать', 
                         command = lambda: do_sort(sort_field, reverse),
                         **settings.button_options)
    sort_btn.pack()
    main_frame.pack()

def on_configure(event):
    """
    Обновляет регион скролла для объекта canvas\n
    Входные параметры:\n
        event – объект события, для которого был вызван данный обработчик
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

def update_canvas():
    """
    Обновляет содержимое таблицы с запиями БД\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global root, entries_table, db, canvas, scrollbar
    
    entries_table.pack_forget()
    entries_table.destroy()
    canvas.pack_forget()
    canvas.destroy()
    scrollbar.pack_forget()
    scrollbar.destroy()
    
    canvas = tk.Canvas(root, width=880, height=520)
    canvas.bind('<Configure>',on_configure)
    entries_table = create_table_from_entries(db, canvas)
    
    scrollbar = tk.Scrollbar(root,command=canvas.yview,orient="vertical")
    scrollbar.pack(side=tk.RIGHT,fill='y')
    canvas.create_window((0,0),window=entries_table,anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.update()
    
    canvas.pack()

def delete_entry(key):
    """
    Удаляет запись из БД\n
    Входные параметры:\n
        key – ключ записи, которую необходимо удалить\n
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    db_operations.db_delete(settings.DB_PATH, key)
    setup_db()
    update_canvas()

def reset_filters():
    """
    Сбрасывает текущие фильтры\n
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global db
    db = db_helper.dict_from_db_file(settings.DB_PATH)
    db = db_operations.db_sort_by_id(db, False)
    update_canvas()



def main_window():
    """
    Создает главное окно, таблицу с записями и кнопки управления, затем запускет главный цикл приложения
    Входные параметры:\n
        –
    Выходные параметры:\n
        –
    Автор: Калентьев А.А., Жеребцов Д.Д.
    """
    global entries_table, root, canvas, scrollbar
    root = tk.Tk()
    root.wm_title('Movie database')
    root.configure(background="#ffffff")  
    root.geometry("900x600")
    root.grid_propagate(0)
    
    canvas = tk.Canvas(root, width=880, height=520)    
    entries_table = create_table_from_entries(db, canvas)
    
    #Кнопки
    buttons_frame = tk.Frame(root, width = 200, pady=20, height=80)
    
    add_btn = tk.Button(buttons_frame, text = 'Добавить запись', 
                          command=add_entry_window, **settings.button_options)
    select_btn = tk.Button(buttons_frame, text = 'Фильтры', 
                           command = show_selection, **settings.button_options)
    sort_btn = tk.Button(buttons_frame, text = 'Сортировка', 
                         command = sort_window, **settings.button_options)
    reset_btn = tk.Button(buttons_frame, text = 'Сбросить фильтры',
                          command = reset_filters, **settings.button_options)
    stats_btn = tk.Button(buttons_frame, text = 'Статистика выборки',
                          command = show_stats, **settings.button_options)
    close_btn = tk.Button(buttons_frame, text = 'Выход', 
                          command=root.destroy, **settings.button_options)
    
    add_btn.grid(row=0,column=0)
    select_btn.grid(row=0,column=1)
    sort_btn.grid(row=0,column=2)
    reset_btn.grid(row=0,column=3)
    stats_btn.grid(row=0,column=4)
    close_btn.grid(row=0,column=5)
    buttons_frame.pack()
    
    scrollbar = tk.Scrollbar(root,command=canvas.yview,orient="vertical")
    scrollbar.pack(side=tk.RIGHT,fill='y')
    
    canvas.create_window((0,0),window=entries_table,anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>',on_configure)    
    canvas.pack()
    
    root.mainloop()