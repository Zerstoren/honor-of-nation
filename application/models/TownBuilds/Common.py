import models.Abstract.Common

BUILD_FIELD = 'field'                # Поля
BUILD_FARM = 'farm'                  # Фермы
BUILD_MILL = 'mill'                  # Мельницы
BUILD_MINE = 'mine'                  # Шахты
BUILD_ROAD = 'road'                  # Дороги
BUILD_STORAGE = 'storage'            # Хранилища
BUILD_V_COUNCIL = 'v_council'        # Сель. совет
BUILD_T_COUNCIL = 't_council'        # Гор. совет
BUILD_HEADQUARTERS = 'headquarters'  # Штаб
BUILD_GUILDHALL = 'guildhall'        # Ратуша
BUILD_HUT = 'hut'                    # Хибара
BUILD_HOUSE = 'house'                # Дом
BUILD_SMITHY = 'smithy'              # Кузня
BUILD_CASERN = 'casern'              # Казарма
BUILD_BARRACK = 'barrack'            # Бараки
BUILD_PRISON = 'prison'              # Тюрьма
BUILD_HIGH_WALL = 'high_wall'        # Высокие стены
BUILD_WALL = 'wall'                  # Стены


class Common_Set(models.Abstract.Common.Common_Set):
    pass


class Common_Filter(models.Abstract.Common.Common_Filter):
    pass


class Common_Limit(models.Abstract.Common.Common_Limit):
    pass


class Common_Order(models.Abstract.Common.Common_Order):
    pass
