define('view/elements/ractive-helper', [
    'view/elements/map/help'
], function (ViewElementsMapHelp) {

    var mapHelp = new ViewElementsMapHelp();

    Ractive.defaults.data = {
        formatters: {
            fromIdToPlace: function (posId) {
                var pos = mapHelp.fromIdToPlace(parseInt(posId, 10));
                return pos.x + 'x' + pos.y;
            },

            transformNumberToPretty: function (num) {
                var i, pos,
                    newString = '';

                if(num === undefined) {
                    return '0';
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
                if(num === undefined) {
                    num = 0;
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
            }
        }
    };
});