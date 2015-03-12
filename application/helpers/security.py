"""
Набор методов для фильтрации данных и обезопасивания онных
"""
import re

S_S_STRING = re.compile(r'[^a-zA-Z0-9_-]', re.M + re.I)

XSS_SAVE_STRING = re.compile(r'(<script>.*</.*>|<script>|&#x[0-9]+;|javascript\s*:|expression\s*(\(|&\#40;)|<!--|-->|<!\[CDATA\[.*\]\]>|Redirect\s+302|\%[A-F0-9]{2})', re.M + re.I)


def ssString(chars):
    """
    Производит фильрацию всех спец символов, оставляе только стандартный набор
    латинских буква a-zA-Z, цифры 0-9 и _ -
    """
    return re.sub(globals()['S_S_STRING'], '', chars)


def xssClean(chars):
    return re.sub(globals()['XSS_SAVE_STRING'], '', chars)


def deepMapClean(fnClean, item):
    itemType = type(item)

    if itemType == str:
        return fnClean(item)
    elif itemType == int:
        return fnClean(item)
    elif itemType == dict:
        for x in item:
            item[x] = deepMapClean(fnClean, item[x])

        return item
    elif itemType == list:
        for i in range(len(item)):
            item[i] = deepMapClean(fnClean, item[i])

    else:
        raise TypeError("Type %s not supported for deepMapClean", itemType)


def deleteOtherKeys(obj, insKeys):
    if type(obj) != dict:
        return False

    forDel = [i for i in obj if i not in insKeys]

    for x in forDel:
        del obj[x]

    return obj
