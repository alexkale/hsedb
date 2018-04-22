#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 11:31:12 2018

@author: AlexKale
"""

import library.database as database

#убрать, читать имена файлов из консоли
DB_PATH = 'data/database_films'
SCHEME_PATH = 'data/scheme.txt'

#global to-do: разобраться с конвертацией в нужные типы данных после чтения файла

def main():
    """
    Точка входа
    """
    print('Make DBs great again v0.1 ready')
    base = database.DataBase(DB_PATH, ';', SCHEME_PATH)
    base.print_entries()

if __name__ == '__main__':
    main()

