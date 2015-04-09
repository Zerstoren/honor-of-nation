define('system/imageLoader', [], function () {
    var imagesConfig, preloader, imager;
    imagesConfig = {
        // ground
        'ground-2-1': 'ground/2-1.png'
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
            this.trigger('progress', preloader)
        }
    }));

    preloader.events.add('ready', imager.triggerReady.bind(imager));
    preloader.events.add('progress', imager.triggerProgress.bind(imager));

    return imager;
});