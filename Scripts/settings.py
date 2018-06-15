DB_PATH = 'data/main.shl'

field_types = {'Title':'string','Genre':'string',
               'Director':'string','Country':'string',
               'Budget, $ million':'float',
               'Year':'int'}

string_operations = {'Полное совпадение' : '=',
                         'Вхождение подстроки' : 'contains'}

number_operations = {'=' : '=',
                     '>=' : '>=',
                     '<=' : '<=',
                     '!=' : '!=',
                     '>' : '>',
                     '<' : '<'}

sort_options = {'ID' : 'ID', 'Title' : 'Title', 'Genre' : 'Genre', 
                'Director' : 'Director', 'Country' : 'Country', 
                'Budget' : 'Budget, $ million',
                'Year' : 'Year'}

button_options = {'width':16,'height':2}