import system.mongo

class _RefErrorLocalException(Exception):
    def __init__(self, collection, field):
        self.collection = collection
        self.field = field
        super().__init__()

class RefError(Exception):
    pass


class TypeValueError(Exception):
    pass


class NotExistsTypeKey(Exception):
    pass


class MissingItemsData(Exception):
    pass


class RedundantItemsData(Exception):
    pass


class CheckDatabaseIndexes():
    def __init__(self, config):
        self._db = system.mongo.mongo

        for conf in config:
            if conf == 'DEFAULT':
                continue

            self.parseField(conf, dict(config[conf]))

    def parseField(self, collectionName, conf):
        parsedConf = self.parseConfig(conf)
        result = self._db[collectionName].find()

        for i in result:
            self.checkData(collectionName, i, parsedConf)


    def checkData(self, collectionName, item, configParse):
        configKeys = list(configParse.keys())
        itemKeys = list(item.keys())

        for i in configParse:
            result = False
            try:

                if i.find('.') != -1:
                    inc = i.split('.')
                    value = eval('item["' + '"]["'.join(inc) + '"]')
                    configKeys.remove(i)
                else:
                    value = item[i]

                result = configParse[i][0](value)
            except KeyError:
                if configParse[i][1].find('empty') != -1:
                    configKeys.remove(i)
                continue

            if result is False and configParse[i][1].find('empty') == -1:
                raise TypeValueError("Field `%s` in collection `%s` has wrong type" % (i, collectionName))
            elif configParse[i][1].find('empty') != -1:
                configKeys.remove(i)

        itemKeys.remove('_id')

        if len(list(set(itemKeys) - set(configKeys))):
            raise RedundantItemsData('Redundant fields `%s` in collection %s' % (
                "`, `".join(list(set(itemKeys) - set(configKeys))),
                collectionName
            ))

        if len(list(set(configKeys) - set(itemKeys))):
            raise MissingItemsData('Missing fields `%s` in collection %s' % (
                "`, `".join(list(set(configKeys) - set(itemKeys))),
                collectionName
            ))

    def parseConfig(self, conf):
        resultFn = {}
        for i in conf:
            if i.find('_index_') != -1:
                continue

            resultFn[i] = self.getParseConfigElement(conf[i])

        return resultFn

    def getParseConfigElement(self, info):
        def started(value):
            return None

        def intParse(fn):
            return lambda value: fn(value) or type(value) is int

        def strParse(fn):
            return lambda value: fn(value) or type(value) is str

        def floatParse(fn):
            return lambda value: fn(value) or type(value) is float

        def listParse(fn):
            return lambda value: fn(value) or type(value) is list

        def dictParse(fn):
            return lambda value: fn(value) or type(value) is dict

        def boolParse(fn):
            return lambda value: fn(value) or type(value) is bool

        def objectIDParse(fn):
            return lambda value: fn(value) or isinstance(value, system.mongo.types.ObjectId)

        def noneParse(fn):
            return lambda value: fn(value)

        def refParse(fn, ref):
            collection, field = ref.split('->')
            def v(value):
                search = {}
                search[field] = value
                result = system.mongo.mongo[collection].find(search).count()

                if result == 0:
                    raise _RefErrorLocalException(collection, field)

                return fn(value)
            return v

        fn = started
        for i in info.split('|'):
            if i.find('ref') == -1 and i != 'empty':
                try:
                    fn = locals()[i + 'Parse'](fn)
                except KeyError as e:
                    raise NotExistsTypeKey('Checker not have type `%s`' % str(i))
            elif i.find('ref') != -1:
                fn = refParse(fn, i.split(' ')[1])

        return (fn, info)
