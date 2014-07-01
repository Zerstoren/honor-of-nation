(function () {
    "use strict";

    function transformNumberToPretty(num) {
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
    }

    Handlebars.registerHelper('transformNumberToPretty', function (num) {
        return transformNumberToPretty(num);
    });

    Handlebars.registerHelper('transformNumberToView', function (num) {
        if(num === undefined) {
            num = 0;
        }

        var number = num.toString(),
            len = number.length,
            mod = len % 3 === 0 ? 3 : len % 3,
            joinArray = [];

        joinArray.length = Math.ceil(len / 3);

        if(num <= 99999) {
            return transformNumberToPretty(num);
        }

        return number.substr(0, mod) + ' ' + (joinArray.join('k'));
    });


    Handlebars.JavaScriptCompiler.prototype.nameLookup = function(parent, name, type) {
        var result = '(' + parent + ' instanceof Backbone.Model ? ' + parent + '.get("' + name + '") : ' + parent;
        if (/^[0-9]+$/.test(name)) {
            return result + "[" + name + "])";
        } else if (Handlebars.JavaScriptCompiler.isValidJavaScriptVariableName(name)) {
            return result + "." + name + ')';
        } else {
            return result + "['" + name + "'])";
        }
    };
});
