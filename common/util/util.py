TRUE_VALUES = ['1', 'true', 'ok']


def bool_check(value: str):
    return value.lower() in TRUE_VALUES