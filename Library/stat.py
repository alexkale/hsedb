def sample_variance(items):
    """
    Вычисляет выборочную дисперсию списка величин\n
    Входные параметры:
        items – список с величинами, для которых необходимо вычислить дисперсию
    Выходные параметры:
        sv – вычисленная дисперсия
    Автор: Калентьев А.А.
    """
    mean = sum(items)/len(items)
    sq_deviations = [(x-mean)*(x-mean) for x in items]
    sv = sum(sq_deviations)/len(sq_deviations)
    return sv