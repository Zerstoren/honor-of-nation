define('system/imageLoader', [], function () {
    var imagesConfig, preloader, imager;
    imagesConfig = {
        'shadow': 'ground/shadow.png',

        'ground-debug': 'ground/debug.png',
        'cursor'      : 'ground/cursor.png',

        // ground
        'ground-1-1': 'ground/1-1.png',
        'ground-1-2': 'ground/1-2.png',
        'ground-1-3': 'ground/1-3.png',
        'ground-1-4': 'ground/1-4.png',
        'ground-1-5': 'ground/1-5.png',
        'ground-1-6': 'ground/1-6.png',
        'ground-1-7': 'ground/1-7.png',

        'ground-2-1': 'ground/2-1.png',

        // decor
        'decor-0': 'decor/decor-0.png',
        'decor-1': 'decor/decor-1.png',
        'decor-2': 'decor/decor-2.png',

        // builds
        'city-castle': 'build/castle.png',
        'city-town': 'build/town.png',
        'city-village': 'build/village.png',

        // resources
        'resource-rubins': 'build/rubins.png',
        'resource-steel': 'build/steel.png',
        'resource-stone': 'build/stone.png',
        'resource-wood': 'build/wood.png',

        // units
        'commander': 'units/commander.png',
        'unit-marker-move': 'units/marker.png',
        'unit-attack': 'units/attack.png',

        'move-top':          'units/path.png [0:0:64:64]',
        'move-top-right':    'units/path.png [0:64:64:64]',
        'move-right':        'units/path.png [0:128:64:64]',
        'move-bottom-right': 'units/path.png [0:192:64:64]',
        'move-bottom':       'units/path.png [0:256:64:64]',
        'move-bottom-left':  'units/path.png [0:320:64:64]',
        'move-left':         'units/path.png [0:384:64:64]',
        'move-top-left':     'units/path.png [0:448:64:64]',
        'move-center':       'units/path.png [0:512:64:64]'

    };

    preloader = new atom.ImagePreloader({
        prefix: '/img/canvas/',
        images: imagesConfig
    });

    imager = new (AbstractService.extend({
        isReady: false,
        get: preloader.get.bind(preloader),
        exists: preloader.exists.bind(preloader),

        triggerReady: function () {
            this.trigger('ready');
            this.isReady = true;
        },

        triggerProgress: function () {
            this.trigger('progress', preloader.progress);
        }
    }));

    preloader.events.add('ready', imager.triggerReady.bind(imager));
    preloader.events.add('progress', imager.triggerProgress.bind(imager));

    return imager;
});