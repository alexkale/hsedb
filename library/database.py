#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 19:27:26 2018

@author: AlexKale
"""

import builtins
import operator

class DataBase:
    """
    Класс, описывающий базу данных
    Автор: Калентьев А. А.\n
    """

    def __init__(self, filename, delimiter, scheme_file):
        """
        Конструктор\n
        Параметры:
        \tfilename – имя файла, содержащего записи БД\n
        \tdelimiter – разделитель полей записи, используемый в файле БД\n
        \tschemeFile – имя файла, содержащего схему базы данных
        Автор: Калентьев А. А.\n
        """
        self.data = []
        self.scheme = {}
        self.database_file = filename
        self.scheme_file = scheme_file
        self.delim = delimiter
        self.read_scheme()
        self.read_file()
        self.ops = {'<' : operator.lt, '<=' : operator.le, '=' : operator.eq,
                    '>' : operator.gt, '>=' : operator.ge, '!' : operator.not_}
        print('Создан объект базы данных')

    def write_file(self):
        """
        Записывает содержимое БД в файл
        Автор: Калентьев А. А.\n
        """
        try:
            with open(self.database_file, 'w') as db_file:
                for entry in self.data:
                    db_file.write('{0}\n'.format(self.delim.join([str(x) for x in entry])))
        except Exception as exc:
            print('Ошибка записи в файл: {0}'.format(exc))

    def read_scheme(self):
        """
        Читает схему БД и загружает ее в память\n
        Автор: Калентьев А. А.\n
        """
        try:
            with open(self.scheme_file) as sc_file:
                for field in sc_file:
                    #Формат файла схемы БД:
                    #Имя поля,Тип поля,Индекс поля
                    field_info = field[:-1].split(',')
                    self.scheme[field_info[0]] = {'index' : int(field_info[2]),
                                                  'type'  : field_info[1]}
        except Exception as exc:
            print('Ошибка чтения файла схемы базы данных: {0}'.format(exc))

    def read_file(self):
        """
        Загружает базу данных из файла в память\n
        Автор: Калентьев А. А.\n
        """
        self.data = []
        try:
            with open(self.database_file, 'r') as db_file:
                for entry in db_file:
                    self.data.append(entry[:-1].split(self.delim))
        except Exception as exc:
            print('Ошибка чтения файла базы данных: {0}'.format(exc))

    def print_scheme(self):
        """
        Печатает в консоль описание схемы БД\n
        Автор: Калентьев А. А.\n
        """
        print('Схема <{0}>'.format(self.scheme_file))
        print('Всего полей: {0}'.format(len(self.scheme)))
        for key, field in self.scheme.items():
            print('Поле {0}:\n\tтип – {1}\n\tиндекс – {2}'.format(key,
                                                                  field['type'],
                                                                  field['index']))

    def print_entry(self, id_):
        """
        Выводит отдельную запись в консоль
        """
        pass

    def print_entries(self):
        """
        Печатает в консоль все записи БД\n
        Автор: Калентьев А. А.
        """
        print('Записи в БД:')
        for index, entry in enumerate(self.data):
            print('{0}: {1}'.format(index, ' '.join([str(x) for x in entry])))

    def add_entry(self, data):
        """
        Добавляет запись в базу данных\n
        Параметры:
        \tdata – список с данными новой записи\n
        Автор: Калентьев А. А.\n
        """
        #TO-DO: обработка ошибок и проверка данных
        self.data.append(data)

    def add_with_prompt(self):
        """
        Интерактивное добавление записи (ввод данных через консоль)\n
        Автор: Калентьев А. А.\n
        """
        print('Добавление записи:')
        new_entry = []
        for key, field in self.scheme.items():
            while True:
                inp = input('{0} (тип {1}): '.format(key, field['type']))
                try:
                    val = getattr(builtins, field['type'])(inp)
                except ValueError:
                    print('Неверный тип данных')
                else:
                    new_entry.append(val)
                    break
        print('Запись к добавлению: ')
        print(new_entry)
        self.data.append(new_entry)

    def delete_entry(self, id_):
        """
        Удаляет запись из базы данных\n
        Параметры:
        \tid - ID записи для удаления\n
        Возвращает:
        \t0 при успешном удалении, -1 если запись с указанным ID не существует
        Автор: Калентьев А. А.
        """
        if id_ < len(self.data):
            del self.data[id_]
            return 0
        return -1

    def select(self, field, operator, value):
        """
        Возвращает список записей, удовлетворяющих условию
        Автор: Калентьев А. А.
        """
        idx = self.scheme[field]['index']
        return [x for x in self.data if self.ops[operator](x[idx], value)]

