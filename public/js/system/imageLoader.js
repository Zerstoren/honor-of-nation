define('system/imageLoader', [], function () {
    var imagesConfig, preloader, imager;
    imagesConfig = {
        'shadow': 'ground/shadow.png',

        // ground
        'ground-1-1': 'ground/1-1.png',
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
        'rubins': 'build/rubins.png',
        'steel': 'build/steel.png',
        'stone': 'build/stone.png',
        'wood': 'build/wood.png'
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