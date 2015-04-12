define('view/elements/ractive-helper', [
    'service/standalone/map/canvas/help'
], function (ServiceStandaloneMapCanvasHelp) {

    var mapHelp = new ServiceStandaloneMapCanvasHelp();

    Ractive.defaults.data = {
        console: {
            log: function () {
                console.log(arguments);
            }
        },

        formatters: {
            fromIdToPlace: function (posId) {
                var pos = mapHelp.fromIdToPlace(parseInt(posId, 10));
                return pos.x + 'x' + pos.y;
            },

            transformNumberToPretty: function (num) {
                var i, pos,
                    newString = '';

                if(num === undefined || isNaN(num)) {
                    return '';
                }

                num = num.toString();

                switch(num.length % 3) {
                    case 0:
                        pos = 1;
                        break;
                    case 1:
                        pos = 3;
                        break;
                    case 2:
                        pos = 2;
                        break;
                }

                for(i = 0; i < num.length; i += 1) {
                    newString += num[i];

                    if(pos % 3 === 0) {
                        newString += ' ';
                    }

                    pos += 1;
                }

                return newString.trim();
            },

            transformNumberToView: function (num) {
                if(num === undefined || isNaN(num)) {
                    return '';
                }

                var number = num.toString(),
                    len = number.length,
                    mod = len % 3 === 0 ? 3 : len % 3,
                    joinArray = [];

                joinArray.length = Math.ceil(len / 3);

                if(num <= 99999) {
                    return Ractive.defaults.data.formatters.transformNumberToPretty(num);
                }

                return number.substr(0, mod) + ' ' + (joinArray.join('k'));
            },

            fromIntToTime: function (time) {
                if(time === undefined || isNaN(time)) {
                    return '';
                }

                var content = '';

                if(time / 3600 >= 1) {
                    content += parseInt(time / 3600, 10) + ' час. ';
                    time = time % 3600;
                }

                if(time / 60 >= 1) {
                    content += parseInt(time / 60, 10) + ' мин. ';
                    time = time % 60;
                }

                if(time > 0) {
                    content  += time + ' сек.';
                }

                return content;
            }
        }
    };
});