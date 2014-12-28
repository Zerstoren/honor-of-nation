define('view/town/builds', [
    'view/elements/popup',

    'service/standalone/math',

    'system/config',
    'system/interval'
], function (
    ViewElementsPopup,

    serviceStandaloneMath,

    config,
    interval
) {
    var builds, buildsView;

    buildsView = AbstractView.extend({
        events: {
            'click .build_container .btn': 'onCreate',
            'click .buildInProgress .cancel': 'onCancelBuild',
            'click .triangle .cancel': 'onCancelBuild'
        },

        initialize: function () {
            this.template = this.getTemplate('town/builds/builds');
            this.setPartials({
                'buildItem': 'town/builds/buildItem',
                'buildProgress': 'town/builds/buildsInProgress'
            });

            this.initRactive();
            interval.on(interval.EVERY_1_SEC, this.updateQueue, this);
        },

        render: function (holder, currentTown) {
            this.currentTown = currentTown;
            holder.append(this.$el);

            this.popupBuilds = new ViewElementsPopup(
                this.$el, {
                    liveTarget: '.build_container',
                    timeout: 100
                }
            );

            this.popupQueue = new ViewElementsPopup(
                this.$el, {
                    timeout: 100,
                    liveTarget: '.triangle',
                    ignoreTop: true
                }
            );

            this.currentTown.on('change:builds', this.updateBuilds, this);
            this.currentTown.on('change:queue', this.onQueueUpdate, this);
        },

        update: function (buildsList, queue) {
            this.currentTown.set({
                builds: buildsList,
                queue: queue
            });
        },

        updateBuilds: function () {
            var key,
                buildsList = this.currentTown.get('builds'),
                result = [];

            for (key in buildsList) {
                if (buildsList.hasOwnProperty(key)) {
                    result.push({
                        'key': key,
                        'name': builds[key].name,
                        'price': serviceStandaloneMath.getBuildPrice(builds[key].price, this._getMaximumLevel(key)),
                        'desc': builds[key].desc,
                        'maxLevel': builds[key].maxLevel[this.currentTown.get('type')],
                        'level': buildsList[key],
                        'levelWithQueue': this._getMaximumLevel(key)
                    });
                }
            }

            this.set('builds', result);
        },

        updateQueue: function () {
            if (!this.currentTown) {
                return;
            }

            var key,
                i = 0,
                item,
                tmp,
                buildsQueue = this.currentTown.get('queue'),
                result = [],
                firstSection = {};

            for (key in buildsQueue) {
                if (buildsQueue.hasOwnProperty(key)) {
                    item = buildsQueue[key];

                    tmp = {
                        name: builds[item.key].name,
                        key: item.key,
                        level: item.level,
                        timeToCreate: item.complete_after
                    };

                    if (i === 0) {
                        tmp.timeToComplete = item.complete_after - (config.getTime() - item.start_at);
                        tmp.percentComplete = 100 - parseInt(((config.getTime() - item.start_at) / item.complete_after) * 100, 10);

                        firstSection = tmp;
                    } else {
                        result.push(tmp);
                    }

                    i += 1;
                }
            }

            if (_.isEmpty(firstSection)) {
                firstSection = false;
            }

            result.reverse();

            this.set('firstSection', firstSection);
            this.set('queue', result);
        },

        onCreate: function (e) {
            this.trigger(
                'createBuild',
                jQuery(e.target).parents('.build_container').attr('id')
            );
            return false;
        },

        onCancelBuild: function (e) {
            this.trigger(
                'cancelBuild',
                jQuery(e.target).attr('data-key'),
                parseInt(jQuery(e.target).attr('data-level'), 10)
            );
        },

        onQueueUpdate: function () {
            this.updateQueue();
            this.updateBuilds();
        },

        _getMaximumLevel: function (key) {
            var i,
                itemQueue,
                currentLevel = this.currentTown.get('builds')[key],
                queue = this.currentTown.get('queue');

            for (i = 0; i < queue.length; i++) {
                itemQueue = queue[i];

                if (itemQueue.key === key) {
                    currentLevel = itemQueue.level;
                }
            }

            return currentLevel;
        }
    });

    builds = {
        "mill": {
            "price": {
                "wood": 1500,
                "rubins": 3000,
                "stone": 3000,
                "steel": 0,
                "time": 40
            },
            "maxLevel": {
                0: 10,
                1: 50,
                2: 0
            },
            "name": "Мельница",
            "desc": [{
                "name": "Повышает прирост еды на 0.5%",
                "detail": "Чем более качественные перерабатывающие установки, тем меньшее количество брака конечной продукции."
            }],
            "bonus": {
                "eat": 0.5
            }
        },
        "field": {
            "price": {
                "wood": 1000,
                "rubins": 7500,
                "stone": 0,
                "steel": 0,
                "time": 32
            },
            "maxLevel": {
                0: 20,
                1: 50,
                2: 0
            },
            "name": "Поля",
            "desc": [{
                "name": "Повышает прирост еды на +0.5%",
                "detail": "Чем более поля защищены от зверей и лучше обрабатываются, тем выше прирост злаков с них"
            }],
            "bonus": {
                "eat": 0.5
            }
        },
        "farm": {
            "price": {
                "wood": 1400,
                "rubins": 800,
                "stone": 50,
                "steel": 0,
                "time": 45
            },
            "maxLevel": {
                0: 20,
                1: 50,
                2: 20
            },
            "name": "Ферма",
            "desc": [{
                "name": "Повышает прирост еды на 1%",
                "detail": "Домашнее хозяйство отличный источник мясных продуктов для нашего государства"
            }],
            "bonus": {
                "eat": 1
            }
        },
        "mine": {
            "price": {
                "wood": 6000,
                "rubins": 12000,
                "stone": 1500,
                "steel": 3000,
                "time": 61
            },
            "maxLevel": {
                0: 10,
                1: 50,
                2: 0
            },
            "name": "Шахты",
            "desc": [{
                "name": "Повышает прирост ископаемых на 2%",
                "detail": "Расширение и модернизация шахт и карьеров позволяет более ефективно добывать ресурсы"
            }],
            "bonus": {
                "minerals": 2
            }
        },
        "road": {
            "price": {
                "wood": 1500,
                "rubins": 1000,
                "stone": 0,
                "steel": 0,
                "time": 18
            },
            "maxLevel": {
                0: 5,
                1: 40,
                2: 10
            },
            "name": "Дороги",
            "desc": [{
                "name": "Повышает прирост ископаемых на 0.125%",
                "detail": "Более быстрая доставка ресурсов позволяет тратить меньше сил кресьян"
            },
            {
                "name": "Повышает прирост еды на 0.125%",
                "detail": "Чем быстрее продукт будет доставлен в хранилище, тем меньше шансов что он испортится"
            }],
            "bonus": {
                "eat": 0.125,
                "minerals": 0.125
            }
        },
        "storage": {
            "price": {
                "wood": 30000,
                "rubins": 40000,
                "stone": 25000,
                "steel": 2250,
                "time": 520
            },
            "maxLevel": {
                0: 0,
                1: 20,
                2: 0
            },
            "name": "Хранилище",
            "desc": [{
                "name": "Повышает прирост еды на 0.5%",
                "detail": "Долгое хранение мяса и зерновых позволяет уменьшить количество не качественной пищи"
            }],
            "bonus": {
                "eat": 0.5
            }
        },
        "v_council": {
            "price": {
                "wood": 30000,
                "rubins": 12000,
                "stone": 1000,
                "steel": 0,
                "time": 520
            },
            "maxLevel": {
                0: 12,
                1: 0,
                2: 0
            },
            "name": "Сель. Совет",
            "desc": [{
                "name": "Повышает налог на 0.05 рубина с человека",
                "detail": "Налоговая система позволяет организовать сбор дани с своих подчиненных"
            },
            {
                "name": "Повышает скорость постройки зданий 2%",
                "detail": "Управляющие бригадиры при дворе ускоряют постройку зданий"
            },
            {
                "name": "Повышает шанс подавление бунта 2%",
                "detail": "Стражники в деревене могут выследить и казнить зачинщика бунта в городе"
            }],
            "bonus": {
                "tax": 0.05,
                "builds_speed": 2,
                "riot": 2
            }
        },
        "t_council": {
            "price": {
                "wood": 4000,
                "rubins": 15000,
                "stone": 14000,
                "steel": 1500,
                "time": 0
            },
            "maxLevel": {
                0: 0,
                1: 35,
                2: 0
            },
            "name": "Гор. Совет",
            "desc": [{
                "name": "Повышение налогов 0.05 рубина с человека",
                "detail": "Налоговая система позволяет организовать сбор дани с своих подчиненных"
            },
            {
                "name": "Повышает скорость постройки зданий 1%",
                "detail": "Управляющие бригадиры при дворе ускоряют постройку зданий"
            },
            {
                "name": "Повышает шанс подавление бунта 1%",
                "detail": "Стражники в городе могут выследить и казнить зачинщика бунта в городе"
            }],
            "bonus": {
                "tax": 0.05,
                "builds_speed": 1,
                "riot": 1
            }
        },
        "headquarters": {
            "price": {
                "wood": 15000,
                "rubins": 100000,
                "stone": 240000,
                "steel": 30000,
                "time": 844
            },
            "maxLevel": {
                0: 0,
                1: 0,
                2: 20
            },
            "name": "Штаб",
            "desc": [{
                "name": "Повышает скорость постройки зданий 2%",
                "detail": "Управляющие бригадиры при дворе ускоряют постройку зданий"
            },
            {
                "name": "Повышает скорость обучения солдат 1%",
                "detail": "Стражники в замке могут выследить и казнить зачинщика бунта в городе"
            },
            {
                "name": "Повышает шанс подавление бунта на 4%",
                "detail": "Стражники в деревене могут выследить и казнить зачинщика бунта в городе"
            }],
            "bonus": {
                "builds_speed": 2,
                "soliders_speed": 1,
                "riot": 4
            }
        },
        "guildhall": {
            "price": {
                "wood": 100000,
                "rubins": 150000,
                "stone": 10000,
                "steel": 30000,
                "time": 2900
            },
            "maxLevel": {
                0: 0,
                1: 10,
                2: 0
            },
            "name": "Ратуша",
            "desc": [{
                "name": "Повышение налогов 0.2 рубина с человека",
                "detail": "Создание комисии казначеев позволяет начинать эффективный сбор налогов с жителей"
            }],
            "bonus": {
                "tax": 0.2
            }
        },
        "hut": {
            "price": {
                "wood": 800,
                "rubins": 2000,
                "stone": 0,
                "steel": 0,
                "time": 35
            },
            "maxLevel": {
                0: 20,
                1: 0,
                2: 0
            },
            "name": "Хибара",
            "desc": [{
                "name": "Увеличивает приток селчан на 4 человека",
                "detail": "Если есть где жить, то там должен кто-то жить. Чем больше людей, тем лучше для поселка"
            }, {
                "name": "Вместительность города повышается на 200 человек",
                "detail": "К нам не приедут жить, если над головой гостей будет небо со звездами"
            }],
            "bonus": {
                "villagers": 4,
                "max_villagers": 200
            }
        },
        "house": {
            "price": {
                "wood": 1200,
                "rubins": 3000,
                "stone": 1000,
                "steel": 0,
                "time": 15
            },
            "maxLevel": {
                0: 0,
                1: 50,
                2: 0
            },
            "name": "Дом",
            "desc": [{
                "name": "Увеличивает приток селчан на 6 человека",
                "detail": "Если есть где жить, то там должен кто-то жить. Чем больше людей, тем лучше для города"
            }, {
                "name": "Вместительность города повышается на 2000 человек",
                "detail": "К нам не приедут жить, если над головой гостей будет небо со звездами"
            }],
            "bonus": {
                "villagers": 6,
                "max_villagers": 2000
            }
        },
        "barrack": {
            "price": {
                "wood": 1200,
                "rubins": 32000,
                "stone": 30000,
                "steel": 5000,
                "time": 360
            },
            "maxLevel": {
                0: 0,
                1: 0,
                2: 25
            },
            "name": "Бараки",
            "desc": [{
                "name": "Увеличивает приток селчан на 4 человека",
                "detail": "Если есть где жить, то там должен кто-то жить. Чем больше людей, тем лучше для поселка"
            }, {
                "name": "Вместительность города повышается на 400 человек",
                "detail": "К нам не приедут жить, если над головой гостей будет небо со звездами"
            }],
            "bonus": {
                "villagers": 4,
                "max_villagers": 400
            }
        },
        "smithy": {
            "price": {
                "wood": 800,
                "rubins": 5000,
                "stone": 4000,
                "steel": 3000,
                "time": 85
            },
            "maxLevel": {
                0: 0,
                1: 40,
                2: 40
            },
            "name": "Кузница",
            "desc": [{
                "name": "Скорость создания доспеха и оружия повышается на 1%",
                "detail": "Чем более комфортные условия для кузнецов, тем выше их эффективность"
            }, {
                "name": "Цена доспеха и оружия снижается на 0.5%",
                "detail": "Хорошие кузнецы могут творить чудеса с металлом, а в простой работе еще его и экономить"
            }],
            "bonus": {
                "armory_speed": 1,
                "armory_price": -0.5
            }
        },
        "casern": {
            "price": {
                "wood": 8000,
                "rubins": 35000,
                "stone": 20000,
                "steel": 15000,
                "time": 500
            },
            "maxLevel": {
                0: 0,
                1: 20,
                2: 30
            },
            "name": "Казармы",
            "desc": [{
                "name": "Повышает скорость обучения солдат на 1%",
                "detail": "Хорошие командиры, залог успеха в подготовке хорошого бойца"
            }],
            "bonus": {
                "soliders_speed": 1
            }
        },
        "prison": {
            "price": {
                "wood": 1500,
                "rubins": 100000,
                "stone": 50000,
                "steel": 20000,
                "time": 4000
            },
            "maxLevel": {
                0: 0,
                1: 10,
                2: 0
            },
            "name": "Тюрьмы",
            "desc": [{
                "name": "Повышает шанс подавление бунта на 5%",
                "detail": "Хоть и строго, но справедливо. Предатель должен быть наказан"
            }],
            "bonus": {
                "riot": 5
            }
        },
        "wall": {
            "price": {
                "wood": 100,
                "rubins": 20000,
                "stone": 30000,
                "steel": 15000,
                "time": 665
            },
            "maxLevel": {
                0: 0,
                1: 15,
                2: 0
            },
            "name": "Стены",
            "desc": [{
                "name": "Повышает защиты солдат в битве на 1%",
                "detail": "Чем прочнее наши стены, тем меньше солдат умрет в битве"
            }, {
                "name": "Время штурма стен повышается на 2 шага",
                "detail": "Чем выше наши стены, тем больше времени будет нашим лучникам"
            }],
            "bonus": {
                "city_defence": 1,
                "city_steps": 2
            }
        },
        "high_wall": {
            "price": {
                "wood": 10000,
                "rubins": 70000,
                "stone": 75000,
                "steel": 15000,
                "time": 690
            },
            "maxLevel": {
                0: 0,
                1: 0,
                2: 20
            },
            "name": "Высокие стены",
            "desc": [{
                "name": "Повышает защиты солдат в битве на 2%",
                "detail": "Чем прочнее наши стены, тем меньше солдат умрет в битве"
            }, {
                "name": "Время штурма стен повышается на 4 шага",
                "detail": "Чем выше наши стены, тем больше времени будет нашим лучникам"
            }],
            "bonus": {
                "city_defence": 2,
                "city_steps": 4
            }
        }
    };

    return buildsView;
});