#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helpers.security
import exceptions.args

def unitary(message, **params):
    """
    Функция производит фильтрацию данных message исходя из данных
    присланных в последующих аргументах

    В message передается словарь с данными
    В аргументах указывается ключ дейсвия и его значение

    Параметры обработки:
        type - тип даных, передается стандартная функция типа (int|str|list|dict|bool).
            Если тип данных не совпадет, то будет вызвано исключение

        enum - перечесление возможных вариантов для значения. Передается список возможных вариантов
            для этого элемента

        clean - тип очистки данных (none|soft|hard)
            soft - очищает возможный xss
            hard - оставляет только символы A-Za-z0-9\-_

        subType - Для словарей и списков. Тип данных в словарях и списках. Если он не совпадет, будет
            вызвано исключение

        subDict - Для словаря. Список данных, которые находятся в словаре. Каждый элемент списка будет
            отвечать одному ключу

        lambda - Функция пред-обработчик. Вызывается перед всеми действиями

        lambdaAft - Функция пост-обработчик. Вызывается после всех действий

    Функция вернет модифицированный message.

    :rtype: bool or message
    """

    itemType = params['type'] if 'type' in params else None
    cleanType = params['clean'] if 'clean' in params else False
    enum = params['enum'] if 'enum' in params else False
    lambdaPre = params['lambda'] if 'lambda' in params else False
    lambdaAft = params['lambdaAft'] if 'lambdaAft' in params else False
    subItemsType = params['subType'] if 'subType' in params else False
    subItemsDict = params['subDict'] if 'subDict' in params else False
    subLambda = params['subLambda'] if 'subLambda' in params else False

    if lambdaPre is not False:
        message = lambdaPre(message)

    if enum is not False:
        _enum_test(message, enum)

    if itemType is not None:
        if type(message) is not itemType:
            raise exceptions.args.WrongArgumentType('Argument has wrong type %s but need %s' % (type(message), itemType))

    if cleanType is not False:
        message = _clean(cleanType, message, 'base')

    if subItemsType is not False and itemType is list:
        _deep_list_test(subItemsType, message, subLambda)

    if subItemsType is not False and subItemsDict is not False and itemType is dict:
        _deep_dict_test(subItemsType, subItemsDict, message, subLambda)

    if lambdaAft is not False:
        message = lambdaAft(message)

    return message


def set(message, **params):
    """
    Функция производит фильтрацию параметров message исходя из данных
    присланных в последующих аргументах

    В message передается словарь с данными
    В следущих аргументах указывается ключ словаря и его параметры обработки

    Параметры обработки:
        type - тип даных, передается стандартная функция типа (int|str|list|dict|bool).
            Если тип данных не совпадет, то будет вызвано исключение

        enum - перечесление возможных вариантов для значения. Передается список возможных вариантов
            для этого элемента

        clean - тип очистки данных (none|soft|strong)
            soft - очищает возможный xss
            hard - оставляет только символы A-Za-z0-9\-_

        required - Строка required, является ли этот аргумент обязательным. Если оставить пустую строку,
            то на его место будет вставлено пустое значение, которое создаст тип данных

        subType - Для словарей и списков. Тип данных в словарях и списках. Если он не совпадет, будет
            вызвано исключение

        subDict - Для словаря. Список данных, которые находятся в словаре. Каждый элемент списка будет
            отвечать одному ключу

        lambda - Функция пред-обработчик. Вызывается перед всеми действиями

        lambdaAft - Функция пост-обработчик. Вызывается после всех действий

    Функция вернет модифицированный message.
    """

    if type(message) is not dict:
        raise exceptions.args.Arguments("Wrong message type, use `unitary` method")

    for param in params:
        itemType = params[param]['type'] if 'type' in params[param] else False
        enum = params[param]['enum'] if 'enum' in params[param] else False
        cleanType = params[param]['clean'] if 'clean' in params[param] else False
        isRequired = params[param]['required'] if 'required' in params[param] else True
        lambdaPre = params[param]['lambda'] if 'lambda' in params[param] else False
        lambdaAft = params[param]['lambdaAft'] if 'lambdaAft' in params[param] else False
        subItemsType = params[param]['subType'] if 'subType' in params[param] else False
        subItemsDict = params[param]['subDict'] if 'subDict' in params[param] else False
        subLambda = params[param]['subLambda'] if 'subLambda' in params[param] else False

        if enum is not False:
            _enum_test(message[param], enum)

        if lambdaPre is not False and param in message:
            message[param] = lambdaPre(message[param])

        if isRequired:
            if param not in message:
                raise exceptions.args.NotEnoughArguments('Argument %s not contain in message' % param)
        elif itemType is not False:
            if param not in message:
                message[param] = itemType()

        if itemType is not False:
            if type(message[param]) is not itemType:
                raise exceptions.args.WrongArgumentType('Argument %s has wrong type %s but need %s' %
                                        (param, type(message[param]), itemType))

        if cleanType is not False:
            message[param] = _clean(cleanType, message[param], param)

        if subItemsType is not False and itemType is list:
            _deep_list_test(subItemsType, message[param], subLambda)

        if subItemsType is not False and subItemsDict is not False and itemType is dict:
            _deep_dict_test(subItemsType, subItemsDict, message[param], subLambda)

        if lambdaAft is not False:
            message[param] = lambdaAft(message[param])

    helpers.security.deleteOtherKeys(message, params.keys())
    return message


def _clean(cleanParam, message, param):
    if cleanParam == 'soft':
        return helpers.security.deepMapClean(helpers.security.xssClean, message)
    elif cleanParam == 'strong':
        return helpers.security.deepMapClean(helpers.security.ssString, message)
    else:
        raise exceptions.args.WrongCleanType('Wrong clean type for parametr %s' % param)


def _deep_list_test(itemsType, message, lambdaF=False):
    if itemsType is list or itemsType is dict:
        raise exceptions.args.DeepArgumentsError('Don`t use very deep arguments')

    for i in range(len(message)):
        if lambdaF is not False:
            message[i] = lambdaF(message[i])

        if type(message[i]) is not itemsType:
            raise exceptions.args.WrongArgumentType("Deep list argument has wrong type")


def _deep_dict_test(itemsType, subItems, message, lambdaF=False):
    if itemsType is dict or itemsType is list:
        raise exceptions.args.DeepArgumentsError('Don`t use very deep arguments')

    for item in subItems:
        if item not in message:
            raise exceptions.args.NotEnoughArguments("Deep dict don`t have argument %s" % item)

        if lambdaF is not False:
            message[item] = lambdaF(message[item])

        if type(message[item]) is not itemsType:
            raise exceptions.args.WrongArgumentType("Deep dict argument has wrong type")


def _enum_test(message, enum):
    if message not in enum:
        raise exceptions.args.EnumError('%s not in enum list' % message)
