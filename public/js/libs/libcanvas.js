
/*
---

name: "AtomJS"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

inspiration:
    - "[JQuery](http://jquery.com)"
    - "[MooTools](http://mootools.net)"

...
*/

(function (Object, Array, undefined) { // AtomJS
// Safari 5 bug:
// 'use strict';

var
    toString  = Object.prototype.toString,
    hasOwn    = Object.prototype.hasOwnProperty,
    slice     = Array .prototype.slice,
    atom = this.atom = function () {
        if (atom.initialize) return atom.initialize.apply(this, arguments);
    };

atom.global = this;

/*
---

name: "JavaScript 1.8.5"

description: "JavaScript 1.8.5 Compatiblity."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

inspiration:
  - "[JQuery](http://jquery.com)"
  - "[MooTools](http://mootools.net)"

provides: js185

...
*/

// https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Function/bind
if (!Function.prototype.bind) {
    Function.prototype.bind = function(context /*, arg1, arg2... */) {
        if (typeof this !== "function") throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");

        var args   = slice.call(arguments, 1),
            toBind = this,
            Nop    = function () {},
            Bound  = function () {
                var isInstance;
                // Opera & Safari bug fixed. I must fix it in right way
                // TypeError: Second argument to 'instanceof' does not implement [[HasInstance]]
                try {
                    isInstance = this instanceof Nop;
                } catch (ignored) {
                    // console.log( 'bind error', Nop.prototype );
                    isInstance = false;
                }
                return toBind.apply(
                    isInstance ? this : ( context || {} ),
                    args.concat( slice.call(arguments) )
                );
            };
        Nop.prototype   = toBind.prototype;
        Bound.prototype = new Nop();
        return Bound;
    };
}

// https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Object/keys
if (!Object.keys) (function (has) {

    Object.keys = function(obj) {
        if (obj !== Object(obj)) throw new TypeError('Object.keys called on non-object');

        var keys = [], i;
        for (i in obj) if (has.call(obj, i)) keys.push(i);
        return keys;
    };
})({}.hasOwnProperty);

// https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Array/isArray
if (!Array.isArray) {
    Array.isArray = function(o) {
        return o && toString.call(o) === '[object Array]';
    };
}

// https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Object/create
if (!Object.create) {
    Object.create = function (o) {
        if (arguments.length > 1) {
            throw new Error('Object.create implementation only accepts the first parameter.');
        }
        function F() {}
        F.prototype = o;
        return new F();
    };
}

if (!String.prototype.trim) {
    String.prototype.trim = function () {
        return this.replace(/^\s+|\s+$/g, '');
    }
}

if (!String.prototype.trimLeft) {
    String.prototype.trimLeft = function () {
        return this.replace(/^\s+/, '');
    }
}

if (!String.prototype.trimRight) {
    String.prototype.trimRight = function () {
        return this.replace(/\s+$/g, '');
    }
}

/*
---

name: "Core"

description: "The core of AtomJS."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

inspiration:
  - "[JQuery](http://jquery.com)"
  - "[MooTools](http://mootools.net)"

provides: Core

requires:
    - js185

...
*/

function coreIsFunction (item) {
    return item && toString.call(item) == '[object Function]';
}

function coreObjectize (properties, value) {
    if (typeof properties != 'object') {
        var key = properties;
        properties = {};
        if (key != null) {
            properties[key] = value;
        }
    }
    return properties;
}

function coreContains (array, element) {
    return array.indexOf(element) >= 0;
}

function includeUnique(array, element) {
    if (!coreContains(array, element)) {
        array.push(element);
    }
    return array;
}

function coreEraseOne(array, element) {
    element = array.indexOf(element);
    if (element != -1) {
        array.splice( element, 1 );
    }
    return array;
}

function coreEraseAll(array, element) {
    for (var i = array.length; i--;) {
        if (array[i] == element) {
            array.splice( i, 1 );
        }
    }
    return array;
}
function coreToArray (elem) { return slice.call(elem) }
function coreIsArrayLike (item) {
    return item && (Array.isArray(item) || (
        typeof item != 'string' &&
        !coreIsFunction(item) &&
        typeof item.nodeName != 'string' &&
        typeof item.length == 'number'
    ));
}
function coreAppend(target, source) {
    if (source) for (var key in source) if (hasOwn.call(source, key)) {
        target[key] = source[key];
    }
    return target;
}

new function () {

    function ensureObjectSetter (fn) {
        return function (properties, value) {
            return fn.call(this, coreObjectize(properties, value))
        }
    }
    function overloadSetter (fn) {
        return function (properties, value) {
            properties = coreObjectize(properties, value);
            for (var i in properties) fn.call( this, i, properties[i] );
            return this;
        };
    }
    function overloadGetter (fn, ignoreEmpty) {
        return function (properties) {
            if (Array.isArray(properties)) {
                var result = {}, name, value;
                for (var i = properties.length; i--;) {
                    name = properties[i];
                    value = fn.call(this, name);
                    if (!ignoreEmpty || typeof value !== 'undefined') {
                        result[name] = value;
                    }
                }
                return result;
            }
            return fn.call(this, properties);
        };
    }
    /**
     * Returns function that calls callbacks.get
     * if first parameter is primitive & second parameter is undefined
     *     object.attr('name')          - get
     *     object.attr('name', 'value') - set
     *     object.attr({name: 'value'}) - set
     * @param {Object} callbacks
     * @param {Function} callbacks.get
     * @param {Function} callbacks.set
     */
    function slickAccessor (callbacks) {
        var setter =  atom.core.overloadSetter(callbacks.set);

        return function (properties, value) {
            if (typeof value === 'undefined' && typeof properties !== 'object') {
                return callbacks.get.call(this, properties);
            } else {
                return setter.call(this, properties, value);
            }
        };
    }

    atom.core = {
        isFunction: coreIsFunction,
        objectize : coreObjectize,
        contains  : coreContains,
        eraseOne  : coreEraseOne,
        eraseAll  : coreEraseAll,
        toArray   : coreToArray,
        append    : coreAppend,
        isArrayLike   : coreIsArrayLike,
        includeUnique : includeUnique,
        slickAccessor : slickAccessor,
        overloadSetter: overloadSetter,
        overloadGetter: overloadGetter,
        ensureObjectSetter: ensureObjectSetter
    };

    /** @deprecated - use atom.core.toArray instead */
    atom.toArray   = coreToArray;
    /** @deprecated - use console-cap instead: https://github.com/theshock/console-cap/ */
    atom.log = function () { throw new Error('deprecated') };
    /** @deprecated - use atom.core.isArrayLike instead */
    atom.isArrayLike = coreIsArrayLike;
    /** @deprecated - use atom.core.append instead */
    atom.append = coreAppend;

};

/*
---

name: "Accessors"

description: "Implementing accessors"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core

provides: accessors

...
*/

(function (Object) {
    var standard = !!Object.getOwnPropertyDescriptor, nonStandard = !!{}.__defineGetter__;

    if (!standard && !nonStandard) throw new Error('Accessors are not supported');

    var lookup = nonStandard ?
        function (from, key, bool) {
            var g = from.__lookupGetter__(key), s = from.__lookupSetter__(key), has = !!(g || s);

            if (bool) return has;

            return has ? { get: g, set: s } : null;
        } :
        function (from, key, bool) {
            var descriptor = Object.getOwnPropertyDescriptor(from, key);
            if (!descriptor) {
                // try to find accessors according to chain of prototypes
                var proto = Object.getPrototypeOf(from);
                if (proto) return atom.accessors.lookup(proto, key, bool);
            } else if ( descriptor.set || descriptor.get ) {
                if (bool) return true;

                return {
                    set: descriptor.set,
                    get: descriptor.get
                };
            }
            return bool ? false : null;
        }; /* lookup */

    var define = nonStandard ?
        function (object, prop, descriptor) {
            if (descriptor) {
                if (descriptor.get) object.__defineGetter__(prop, descriptor.get);
                if (descriptor.set) object.__defineSetter__(prop, descriptor.set);
            }
            return object;
        } :
        function (object, prop, descriptor) {
            if (descriptor) {
                var desc = {
                    get: descriptor.get,
                    set: descriptor.set,
                    configurable: true,
                    enumerable: true
                };
                Object.defineProperty(object, prop, desc);
            }
            return object;
        };

    atom.accessors = {
        lookup: lookup,
        define: function (object, prop, descriptor) {
            if (typeof prop == 'object') {
                for (var i in prop) define(object, i, prop[i]);
            } else {
                define(object, prop, descriptor);
            }
            return object;
        },
        has: function (object, key) {
            return atom.accessors.lookup(object, key, true);
        },
        inherit: function (from, to, key) {
            var a = atom.accessors.lookup(from, key);

            if ( a ) {
                atom.accessors.define(to, key, a);
                return true;
            }
            return false;
        }
    };
})(Object);

/*
---

name: "Dom"

description: "todo"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - accessors

inspiration:
  - "[JQuery](http://jquery.org)"

provides: dom

...
*/
(function (window, document) {
    var
        regexp = {
            Tag  : /^[-_a-z0-9]+$/i,
            Class: /^\.[-_a-z0-9]+$/i,
            Id   : /^#[-_a-z0-9]+$/i
        },
        isArray = Array.isArray,
        prevent = function (e) {
            e.preventDefault();
            return false;
        },
        ignoreCssPostfix = {
            zIndex: true,
            fontWeight: true,
            opacity: true,
            zoom: true,
            lineHeight: true
        },
        domReady = false,
        onDomReady = [],
        camelCase = function (str) {
            return String(str).replace(/-\D/g, function(match){
                return match[1].toUpperCase();
            });
        },
        hyphenate = function (str) {
            return String(str).replace(/[A-Z]/g, function(match){
                return '-' + match[0].toLowerCase();
            });
        },
        readyCallback = function () {
            if (domReady) return;
            
            domReady = true;
            
            for (var i = 0; i < onDomReady.length;) {
                onDomReady[i++]();
            }
            
            onDomReady = [];
        },
        findParentByLevel = function (elem, level) {
            if (level == null || level < 0) level = 1;

            if (!elem || level <= 0) return atom.dom(elem);

            return findParentByLevel(elem.parentNode, level-1);
        };
        
    document.addEventListener('DOMContentLoaded', readyCallback, false);
    window.addEventListener('load', readyCallback, false);

    var Dom = function (sel, context) {
        if (! (this instanceof Dom)) {
            return new Dom(sel, context);
        }

        if (!arguments.length) {
            this.elems = [document];
            return this;
        }

        if (!context && sel === 'body') {
            this.elems = [document.body];
            return this;
        }

        if (context !== undefined) {
            return new Dom(context || document).find(sel);
        }
        context = context || document;

        if (typeof sel == 'function' && !(sel instanceof Dom)) {
            // onDomReady
            var fn = sel.bind(this, atom, Dom);
            domReady ? setTimeout(fn, 1) : onDomReady.push(fn);
            return this;
        }

        var elems = this.elems =
              sel == window          ? [ document ]
            : sel instanceof Dom     ? coreToArray(sel.elems)
            : coreIsArrayLike(sel)   ? coreToArray(sel)
            : typeof sel == 'string' ? Dom.query(context, sel)
            :                          Dom.find(context, sel);

        if (elems.length == 1 && elems[0] == null) {
            elems.length = 0;
        }

        return this;
    };
    coreAppend(Dom, {
        query : function (context, sel) {
            return sel.match(regexp.Id)    ? [(context.getElementById ? context : document).getElementById(sel.substr(1))] :
                   sel.match(regexp.Class) ? coreToArray(context.getElementsByClassName(sel.substr(1))) :
                   sel.match(regexp.Tag)   ? coreToArray(context.getElementsByTagName  (sel)) :
                                             coreToArray(context.querySelectorAll      (sel));
        },
        find: function (context, sel) {
            if (!sel) return context == null ? [] : [context];

            var result = sel.nodeName ? [sel]
                : typeof sel == 'string' ? Dom.query(context, sel) : [context];
            return (result.length == 1 && result[0] == null) ? [] : result;
        },
        create: function (tagName, attr) {
            var elem = new Dom(document.createElement(tagName));
            if (attr) elem.attr(attr);
            return elem;
        },
        isElement: function (node) {
            return !!(node && node.nodeName);
        }
    });
    Dom.prototype = {
        constructor: Dom,
        elems: [],
        get length() {
            return this.elems ? this.elems.length : 0;
        },
        get body() {
            return this.find('body');
        },
        get first() {
            return this.elems[0];
        },
        get : function (index) {
            return this.elems[Number(index) || 0];
        },
        parent : function(step) {
            return findParentByLevel(this.first, step);
        },
        contains: function (child) {
            var parent = this.first;
            child = atom.dom(child).first;
            if ( child ) while ( child = child.parentNode ) {
                if( child == parent ) {
                    return true;
                }
            }
            return false;
        },
        filter: function (selector) {
            var property = null;
            // speed optimization for "tag" & "id" filtering
            if (selector.match(regexp.Tag)) {
                selector = selector.toUpperCase();
                property = 'tagName';
            } else if (selector.match(regexp.Id)) {
                selector = selector.substr(1).toUpperCase();
                property = 'id';
            }

            return new Dom(this.elems.filter(function (elem) {
                if (property) {
                    return elem[property].toUpperCase() == selector;
                } else {
                    return elem.parentNode && coreToArray(
                        elem.parentNode.querySelectorAll(selector)
                    ).indexOf(elem) >= 0;
                }
            }));
        },
        is: function (selector) {
            return this.filter(selector).length > 0;
        },
        html : function (value) {
            if (value != null) {
                this.first.innerHTML = value;
                return this;
            } else {
                return this.first.innerHTML;
            }
        },
        text : function (value) {
            var property = document.body.innerText == null ? 'textContent' : 'innerText';
            if (value == null) {
                return this.first[property];
            }
            this.first[property] = value;
            return this;
        },
        create : function (tagName, index, attr) {
            if (typeof index == 'object') {
                attr  = index;
                index = 0;
            }
            atom.dom.create(tagName, attr).appendTo( this.get(index) );
            return this;
        },
        each : function (fn) {
            this.elems.forEach(fn.bind(this));
            return this;
        },
        attr : atom.core.slickAccessor({
            get: function (name) {
                return this.first.getAttribute(name);
            },
            set: function (name, value) {
                var e = this.elems, i = e.length;
                while (i--) {
                    e[i].setAttribute(name, value)
                }
            }
        }),
        css : atom.core.slickAccessor({
            get: function (name) {
                return window.getComputedStyle(this.first, "").getPropertyValue(hyphenate(name));
            },
            set: function (name, value) {
                var e = this.elems, i = e.length;
                while (i--) {
                    if (typeof value == 'number' && !ignoreCssPostfix[name]) {
                        value += 'px';
                    }
                    e[i].style[camelCase(name)] = value;
                }
            }
        }),

        addEvent: atom.core.overloadSetter(function (event, callback) {
            if (callback === false) callback = prevent;

            this.each(function (elem) {
                if (elem == document && event == 'load') elem = window;
                elem.addEventListener(event, callback, false);
            });

            return this;
        }),
        removeEvent : atom.core.overloadSetter(function (event, callback) {
            if (callback === false) callback = prevent;

            this.each(function (elem) {
                if (elem == document && event == 'load') elem = window;
                elem.removeEventListener(event, callback, false);
            });

            return this;
        }),
        /** @deprecated */
        bind : function (event, callback) {
            return this.addEvent.apply(this, arguments)
        },
        /** @deprecated */
        unbind : function (event, callback) {
            return this.removeEvent.apply(this, arguments)
        },
        delegate : function (selector, event, fn) {
            return this.bind(event, function (e) {
                if (new Dom(e.target).is(selector)) {
                    fn.apply(this, arguments);
                }
            });
        },
        wrap : function (wrapper) {
            wrapper = new Dom(wrapper).first;
            return this.replaceWith(wrapper).appendTo(wrapper);
        },
        replaceWith: function (element) {
            var obj = this.first;
            element = Dom(element).first;
            obj.parentNode.replaceChild(element, obj);
            return this;
        },
        find : function (selector) {
            var result = [];
            this.each(function (elem) {
                var i = 0,
                    found = Dom.find(elem, selector),
                    l = found.length;
                while (i < l) includeUnique(result, found[i++]);
            });
            return new Dom(result);
        },
        appendTo : function (to) {
            var fr = document.createDocumentFragment();
            this.each(function (elem) {
                fr.appendChild(elem);
            });
            Dom(to).first.appendChild(fr);
            return this;
        },
        appendBefore: function (elem) {
            var fr = document.createDocumentFragment();
            this.each(function (elem) {
                fr.appendChild(elem);
            });
            Dom(elem).parent().first.insertBefore(fr, Dom(elem).first);
            return this;
        },
        appendAfter: function (elem) {
            var parent = Dom(elem).parent().first;
            var next = Dom(elem).first.nextSibling;
            var fr = document.createDocumentFragment();
            this.each(function (elem) {
                fr.appendChild(elem);
            });
            
            if (next) {
                parent.insertBefore(fr, next);
            } else {
                parent.appendChild(fr);
            }
            
            return this;
        },
        /** @private */
        manipulateClass: function (classNames, fn) {
            if (!classNames) return this;
            if (!isArray(classNames)) classNames = [classNames];

            return this.each(function (elem) {
                var i, all = elem.className.split(/\s+/);

                for (i = classNames.length; i--;) {
                    fn.call(this, all, classNames[i]);
                }

                elem.className = all.join(' ').trim();
            });
        },
        addClass: function (classNames) {
            return this.manipulateClass(classNames, includeUnique);
        },
        removeClass: function (classNames) {
            return this.manipulateClass(classNames, coreEraseAll);
        },
        toggleClass: function(classNames) {
            return this.manipulateClass(classNames, function (all, c) {
                var i = all.indexOf(c);
                if (i === -1) {
                    all.push(c);
                } else {
                    all.splice(i, 1);
                }
            });
        },
        hasClass: function(classNames) {
            if (!classNames) return this;
            if (!isArray(classNames)) classNames = [classNames];
            
            var result = false;
            this.each(function (elem) {
                if (result) return;
                
                var i = classNames.length,
                    all = elem.className.split(/\s+/);

                while (i--) if (!coreContains(all, classNames[i])) {
                    return;
                }

                result = true;
            });
            return result;
        },
        offset: function () {
            var element = this.first;
            if (element.offsetX != null) {
                return { x: element.offsetX, y: element.offsetY };
            }

            var box = element.getBoundingClientRect(),
                body    = document.body,
                docElem = document.documentElement,
                scrollLeft = window.pageXOffset || docElem.scrollLeft || body.scrollLeft,
                scrollTop  = window.pageYOffset || docElem.scrollTop  || body.scrollTop,
                clientLeft = docElem.clientLeft || body.clientLeft || 0,
                clientTop  = docElem.clientTop  || body.clientTop  || 0;

            return {
                x: Math.round(box.left + scrollLeft - clientLeft),
                y: Math.round(box.top  + scrollTop  - clientTop )
            };
        },
        clone: function (deep) {
            var i = 0, elements = [];

            if (deep == null) deep = true;

            for (; i < this.elems.length; i++) {
                elements.push(this.elems[i].cloneNode(deep));
            }

            return atom.dom(elements);
        },
        empty: function () {
            return this.each(function (elem) {
                while (elem.hasChildNodes()) {
                    elem.removeChild( elem.firstChild );
                }
            });
        },
        log : function () {
            console.log('atom.dom: ', this.elems);
            return this;
        },
        destroy : function () {
            return this.each(function (elem) {
                if (elem.parentNode) {
                    elem.parentNode.removeChild(elem);
                }
            });
        }
    };

    atom.dom = Dom;
}(window, window.document));


/*
---

name: "CoreExtended"

description: "Extended core of AtomJS  - extend, implements, clone, typeOf"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

inspiration:
  - "[JQuery](http://jquery.com)"
  - "[MooTools](http://mootools.net)"

provides: CoreExtended

requires:
    - js185
    - Core

...
*/

new function () {

function innerExtend (proto) {
    return function (elem, from) {
        if (from == null) {
            from = elem;
            elem = atom;
        }

        var ext = proto ? elem.prototype : elem,
            accessors = atom.accessors && atom.accessors.inherit;

        for (var i in from) if (i != 'constructor') {
            if ( accessors && accessors(from, ext, i) ) continue;

            ext[i] = clone(from[i]);
        }
        return elem;
    };
}

function typeOf (item) {
    if (item == null) return 'null';

    var string = toString.call(item);
    for (var i in typeOf.types) if (i == string) return typeOf.types[i];

    if (item.nodeName){
        if (item.nodeType == 1) return 'element';
        if (item.nodeType == 3) return /\S/.test(item.nodeValue) ? 'textnode' : 'whitespace';
    }

    var type = typeof item;

    if (item && type == 'object') {
        if (atom.Class && item instanceof atom.Class) return 'class';
        if (coreIsArrayLike(item)) return 'arguments';
    }

    return type;
}

typeOf.types = {};
['Boolean', 'Number', 'String', 'Function', 'Array', 'Date', 'RegExp', 'Class'].forEach(function(name) {
    typeOf.types['[object ' + name + ']'] = name.toLowerCase();
});


function clone (object) {
    var type = typeOf(object);
    return type in clone.types ? clone.types[type](object) : object;
}
clone.types = {
    'array': function (array) {
        var i = array.length, c = new Array(i);
        while (i--) c[i] = clone(array[i]);
        return c;
    },
    'class':function (object) {
        return typeof object.clone == 'function' ?
            object.clone() : object;
    },
    'object': function (object) {
        if (typeof object.clone == 'function') return object.clone();

        var c = {}, accessors = atom.accessors && atom.accessors.inherit;
        for (var key in object) {
            if (accessors && accessors(object, c, key)) continue;
            c[key] = clone(object[key]);
        }
        return c;
    }
};

atom.core.extend    = innerExtend(false);
atom.core.implement = innerExtend(true);
atom.core.typeOf    = typeOf;
atom.core.clone     = clone;

atom.extend    = atom.core.extend;
atom.implement = atom.core.implement;
atom.typeOf    = atom.core.typeOf;
atom.clone     = atom.core.clone;

};

/*
---

name: "Ajax"

description: "todo"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - CoreExtended

provides: ajax

...
*/

(function () {
    var extend = atom.core.extend, emptyFn = function () {};

    var ajax = function (userConfig) {
        var data, config, method, req, url;
        config = {};
        extend(config, ajax.defaultProps);
        extend(config, userConfig);
        config.headers = {};
        extend(config.headers, ajax.defaultHeaders);
        extend(config.headers, userConfig.headers);

        data = ajax.stringify( config.data );
        req  = new XMLHttpRequest();
        url  = config.url;
        method = config.method.toUpperCase();
        if (method == 'GET' && data) {
            url += (url.indexOf( '?' ) == -1 ? '?' : '&') + data;
        }
        if (!config.cache) {
            url += (url.indexOf( '?' ) == -1 ? '?' : '&') + '_no_cache=' + Date.now();
        }
        req.onreadystatechange = ajax.onready(req, config);
        req.open(method, url, true);
        for (var i in config.headers) {
            req.setRequestHeader(i, config.headers[i]);
        }
        req.send( method == 'POST' && data ? data : null );
    };

    ajax.stringify = function (object) {
        if (!object) return '';
        if (typeof object == 'string' || typeof object == 'number') return String( object );

        var array = [], e = encodeURIComponent;
        for (var i in object) if (object.hasOwnProperty(i)) {
            array.push( e(i) + '=' + e(object[i]) );
        }
        return array.join('&');
    };

    ajax.defaultProps = {
        interval: 0,
        type    : 'plain',
        method  : 'post',
        data    : {},
        headers : {},
        cache   : false,
        url     : location.href,
        onLoad  : emptyFn,
        onError : emptyFn
    };

    ajax.defaultHeaders = {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*'
    };
    /** @type {function} */
    ajax.onready = function (req, config) {
        return function (e) {
            if (req.readyState == 4) {
                if (req.status != 200) return config.onError(e);

                var result = req.responseText;
                if (config.type.toLowerCase() == 'json') {
                    result = JSON.parse(result);
                }
                if (config.interval > 0) setTimeout(function () {
                    atom.ajax(config);
                }, config.interval * 1000);
                config.onLoad(result);
            }
        };
    };

    atom.ajax = ajax;
})();


/*
---

name: "Ajax.Dom"

description: todo

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - dom
    - ajax

provides: ajax.dom

...
*/

atom.dom.prototype.ajax = function (config) {
    config = coreAppend({}, config);

    var $dom = this;

    if (config.onLoad ) {
        config.onLoad  = config.onLoad.bind($dom);
    } else {
        config.onLoad = function (r) { $dom.first.innerHTML = r };
    }
    if (config.onError) config.onError = config.onError.bind($dom);
    
    atom.ajax(config);
    return $dom;
};


/*
---

name: "Cookie"

description: "todo"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core

provides: cookie

...
*/

atom.cookie = {
    get: function (name) {
        var matches = document.cookie.match(new RegExp(
          "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ));
        return matches ? decodeURIComponent(matches[1]) : null;
    },
    set: function (name, value, options) {
        options = options || {};
        var exp = options.expires;
        if (exp) {
            if (typeof exp == 'number') {
                exp = new Date(exp * 1000 + Date.now());
            }
            if (exp.toUTCString) {
                exp = exp.toUTCString();
            }
            options.expires = exp;
        }

        var cookie = [name + "=" + encodeURIComponent(value)];
        for (var o in options) cookie.push(
            options[o] === true ? o : o + "=" + options[o]
        );
        document.cookie = cookie.join('; ');

        return atom.cookie;
    },
    del: function (name) {
        return atom.cookie.set(name, '', { expires: -1 });
    }
};

/*
---

name: "Frame"

description: "Provides cross-browser interface for requestAnimationFrame"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core

provides: frame

...
*/
(function () {

    var previous,
        started   = false,
        callbacks = [],
        remove    = [],
        frameTime = 16, // 62 fps
        // we'll switch to real `requestAnimationFrame` here
        // when all browsers will be ready
        requestAnimationFrame = function (callback) {
            window.setTimeout(callback, frameTime);
        };

    function startAnimation () {
        if (!started) {
            previous  = Date.now();
            requestAnimationFrame(frame);
            started = true;
        }
    }

    function invokeFrame () {
        var fn, i, l,
            now = Date.now(),
            // 1 sec is max time for frame to avoid some bugs with too large time
            delta = Math.min(now - previous, 1000);

        for (i = 0, l = remove.length; i < l; i++) {
            coreEraseOne(callbacks, remove[i]);
        }
        remove.length = 0;

        for (i = 0, l = callbacks.length; i < l; i++) {
            fn = callbacks[i];
            // one of previous calls can remove our fn
            if (remove.indexOf(fn) == -1) {
                fn.call(null, delta);
            }
        }

        previous = now;
    }

    function frame() {
        requestAnimationFrame(frame);

        if (callbacks.length == 0) {
            remove.length = 0;
            previous = Date.now();
        } else invokeFrame();
    }

    atom.frame = {
        add: function (fn) {
            startAnimation();
            includeUnique(callbacks, fn);
        },
        // we dont want to fragmentate callbacks, so remove only before frame started
        remove: function (fn) {
            if (started) includeUnique(remove, fn);
        }
    };

}());

/*
---

name: "PointerLock"

description: "Provides cross-browser interface for locking pointer"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core

provides: PointerLock

...
*/
(function (document) {
    var prefix =
          'pointerLockElement' in document ? '':
       'mozPointerLockElement' in document ? 'moz':
    'webkitPointerLockElement' in document ? 'webkit': null;

    function PointerLock (supports) {
        this.supports = supports;
    }

    function p (string) {
        return prefix ? prefix + string :
        string[0].toLowerCase() + string.substr(1);
    }

    function isLocked (element) {
        return document[p('PointerLockElement')] === element;
    }

    if (prefix == null) {
        PointerLock.prototype = {
            locked  : function () { return false },
            request : function () {},
            exit    : function () {}
        };
    } else {

        document.addEventListener("mousemove", function onMove (e) {
            if (lockedElement && isLocked(lockedElement)) {
                e.movementX = e[p('MovementX')] || 0;
                e.movementY = e[p('MovementY')] || 0;

                callback && callback(e);
            }
        }, false);


        var lockedElement = false, callback = null;

        PointerLock.prototype = {
            locked: function (element) {
                return isLocked(element || lockedElement);
            },
            request: function (element, fn) {
                lockedElement = element;
                callback = fn;
                element[p('RequestPointerLock')]();
            },
            exit: function () {
                lockedElement = null;
                callback = null;
                document[p('ExitPointerLock')]();
            }
        };
    }

    atom.pointerLock = new PointerLock(prefix != null);

}(document));

/*
---

name: "Uri"

description: "Port of parseUri function"

license: "MIT License"

author: "Steven Levithan <stevenlevithan.com>"

requires:
    - Core

provides: uri

...
*/
new function () {

var uri = function (str) {
    var o   = atom.uri.options,
        m   = o.parser.exec(str || window.location.href),
        uri = {},
        i   = 14;

    while (i--) uri[o.key[i]] = m[i] || "";

    uri[o.q.name] = {};
    uri[o.key[12]].replace(o.q.parser, function ($0, $1, $2) {
        if ($1) uri[o.q.name][$1] = $2;
    });

    return uri;
};
uri.options = {
    key: ["source","protocol","authority","userInfo","user","password","host","port","relative","path","directory","file","query","anchor"],
    q:   {
        name:   "queryKey",
        parser: /(?:^|&)([^&=]*)=?([^&]*)/g
    },
    parser: /^(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/
};

atom.uri = uri;

};

/*
---

name: "Class"

description: "Contains the Class Function for easily creating, extending, and implementing reusable Classes."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - CoreExtended
    - accessors
    - Array

inspiration:
  - "[MooTools](http://mootools.net)"

provides: Class

deprecated: "Use declare instead"

...
*/


(function(atom){

var typeOf = atom.core.typeOf,
    extend = atom.core.extend,
    accessors = atom.accessors.inherit,
    prototype = 'prototype',
    lambda    = function (value) { return function () { return value; }},
    prototyping = false;

var Class = function (params) {
    if (prototyping) return this;

    if (typeof params == 'function' && typeOf(params) == 'function') params = { initialize: params };

    var Constructor = function(){
        if (this instanceof Constructor) {
            if (prototyping) return this;
            return this.initialize ? this.initialize.apply(this, arguments) : this;
        } else {
            return Constructor.invoke.apply(Constructor, arguments);
        }
    };
    extend(Constructor, Class);
    Constructor.prototype = getInstance(Class);

    Constructor
        .implement(params, false)
        .reserved(true, {
            parent: parent,
            self  : Constructor
        })
        .reserved({
            factory : function() {
                function Factory(args) { return Constructor.apply(this, args); }
                Factory.prototype = Constructor.prototype;
                return function(args) { return new Factory(args || []); }
            }()
        });

    Constructor.prototype.constructor = Constructor;

    return Constructor;
};

var parent = function(){
    if (!this.$caller) throw new Error('The method «parent» cannot be called.');
    var name    = this.$caller.$name,
        parent   = this.$caller.$owner.parent,
        previous = parent && parent.prototype[name];
    if (!previous) throw new Error('The method «' + name + '» has no parent.');
    return previous.apply(this, arguments);
};

var wrap = function(self, key, method){
    // if method is already wrapped
    if (method.$origin) method = method.$origin;
    
    var wrapper = function() {
        if (!this || this == atom.global) throw new TypeError('Context lost');
        if (method.$protected && !this.$caller) throw new Error('The method «' + key + '» is protected.');
        var current = this.$caller;
        this.$caller = wrapper;
        var result = method.apply(this, arguments);
        this.$caller = current;
        return result;
    };
    wrapper.$owner  = self;
    wrapper.$origin = method;
    wrapper.$name   = key;
    
    return wrapper;
};

var getInstance = function(Class){
    if (atom.declare && Class instanceof atom.declare) {
        return atom.declare.config.methods.proto(Class);
    }

    prototyping = true;
    var proto = new Class;
    prototyping = false;
    return proto;
};

Class.extend =  function (name, fn) {
    if (typeof name == 'string') {
        var object = {};
        object[name] = fn;
    } else {
        object = name;
    }

    for (var i in object) if (!accessors(object, this, i)) {
         this[i] = object[i];
    }
    return this;
};

Class.extend({
    implement: function(name, fn, retain){
        if (typeof name == 'string') {
            var params = {};
            params[name] = fn;
        } else {
            params = name;
            retain = fn;
        }

        for (var key in params) {
            if (!accessors(params, this.prototype, key)) {
                var value = params[key];

                if (Class.Mutators.hasOwnProperty(key)){
                    value = Class.Mutators[key].call(this, value);
                    if (value == null) continue;
                }

                if (typeof value == 'function' && typeOf(value) == 'function'){
                    if (value.$origin) value = value.$origin;
                    if (value.$hidden == 'next') {
                        value.$hidden = true
                    } else if (value.$hidden) {
                        continue;
                    }
                    this.prototype[key] = (retain) ? value : wrap(this, key, value);
                } else {
                    this.prototype[key] = atom.clone(value);
                }
            }
        }
        return this;
    },
    mixin: function () {
        Array.from(arguments).forEach(function (item) {
            this.implement(getInstance(item));
        }.bind(this));
        return this;
    },
    reserved: function (toProto, props) { // use careful !!
        if (arguments.length == 1) {
            props = toProto;
            toProto = false;
        }
        var target = toProto ? this.prototype : this;
        for (var name in props) {
            atom.accessors.define(target, name, { get: lambda(props[name]) });
        }
        return this;
    },
    isInstance: function (object) {
        return object instanceof this;
    },
    invoke: function () {
        return this.factory( arguments );
    },
    Mutators: {
        Extends: function(parent){
            if (parent == null) throw new TypeError('Cant extends from null');
            this.extend(parent).reserved({ parent: parent });
            this.prototype = getInstance(parent);
        },

        Implements: function(items){
            this.mixin.apply(this, Array.from(items));
        },

        Static: function(properties) {
            this.extend(properties);
        }
    },
    abstractMethod: function () {
        throw new Error('Abstract Method «' + this.$caller.$name + '» called');
    },
    protectedMethod: function (fn) {
        return extend(fn, { $protected: true });
    },
    hiddenMethod: function (fn) {
        return extend(fn, { $hidden: 'next' });
    }
});

Class.abstractMethod.$abstract = true;
atom.Class = Class;

})(atom);

/*
---

name: "Class.BindAll"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - Class

inspiration:
  - "[MooTools](http://mootools.net)"

provides: Class.BindAll

...
*/

atom.Class.bindAll = function (object, methods) {
    if (typeof methods == 'string') {
        if (
            methods != '$caller' &&
            !atom.accessors.has(object, methods) &&
            coreIsFunction(object[methods])
        ) {
            object[methods] = object[methods].bind( object );
        }
    } else if (methods) {
        for (var i = methods.length; i--;) atom.Class.bindAll( object, methods[i] );
    } else {
        for (var i in object) atom.Class.bindAll( object, i );
    }
    return object;
};


/*
---

name: "Class.Events"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - Class

inspiration:
  - "[MooTools](http://mootools.net)"

provides: Class.Events

...
*/

new function () {

var Class = atom.Class;

var fire = function (name, fn, args) {
    var result = fn.apply(this, Array.from(args || []));
    if (typeof result == 'string' && result.toLowerCase() == 'removeevent') {
        this.removeEvent(name, fn);
    }
};

var removeOn = function(string){
    return (string || '').replace(/^on([A-Z])/, function(full, first){
        return first.toLowerCase();
    });
};

var initEvents = function (object, reset) {
    if (reset || !object._events) object._events = { $ready: {} };
};

var nextTick = function (fn) {
    nextTick.fn.push(fn);
    if (!nextTick.id) {
        nextTick.id = function () {
            nextTick.reset().invoke();
        }.delay(1);
    }
};
nextTick.reset = function () {
    var fn = nextTick.fn;
    nextTick.fn = [];
    nextTick.id = 0;
    return fn;
};
nextTick.reset();

coreAppend(Class, {
    Events: Class({
        addEvent: function(name, fn) {
            initEvents(this);

            var i, l, onfinish = [];
            if (arguments.length == 1 && typeof name != 'string') {
                for (i in name) {
                    this.addEvent(i, name[i]);
                }
            } else if (Array.isArray(name)) {
                for (i = 0, l = name.length; i < l; i++) {
                    this.addEvent(name[i], fn);
                }
            } else {
                name = removeOn(name);
                if (name == '$ready') {
                    throw new TypeError('Event name «$ready» is reserved');
                } else if (!fn) {
                    throw new TypeError('Function is empty');
                } else {
                    Object.ifEmpty(this._events, name, []);

                    this._events[name].include(fn);

                    var ready = this._events.$ready[name];
                    if (ready) fire.apply(this, [name, fn, ready, onfinish]);
                    onfinish.invoke();
                }
            }
            return this;
        },
        removeEvent: function (name, fn) {
            if (!arguments.length) {
                initEvents( this, true );
                return this;
            }

            initEvents(this);

            if (Array.isArray(name)) {
                for (var i = name.length; i--;) {
                    this.removeEvent(name[i], fn);
                }
            } else if (arguments.length == 1 && typeof name != 'string') {
                for (i in name) {
                    this.removeEvent(i, name[i]);
                }
            } else {
                name = removeOn(name);
                if (name == '$ready') {
                    throw new TypeError('Event name «$ready» is reserved');
                } else if (arguments.length == 1) {
                    this._events[name] = [];
                } else if (name in this._events) {
                    this._events[name].erase(fn);
                }
            }
            return this;
        },
        isEventAdded: function (name) {
            initEvents(this);
            
            var e = this._events[name];
            return !!(e && e.length);
        },
        fireEvent: function (name, args) {
            initEvents(this);
            
            name = removeOn(name);
            // we should prevent skipping next event on removing this in different fireEvents
            var funcs = atom.clone(this._events[name]);
            if (funcs) {
                var l = funcs.length,
                    i = 0;
                for (;i < l; i++) fire.call(this, name, funcs[i], args || []);
            }
            return this;
        },
        readyEvent: function (name, args) {
            initEvents(this);
            
            nextTick(function () {
                name = removeOn(name);
                this._events.$ready[name] = args || [];
                this.fireEvent(name, args || []);
            }.bind(this));
            return this;
        }
    })
});

};

/*
---

name: "Class.Mutators.Generators"

description: "Provides Generators mutator"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - Core
    - accessors
    - Class

provides: Class.Mutators.Generators

...
*/

new function () {

var getter = function (key, fn) {
    return function() {
        var pr = '_' + key, obj = this;
        return pr in obj ? obj[pr] : (obj[pr] = fn.call(obj));
    };
};

atom.Class.Mutators.Generators = function(properties) {
    atom.Class.Mutators.Generators.init(this, properties);
};

atom.Class.Mutators.Generators.init = function (Class, properties) {
    for (var i in properties) atom.accessors.define(Class.prototype, i, { get: getter(i, properties[i]) });
};

};

/*
---

name: "Class.Options"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - Class

inspiration:
  - "[MooTools](http://mootools.net)"

provides: Class.Options

...
*/

atom.Class.Options = atom.Class({
    options: {},
    fastSetOptions: false,
    setOptions: function(){
        if (!this.options) {
            this.options = {};
        } else if (this.options == this.self.prototype.options) {
            // it shouldn't be link to static options
            if (this.fastSetOptions) {
                this.options = coreAppend({}, this.options);
            } else {
                this.options = atom.clone(this.options);
            }
        }
        var options = this.options;

        for (var a = arguments, i = 0, l = a.length; i < l; i++) {
            if (typeof a[i] == 'object') {
                if (this.fastSetOptions) {
                    coreAppend(options, a[i]);
                } else {
                    atom.extend(options, a[i]);
                }
            }
        }
        
        if (this.addEvent) for (var option in options){
            if (atom.typeOf(options[option]) == 'function' && (/^on[A-Z]/).test(option)) {
                this.addEvent(option, options[option]);
                delete options[option];
            }
        }
        return this;
    }
});

/*
---

name: "Declare"

description: "Contains the Class Function for easily creating, extending, and implementing reusable Classes."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - accessors

provides: declare

...
*/

var declare = (function(atom){

var
    declare, methods,
    accessors   = atom.accessors.inherit,
    factory     = false,
    prototyping = false,
    mutators    = [];

declare = function (declareName, Parent, params) {
    if (prototyping) return this;

    params = methods.prepareParams(declareName, Parent, params);

    // line break for more user-friendly debug string
    var Constructor = function ()
    { return methods.construct.call(this, Constructor, arguments) };

    // <debug> - should be removed on production
    if (params.name) {
        Constructor = new Function('con', 'return {"' + params.name + '": ' +
            function(){ return con.apply(this, arguments) }
         + '}["' + params.name + '"];')(Constructor);
    }
    // </debug>

    for (var i = 0, l = mutators.length; i < l; i++) {
        mutators[i].fn( Constructor, params[mutators[i].name] );
    }

    Constructor.prototype.constructor = Constructor;

    if (params.declareName) methods.define( params.declareName, Constructor );

    return Constructor;
};

declare.prototype.bindMethods = function (methods) {
    var i;

    if (typeof methods == 'string') {
        if (typeof this[methods] == 'function') {
            this[methods] = this[methods].bind(this);
        }
        return this;
    }

    if (!methods) {
        for (i in this) this.bindMethods(i);
        return this;
    }

    for (i = methods.length; i--;) this.bindMethods( methods[i] );
    return this;
};

declare.prototype.toString = function () {
    return '[object ' + (this.constructor.NAME || 'Declare') + ']';
};

declare.NAME = 'atom.declare';

declare.invoke = function () {
    return this.factory( arguments );
};

declare.own = function (properties) {
    methods.addTo(this, properties, this.NAME + '.');
    return this;
};

declare.factory = function (args) {
    factory = true;
    return new this(args);
};

declare.castArguments = function (args) {
    if (args == null) return null;

    var constructor = this;

    return (args != null && args[0] && args[0] instanceof constructor) ?
        args[0] : args instanceof constructor ? args : new constructor( args );
};

methods = {
    define: function (path, value) {
        var key, part, target = atom.global;

        path = path.split('.');
        key  = path.pop();

        while (path.length) {
            part = path.shift();
            if (!target[part]) {
                target = target[part] = {};
            } else {
                target = target[part];
            }
        }

        target[key] = value;
    },
    mixin: function (target, items) {
        if (!Array.isArray(items)) items = [ items ];
        for (var i = 0, l = items.length; i < l; i++) {
            methods.addTo( target.prototype, methods.proto(items[i]) );
        }
        return this;
    },
    addTo: function (target, source, name) {
        var i, property;
        if (source) for (i in source) if (source.hasOwnProperty(i)) {
            if (!accessors(source, target, i) && source[i] != declare.config) {
                property = source[i];
                if (coreIsFunction(property)) {
                    if (name) property.path = name + i;
                    if (!property.previous && coreIsFunction(target[i])) {
                        property.previous = target[i];
                    }
                }
                target[i] = property;
            }
        }
        return target;
    },
    prepareParams: function (declareName, Parent, params) {
        if (typeof declareName != 'string') {
            params = Parent;
            Parent = declareName;
            declareName = null;
        }

        if (params == null && typeof Parent != 'function') {
            params = Parent;
            Parent = null;
        }

        if (!params                 ) params = {};
        if (!params.prototype       ) params = { prototype: params };
        if (!params.name            ) params.name = declareName;
        if (!params.declareName     ) params.declareName = declareName;
        if (!params.parent && Parent) params.parent = Parent;

        if (!params.prototype.initialize) {
            params.prototype.initialize = function () {
                if (!params.parent) return;
                return params.parent.prototype.initialize.apply(this, arguments);
            };
        }
        return params;
    },
    proto: function (Fn) {
        prototyping = true;
        var result = new Fn;
        prototyping = false;
        return result;
    },
    construct: function (Constructor, args) {
        if (factory) {
            args = args[0];
            factory = false;
        }

        if (prototyping) return this;

        if (this instanceof Constructor) {
            if (Constructor.NAME) this.Constructor = Constructor.NAME;
            return this.initialize.apply(this, args);
        } else {
            return Constructor.invoke.apply(Constructor, args);
        }
    }
};

declare.config = {
    methods: methods,
    mutator: atom.core.overloadSetter(function (name, fn) {
        mutators.push({ name: name, fn: fn });
        return this;
    })
};

declare.config
    .mutator( 'parent', function (Constructor, parent) {
        parent = parent || declare;
        methods.addTo( Constructor, parent );
        Constructor.prototype = methods.proto( parent );
        Constructor.Parent    = parent;
    })
    .mutator( 'mixin', function (Constructor, mixins) {
        if (mixins) methods.mixin( Constructor, mixins );
    })
    .mutator( 'name', function (Constructor, name) {
        if (!name) return;
        Constructor.NAME = name;
    })
    .mutator( 'own', function (Constructor, properties) {
        Constructor.own(properties);
    })
    .mutator( 'prototype', function (Constructor, properties) {
        methods.addTo(Constructor.prototype, properties, Constructor.NAME + '#');
    });

return atom.declare = declare;

})(atom);

/*
---

name: "Transition"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - declare
    
inspiration:
  - "[MooTools](http://mootools.net)"

provides: Transition

...
*/

atom.Transition = function (method, noEase) {
    var easeIn = function (progress) {
        return method(progress);
    };

    if (noEase) {
        return coreAppend( easeIn, {
            easeIn   : easeIn,
            easeOut  : easeIn,
            easeInOut: easeIn
        });
    }

    return coreAppend( easeIn, {
        easeIn: easeIn,
        easeOut: function(progress){
            return 1 - method(1 - progress);
        },
        easeInOut: function(progress){
            if (progress > 0.5) {
                return ( 2 - method(2 * (1 - progress)) ) /2
            } else {
                return method(2 * progress)/2;
            }
        }
    });
};

atom.Transition.set = atom.core.overloadSetter(function (id, fn) {
    atom.Transition[id] = atom.Transition(fn);
});

atom.Transition.get = function (fn) {
    if (typeof fn != 'string') return fn;
    var method = fn.split('-')[0], ease = 'easeInOut', In, Out;
    if (method != fn) {
        In  = fn.indexOf('-in' ) > 0;
        Out = fn.indexOf('-out') > 0;
        if (In ^ Out) {
            if (In ) ease = 'easeIn';
            if (Out) ease = 'easeOut';
        }
    }
    method = method[0].toUpperCase() + method.substr(1);
    if (!atom.Transition[method]) {
        throw new Error('No Transition method: ' + method);
    }
    return atom.Transition[method][ease];
};

atom.Transition.Linear = atom.Transition(function(p) { return p }, true);

atom.Transition.set({
    Expo: function(p){
        return Math.pow(2, 8 * (p - 1));
    },

    Circ: function(p){
        return 1 - Math.sin(Math.acos(p));
    },

    Sine: function(p){
        return 1 - Math.cos(p * Math.PI / 2);
    },

    Back: function(p){
        var x = 1.618;
        return Math.pow(p, 2) * ((x + 1) * p - x);
    },

    Bounce: function(p){
        var value, a = 0, b = 1;
        for (;;){
            if (p >= (7 - 4 * a) / 11){
                value = b * b - Math.pow((11 - 6 * a - 11 * p) / 4, 2);
                break;
            }
            a += b, b /= 2
        }
        return value;
    },

    Elastic: function(p){
        return Math.pow(2, 10 * --p) * Math.cos(12 * p);
    }

});

['Quad', 'Cubic', 'Quart', 'Quint'].forEach(function(transition, i){
    atom.Transition.set(transition, function(p){
        return Math.pow(p, i + 2);
    });
});

/*
---

name: "Events"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - declare

inspiration:
  - "[MooTools](http://mootools.net)"

provides: Events

...
*/

/** @class atom.Events */
declare( 'atom.Events', {

    /** @constructs */
    initialize: function (context) {
        this.context   = context || this;
        this.locked    = [];
        this.events    = {};
        this.actions   = {};
        this.readyList = {};
    },

    /**
     * @param {String} name
     * @return Boolean
     */
    exists: function (name) {
        var array = this.events[this.removeOn( name )];
        return !!(array && array.length);
    },

    /**
     * @param {String} name
     * @param {Function} callback
     * @return Boolean
     */
    add: function (name, callback) {
        this.run( 'addOne', name, callback );
        return this;
    },

    /**
     * @param {String} name
     * @param {Function} [callback]
     * @return Boolean
     */
    remove: function (name, callback) {
        if (typeof name == 'string' && !callback) {
            this.removeAll( name );
        } else {
            this.run( 'removeOne', name, callback );
        }
        return this;
    },

    /**
     * @param {String} name
     * @param {Array} args
     * @return atom.Events
     */
    fire: function (name, args) {
        args = args ? slice.call( args ) : [];
        name = this.removeOn( name );

        this.locked.push(name);
        var i = 0, l, events = this.events[name];
        if (events) for (l = events.length; i < l; i++) {
            events[i].apply( this.context, args );
        }
        this.unlock( name );
        return this;
    },

    /**
     * @param {String} name
     * @param {Array} [args=null]
     * @return atom.Events
     */
    ready: function (name, args) {
        name = this.removeOn( name );
        this.locked.push(name);
        if (name in this.readyList) {
            throw new Error( 'Event «'+name+'» is ready' );
        }
        this.readyList[name] = args;
        this.fire(name, args);
        this.removeAll(name);
        this.unlock( name );
        return this;
    },

    /**
     * @param {String} name
     * @param {Array} [args=null]
     * @return atom.Events
     */
    ensureReady: function (name, args) {
        if (!(name in this.readyList)) {
            this.ready(name, args);
        }
        return this;
    },


    // only private are below

    /** @private */
    context: null,
    /** @private */
    events: {},
    /** @private */
    readyList: {},
    /** @private */
    locked: [],
    /** @private */
    actions: {},

    /** @private */
    removeOn: function (name) {
        return (name || '').replace(/^on([A-Z])/, function(full, first){
            return first.toLowerCase();
        });
    },
    /** @private */
    removeAll: function (name) {
        var events = this.events[name];
        if (events) for (var i = events.length; i--;) {
            this.removeOne( name, events[i] );
        }
    },
    /** @private */
    unlock: function (name) {
        var action,
            all    = this.actions[name],
            index  = this.locked.indexOf( name );

        this.locked.splice(index, 1);

        if (all) for (index = 0; index < all.length; index++) {
            action = all[index];

            this[action.method]( name, action.callback );
        }
    },
    /** @private */
    run: function (method, name, callback) {
        var i = 0, l = 0;

        if (Array.isArray(name)) {
            for (i = 0, l = name.length; i < l; i++) {
                this[method](name[i], callback);
            }
        } else if (typeof name == 'object') {
            for (i in name) {
                this[method](i, name[i]);
            }
        } else if (typeof name == 'string') {
            this[method](name, callback);
        } else {
            throw new TypeError( 'Wrong arguments in Events.' + method );
        }
    },
    /** @private */
    register: function (name, method, callback) {
        var actions = this.actions;
        if (!actions[name]) {
            actions[name] = [];
        }
        actions[name].push({ method: method, callback: callback })
    },
    /** @private */
    addOne: function (name, callback) {
        var events, ready, context;

        name = this.removeOn( name );

        if (this.locked.indexOf(name) == -1) {
            ready = this.readyList[name];
            if (ready) {
                context = this.context;
                setTimeout(function () {
                    callback.apply(context, ready);
                }, 0);
                return this;
            } else {
                events = this.events;
                if (!events[name]) {
                    events[name] = [callback];
                } else {
                    events[name].push(callback);
                }
            }
        } else {
            this.register(name, 'addOne', callback);
        }
    },
    /** @private */
    removeOne: function (name, callback) {
        name = this.removeOn( name );

        if (this.locked.indexOf(name) == -1) {
            var events = this.events[name], i = events.length;
            while (i--) if (events[i] == callback) {
                events.splice(i, 1);
            }
        } else {
            this.register(name, 'removeOne', callback);
        }
    }
});

// local alias
var Events = atom.Events;

/*
---

name: "Settings"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - declare

provides: Settings

...
*/

/** @class atom.Settings */
declare( 'atom.Settings', {
    /** @private */
    recursive: false,

    /** @private */
    values: {},

    /**
     * @constructs
     * @param {Object} [initialValues]
     */
    initialize: function (initialValues) {
        this.values    = {};

        if (initialValues) this.set(initialValues);
    },

    /**
     * @param {atom.Events} events
     * @return atom.Options
     */
    addEvents: function (events) {
        this.events = events;
        return this.invokeEvents();
    },

    /**
     * @param {string|Array} name
     */
    get: function (name, defaultValue) {
        if (Array.isArray(name)) return this.subset(name, defaultValue);

        return name in this.values ? this.values[name] : defaultValue;
    },

    /**
     * @param {object} target
     * @param {string[]} [names=undefined]
     * @return {atom.Settings}
     */
    properties: function (target, names) {
        var originalNames = this.propertiesNames;

        if (typeof names == 'string') {
            names = names.split(' ');
        }

        if (names == null || names === true) {
            this.propertiesNames = true;
        } else if (originalNames == null) {
            this.propertiesNames = names;
        } else if (originalNames !== true) {
            atom.array.append(originalNames, names);
        }

        this.propertiesTarget = target;

        for (var i in this.values) {
            this.exportProperty(i, this.values);
        }

        return this;
    },

    subset: function (names, defaultValue) {
        var i, values = {};

        for (i = names.length; i--;) {
            values[names[i]] = this.get( names[i], defaultValue );
        }

        return values;
    },

    /** @private */
    propertiesNames : null,
    /** @private */
    propertiesTarget: null,

    /**
     * @param {Object} options
     * @return atom.Options
     */
    set: function (options, value) {
        var i, values = this.values;

        options = this.prepareOptions(options, value);

        for (i in options) {
            value = options[i];
            if (values[i] != value) {
                values[i] = value;
                this.exportProperty(i, values);
            }
        }

        this.invokeEvents();

        return this;
    },

    /** @private */
    exportProperty: function (i, values) {
        var
            target = this.propertiesTarget,
            names  = this.propertiesNames;

        if (target && (names === true || names.indexOf(i) >= 0)) {
            target[i] = values[i];
        }
    },

    /** @private */
    prepareOptions: function (options, value) {
        if (typeof options == 'string') {
            var i = options;
            options = {};
            options[i] = value;
        } else if (options instanceof this.constructor) {
            options = options.values;
        }
        return options;
    },

    /**
     * @param {String} name
     * @return atom.Options
     */
    unset: function (name) {
        delete this.values[name];
        return this;
    },

    /** @private */
    invokeEvents: function () {
        if (!this.events) return this;

        var values = this.values, name, option;
        for (name in values) if (values.hasOwnProperty(name)) {
            option = values[name];
            if (this.isInvokable(name, option)) {
                this.events.add(name, option);
                this.unset(name);
            }
        }
        return this;
    },

    /** @private */
    isInvokable: function (name, option) {
        return name &&
            option &&
            coreIsFunction(option) &&
            (/^on[A-Z]/).test(name);
    }
});

var Settings = atom.Settings;

/*
---

name: "Types.Object"

description: "Object generic methods"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core

provides: Types.Object

...
*/

atom.object = {
    append: function (target, source1, source2) {
        for (var i = 1, l = arguments.length; i < l; i++) {
            atom.core.append(target, arguments[i]);
        }
        return target;
    },
    invert: function (object) {
        var newObj = {};
        for (var i in object) newObj[object[i]] = i;
        return newObj;
    },
    collect: function (obj, props, Default) {
        var newObj = {};
        props.forEach(function (i){
            newObj[i] = i in obj ? obj[i] : Default;
        });
        return newObj;
    },
    values: function (obj) {
        var values = [];
        for (var i in obj) values.push(obj[i]);
        return values;
    },
    /** @deprecated */
    isDefined: function (obj) {
        return typeof obj !== 'undefined';
    },
    /** @deprecated */
    isReal: function (obj) {
        return obj != null;
    },
    map: function (obj, fn) {
        var mapped = {};
        for (var i in obj) if (obj.hasOwnProperty(i)) {
            mapped[i] = fn( obj[i], i, obj );
        }
        return mapped;
    },
    max: function (obj) {
        var max = null, key = null;
        for (var i in obj) if (max == null || obj[i] > max) {
            key = i;
            max = obj[i];
        }
        return key;
    },
    min: function (obj) {
        var min = null, key = null;
        for (var i in obj) if (min == null || obj[i] < min) {
            key = i;
            min = obj[i];
        }
        return key;
    },
    deepEquals: function (first, second) {
        if (!first || (typeof first) !== (typeof second)) return false;

        for (var i in first) {
            var f = first[i], s = second[i];
            if (typeof f === 'object') {
                if (!s || !Object.deepEquals(f, s)) return false;
            } else if (f !== s) {
                return false;
            }
        }

        for (i in second) if (!(i in first)) return false;

        return true;
    },
    isEmpty: function (object) {
        for (var i in object) if (object.hasOwnProperty(i)) {
            return false;
        }
        return true;
    },
    ifEmpty: function (object, key, defaultValue) {
        if (!(key in object)) {
            object[key] = defaultValue;
        }
        return object;
    },
    path: {
        parts: function (path, delimiter) {
            return Array.isArray(path) ? path : String(path).split( delimiter || '.' );
        },
        get: function (object, path, delimiter) {
            if (!path) return object;

            path = atom.object.path.parts( path, delimiter );

            for (var i = 0; i < path.length; i++) {
                if (object != null && path[i] in object) {
                    object = object[path[i]];
                } else {
                    return;
                }
            }

            return object;
        },
        set: function (object, path, value, delimiter) {
            path = atom.object.path.parts( path, delimiter );

            var key = path.pop();

            while (path.length) {
                var current = path.shift();
                if (object[current]) {
                    object = object[current];
                } else {
                    object = object[current] = {};
                }
            }

            object[key] = value;
        }
    }
};

/*
---

name: "Animatable"

description: "Provides Color class"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - declare
    - frame
    - Transition
    - Events
    - Settings
    - Types.Object

provides: Animatable

...
*/

/** @class atom.Animatable */
declare( 'atom.Animatable', {
    
    element: null,

    initialize: function (callbacks, context) {
        this.bindMethods('animate');
        this.context = context || null;

        if (!callbacks) throw new TypeError( 'callbacks cant be null' );

        this.animations = [];
        if (this.isValidCallbacks(callbacks)) {
            this.callbacks = callbacks;
        } else {
            this.callbacks = this.getDefaultCallbacks(callbacks);
        }
    },

    get current () {
        return this.animations[0];
    },

    /**
     * Binded to `Animatable`
     * @returns {atom.Animatable.Animation}
     */
    animate: atom.core.ensureObjectSetter(function (properties) {
        return this.next(new atom.Animatable.Animation(this, properties));
    }),

    stop: function (all) {
        var current = this.current;
        if (current) {
            if (all) this.animations.length = 0;
            current.destroy('stop');
        }
        return this;
    },

    /** @private */
    getDefaultCallbacks: function (element) {
        return {
            get: function (property) {
                return atom.object.path.get(element, property);
            },
            set: atom.core.overloadSetter(function (property, value) {
                return atom.object.path.set(element, property, value);
            })
        };
    },
    /** @private */
    isValidCallbacks: function (callbacks) {
        return typeof callbacks == 'object' &&
            Object.keys(callbacks).length == 2 &&
            coreIsFunction(callbacks.set) &&
            coreIsFunction(callbacks.get);
    },

    /** @private */
    animations: null,

    /** @private */
    next: function (animation) {
        var queue = this.animations;
        if (animation) {
            queue.push(animation);
            if (queue.length == 1) {
                this.launch(animation);
            }
        } else if (queue.length) {
            this.launch(this.current);
        }
        return animation;
    },
    /** @private */
    launch: function (animation) {
        var queue = this.animations, animatable = this;
        animation.events.add('destroy', function remove () {
            queue.splice(queue.indexOf(animation), 1);
            animation.events.remove('destroy', remove);
            animatable.next();
        });
        animation.start();
    },
    /** @private */
    get: function (name) {
        return this.callbacks.get.apply(this.context, arguments);
    },
    /** @private */
    set: function (name, value) {
        return this.callbacks.set.apply(this.context, arguments);
    }
});

/** @class atom.Animatable.Animation */
declare( 'atom.Animatable.Animation', {
    /** @property {atom.Animatable} */
    animatable: null,

    /**
     * initial values of properties
     * @property {Object}
     */
    initial: null,

    /**
     * target values of properties
     * @property {Object}
     */
    target: null,

    initialize: function (animatable, settings) {
        this.bindMethods([ 'tick', 'start' ]);

        if (!settings.props) settings = {props: settings};
        this.events   = new atom.Events(animatable);
        this.settings = new atom.Settings({
                fn  : 'linear',
                time: 500
            })
            .set(settings)
            .addEvents(this.events);
        this.animatable = animatable;
        this.transition = atom.Transition.get(this.settings.get('fn'));
        this.allTime = this.settings.get('time');
        this.target  = this.settings.get('props');
    },

    start: function () {
        this.initial  = this.fetchInitialValues();
        this.delta    = this.countValuesDelta();
        this.timeLeft = this.allTime;
        this.events.fire( 'start', [ this ]);
        atom.frame.add(this.tick);
        return this;
    },

    /** @private */
    countValuesDelta: function () {
        var initial = this.initial;
        return atom.object.map(this.target, function (value, key) {
            var start = initial[key];
            if (atom.Color && start instanceof atom.Color) {
                return start.diff( new atom.Color(value) );
            } else {
                return value - start;
            }
        });
    },

    /** @private */
    fetchInitialValues: function () {
        var animatable = this.animatable;
        return atom.object.map(this.target, function (value, key) {
            var v = animatable.get(key);
            if (atom.Color && atom.Color.isColorString(value) || value instanceof atom.Color) {
                if (!v) {
                    v = new atom.Color(value);
                    v.alpha = 0;
                    return v;
                }
                return new atom.Color(v);
            } else if (isNaN(v)) {
                throw new Error('value is not animatable: ' + v);
            } else {
                return v;
            }
        });
    },

    /** @private */
    changeValues: function (progress) {
        var delta = this.delta, animatable = this.animatable, initial, target;
        for (var i in delta) if (delta.hasOwnProperty(i)) {
            if (progress == null) {
                target = this.target[i];
                animatable.set( i,
                    atom.Color && target instanceof atom.Color
                        ? target.toString() : target
                );
            } else {
                initial = this.initial[i];
                animatable.set( i,
                    atom.Color && initial instanceof atom.Color ?
                        initial.clone().move(delta[i].clone().mul(progress)).toString() :
                        initial + delta[i] * progress
                );
            }
        }
    },

    /** @private */
    tick: function (time) {
        var lastTick = time >= this.timeLeft;
        this.timeLeft = lastTick ? 0 : this.timeLeft - time;

        this.changeValues(this.transition(
            lastTick ? 1 : (this.allTime - this.timeLeft) / this.allTime
        ));
        this.events.fire( 'tick', [ this ]);

        if (lastTick) this.destroy('complete');
    },

    destroy: function (type) {
        if (!type) type = 'error';
        this.events.fire( type, [ this ]);
        this.events.fire( 'destroy', [ this ]);
        atom.frame.remove(this.tick);
        return this;
    }
});

if (atom.dom) (function (animatable) {
    var accessors = {
        get: function (name) {
            var value = this.css(name);
            return atom.Color && atom.Color.isColorString(value) ? value : parseFloat(value);
        },
        set: function (name, value) {
            this.css(name, value);
        }
    };

    atom.dom.prototype.animate = atom.core.ensureObjectSetter(function (params) {
        this.each(function (elem) {
            if (!elem[animatable]) {
                elem[animatable] = new atom.Animatable(accessors, atom.dom(elem));
            }
            elem[animatable].animate(params);
        });
        return this
    });

    atom.dom.prototype.stopAnimation = function (force) {
        this.each(function (elem) {
            if (elem[animatable]) {
                elem[animatable].stop(force);
            }
        });
        return this;
    };
})('atom.animatable');

/*
---

name: "ClassCompat"

description: "Contains the Class Function for easily creating, extending, and implementing reusable Classes."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - CoreExtended
    - declare

provides: ClassCompat
...
*/

declare( 'atom.Settings.Mixin',
/** @deprecated */
{
    /**
     * @private
     * @property atom.Settings
     */
    settings: null,
    options : {},

    setOptions: function (options) {
        if (!this.settings) {
            this.settings = new atom.Settings(
                atom.clone(this.options || {})
            );
            this.options = this.settings.values;
        }

        for (var i = 0; i < arguments.length; i++) {
            this.settings.set(arguments[i]);
        }

        return this;
    }
});

declare( 'atom.Events.Mixin', new function () {
    var init = function () {
        var events = this.__events;
        if (!events) events = this.__events = new atom.Events(this);
        if (this._events) {
            for (var name in this._events) if (name != '$ready') {
                this._events[name].forEach(function (fn) {
                    events.add(name, fn);
                });
            }
        }
        return events;
    };

    var method = function (method, useReturn) {
        return function () {
            var result, events = init.call(this);

            result = events[method].apply( events, arguments );
            return useReturn ? result : this;
        }
    };

    return {
        get events ( ) { return init.call(this); },
        set events (e) { this.__events = e;       },
        isEventAdded: method( 'exists', true ),
        addEvent    : method( 'add'   , false ),
        removeEvent : method( 'remove', false ),
        fireEvent   : method( 'fire'  , false ),
        readyEvent  : method( 'ready' , false )
    };
});

/*
---

name: "Color"

description: "Provides Color class"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - declare

provides: Color

...
*/
/** @class atom.Color */
declare( 'atom.Color', {
    initialize: function (value) {
        var a = arguments, type;
        if (a.length == 4 || a.length == 3) {
            value = slice.call(a);
        } else if (value && value.length == 1) {
            value = value[0];
        }

        type = typeof value;
        if (Array.isArray(value)) {
            this.fromArray(value);
        } else if (type == 'number') {
            this.fromNumber(value);
        } else if (type == 'string') {
            this.fromString(value);
        } else if (type == 'object') {
            this.fromObject(value);
        } else {
            throw new TypeError('Unknown type in atom.Color: ' + typeof value + ';\n' + value);
        }
    },

    /** @private */
    r: 0,
    /** @private */
    g: 0,
    /** @private */
    b: 0,
    /** @private */
    a: 1,

    /**
     * We are array-like object (looks at accessors at bottom of class)
     * @constant
     */
    length: 4,

    noLimits: false,

    get red   () { return this.r; },
    get green () { return this.g; },
    get blue  () { return this.b; },
    get alpha () { return this.a; },

    set red   (v) { this.setValue('r', v) },
    set green (v) { this.setValue('g', v) },
    set blue  (v) { this.setValue('b', v) },
    set alpha (v) { this.setValue('a', v, true) },

    /** @private */
    safeAlphaSet: function (v) {
        if (v != null) {
            this.alpha = Math.round(v*1000)/1000;
        }
    },

    /** @private */
    setValue: function (prop, value, isFloat) {
        value = Number(value);
        if (value != value) { // isNaN
            throw new TypeError('Value is NaN (' + prop + '): ' + value);
        }

        if (!isFloat) value = Math.round(value);
        // We don't want application down, if user script (e.g. animation)
        // generates such wrong array: [150, 125, -1]
        // `noLimits` switch off this check
        this[prop] = this.noLimits ? value :
            atom.number.limit( value, 0, isFloat ? 1 : 255 );
    },

    // Parsing

    /**
     * @param {int[]} array
     * @returns {atom.Color}
     */
    fromArray: function (array) {
        if (!array || array.length < 3 || array.length > 4) {
            throw new TypeError('Wrong array in atom.Color: ' + array);
        }
        this.red   = array[0];
        this.green = array[1];
        this.blue  = array[2];
        this.safeAlphaSet(array[3]);
        return this;
    },
    /**
     * @param {Object} object
     * @param {number} object.red
     * @param {number} object.green
     * @param {number} object.blue
     * @returns {atom.Color}
     */
    fromObject: function (object) {
        if (typeof object != 'object') {
            throw new TypeError( 'Not object in "fromObject": ' + typeof object );
        }

        function fetch (p1, p2) {
            return object[p1] != null ? object[p1] : object[p2]
        }

        this.red   = fetch('r', 'red'  );
        this.green = fetch('g', 'green');
        this.blue  = fetch('b', 'blue' );
        this.safeAlphaSet(fetch('a', 'alpha'));
        return this;
    },
    /**
     * @param {string} string
     * @returns {atom.Color}
     */
    fromString: function (string) {
        if (!this.constructor.isColorString(string)) {
            throw new TypeError( 'Not color string in "fromString": ' + string );
        }

        var hex, array;

        string = string.toLowerCase();
        string = this.constructor.colorNames[string] || string;

        if (hex = string.match(/^#(\w{1,2})(\w{1,2})(\w{1,2})(\w{1,2})?$/)) {
            array = atom.array.clean(hex.slice(1));
            array = array.map(function (part) {
                if (part.length == 1) part += part;
                return parseInt(part, 16);
            });
            if (array.length == 4) array[3] /= 255;
        } else {
            array = string.match(/([\.\d]{1,})/g).map( Number );
        }
        return this.fromArray(array);
    },
    /**
     * @param {number} number
     * @returns {atom.Color}
     */
    fromNumber: function (number) {
        if (typeof number != 'number' || number < 0 || number > 0xffffffff) {
            throw new TypeError( 'Not color number in "fromNumber": ' + (number.toString(16)) );
        }

        return this.fromArray([
            (number>>24) & 0xff,
            (number>>16) & 0xff,
            (number>> 8) & 0xff,
            (number      & 0xff) / 255
        ]);
    },

    // Casting

    /** @returns {int[]} */
    toArray: function () {
        return [this.r, this.g, this.b, this.a];
    },
    /** @returns {string} */
    toString: function (type) {
        var arr = this.toArray();
        if (type == 'hex' || type == 'hexA') {
            return '#' + arr.map(function (color, i) {
                if (i == 3) { // alpha
                    if (type == 'hex') return '';
                    color = Math.round(color * 255);
                }
                var bit = color.toString(16);
                return bit.length == 1 ? '0' + bit : bit;
            }).join('');
        } else {
            return 'rgba(' + arr + ')';
        }
    },
    /** @returns {number} */
    toNumber: function () {
        // maybe needs optimizations
        return parseInt( this.toString('hexA').substr(1) , 16)
    },
    /** @returns {object} */
    toObject: function (abbreviationNames) {
        return abbreviationNames ?
            { r  : this.r, g    : this.g, b   : this.b, a    : this.a } :
            { red: this.r, green: this.g, blue: this.b, alpha: this.a };
    },

    // manipulations

    /**
     * @param {atom.Color} color
     * @returns {atom.Color}
     */
    diff: function (color) {
        // we can't use this.constructor, because context exists in such way
        // && invoke is not called
        color = atom.Color( color );
        return new atom.Color.Shift([
            color.red   - this.red  ,
            color.green - this.green,
            color.blue  - this.blue ,
            color.alpha - this.alpha
        ]);
    },
    /**
     * @param {atom.Color} color
     * @returns {atom.Color}
     */
    move: function (color) {
        color = atom.Color.Shift(color);
        this.red   += color.red  ;
        this.green += color.green;
        this.blue  += color.blue ;
        this.alpha += color.alpha;
        return this;
    },
    /** @deprecated - use `clone`+`move` instead */
    shift: function (color) {
        return this.clone().move(color);
    },
    map: function (fn) {
        var color = this;
        ['red', 'green', 'blue', 'alpha'].forEach(function (component) {
            color[component] = fn.call( color, color[component], component, color );
        });
        return color;
    },
    add: function (factor) {
        return this.map(function (value) {
            return value + factor;
        });
    },
    mul: function (factor) {
        return this.map(function (value) {
            return value * factor;
        });
    },
    /**
     * @param {atom.Color} color
     * @returns {boolean}
     */
    equals: function (color) {
        return color &&
            color instanceof this.constructor &&
            color.red   == this.red   &&
            color.green == this.green &&
            color.blue  == this.blue  &&
            color.alpha == this.alpha;
    },

    /** @private */
    dump: function () {
        return '[atom.Color(' + this.toString('hexA') + ')]';
    },

    /**
     * @returns {atom.Color}
     */
    clone: function () {
        return new this.constructor(this);
    }
}).own({
    invoke: declare.castArguments,

    /**
     * Checks if string is color description
     * @param {string} string
     * @returns {boolean}
     */
    isColorString : function (string) {
        if (typeof string != 'string') return false;
        return Boolean(
            string in this.colorNames  ||
            string.match(/^#\w{3,6}$/) ||
            string.match(/^rgba?\([\d\., ]+\)$/)
        );
    },

    colorNames: {
        white:  '#ffffff',
        silver: '#c0c0c0',
        gray:   '#808080',
        black:  '#000000',
        red:    '#ff0000',
        maroon: '#800000',
        yellow: '#ffff00',
        olive:  '#808000',
        lime:   '#00ff00',
        green:  '#008000',
        aqua:   '#00ffff',
        teal:   '#008080',
        blue:   '#0000ff',
        navy:   '#000080',
        fuchsia:'#ff00ff',
        purple: '#800080',
        orange: '#ffa500'
    },

    /**
     * @param {boolean} [html=false] - only html color names
     * @returns {atom.Color}
     */
    random: function (html) {
        var source, random = atom.number.random;

        if (html) {
            source = atom.array.random( this.colorNamesList );
        } else {
            source = [ random(0, 255), random(0, 255), random(0, 255) ];
        }

        return new this(source);
    }
});

atom.Color.colorNamesList = Object.keys(atom.Color.colorNames);

/** @class atom.Color.Shift */
declare( 'atom.Color.Shift', atom.Color, { noLimits: true });

/*
---

name: "ImagePreloader"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - declare
    - Events
    - Settings

provides: ImagePreloader

...
*/

atom.declare( 'atom.ImagePreloader', {
    processed : 0,
    number    : 0,

    initialize: function (settings) {
        this.events   = new Events(this);
        this.settings = new Settings(settings).addEvents(this.events);

        this.count = {
            error: 0,
            abort: 0,
            load : 0
        };

        this.suffix    = this.settings.get('suffix') || '';
        this.usrImages = this.prefixImages(this.settings.get('images'));
        this.imageUrls = this.fetchUrls();
        this.domImages = {};
        //this.domImages = this.createDomImages();
        this.images    = {};
        this.createNext();
    },
    get isReady () {
        return this.number == this.processed;
    },
    get info () {
        var stat = atom.string.substitute(
            "Images loaded: {load}; Errors: {error}; Aborts: {abort}",
            this.count
        );
        if (this.isReady) stat = "Image preloading has completed;\n" + stat;
        return stat;
    },
    get progress () {
        return this.isReady ? 1 : atom.number.round(this.processed / this.number, 4);
    },
    append: function (preloader) {
        for (var i in preloader.images) {
            this.images[i] = preloader.images[i];
        }
        return this;
    },
    exists: function (name) {
        return !!this.images[name];
    },
    get: function (name) {
        var image = this.images[name];
        if (image) {
            return image;
        } else {
            throw new Error('No image «' + name + '»');
        }
    },

    /** @private */
    cropImage: function (img, c) {
        if (!c) return img;

        var canvas = document.createElement('canvas');
        canvas.width  = c[2];
        canvas.height = c[3];
        canvas.getContext('2d').drawImage( img,
            c[0], c[1], c[2], c[3], 0, 0, c[2], c[3]
        );
        return canvas;
    },
    /** @private */
    withoutPrefix: function (src) {
        return src.indexOf('http://') === 0 || src.indexOf('https://') === 0;
    },
    /** @private */
    prefixImages: function (images) {
        var prefix = this.settings.get('prefix');
        if (!prefix) return images;

        return atom.object.map(images, function (src) {
            return this.withoutPrefix(src) ? src : prefix + src;
        }.bind(this));
    },
    /** @private */
    cutImages: function () {
        var i, parts, img;
        for (i in this.usrImages) if (this.usrImages.hasOwnProperty(i)) {
            parts = this.splitUrl( this.usrImages[i] );
            img   = this.domImages[ parts.url ];
            this.images[i] = this.cropImage(img, parts.coords);
        }
        return this;
    },
    /** @private */
    splitUrl: function (str) {
        var url = str, size, cell, match, coords = null;

                // searching for pattern 'url [x:y:w:y]'
        if (match = str.match(/ \[(\d+):(\d+):(\d+):(\d+)\]$/)) {
            coords = match.slice( 1 );
                // searching for pattern 'url [w:y]{x:y}'
        } else if (match = str.match(/ \[(\d+):(\d+)\]\{(\d+):(\d+)\}$/)) {
            coords = match.slice( 1 ).map( Number );
            size = coords.slice( 0, 2 );
            cell = coords.slice( 2, 4 );
            coords = [ cell[0] * size[0], cell[1] * size[1], size[0], size[1] ];
        }
        if (match) {
            url = str.substr(0, str.lastIndexOf(match[0]));
            coords = coords.map( Number );
        }
        if (this.suffix) {
            if (typeof this.suffix == 'function') {
                url = this.suffix( url );
            } else {
                url += this.suffix;
            }
        }

        return { url: url, coords: coords };
    },
    /** @private */
    fetchUrls: function () {
        var i, result = [], hash = {}, url, images = this.usrImages;
        for (i in images) if (images.hasOwnProperty(i)) {
            url = this.splitUrl( images[i] ).url;
            if (!hash[url]) {
                result.push(url);
                hash[url] = true;
                this.number++;
            }
        }
        return result;
    },
    /** @private */
    createDomImage : function (src) {
        var img = new Image();
        img.src = src;
        if (window.opera && img.complete) {
            setTimeout(this.onProcessed.bind(this, 'load', img), 10);
        } else {
            ['load', 'error', 'abort'].forEach(function (event) {
                img.addEventListener( event, this.onProcessed.bind(this, event, img), false );
            }.bind(this));
        }
        return img;
    },
    createNext: function () {
        if (this.imageUrls.length) {
            var url = this.imageUrls.shift();
            this.domImages[url] = this.createDomImage(url);
        }
    },
    resetImage: function (img) {
        // opera fullscreen bug workaround
        img.width  = img.width;
        img.height = img.height;
        img.naturalWidth  = img.naturalWidth;
        img.naturalHeight = img.naturalHeight;
    },
    /** @private */
    onProcessed : function (type, img) {
        if (type == 'load' && window.opera) {
            this.resetImage(img);
        }
        this.count[type]++;
        this.processed++;
        this.events.fire('progress', [this, img]);

        if (this.isReady) {
            this.cutImages();
            this.events.ensureReady('ready', [this]);
        } else {
            this.createNext();
        }
        return this;
    }
}).own({
    run: function (images, callback, context) {
        var preloader = new this({ images: images });

        preloader.events.add( 'ready', context ? callback.bind(context) : callback );

        return preloader;
    }
});

/*
---

name: "Keyboard"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - declare
    - Events

provides: Keyboard

...
*/

var Keyboard = function () {

var
    keyName,
    codeNames = {},
    keyCodes  = {
        // Alphabet
        a:65, b:66, c:67, d:68, e:69,
        f:70, g:71, h:72, i:73, j:74,
        k:75, l:76, m:77, n:78, o:79,
        p:80, q:81, r:82, s:83, t:84,
        u:85, v:86, w:87, x:88, y:89, z:90,
        // Numbers
        n0:48, n1:49, n2:50, n3:51, n4:52,
        n5:53, n6:54, n7:55, n8:56, n9:57,
        // Controls
        tab:  9, enter:13, shift:16, backspace:8,
        ctrl:17, alt  :18, esc  :27, space    :32,
        menu:93, pause:19, cmd  :91,
        insert  :45, home:36, pageup  :33,
        'delete':46, end :35, pagedown:34,
        // F*
        f1:112, f2:113, f3:114, f4 :115, f5 :116, f6 :117,
        f7:118, f8:119, f9:120, f10:121, f11:122, f12:123,
        // numpad
        np0: 96, np1: 97, np2: 98, np3: 99, np4:100,
        np5:101, np6:102, np7:103, np8:104, np9:105,
        npslash:11,npstar:106,nphyphen:109,npplus:107,npdot:110,
        // Lock
        capslock:20, numlock:144, scrolllock:145,

        // Symbols
        equals: 61, hyphen   :109, coma  :188, dot:190,
        gravis:192, backslash:220, sbopen:219, sbclose:221,
        slash :191, semicolon: 59, apostrophe: 222,

        // Arrows
        aleft:37, aup:38, aright:39, adown:40
    };

for (keyName in keyCodes) if (keyCodes.hasOwnProperty(keyName)) {
    codeNames[ keyCodes[keyName] ] = keyName;
}

/** @class atom.Keyboard */
return declare( 'atom.Keyboard', {
    initialize : function (element, preventDefault) {
        if (Array.isArray(element)) {
            preventDefault = element;
            element = null;
        }
        if (element == null) element = document;

        if (element == document) {
            if (this.constructor.instance) {
                return this.constructor.instance;
            }
            this.constructor.instance = this;
        }

        this.events = new Events(this);
        this.keyStates = {};
        this.preventDefault = preventDefault;

        atom.dom(element).bind({
            keyup:    this.keyEvent('up'),
            keydown:  this.keyEvent('down'),
            keypress: this.keyEvent('press')
        });
    },
    /** @private */
    keyEvent: function (event) {
        return this.onKeyEvent.bind(this, event);
    },
    /** @private */
    onKeyEvent: function (event, e) {
        var key = this.constructor.keyName(e),
            prevent = this.prevent(key);

        e.keyName = key;

        if (prevent) e.preventDefault();
        this.events.fire( event, [e] );

        if (event == 'down') {
            this.events.fire(key, [e]);
            this.keyStates[key] = true;
        } else if (event == 'up') {
            this.events.fire(key + ':up', [e]);
            delete this.keyStates[key];
        } else if (event == 'press') {
            this.events.fire(key + ':press', [e]);
        }

        return !prevent;
    },
    /** @private */
    prevent : function (key) {
        var pD = this.preventDefault;
        return pD && (pD === true || pD.indexOf(key) >= 0);
    },
    key: function (keyName) {
        return !!this.keyStates[ this.constructor.keyName(keyName) ];
    }
}).own({
    keyCodes : keyCodes,
    codeNames: codeNames,
    keyName: function (code) {
        if (code && code.keyCode != null) {
            code = code.keyCode;
        }

        var type = typeof code;

        if (type == 'number') {
            return this.codeNames[code];
        } else if (type == 'string' && code in this.keyCodes) {
            return code;
        }

        return null;
    }
});

}();


/*
---

name: "Registry"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - declare

provides: Registry

...
*/

/** @class atom.Registry */
declare( 'atom.Registry', {
    items: {},
    initialize: function (initial) {
        this.items = {};
        if (initial) this.set(initial);
    },
    set: atom.core.overloadSetter(function (name, value) {
        this.items[name] = value;
    }),
    get: atom.core.overloadGetter(function (name) {
        return this.items[name];
    })
});

var Registry = atom.Registry;

/*
---

name: "trace"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - declare
    - dom
    - CoreExtended

provides: trace

...
*/

atom.trace = declare( 'atom.trace', {
    initialize : function (object) {
        this.value = object;
        this.stopped = false;
    },
    set value (value) {
        if (!this.stopped) {
            var html = atom.string.replaceAll( this.constructor.dump(value), {
                '\t': '&nbsp;'.repeat(3),
                '\n': '<br />'
            });
            this.createNode().html(html);
        }
    },
    destroy : function (force) {
        var trace = this;
        if (force) this.stop();
        if (trace.node) {
            trace.node.addClass('atom-trace-node-destroy');
            trace.timeout = setTimeout(function () {
                if (trace.node) {
                    trace.node.destroy();
                    trace.node = null;
                }
            }, 500);
        }
        return trace;
    },
    /** @private */
    stop  : function () {
        this.stopped = true;
        return this;
    },
    /** @private */
    getContainer : function () {
        var cont = atom.dom('#atom-trace-container');
        return cont.length ? cont :
            atom.dom.create('div', { 'id' : 'atom-trace-container'})
                .appendTo('body');
    },
    /** @deprecated */
    trace : function (value) {
        this.value = value;
        return this;
    },
    /** @private */
    createNode : function () {
        var trace = this, node = trace.node;

        if (node) {
            if (trace.timeout) {
                clearTimeout(trace.timeout);
                node.removeClass('atom-trace-node-destroy');
            }
            return node;
        }

        return trace.node = atom.dom
            .create('div')
            .addClass('atom-trace-node')
            .appendTo(trace.getContainer())
            .bind({
                click    : function () { trace.destroy(0) },
                dblclick : function () { trace.destroy(1) }
            });
    }
}).own({
    dumpRec : function dumpRec (obj, level, plain) {
        var html = '', type, tabs;

        level  = parseInt(level) || 0;

        if (level > 5) return '*TOO_DEEP*';

        if (obj && typeof obj == 'object' && coreIsFunction(obj.dump)) return obj.dump();

        function escape (v) {
            return plain ? v : atom.string.safeHtml(v);
        }

        function subDump (elem, index) {
            return tabs + '\t' + index + ': ' + dumpRec(elem, level+1, plain) + '\n';
        }

        type = atom.typeOf(obj);
        tabs = '\t'.repeat(level);

        switch (type) {
            case 'object':
                for (var index in obj) if (obj.hasOwnProperty(index)) {
                    html += subDump(obj[index], index);
                }
                return '{\n' + html + tabs + '}';

            case 'element':
                var prop = (obj.width && obj.height) ? '('+obj.width+'×'+obj.height+')' : '';
                return '[DOM ' + obj.tagName.toLowerCase() + prop + ']';

            case 'textnode':
            case 'whitespace':
                return '[DOM ' + type + ']';

            case 'array'  : return '[\n' + obj.map(subDump).join('') + tabs + ']';
            case 'null'   : return 'null';
            case 'boolean': return obj ? 'true' : 'false';
            case 'string' : return escape('"' + obj + '"');
            default       : return escape('' + obj);
        }
    },
    dumpPlain: function (object) {
        return (this.dumpRec(object, 0, true));
    },
    dump : function (object) {
        return (this.dumpRec(object, 0));
    }
});

/*
---

name: "Types.Number"

description: "Contains number-manipulation methods like limit, round, times, and ceil."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core

provides: Types.Number

...
*/

atom.number = {
    randomFloat: function (max, min) {
        return Math.random() * (max - min) + min;
    },
    random : function (min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    },
    between: function (number, n1, n2, equals) {
        number = Number(number);
        n1 = Number(n1);
        n2 = Number(n2);
        return (n1 <= n2) && (
            (equals == 'L' && number == n1) ||
            (equals == 'R' && number == n2) ||
            (number  > n1  && number  < n2) ||
            ([true,'LR','RL'].indexOf(equals) != -1 && (n1 == number || n2 == number))
        );
    },
    equals : function (number, to, accuracy) {
        if (accuracy == null) accuracy = 8;
        return number.toFixed(accuracy) == to.toFixed(accuracy);
    },
    limit: function(number, min, max){
        var bottom = Math.max(min, Number(number));
        return max != null ? Math.min(max, bottom) : bottom;
    },
    round: function(number, precision){
        if (!precision) return Math.round(number);

        if (precision < 0) {
            precision = Number( Math.pow(10, precision).toFixed( -precision ) );
        } else {
            precision = Math.pow(10, precision);
        }
        return Math.round(number * precision) / precision;
    },
    stop: function(num) {
        num = Number(num);
        if (num) {
            clearInterval(num);
            clearTimeout (num);
        }
        return this;
    }
};

/*
---

name: "Types.Array"

description: "Contains array-manipulation methods like include, contains, and erase."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - Types.Number

provides: Types.Array

...
*/

atom.array = {
    /**
     * Checks if arguments is array
     * @param {Array} array
     * @returns {boolean}
     */
    is: function (array) {
        return Array.isArray(array);
    },
    /**
     * Creates rangearray
     * @param {int} from
     * @param {int} to
     * @param {int} [step=1] - should be
     * @returns {int[]}
     */
    range: function (from, to, step) {
        from = Number(from);
        to   = Number(to  );
        step = Number(step);

        if (typeof from != 'number') throw new TypeError( '`from` should be number' );
        if (typeof to   != 'number') throw new TypeError(   '`to` should be number' );

        var increase = to > from, stepIncrease = step > 0;

        if (!step) {
            step = increase ? 1 : -1;
        } else if ( increase != stepIncrease ) {
            throw new RangeError( 'step direction is wrong' );
        }

        var result = [];
        do {
            result.push(from);
            from += step;
        } while (increase ? from <= to : from >= to);

        return result;
    },
    /**
     * @param {*} item
     * @returns {Array}
     */
    from: function (item) {
        if (item == null) return [];
        return (!coreIsArrayLike(item)) ? [item] :
            Array.isArray(item) ? item : slice.call(item);
    },
    /**
     * @private
     * @param {Array} args
     * @returns {Array}
     */
    pickFrom: function (args) {
        var fromZeroArgument = args && args.length == 1
            && coreIsArrayLike( args[0] );

        return atom.array.from( fromZeroArgument ? args[0] : args );
    },
    /**
     * @param {number|Array} array
     * @param {*} fill
     * @returns {Array}
     */
    fill: function (array, fill) {
        array = Array.isArray(array) ? array : new Array(Number(array));
        for (var i = array.length; i--;) array[i] = fill;
        return array;
    },
    /**
     * @param {number} width
     * @param {number} height
     * @param {*} fill
     * @returns {Array[]}
     */
    fillMatrix: function (width, height, fill) {
        var array = new Array(height);
        while (height--) {
            array[height] = Array.fill(width, fill);
        }
        return array;
    },
    /**
     * It returns array, atom.object.collect returns hash
     * @param {Object} source
     * @param {Array} props
     * @param {*} [defaultValue=undefined]
     * @returns {Array}
     */
    collect: function (source, props, defaultValue) {
        var array = [], i = 0, l = props.length, prop;
        for (;i < l; i++) {
            prop = props[i];
            array.push(prop in source ? source[prop] : defaultValue);
        }
        return array;
    },
    /**
     * @param {Number} length
     * @param {function} callback
     * @param {Object} [context=undefined]
     * @returns {Array}
     */
    create: function (length, callback, context) {
        if (!coreIsFunction(callback)) {
            throw new TypeError('callback should be function');
        }
        var array = new Array(Number(length));
        for (var i = 0; i < length; i++) {
            array[i] = callback.call(context, i, array);
        }
        return array;
    },
    /**
     * @param {Array} array
     * @returns {Object}
     */
    toHash: function (array) {
        var hash = {}, i = 0, l = array.length;
        for (; i < l; i++) {
            hash[i] = array[i];
        }
        return hash;
    },
    /**
     * @param {Array} array
     * @returns {*}
     */
    last: function (array) {
        return array.length ? array[array.length - 1] : null;
    },
    /**
     * @param {Array} array
     * @returns number
     */
    randomIndex: function (array) {
        if (array.length == 0) return null;

        return atom.number.random(0, array.length - 1);
    },
    /**
     * @param {Array} array
     * @param {boolean} erase - erase element after splice, or leave at place
     * @returns {*}
     */
    random: function (array, erase) {
        if (array.length == 0) return null;

        var index = atom.array.randomIndex(array);

        return erase ? array.splice(index, 1)[0] : array[index];
    },
    /**
     * Return array of property `name` values of objects
     * @param {Array} array
     * @param {string} name
     * @returns {Array}
     */
    property: function (array, name) {
        return array.map(function (elem) {
            return elem != null ? elem[ name ] : null;
        });
    },
    /** @deprecated - use `create` instead */
    fullMap: function (array, fn, bind) {
        var mapped = new Array(array.length);
        for (var i = 0, l = mapped.length; i < l; i++) {
            mapped[i] = fn.call(bind, array[i], i, array);
        }
        return mapped;
    },
    /**
     * Check, if array contains elem
     * @param {Array} array
     * @param {*} elem
     * @param {number} [fromIndex=0]
     * @returns {boolean}
     */
    contains: function (array, elem, fromIndex) {
        return array.indexOf(elem, fromIndex) != -1;
    },
    /**
     * Push element to array, if it doesn't contains such element
     * @param {Array} target
     * @param {*} item
     * @returns {Array} - target array
     */
    include: includeUnique,
    /**
     * Erase item from array
     * @param {Array} target
     * @param {*} item
     * @returns {Array} - target array
     */
    erase: coreEraseAll,
    /**
     * `push` source array values to the end of target array
     * @param {Array} target
     * @param {Array} source
     * @returns {Array} - target array
     */
    append: function (target, source) {
        for (var i = 1, l = arguments.length; i < l; i++) if (arguments[i]) {
            target.push.apply(target, arguments[i]);
        }
        return target;
    },
    /** @deprecated */
    toKeys: function (value) {
        var useValue = arguments.length == 1, obj = {};
        for (var i = 0, l = this.length; i < l; i++)
            obj[this[i]] = useValue ? value : i;
        return obj;
    },
    /**
     * `include` source array values to the end of target array
     * @param {Array} target
     * @param {Array} source
     * @returns {Array} - target array
     */
    combine: function(target, source){
        for (var i = 0, l = source.length; i < l; i++) {
            atom.array.include(target, source[i]);
        }
        return target;
    },
    /**
     * returns first not-null value, or returns null
     * @param {Array} source
     * @returns {*}
     */
    pick: function(source){
        for (var i = 0, l = source.length; i < l; i++) {
            if (source[i] != null) return source[i];
        }
        return null;
    },
    /**
     * You can invoke array of functions with context "context"
     * Or all methods of objects in array
     * all params except zero & first will be sed as argument
     * @param {Array} array
     * @param {Object|string} [context=null]
     * @returns {Array} - array of results
     */
    invoke: function(array, context){
        var args = slice.call(arguments, 2);
        if (typeof context == 'string') {
            var methodName = context;
            context = null;
        }
        return array.map(function(item){
            return item && (methodName ? item[methodName] : item).apply(methodName ? item : context, args);
        });
    },
    /**
     * shuffle array with smart algorithm
     * @param {Array} array
     * @returns {Array}
     */
    shuffle : function (array) {
        var tmp, moveTo, index = array.length;
        while (index--) {
            moveTo = atom.number.random( 0, index );
            tmp           = array[index ];
            array[index]  = array[moveTo];
            array[moveTo] = tmp;
        }
        return array;
    },
    /**
     * sort array by property value or method returns
     * @param {Array} array
     * @param {string} method
     * @param {boolean} [reverse=false] (if true) first - smallest, last - biggest
     * @returns {Array}
     */
    sortBy : function (array, method, reverse) {
        var get = function (elem) {
            return (coreIsFunction(elem[method]) ? elem[method]() : elem[method]) || 0;
        };
        var multi = reverse ? -1 : 1;
        return array.sort(function ($0, $1) {
            var diff = get($1) - get($0);
            return diff ? (diff < 0 ? -1 : 1) * multi : 0;
        });
    },
    /**
     * Returns min value in array
     * @param {Array} array
     * @returns {Array}
     */
    min: function(array){
        return Math.min.apply(null, array);
    },
    /**
     * Returns max value in array
     * @param {Array} array
     * @returns {Array}
     */
    max: function(array){
        return Math.max.apply(null, array);
    },
    /**
     * Multiply all values in array to factor & returns result array
     * @param {Array} array
     * @param {number} factor
     * @returns {Array}
     */
    mul: function (array, factor) {
        for (var i = array.length; i--;) array[i] *= factor;
        return array;
    },
    /**
     * Add to all values in array number & returns result array
     * @param {Array} array
     * @param {number} number
     * @returns {Array}
     */
    add: function (array, number) {
        for (var i = array.length; i--;) array[i] += number;
        return array;
    },
    /**
     * Returns sum of all elements in array
     * @param {Array} array
     * @returns {number}
     */
    sum: function (array) {
        for (var result = 0, i = array.length; i--;) result += array[i];
        return result;
    },
    /**
     * Returns product (result of multiplying) of all elements in array
     * @param {Array} array
     * @returns {number}
     */
    product: function (array) {
        for (var result = 1, i = array.length; i--;) result *= array[i];
        return result;
    },
    /**
     * Returns average value in array ( sum / length )
     * @param {Array} array
     * @returns {number}
     */
    average: function (array) {
        return array.length ? atom.array.sum(array) / array.length : 0;
    },
    /**
     * returns array with only unique values ( [1,2,2,3] => [1,2,3] )
     * @param {Array} array
     * @returns {Array}
     */
    unique: function(array){
        return atom.array.combine([], array);
    },
    /**
     * associate array values with keys
     * if `keys` is array it used as keys names, and array used as values
     * if `keys` if function it used as function, generated values & array used as keys
     * @param {Array} array
     * @param {Function|Array} keys
     * @returns {Object}
     */
    associate: function(array, keys){
        var
            i = 0,
            obj = {},
            length = array.length,
            isFn = coreIsFunction(keys),
            keysSource = isFn ? array : keys;

        if (!isFn) length = Math.min(length, keys.length);
        for (;i < length; i++) {
            obj[ keysSource[i] ] = isFn ? keys(array[i], i) : array[i];
        }
        return obj;
    },
    /**
     * clean array from empty values & returns empty array
     * @param {Array} array
     * @returns {Array}
     */
    clean: function (array){
        return array.filter(function (item) { return item != null });
    },
    /**
     * quickly erase all values from array
     * @param {Array} array
     * @returns {Array}
     */
    empty: function (array) {
        array.length = 0;
        return array;
    },
    /** @deprecated */
    clone: function (array) { return atom.clone(array) },
    /**
     * @param array
     * @param {boolean} [asArray=false] - returns result as array, or as string
     * @returns {Array|string}
     */
    hexToRgb: function(array, asArray){
        if (array.length != 3) return null;
        var rgb = array.map(function(value){
            if (value.length == 1) value += value;
            return parseInt(value, 16);
        });
        return asArray ? rgb : 'rgb(' + rgb + ')';
    },
    /**
     * @param array
     * @param {boolean} [asArray=false] - returns result as array, or as string
     * @returns {Array|string}
     */
    rgbToHex: function(array, asArray) {
        if (array.length < 3) return null;
        if (array.length == 4 && array[3] == 0 && !asArray) return 'transparent';
        var hex = [], i = 0, bit;
        for (; i < 3; i++){
            bit = (array[i] - 0).toString(16);
            hex.push((bit.length == 1) ? '0' + bit : bit);
        }
        return asArray ? hex : '#' + hex.join('');
    },

    /**
     * @param {Array} array
     * @param {Function} callback
     * @param {*} value
     * @returns {*}
     */
    reduce: function(array, callback, value){
        if (coreIsFunction(array.reduce)) return array.reduce(callback, value);

        for (var i = 0, l = array.length; i < l; i++) if (i in array) {
            value = value === undefined ? array[i] : callback.call(null, value, array[i], i, array);
        }
        return value;
    },

    /**
     * @param {Array} array
     * @param {Function} callback
     * @param {*} value
     * @returns {*}
     */
    reduceRight: function(array, callback, value){
        if (coreIsFunction(array.reduceRight)) return array.reduceRight(callback, value);

        for (var i = array.length; i--;) if (i in array) {
            value = value === undefined ? array[i] : callback.call(null, value, array[i], i, array);
        }
        return value;
    }
};

/*
---

name: "Prototypes.Abstract"

description: "Contains office methods for prototypes extension."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - Types.Array
    - Types.Object

provides: Prototypes.Abstract

...
*/

var prototypize = {
    callbacks: [],
    fn: function (source) {
        return function (methodName) {
            return function () {
                var args = slice.call(arguments);
                args.unshift(this);
                return source[methodName].apply(source, args);
            };
        };
    },
    proto: function (object, proto, methodsString) {
        coreAppend(object.prototype, atom.array.associate(
            methodsString.split(' '), proto
        ));
        return prototypize;
    },
    own: function (object, source, methodsString) {
        coreAppend(object, atom.object.collect( source, methodsString.split(' ') ));
        return prototypize;
    },
    add: function (callback) {
        this.callbacks.push(callback);
    }
};

atom.patching = function (globalObject) {
    prototypize.callbacks.forEach(function (callback) {
        callback(globalObject);
    });
};

/*
---

name: "Prototypes.Array"

description: "Contains Array Prototypes like include, contains, and erase."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Types.Array
    - Prototypes.Abstract

provides: Prototypes.Array

...
*/

prototypize.add(function (globalObject) {

var Array = globalObject.Array;

var proto = prototypize.fn(atom.array);

prototypize
    .own(Array, atom.array, 'range from pickFrom fill fillMatrix collect create toHash')
    .proto(Array, proto, 'randomIndex property contains include append erase combine pick invoke shuffle sortBy min max mul add sum product average unique associate clean empty clone hexToRgb rgbToHex' );

atom.accessors.define(Array.prototype, {
    last  : { get: function () {
        return atom.array.last(this);
    }},
    random: { get: function () {
        return atom.array.random(this, false);
    }}
});

coreAppend(Array.prototype, {
    popRandom: function () {
        return atom.array.random(this, true);
    },
    /** @deprecated */
    toKeys: function () {
        console.log( '[].toKeys is deprecated. Use forEach instead' );
        return atom.array.toKeys(this);
    },
    /** @deprecated */
    fullMap: function (callback, context) {
        console.log( '[].fullMap is deprecated. Use atom.array.create instead' );
        return atom.array.create(this.length, callback, context);
    }
});

if (!Array.prototype.reduce     ) Array.prototype.reduce      = proto('reduce');
if (!Array.prototype.reduceRight) Array.prototype.reduceRight = proto('reduceRight');

});

/*
---

name: "Types.Function"

description: "Contains function manipulation methods."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - Types.Array

provides: Types.Function

...
*/

atom.fn = {
    lambda: function (value) {
        var returnThis = (arguments.length == 0);
        return function () { return returnThis ? this : value; };
    },

    after: function (onReady, fnName) {
        var after = {}, ready = {};
        function checkReady (){
            for (var i in after) if (!ready[i]) return;
            onReady(ready);
        }
        slice.call(arguments, 1).forEach(function (key) {
            after[key] = function () {
                ready[key] = slice.call(arguments);
                ready[key].context = this;
                checkReady();
            };
        });
        return after;
    }
};


/*
---

name: "Prototypes.Function"

description: "Contains Function Prototypes like after, periodical and delay."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core
    - Types.Function
    - Prototypes.Abstract

provides: Prototypes.Function

...
*/

prototypize.add(function (globalObject) {

    var Function = globalObject.Function;

    Function.lambda = atom.fn.lambda;

    function timer (periodical) {
        var set = periodical ? setInterval : setTimeout;

        return function (time, bind, args) {
            var fn = this;
            return set(function () {
                fn.apply( bind, args || [] );
            }, time);
        };
    }
    
    coreAppend(Function.prototype, {
        after: prototypize.fn(atom.fn)('after'),
        delay     : timer(false),
        periodical: timer(true )
    });

});


/*
---

name: "Types.Math"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core

provides: Types.Math

...
*/

(function () {

var
    degree = Math.PI / 180,
    deg360 = Math.PI * 2;

atom.math = {

    DEGREE360: deg360,

    /**
     * Cast degrees to radians
     * atom.math.degree(90) == Math.PI/2
     */
    degree: function (degrees) {
        return degrees * degree;
    },

    /**
     * Cast radians to degrees
     * atom.math.getDegree(Math.PI/2) == 90
     */
    getDegree: function (radians, round) {
        radians /= degree;

        return round ? Math.round(radians) : radians;
    },
    normalizeAngle : function (radians) {
        radians %= deg360;

        return radians + ( radians < 0 ? deg360 : 0 );
    },

    hypotenuse: function (cathetus1, cathetus2)  {
        return Math.sqrt(cathetus1*cathetus1 + cathetus2*cathetus2);
    },
    cathetus: function (hypotenuse, cathetus2)  {
        return Math.sqrt(hypotenuse*hypotenuse - cathetus2*cathetus2);
    }
};

})();


/*
---

name: "Prototypes.Number"

description: "Contains Number Prototypes like limit, round, times, and ceil."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Types.Number
    - Types.Math
    - Prototypes.Abstract

provides: Prototypes.Number

...
*/

prototypize.add(function (globalObject) {

var Number = globalObject.Number;

prototypize
    .own(Number, atom.number, 'random randomFloat')
    .proto(Number, prototypize.fn(atom.number), 'between equals limit round stop' )
    .proto(Number, prototypize.fn(atom.math  ), 'degree getDegree normalizeAngle' );

coreAppend(Number.prototype, {
    toFloat: function(){
        return parseFloat(this);
    },
    toInt: function(base){
        return parseInt(this, base || 10);
    }
});

'abs acos asin atan atan2 ceil cos exp floor log max min pow sin sqrt tan'
    .split(' ')
    .forEach(function(method) {
        if (Number[method]) return;
        
        Number.prototype[method] = function() {
            return Math[method].apply(null, [this].append(arguments));
        };
    });
});

/*
---

name: "Prototypes.Object"

description: "Object generic methods"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Types.Object

provides: Prototypes.Object

...
*/

prototypize.add(function (globalObject) {
    coreAppend(globalObject.Object, atom.object);
});

/*
---

name: "Types.String"

description: "Contains string-manipulation methods like repeat, substitute, replaceAll and begins."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Core

provides: Types.String

...
*/

new function () {

var UID = Date.now();

atom.string = {
    /**
     * @returns {string} - unique for session value in 36-radix
     */
    uniqueID: function () {
        return (UID++).toString(36);
    },
    /**
     * escape all html unsafe characters - & ' " < >
     * @param {string} string
     * @returns {string}
     */
    safeHtml: function (string) {
        return this.replaceAll(string, /[<'&">]/g, {
            '&'  : '&amp;',
            '\'' : '&#039;',
            '\"' : '&quot;',
            '<'  : '&lt;',
            '>'  : '&gt;'
        });
    },
    /**
     * repeat string `times` times
     * @param {string} string
     * @param {int} times
     * @returns {string}
     */
    repeat: function(string, times) {
        return new Array(times + 1).join(string);
    },
    /**
     * @param {string} string
     * @param {Object} object
     * @param {RegExp} [regexp=null]
     * @returns {string}
     */
    substitute: function(string, object, regexp){
        return string.replace(regexp || /\\?\{([^{}]+)\}/g, function(match, name){
            return (match[0] == '\\') ? match.slice(1) : (object[name] == null ? '' : object[name]);
        });
    },
    /**
     * @param {string} string
     * @param {Object|RegExp|string} find
     * @param {Object|string} [replace=null]
     * @returns {String}
     */
    replaceAll: function (string, find, replace) {
        if (toString.call(find) == '[object RegExp]') {
            return string.replace(find, function (symb) { return replace[symb]; });
        } else if (typeof find == 'object') {
            for (var i in find) string = this.replaceAll(string, i, find[i]);
            return string;
        }
        return string.split(find).join(replace);
    },
    /**
     * Checks if string contains such substring
     * @param {string} string
     * @param {string} substr
     */
    contains: function (string, substr) {
        return string ? string.indexOf( substr ) >= 0 : false;
    },
    /**
     * Checks if string begins with such substring
     * @param {string} string
     * @param {string} substring
     * @param {boolean} [caseInsensitive=false]
     * @returns {boolean}
     */
    begins: function (string, substring, caseInsensitive) {
        if (!string) return false;
        return (!caseInsensitive) ? substring == string.substr(0, substring.length) :
            substring.toLowerCase() == string.substr(0, substring.length).toLowerCase();
    },
    /**
     * Checks if string ends with such substring
     * @param {string} string
     * @param {string} substring
     * @param {boolean} [caseInsensitive=false]
     * @returns {boolean}
     */
    ends: function (string, substring, caseInsensitive) {
        if (!string) return false;
        return (!caseInsensitive) ? substring == string.substr(string.length - substring.length) :
            substring.toLowerCase() == string.substr(string.length - substring.length).toLowerCase();
    },
    /**
     * Uppercase first character
     * @param {string} string
     * @returns {string}
     */
    ucfirst : function (string) {
        return string ? string[0].toUpperCase() + string.substr(1) : '';
    },
    /**
     * Lowercase first character
     * @param {string} string
     * @returns {string}
     */
    lcfirst : function (string) {
        return string ? string[0].toLowerCase() + string.substr(1) : '';
    }
};

}();

/*
---

name: "Prototypes.String"

description: "Contains String Prototypes like repeat, substitute, replaceAll and begins."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

requires:
    - Types.String
    - Prototypes.Abstract

provides: Prototypes.String

...
*/

prototypize.add(function (globalObject) {
    prototypize.proto(globalObject.String, prototypize.fn(atom.string),
        'safeHtml repeat substitute replaceAll contains begins ends ucfirst lcfirst'
    );
});

}.call(typeof exports == 'undefined' ? window : exports, Object, Array)); 






/*
---

name: "LibCanvas"

description: "LibCanvas - free javascript library, based on AtomJS framework."

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

...
*/

(function (atom, Math) { // LibCanvas

// bug in Safari 5.1 ( 'use strict' + 'set prop' )
// 'use strict';

var undefined,
    /** @global {Object} global */
    global   = this,
    /** @global {Function} slice */
    slice    = [].slice,
    /** @global {Function} declare  */
    declare  = atom.declare,
    /** @global {Function} Registry  */
    Registry = atom.Registry,
    /** @global {Function} Events  */
    Events   = atom.Events,
    /** @global {Function} Settings  */
    Settings = atom.Settings;
/*
---

name: "LibCanvas"

description: "LibCanvas initialization"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

provides: LibCanvas

...
*/

var LibCanvas = this.LibCanvas = declare({ name: 'LibCanvas', prototype: {} })
    .own({
        Buffer: function () {
            return LibCanvas.buffer.apply( LibCanvas, arguments );
        },
        buffer: function (width, height, withCtx) {
            var canvas, size, a = slice.call(arguments), last = a[a.length-1];

            withCtx = (typeof last === 'boolean' ? a.pop() : false);

            size = Size(a.length == 1 ? a[0] : a);
            
            canvas = atom.dom.create("canvas", {
                width  : size.width,
                height : size.height
            }).first;
            
            if (withCtx) canvas.ctx = new Context2D(canvas);
            return canvas;
        },
        'declare.classes': {},
        declare: function (declareName, shortName, Parent, object) {
            if (typeof shortName == 'object') {
                object = Parent;
                Parent = shortName;
                shortName = null;
            }
            if (object == null) {
                object = Parent;
                Parent = null;
            }
            var Class = declare( declareName, Parent, object );
            if (shortName) {
                if (shortName in this['declare.classes']) {
                    throw new Error( 'Duplicate declaration: ' + shortName );
                }
                this['declare.classes'][shortName] = Class;
            }
            return Class;
        },
        extract: function (to) {
            to = to || global;
            for (var k in this['declare.classes']) {
                to[k] = this['declare.classes'][k];
            }
            return to;
        }
    });

/*
---

name: "App"

description: "LibCanvas.App"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas

provides: App

...
*/

/** @class App */
LibCanvas.declare( 'LibCanvas.App', 'App', {
    initialize: function (settings) {
        this.bindMethods( 'tick' );

        this.layers    = [];
        this.settings  = new Settings({ appendTo: 'body' }).set(settings);
        this.container = new App.Container(
            this.settings.subset(['simple', 'size', 'appendTo'])
        );
        this.resources = new Registry();

        atom.frame.add( this.tick );
    },

    destroy: function () {
        atom.array.invoke( this.layers, 'destroy' );
        atom.frame.remove( this.tick );
        this.container.destroy();
    },

    get rectangle () {
        return this.container.rectangle;
    },

    /**
     * return "-1" if left is higher, "+1" if right is higher & 0 is they are equals
     * @param {App.Element} left
     * @param {App.Element} right
     * @returns {number}
     */
    zIndexCompare: function (left, right, inverted) {
        var leftZ, rightZ, factor = inverted ? -1 : +1;

        if (!left  || !left .layer) throw new TypeError( 'Wrong left element'  );
        if (!right || !right.layer) throw new TypeError( 'Wrong right element' );


         leftZ =  left.layer.dom.zIndex;
        rightZ = right.layer.dom.zIndex;

        if (leftZ > rightZ) return -1 * factor;
        if (leftZ < rightZ) return +1 * factor;

         leftZ =  left.zIndex;
        rightZ = right.zIndex;

        if (leftZ > rightZ) return -1 * factor;
        if (leftZ < rightZ) return +1 * factor;

        return 0;
    },

    createLayer: function (settings) {
        if (this.settings.get('simple') && this.layers.length) {
            throw new Error('You can create only one layer in "Simple" mode');
        }

        var layer = new App.Layer(this, settings);
        this.layers.push(layer);
        return layer;
    },

    tick: function (time) {
        atom.array.invoke(this.layers, 'tick', time);
    }
});

var App = LibCanvas.App;

/*
---

name: "App.Behavior"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas

provides: App.Behavior

...
*/

/** @class App.Behavior */
var Behavior = declare( 'LibCanvas.App.Behavior', {

    eventName: null,

    initialize: function (element, callback) {
        this.element = element;
        this.events  = element.events;
        this.eventArgs(callback);
    },

    started: false,

    /** @private */
    changeStatus: function (status){
        if (this.started == status) {
            return false;
        } else {
            this.started = status;
            return true;
        }
    },

    /** @private */
    eventArgs: function (callback) {
        if (this.eventName && atom.core.isFunction(callback)) {
            this.events.add( this.eventName, callback );
        }
        return this;
    },

    /** @private */
    getMouse: function (handler, strict) {
        var mouse = this.element.layer.app.resources.get(
            handler ? 'mouseHandler' : 'mouse'
        );

        if (strict && !mouse) {
            throw new Error('No mouse in element');
        }

        return mouse;
    }

});

/*
---

name: "App.Clickable"

description: "Provides interface for clickable canvas objects"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App.Behavior

provides: App.Clickable

...
*/

/** @class App.Clickable */
var Clickable = declare( 'LibCanvas.App.Clickable', App.Behavior, {

    eventName: 'statusChange',

    callbacks: {
        mousedown: function (e) {
            Clickable.setValue(this, 'active', true , e);
        },
        mouseup  : function (e) {
            Clickable.setValue(this, 'active', false, e);
        },
        mouseover: function (e) {
            Clickable.setValue(this, 'hover' , true , e);
        },
        mouseout : function (e) {
            Clickable.setValue(this, 'hover' , false, e);
            Clickable.setValue(this, 'active', false, e);
        }
    },

    start: function (callback) {
        if (this.changeStatus(true)) {
            this.eventArgs(callback);
            this.events.add(this.callbacks);
        }
        return this;
    },

    stop: function () {
        if (this.changeStatus(false)) {
            this.events.remove(this.callbacks);
        }
        return this;
    }

});

Clickable.setValue = function (element, name, val, event) {
    if (element[name] != val) {
        element[name] = val;
        element.events.fire(
            Clickable.prototype.eventName,
            [name, val, event]
        );
    }
};

/*
---

name: "App.Container"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App

provides: App.Container

...
*/

/**
 * @class App.Container
 * @private */
declare( 'LibCanvas.App.Container', {
    /** @private
     *  @property {Size} */
    currentSize: null,

    /** @property {App.Dom[]} */
    doms: [],

    wrapper: null,
    bounds : null,

    initialize: function (settings) {
        this.doms        = [];
        this.settings    = new Settings(settings);
        this.currentSize = new Size(this.settings.get('size') || [0,0]);

        this.isSimple = this.settings.get('simple');

        if (this.isSimple) {
            this.createWrappersSimple();
        } else {
            this.createWrappers();
        }
    },

    get rectangle () {
        var size = this.size;
        return new Rectangle(0, 0, size.width, size.height);
    },

    set size(size) {
        if (this.isSimple) {
            this.doms[0].size = size;
        } else {
            size = this.currentSize.set(size).toObject();
            this.wrapper.css(size);
            this.bounds .css(size);
        }
    },

    get size() {
        return this.currentSize;
    },

    destroy: function () {
        if (!this.isSimple) {
            this.wrapper.destroy();
        }
        return this;
    },

    createDom: function (settings) {
        var dom = new App.Dom( this, settings );
        this.doms.push(dom);
        return dom;
    },

    appendTo: function (element) {
        if (element) this.wrapper.appendTo( element );
        return this;
    },

    /** @private */
    createWrappersSimple: function () {
        var size = this.currentSize.toObject();

        this.wrapper = atom.dom(LibCanvas.buffer(size,true));
        this.bounds  = this.wrapper;

        this.wrapper
            .addClass('libcanvas-app-simple')
            .appendTo( this.settings.get('appendTo') )
    },

    /** @private */
    createWrappers: function () {
        var size = this.currentSize.toObject();

        this.wrapper = atom.dom.create('div')
            .css(size)
            .addClass('libcanvas-app')
            .appendTo(this.settings.get( 'appendTo' ));

        this.bounds = atom.dom.create('div')
            .css({
                overflow: 'hidden',
                position: 'absolute'
            })
            .css(size)
            .appendTo(this.wrapper);
    }
});

/*
---

name: "App.Dom"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App

provides: App.Dom

...
*/


/** @class App.Dom */
declare( 'LibCanvas.App.Dom', {
    /** @private
     *  @property {Size} */
    currentSize: null,
    
    /** @private
     *  @property {App.Container} */
    container: null,

    /** @private
     *  @property {Point} */
    shift: null,

    /** @private */
    z: 0,

    initialize: function (container, settings) {
        this.container = container;
        this.settings  = new Settings(settings);
        this.shift = new Point(0,0);
        this.name  = this.settings.get('name') || '';
        this.createSize();
        this.createElement();
    },

    set zIndex (z) {
        this.z = z;
        if (!this.container.isSimple) {
            this.element.css('zIndex', z);
        }
    },

    get zIndex () {
        return this.z;
    },

    set size(size) {
        size = this.currentSize.set(size);

        this.canvas.width  = size.width ;
        this.canvas.height = size.height;
    },

    get size() {
        return this.currentSize;
    },

    destroy: function () {
        this.element.destroy();
        this.size = new Size(0,0);
    },

    /**
     * @param {Point} shift
     * @returns {App.Dom}
     */
    addShift: function ( shift ) {
        var newShift = this.getShift().move( shift );
        this.element.css({
            marginLeft: newShift.x,
            marginTop : newShift.y
        });
        return this;
    },

    /**
     * @param {Point} shift
     * @returns {App.Dom}
     */
    setShift: function (shift) {
        return this.addShift( this.shift.diff(shift) );
    },

    /** @returns {Point} */
    getShift: function () {
        if (this.container.isSimple) {
            throw new Error('Shift not available in Simple mode');
        }

        return this.shift;
    },

    /** @private */
    createSize: function () {
        var size = this.settings.get('size');

        if (this.container.isSimple) {
            this.currentSize = this.container.size;
            if (size) {
                this.currentSize.set(size);
            }
        } else {
            this.currentSize = size || this.container.size.clone();
        }


    },

    /** @private */
    createElement: function () {
        if (this.container.isSimple) {
            this.createElementSimple();
        } else {
            this.createElementNormal();
        }
    },

    /** @private */
    createElementNormal: function () {
        this.canvas  = new LibCanvas.Buffer(this.size, true);

        this.element = atom.dom(this.canvas);

        this.element
            .attr({ 'data-name': this.name  })
            .css ({ 'position' : 'absolute' })
            .appendTo( this.container.bounds );

        this.zIndex = this.settings.get('zIndex') || 0;
    },

    /** @private */
    createElementSimple: function () {
        this.element = this.container.wrapper;

        this.canvas  = this.element.first;
        this.canvas.width  = this.size.width;
        this.canvas.height = this.size.height;
    }
});

/*
---

name: "App.Draggable"

description: "When object implements LibCanvas.Draggable interface dragging made possible"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App.Behavior

provides: App.Draggable

...
*/

/** @class App.Draggable */
declare( 'LibCanvas.App.Draggable', App.Behavior, {

    eventName: 'moveDrag',

    stopDrag: [ 'up', 'out' ],

    initialize: function method (element, callback) {
        this.bindMethods([ 'onStop', 'onDrag', 'onStart' ]);

        method.previous.call( this, element, callback );
    },

    start: function (callback) {
        if (this.changeStatus(true)) {
            this.mouse = this.getMouse(false, true);
            this.eventArgs(callback);
            this.events.add( 'mousedown', this.onStart )
        }
        return this;
    },

    stop: function () {
        if (this.changeStatus(false)) {
            this.events.remove( 'mousedown', this.onStart );
        }
        return this;
    },

    /** @private */
    bindMouse: function (method) {
        var mouse = this.mouse, stop = this.stopDrag;

        mouse.events
            [method]( 'move', this.onDrag )
            [method](  stop , this.onStop );

        return mouse;
    },

    /** @private */
    onStart: function (e) {
        if (e.button !== 0) return;

        this.bindMouse('add');
        this.events.fire('startDrag', [ e ]);
    },

    /** @private */
    onDrag: function (e) {
        if (!this.element.layer) {
            return this.onStop(e, true);
        }

        var delta = this.mouse.delta;
        this.element.distanceMove( delta );
        this.events.fire('moveDrag', [delta, e]);
    },

    /** @private */
    onStop: function (e, forced) {
        if (e.button === 0 || forced === true) {
            this.bindMouse('remove');
            this.events.fire('stopDrag', [ e ]);
        }
    }
});

/*
---

name: "App.LayerShift"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App

provides: App.LayerShift

...
*/

/** @class App.LayerShift */
declare( 'LibCanvas.App.LayerShift', {

    initialize: function (layer) {
        this.layer    = layer;
        this.shift    = new Point(0, 0);
        this.elementsShift = new Point(0, 0);
    },

    /**
     * @private
     * @property {Point}
     */
    shift: null,

    /**
     * @private
     * @property {Point}
     */
    elementsShift: null,

    /**
     * @param {Point} shift
     */
    addElementsShift: function (shift) {
        if (!shift) {
            shift = this.elementsShift.diff(this.shift);
        } else {
            shift = Point(shift);
        }
        var e = this.layer.elements, i = e.length;
        while (i--) e[i].addShift(shift);
        this.elementsShift.move(shift);
        return this;
    },

    /**
     * @private
     * @property {LibCanvas.Shapes.Rectangle}
     */
    limitShift: null,

    /**
     * @param {Rectangle} limitShift
     */
    setLimitShift: function (limitShift) {
        this.limitShift = limitShift ? Rectangle(limitShift) : null;
        return this;
    },

    /**
     * @param {Point} shift
     */
    addShift: function ( shift, withElements ) {
        shift = new Point( shift );
        var limit = this.limitShift, current = this.shift;
        if (limit) {
            shift.x = atom.number.limit(shift.x, limit.from.x - current.x, limit.to.x - current.x);
            shift.y = atom.number.limit(shift.y, limit.from.y - current.y, limit.to.y - current.y);
        }

        current.move( shift );
        this.layer.dom.addShift( shift );
        this.layer.dom.canvas.ctx.translate( shift, true );
        if (withElements) this.addElementsShift( shift );
        return this;
    },

    /**
     * @param {Point} shift
     */
    setShift: function (shift, withElements) {
        return this.addShift( this.shift.diff(shift), withElements );
    },

    /**
     * @returns {Point}
     */
    getShift: function () {
        return this.shift;
    }
});

/*
---

name: "App.Dragger"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App
    - App.LayerShift

provides: App.Dragger

...
*/
/** @class App.Dragger */
declare( 'LibCanvas.App.Dragger', {
    initialize: function (mouse) {
        this.bindMethods([ 'dragStart', 'dragStop', 'dragMove' ]);
        this.events = new Events(this);

        this.mouse  = mouse;
        this.shifts = [];

        this._events = {
            down: this.dragStart,
            up  : this.dragStop,
            out : this.dragStop,
            move: this.dragMove
        };
    },

    addLayerShift: function (shift) {
        this.shifts.push( shift );
        return this;
    },

    started: false,

    start: function (callback) {
        if (callback !== undefined) {
            this.callback = callback;
        }
        this.started = true;
        this.mouse.events.add( this._events );
        return this;
    },

    stop: function () {
        this.started = false;
        this.mouse.events.remove( this._events );
        return this;
    },

    /** @private */
    dragStart: function (e) {
        if (!this.shouldStartDrag(e)) return;

        for (var i = this.shifts.length; i--;) {
            this.shifts[i].layer.stop();
        }

        this.drag = true;
        this.events.fire( 'start', [ e ]);
    },
    /** @private */
    dragStop: function (e) {
        if (!this.drag) return;

        for (var i = this.shifts.length; i--;) {
            var shift = this.shifts[i];
            shift.addElementsShift();
            shift.layer.start();
        }

        this.drag = false;
        this.events.fire( 'stop', [ e ]);
    },
    /** @private */
    dragMove: function (e) {
        if (!this.drag) return;
        for (var i = this.shifts.length; i--;) {
            this.shifts[i].addShift(this.mouse.delta);
        }
    },
    /** @private */
    shouldStartDrag: function (e) {
        if (!this.started) return false;

        return this.callback ? this.callback(e) : true;
    }
});

/*
---

name: "App.Element"

description: "LibCanvas.Layer"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App

provides: App.Element

...
*/

/** @class App.Element */
declare( 'LibCanvas.App.Element', {

    layer   : null,
    zIndex  : 0,
    renderer: null,
    settings: {},
    opacity : 1,
    opacityThreshold: 0.01,

    /** @constructs */
    initialize: function (layer, settings) {
        this.bindMethods([ 'redraw', 'destroy' ]);

        this.events = new Events(this);
        this.settings = new Settings({ hidden: false })
            .set(this.settings)
            .set(settings)
            .addEvents(this.events);
        layer.addElement( this );

        var ownShape = this.shape && this.shape != this.constructor.prototype.shape;

        if (ownShape || this.settings.get('shape')) {
            if (!ownShape) this.shape = this.settings.get('shape');
            this.saveCurrentBoundingShape();
        }
        if (this.settings.get('zIndex') != null) {
            this.zIndex = Number( this.settings.get('zIndex') );
        }

        this.configure();
    },

    configure: function () {
        return this;
    },

    previousBoundingShape: null,

    get currentBoundingShape () {
        return this.shape.getBoundingRectangle().fillToPixel();
    },

    redraw: function () {
        if (this.layer) {
            this.layer.redrawElement( this );
        }
        return this;
    },

    destroy: function () {
        if (this.layer) {
            this.layer.rmElement( this );
        }
        return this;
    },

    distanceMove: function (point) {
        this.shape.move(point);
        return this;
    },

    hasPoint: function (point) {
        return this.shape.hasPoint( point );
    },

    isTriggerPoint: function (point) {
        if (this.hasMousePoint) {
            return this.hasMousePoint(point);
        } else {
            return this.hasPoint(point);
        }
    },

    addShift: function (shift) {
        this.shape.move( shift );
        if (this.previousBoundingShape)
            this.previousBoundingShape.move( shift );
        return this;
    },

    isVisible: function () {
        return !this.settings.get('hidden') && this.opacity > this.opacityThreshold;
    },

    onUpdate: function (time) {
        return this;
    },

    clearPrevious: function ( ctx ) {
        if (this.previousBoundingShape) ctx.clear( this.previousBoundingShape );
        return this;
    },

    saveCurrentBoundingShape: function () {
        var shape = this.currentBoundingShape;
        this.previousBoundingShape = shape.fillToPixel ?
            shape.clone().fillToPixel() : shape.clone().grow( 2 );
        return this;
    },

    renderToWrapper: function (ctx, resources) {
        if (this.opacity < this.opacityThreshold) {
            return;
        }
        ctx.save();
        if (this.opacity + this.opacityThreshold < 1) {
            ctx.set({ globalAlpha: this.opacity });
        }
        this.renderTo(ctx, resources);
        ctx.restore();
        return this;
    },

    renderTo: function (ctx, resources) {
        if (this.renderer) {
            this.renderer.renderTo(ctx, resources);
        }
        return this;
    }
});

/*
---

name: "App.Layer"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App
    - App.Dom

provides: App.Layer

...
*/


/** @class App.Layer */
declare( 'LibCanvas.App.Layer', {

    initialize: function (app, settings) {
        this.settings = new Settings({
            invoke      : app.settings.get('invoke'),
            intersection: 'auto' // auto|manual|all
        }).set(settings);

        this.intersection  = this.settings.get('intersection');
        this.redrawAllMode = this.intersection === 'all' || this.intersection === 'full';

        this.afterDraw = null;
        this.app      = app;
        this.elements = [];
        this.redraw   = this.redrawAllMode ? this.elements : [];
        this.clear    = [];
        this.createDom();
    },

    get ctx () {
        return this.dom.canvas.ctx;
    },

    /** @private */
    stopped: false,

    destroy: function () {
        atom.array.invoke( this.elements, 'destroy' );
        this.dom.destroy();
    },

    hide: function () {
        this.dom.element.css({ display: 'none' });
        return this.stop();
    },

    show: function () {
        this.dom.element.css({ display: '' });
        return this.stop();
    },

    start: function () {
        this.stopped = false;
        return this;
    },

    stop: function () {
        this.stopped = true;
        return this;
    },

    redrawAll: function () {
        atom.array.invoke(this.elements, 'redraw');
        return this;
    },
    
    redrawForce: function () {
        this.redrawAll();
        this.draw();
    },

    /** @private */
    tick: function (time) {
        if (this.stopped) return this;

        if (this.settings.get( 'invoke' )) {
            this.sortElements();
            this.updateAll(time);
        }

        if (this.needUpdate) {
            this.draw();
            this.needUpdate = false;
        }

        return this;
    },


    /** @private */
    draw: function () {
        var
            intersection = this.intersection,
            ctx          = this.dom.canvas.ctx,
            resources    = this.app.resources;

        if (intersection === 'full') {
            ctx.clearAll();
        } else {
            if (intersection === 'auto') {
                this.addIntersections();
            } else if (intersection === 'all') {
                atom.array.invoke(this.clear, 'clearPrevious', ctx, resources);
            }

            atom.array.invoke(this.redraw, 'clearPrevious', ctx, resources);
        }

        this.drawElements(this.redraw, ctx, resources);

        if (intersection === 'all') {
            this.clear.length = 0;
        } else if (intersection !== 'full') {
            this.redraw.length = 0;
        }
    },

    /** @private */
    drawElements: function (elements, ctx, resources) {
        // draw elements with the lower zIndex first
        atom.array.sortBy( elements, 'zIndex' );
        for (var i = elements.length; i--;) {
            this.drawElement(elements[i], ctx, resources);
        }
    },

    /** @private */
    drawElement: function (elem, ctx, resources) {
        if (elem.layer == this) {
            elem.redrawRequested = false;
            if (elem.isVisible()) {
                elem.renderToWrapper( ctx, resources );
                if (this.intersection !== 'full') {
                    elem.saveCurrentBoundingShape();
                }
            }
        }
    },

    /** @private */
    sortElements: function () {
        atom.array.sortBy( this.elements, 'zIndex' );
    },

    /** @private */
    updateAll: function (time) {
        atom.array.invoke( this.elements, 'onUpdate', time, this.app.resources );
    },

    /** @private */
    needUpdate: false,

    /** @private */
    createDom: function () {
        this.dom = this.app.container.createDom(
            this.settings.subset([ 'name', 'zIndex', 'size' ])
        );
    },

    /** @private */
    addElement: function (element) {
        if (element.layer != this) {
            if (element.layer) {
                element.layer.rmElement( element );
            }

            element.layer = this;
            this.elements.push( element );
            this.redrawElement( element );
        }
        return this;
    },

    /** @private */
    rmElement: function (element) {
        if (element.layer == this) {
            if (this.intersection === 'all') {
                this.needUpdate = true;
                this.clear.push(element);
            } else {
                this.redrawElement( element );
            }
            atom.core.eraseOne( this.elements, element );
            element.layer = null;
        }
        return this;
    },

    /** @private */
    redrawElement: function (element) {
        if (element.layer == this && !element.redrawRequested) {
            this.needUpdate = true;
            element.redrawRequested = true;
            if (!this.redrawAllMode) {
                this.redraw.push( element );
            }
        }
        return this;
    },

    /** @private */
    addIntersections: function () {
        var i, elem, layer = this;

        for (i = 0; i < this.redraw.length; i++) {
            elem = this.redraw[i];

            this.findIntersections(elem.previousBoundingShape, elem, this.redrawElement);
            this.findIntersections(elem. currentBoundingShape, elem, function (e) {
                // we need to redraw it, only if it will be over our element
                if (e.zIndex > elem.zIndex) {
                    layer.redrawElement( e );
                }
            });
        }
    },

    /** @private */
    findIntersections: function (shape, elem, fn) {
        if (!shape) return;

        var i = this.elements.length, e;
        while (i--) {
            e = this.elements[i];
            // check if we need also `e.currentBoundingShape.intersect( shape )`
            if (e != elem && e.isVisible() &&
                e.previousBoundingShape &&
                e.previousBoundingShape.intersect( shape )
            ) fn.call( this, e );
        }
    }

});


/*
---

name: "Geometry"

description: "Base for such things as Point and Shape"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas

provides: Geometry

...
*/

/** @class Geometry */
var Geometry = declare( 'LibCanvas.Geometry', {
    initialize : function () {
        if (arguments.length) this.set.apply(this, arguments);
    },
    cast: function (args) {
        return this.constructor.castArguments(args);
    }
}).own({
    invoke: declare.castArguments,
    from : function (obj) {
        return this(obj);
    }
});

/*
---

name: "Point"

description: "A X/Y point coordinates encapsulating class"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Geometry

provides: Point

...
*/

/** @class Point */
var Point = LibCanvas.declare( 'LibCanvas.Point', 'Point', Geometry, {
    x: 0,
    y: 0,

    /**
     *   new Point(1, 1);
     *   new Point([1, 1]);
     *   new Point({x:1, y:1});
     *   new Point(point);
     * @constructs
     * @param {Number} x
     * @param {Number} y
     * @returns {Point}
     */
    set : function (x, y) {
        if (arguments.length != 2) {
            if (atom.core.isArrayLike(x)) {
                y = x[1];
                x = x[0];
            } else if (x && x.x != null && x.y != null) {
                y = x.y;
                x = x.x;
            } else {
                throw new TypeError( 'Wrong Arguments In Point.Set' );
            }
        }

        this.x = Number(x);
        this.y = Number(y);
        return this;
    },
    /** @returns {Point} */
    move: function (distance, reverse) {
        distance = this.cast(distance);
        reverse  = reverse ? -1 : 1;
        this.x += distance.x * reverse;
        this.y += distance.y * reverse;
        return this;
    },
    /** @returns {Point} */
    moveTo : function (point) {
        return this.move(this.diff(this.cast(point)));
    },
    /** @returns {Number} */
    angleTo : function (point) {
        var diff = this.cast(point).diff(this);
        return atom.math.normalizeAngle( Math.atan2(diff.y, diff.x) );
    },
    /** @returns {Number} */
    distanceTo : function (point) {
        var diff = this.cast(point).diff(this);
        return atom.math.hypotenuse(diff.x, diff.y);
    },
    /** @returns {Boolean} */
    checkDistanceTo : function (point, distance, equals) {
        var deltaX, deltaY, realDistanceSq, maxDistanceSq;

        deltaX = Math.abs(this.x - point.x);
        if (deltaX > distance) return false;

        deltaY = Math.abs(this.y - point.y);
        if (deltaY > distance) return false;

        realDistanceSq = deltaX*deltaX + deltaY*deltaY;
        maxDistanceSq  = distance*distance;

        return (realDistanceSq < maxDistanceSq) ||
            (equals && realDistanceSq == maxDistanceSq)
    },
    /** @returns {Point} */
    diff : function (point) {
        return new this.constructor(point).move(this, true);
    },
    /** @returns {Point} */
    rotate : function (angle, pivot) {
        pivot = pivot ? this.cast(pivot) : new this.constructor(0, 0);
        if (this.equals(pivot)) return this;

        var radius = pivot.distanceTo(this);
        var sides  = pivot.diff(this);
        // TODO: check, maybe here should be "sides.y, sides.x" ?
        var newAngle = Math.atan2(sides.x, sides.y) - angle;

        return this.moveTo({
            x : Math.sin(newAngle) * radius + pivot.x,
            y : Math.cos(newAngle) * radius + pivot.y
        });
    },
    /** @returns {Point} */
    scale : function (power, pivot) {
        pivot = pivot ? this.cast(pivot) : new this.constructor(0, 0);

        var diff = this.diff(pivot), isObject = typeof power == 'object';
        return this.moveTo({
            x : pivot.x - diff.x  * (isObject ? power.x : power),
            y : pivot.y - diff.y  * (isObject ? power.y : power)
        });
    },
    /** @returns {Point} */
    alterPos : function (arg, fn) {
        return this.moveTo({
            x: fn(this.x, typeof arg == 'object' ? arg.x : arg),
            y: fn(this.y, typeof arg == 'object' ? arg.y : arg)
        });
    },
    /** @returns {Point} */
    mul : function (arg) {
        return this.alterPos(arg, function(a, b) {
            return a * b;
        });
    },
    /** @returns {Point} */
    getNeighbour : function (dir) {
        return this.clone().move(this.constructor.shifts[dir]);
    },
    /** @returns {Point[]} */
    get neighbours () {
        return this.getNeighbours( true );
    },
    /** @returns {Point[]} */
    getNeighbours: function (corners, asObject) {
        var shifts = ['t', 'l', 'r', 'b'], result, i, dir;

        if (corners) shifts.push('tl', 'tr', 'bl', 'br');

        if (asObject) {
            result = {};
            for (i = shifts.length; i--;) {
                dir = shifts[i];
                result[dir] = this.getNeighbour( dir );
            }
            return result;
        } else {
            return shifts.map(this.getNeighbour.bind(this));
        }
    },
    /** @returns {boolean} */
    equals : function (to, accuracy) {
        to = this.cast(to);
        if (accuracy == null) {
            return to.x == this.x && to.y == this.y;
        }
        return atom.number.equals(this.x, to.x, accuracy)
            && atom.number.equals(this.y, to.y, accuracy);
    },
    /** @returns {object} */
    toObject: function () {
        return { x: this.x, y: this.y };
    },
    toArray: function () {
        return [ this.x, this.y ];
    },
    /** @returns {Point} */
    invoke: function (method) {
        this.x = this.x[method]();
        this.y = this.y[method]();
        return this;
    },
    /** @returns {Point} */
    map: function (fn, context) {
        this.x = fn.call(context || this, this.x, 'x', this);
        this.y = fn.call(context || this, this.y, 'y', this);
        return this;
    },
    /** @returns {Point} */
    mean: function (points) {
        var l = points.length, i = l, x = 0, y = 0;
        while (i--) {
            x += points[i].x;
            y += points[i].y;
        }
        return this.set(x/l, y/l);
    },
    /** @returns {Point} */
    snapToPixel: function () {
        this.x += 0.5 - (this.x - Math.floor(this.x));
        this.y += 0.5 - (this.y - Math.floor(this.y));
        return this;
    },
    /** @returns {Point} */
    reverse: function () {
        this.x *= -1;
        this.y *= -1;
        return this;
    },
    /** @returns {Point} */
    clone : function () {
        return new this.constructor(this);
    },
    /** @returns {string} */
    dump: function () {
        return '[Point(' + this.x + ', ' + this.y + ')]';
    }
});

/** @private */
Point.from = function (object) {
    if (object == null) return null;

    return object instanceof Point ? object : new Point(object);
};

Point.shifts = atom.object.map({
    top    : [ 0, -1],
    right  : [ 1,  0],
    bottom : [ 0,  1],
    left   : [-1,  0],
    t      : [ 0, -1],
    r      : [ 1,  0],
    b      : [ 0,  1],
    l      : [-1,  0],
    tl     : [-1, -1],
    tr     : [ 1, -1],
    bl     : [-1,  1],
    br     : [ 1,  1]
}, Point);

/*
---

name: "Mouse"

description: "A mouse control abstraction class"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point

provides: Mouse

...
*/

/** @class Mouse */
var Mouse = LibCanvas.declare( 'LibCanvas.Mouse', 'Mouse', {
    /** @private */
    elem: null,

    /** @property {boolean} */
    inside: false,
    /** @property {Point} */
    point: null,
    /** @property {Point} */
    previous: null,
    /** @property {Point} */
    delta: null,
    /** @property {Events} */
    events: null,

    /** @private */
    mapping: {
        click      : 'click',
        dblclick   : 'dblclick',
        contextmenu: 'contextmenu',

        mouseover : 'over',
        mouseout  : 'out',
        mousedown : 'down',
        mouseup   : 'up',
        mousemove : 'move',

        touchstart: 'down',
        touchmove : 'move',
        touchend  : 'up',

        DOMMouseScroll: 'wheel',
        mousewheel    : 'wheel'
    },

    initialize : function (elem, offsetElem) {
        this.bindMethods( 'onEvent' );

        if (elem == null) {
            throw new TypeError('`elem` is undefined');
        }

        this.elem       = atom.dom(elem);
        this.offsetElem = offsetElem ? atom.dom(offsetElem) : this.elem;

        this.point    = new Point(0, 0);
        this.previous = new Point(0, 0);
        this.delta    = new Point(0, 0);
        this.events   = new Events(this);

        this.listen(this.onEvent);
    },
    /** @private */
    fire: function (name, e) {
        this.events.fire(name, [e, this]);
        return this;
    },
    /** @private */
    onEvent: function (e) {
        var
            name = this.mapping[e.type],
            fn   = this.eventActions[name];
        
        if (e.touches && e.touches.length) {
            var attrName = null;
            
            for(attrName in e.touches[0]) {
                if (e.touches[0].hasOwnProperty(attrName)) {
                    delete e[attrName];
                    if (typeof(e.touches[0][attrName]) === "number") {
                        e[attrName] = Math.floor(e.touches[0][attrName]);
                    } else {
                        e[attrName] = e.touches[0][attrName];
                    }
                }
            }
        }

        if (fn) fn.call(this, e);
        this.fire(name, e);
    },
    /** @private */
    getOffset: function (e) {
        return this.constructor.getOffset(e, this.offsetElem);
    },
    /** @private */
    set: function (e, inside) {
        var point = this.getOffset(e);

        this.previous.set( this.point );
        this.delta   .set( this.previous.diff( point ) );
        this.point   .set( point );
        this.inside = inside;
    },
    /** @private */
    eventActions: {
        wheel: function (e) {
            this.constructor.addWheelDelta(e);
        },

        move: function (e) {
            this.set(e, true);
        },

        down: function (e) {
            this.set(e, true);
        },

        over: function (e) {
            if (this.checkEvent(e)) {
                this.fire('enter', e);
            }
        },

        out: function (e) {
            if (this.checkEvent(e)) {
                this.set(e, false);
                this.fire('leave', e);
            }
        }
    },
    /** @private */
    checkEvent: function (e) {
        var related = e.relatedTarget, elem = this.elem;

        return related == null || (
            related && related != elem.first && !elem.contains(related)
        );
    },
    /** @private */
    listen : function (callback) {
        this.elem
            .bind({ selectstart: false })
            .bind(atom.object.map(
                this.mapping, atom.fn.lambda(callback)
            ));
    }
}).own({
    prevent: function (e) {e.preventDefault()},
    addWheelDelta: function (e) {
        e.delta =
            // IE, Opera, Chrome
            e.wheelDelta ? e.wheelDelta > 0 ? 1 : -1 :
            // Fx
            e.detail     ? e.detail     < 0 ? 1 : -1 : null;

        return e;
    },
    eventSource: function (e) {
        return e.changedTouches ? e.changedTouches[0] : e;
    },
    expandEvent: function (e) {
        var source = this.eventSource(e);

        if (e.pageX == null) {
            e.pageX = source.pageX != null ? source.pageX : source.clientX + document.scrollLeft;
            e.pageY = source.pageY != null ? source.pageY : source.clientY + document.scrollTop ;
        }

        return e;
    },
    getOffset : function (e, element) {
        var elementOffset = atom.dom(element || this.eventSource(e).target).offset();

        this.expandEvent(e);

        return new Point(
            e.pageX - elementOffset.x,
            e.pageY - elementOffset.y
        );
    }
});

/*
---

name: "App.PointSearch"

description: "LibCanvas.App.ElementsMouseSearch"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App

provides: App.PointSearch

...
*/

/** @class App.PointSearch */
declare( 'LibCanvas.App.PointSearch', {

    initialize: function () {
        this.elements = [];
    },

    add: function (elem) {
        this.elements.push( elem );
        return this;
    },

    remove: function (elem) {
        atom.core.eraseOne( this.elements, elem );
        return this;
    },

    removeAll: function () {
        this.elements.length = 0;
        return this;
    },

    findByPoint: function (point) {
        var e = this.elements, i = e.length, result = [];
        while (i--) if (e[i].isTriggerPoint( point )) {
            result.push(e[i]);
        }
        return result;
    }

});

/** @deprecated */
App.ElementsMouseSearch = App.PointSearch;

/*
---

name: "App.MouseHandler"

description: "LibCanvas.App.MouseHandler"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Mouse
    - App
    - App.PointSearch

provides: App.MouseHandler

...
*/

/** @class App.MouseHandler */
declare( 'LibCanvas.App.MouseHandler', {

    events: 'down up move out dblclick contextmenu wheel'.split(' '),

    /** @private */
    mouse: null,

    /** @constructs */
    initialize: function (settings) {
        var handler = this;

        handler.settings = new Settings(settings);
        handler.lastMouseMove = [];
        handler.lastMouseDown = [];
        handler.subscribers   = [];

        handler.app    = handler.settings.get('app');
        handler.mouse  = handler.settings.get('mouse');
        handler.compareFunction = function (left, right) {
            return handler.app.zIndexCompare(left, right, true);
        };
        handler.search =
            handler.settings.get('search') ||
            new App.PointSearch();

        this.events.forEach(function (type) {
            handler.mouse.events.add( type, function (e) {
                handler.event(type, e);
            });
        });
    },

    stop: function () {
        this.stopped = true;
        return this;
    },

    start: function () {
        this.stopped = false;
        return this;
    },

    subscribe : function (elem) {
        if (this.subscribers.indexOf(elem) == -1) {
            this.subscribers.push(elem);
            this.search.add(elem);
        }
        return this;
    },

    unsubscribe : function (elem) {
        var index = this.subscribers.indexOf(elem);
        if (index != -1) {
            this.subscribers.splice(index, 1);
            atom.core.eraseOne(this.lastMouseDown, elem);
            atom.core.eraseOne(this.lastMouseMove, elem);
            this.search.remove(elem);
        }
        return this;
    },

    unsubscribeAll: function () {
        this.subscribers.length = 0;
        this.search.removeAll();
        return this;
    },

    fall: function () {
        this.falling = true;
        return this;
    },

    getOverElements: function () {
        if (!this.mouse.inside) return [];

        var
            elements = this.search.findByPoint( this.mouse.point ),
            i = elements.length;

        while (i--) if (!elements[i].layer) {
            this.unsubscribe(elements[i]);
            elements.splice(i, 1);
        }

        return elements.sort( this.compareFunction );
    },

    /** @private */
    stopped: false,

    /** @private */
    falling: false,

    /** @private */
    checkFalling: function () {
        var value = this.falling;
        this.falling = false;
        return value;
    },

    /** @private */
    event: function (type, e) {
        if (this.stopped) return;

        var method = ['dblclick', 'contextmenu', 'wheel'].indexOf( type ) >= 0
            ? 'forceEvent' : 'parseEvent';
        
        return this[method]( type, e );
    },

    /** @private */
    parseEvent: function (type, event) {
        if (type == 'down') this.lastMouseDown.length = 0;

        var i, elem,
            elements = this.getOverElements(),
            stopped  = false,
            eventArgs = [event],
            isChangeCoordEvent = (type == 'move' || type == 'out');

        // В первую очередь - обрабатываем реальный mouseout с элементов
        if (isChangeCoordEvent) {
            this.informOut(eventArgs, elements);
        }

        for (i = elements.length; i--;) {
            elem = elements[i];
            // мышь над элементом, сообщаем о mousemove
            // о mouseover, mousedown, click, если необходимо
            if (!stopped) {
                if (this.fireElem( type, elem, eventArgs )) {
                    stopped = true;
                    if (!isChangeCoordEvent) break;
                }
            // предыдущий элемент принял событие на себя
            // необходимо сообщить остальным элементам под ним о mouseout
            // Но только если это событие передвижения или выхода за границы холста
            // а не активационные, как маусдаун или маусап
            } else {
                this.stoppedElem(elem, eventArgs);
            }
        }

        return stopped;
    },

    /** @private */
    informOut: function (eventArgs, elements) {
        var
            elem,
            lastMove = this.lastMouseMove,
            i = lastMove.length;
        while (i--) {
            elem = lastMove[i];
            if (elements.indexOf(elem) < 0) {
                elem.events.fire( 'mouseout', eventArgs );
                lastMove.splice(i, 1);
            }
        }
    },

    /** @private */
    stoppedElem: function (elem, eventArgs) {
        var
            lastMove = this.lastMouseMove,
            index    = lastMove.indexOf(elem);
        if (index > -1) {
            elem.events.fire( 'mouseout', eventArgs );
            lastMove.splice(index, 1);
        }
    },

    /** @private */
    fireElem: function (type, elem, eventArgs) {
        var
            lastDown = this.lastMouseDown,
            lastMove = this.lastMouseMove;

        if (type == 'move') {
            if (lastMove.indexOf(elem) < 0) {
                elem.events.fire( 'mouseover', eventArgs );
                lastMove.push( elem );
            }
        } else if (type == 'down') {
            lastDown.push(elem);
        // If mouseup on this elem and last mousedown was on this elem - click
        } else if (type == 'up' && lastDown.indexOf(elem) > -1) {
            elem.events.fire( 'click', eventArgs );
        }
        elem.events.fire( 'mouse' + type, eventArgs );

        return !this.checkFalling();
    },

    /** @private */
    forceEvent: function (type, event) {
        var
            elements = this.getOverElements(),
            i = elements.length;
        while (i--) {
            elements[i].events.fire( type, [ event ]);
            if (!this.checkFalling()) {
                break;
            }
        }
    }

});

/*
---

name: "Size"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point

provides: Size

...
*/

/** @class Size */
var Size = LibCanvas.declare( 'LibCanvas.Size', 'Size', Point, {
    set: function method (size) {
        if (typeof size == 'object' && size.width != null) {
            this.x = Number(size.width);
            this.y = Number(size.height);

            return this;
        }
        return method.previous.apply( this, arguments );
    },

    get width  ( ) { return this.x },
    get height ( ) { return this.y },
    set width  (w) { this.x = w },
    set height (h) { this.y = h },

    /** @returns {object} */
    toObject: function () {
        return { width: this.x, height: this.y };
    }
});

/** @private */
Size.from = function (object) {
    if (object == null) return null;

    return object instanceof Size ? object : new Size(object);
};

/*
---

name: "Shape"

description: "Abstract class LibCanvas.Shape defines interface for drawable canvas objects"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Geometry
    - Point

provides: Shape

...
*/

var shapeTestBuffer = function () {
    if (!shapeTestBuffer.buffer) {
        return shapeTestBuffer.buffer = LibCanvas.buffer(1, 1, true);
    }
    return shapeTestBuffer.buffer;
};

/** @class Shape */
var Shape = declare( 'LibCanvas.Shape', Geometry, {
    set        : 'abstract',
    hasPoint   : 'abstract',
    processPath: 'abstract',
    draw : function (ctx, type) {
        this.processPath(ctx)[type]();
        return this;
    },
    // Методы ниже рассчитывают на то, что в фигуре есть точки from и to
    getCoords : function () {
        return this.from;
    },
    /** @returns {LibCanvas.Shape} */
    grow: function (size) {
        if (typeof size == 'number') {
            size = new Point(size/2, size/2);
        } else {
            size = new Point(size.x/2, size.y/2);
        }

        this.from.move(size, true);
        this. to .move(size);
        return this;
    },
    get x () { return this.from.x },
    get y () { return this.from.y },
    set x (x) {
        return this.move(new Point(x - this.x, 0));
    },
    set y (y) {
        return this.move(new Point(0, y - this.y));
    },
    get bottomLeft () {
        return new Point(this.from.x, this.to.y);
    },
    get topRight() {
        return new Point(this.to.x, this.from.y);
    },
    get center() {
        var from = this.from, to = this.to;
        return new Point( (from.x + to.x) / 2, (from.y + to.y) / 2 );
    },
    getBoundingRectangle: function () {
        return new Rectangle( this.from, this.to );
    },
    getCenter : function () {
        return this.center;
    },
    move : function (distance, reverse) {
        this.from.move(distance, reverse);
        this. to .move(distance, reverse);
        return this;
    },
    equals : function (shape, accuracy) {
        return shape instanceof this.constructor &&
            shape.from.equals(this.from, accuracy) &&
            shape.to  .equals(this.to  , accuracy);
    },
    clone : function () {
        return new this.constructor(this.from.clone(), this.to.clone());
    },
    dumpPoint: function (point) {
        return '[' + point.x + ', ' + point.y + ']';
    },
    dump: function (shape) {
        if (!shape) return this.toString();
        return '[shape '+shape+'(from'+this.dumpPoint(this.from)+', to'+this.dumpPoint(this.to)+')]';
    }
});

/*
---

name: "Shapes.Rectangle"

description: "Provides rectangle as canvas object"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Shape

provides: Shapes.Rectangle

...
*/

/** @class Rectangle */
var MinusOnePoint = new Point(-1, -1);

var Rectangle = LibCanvas.declare( 'LibCanvas.Shapes.Rectangle', 'Rectangle', Shape, {
    set : function () {
        var
            center,
            size,
            a = atom.array.pickFrom(arguments),
            first = a[0];

        this.from = null;
        this.to   = null;

        if (a.length == 4) {
            this.from = new Point(a[0], a[1]);
            this.to   = new Point(a[0]+a[2], a[1]+a[3]);
        } else if (a.length == 2) {
            if ('width' in a[1] && 'height' in a[1]) {
                this.set({ from: a[0], size: a[1] });
            } else {
                this.from = Point.from(a[0]);
                this.to   = Point.from(a[1]);
            }
        } else if (first.center && first.size) {
            center = Point.from(first.center);
            size   = Size.from(first.size);

            this.from = new Point(center.x - size.x/2, center.y - size.y/2);
            this.to   = new Point(center.x + size.x/2, center.y + size.y/2);
        } else {
            if (first.from) this.from = Point.from(first.from);
            if (first.to  ) this.to   = Point.from(first.to);

            if (!this.from || !this.to && first.size) {
                size = Size.from(first.size);

                if (this.from) {
                    this.to   = new Point(this.from.x + size.x, this.from.y + size.y);
                } else {
                    this.from = new Point(this.to.x   - size.x, this.to.y   - size.y);
                }
            }
        }

        return this;
    },

    get width() {
        return this.to.x - this.from.x;
    },
    get height() {
        return this.to.y - this.from.y;
    },
    set width (width) {
        this.to.x = this.from.x + width;
    },
    set height (height) {
        this.to.y = this.from.y + height;
    },
    get size () {
        return new Size( this.width, this.height );
    },
    set size (size) {
        this.to.set(this.from.x + size.width, this.from.y + size.height);
    },
    /** @returns {boolean} */
    hasPoint : function (point, padding) {
        point   = Point.from(point);
        padding = padding || 0;
        return point.x != null && point.y != null
            && atom.number.between(point.x, Math.min(this.from.x, this.to.x) + padding, Math.max(this.from.x, this.to.x) - padding, 'L')
            && atom.number.between(point.y, Math.min(this.from.y, this.to.y) + padding, Math.max(this.from.y, this.to.y) - padding, 'L');
    },
    align: function (rect, sides) {
        if (sides == null) sides = 'center middle';

        var moveTo = this.from.clone();
        if (sides.indexOf('left') != -1) {
            moveTo.x = rect.from.x;
        } else if (sides.indexOf('center') != -1) {
            moveTo.x = rect.from.x + (rect.width - this.width) / 2;
        } else if (sides.indexOf('right') != -1) {
            moveTo.x = rect.to.x - this.width;
        }

        if (sides.indexOf('top') != -1) {
            moveTo.y = rect.from.y;
        } else if (sides.indexOf('middle') != -1) {
            moveTo.y = rect.from.y + (rect.height - this.height) / 2;
        } else if (sides.indexOf('bottom') != -1) {
            moveTo.y = rect.to.y - this.height;
        }

        return this.moveTo( moveTo );
    },
    /** @returns {LibCanvas.Shapes.Rectangle} */
    moveTo: function (rect) {
        if (rect instanceof Point) {
            this.move( this.from.diff(rect) );
        } else {
            rect = Rectangle.from(rect);
            this.from.moveTo(rect.from);
            this.  to.moveTo(rect.to);
        }
        return this;
    },
    /** @returns {LibCanvas.Shapes.Rectangle} */
    draw : function (ctx, type) {
        // fixed Opera bug - cant drawing rectangle with width or height below zero
        ctx.original(type + 'Rect', [
            Math.min(this.from.x, this.to.x),
            Math.min(this.from.y, this.to.y),
            Math.abs(this.width ),
            Math.abs(this.height)
        ]);
        return this;
    },
    /** @returns {LibCanvas.Context2D} */
    processPath : function (ctx, noWrap) {
        if (!noWrap) ctx.beginPath();
        ctx.ctx2d.rect( this.from.x, this.from.y, this.width, this.height );
        if (!noWrap) ctx.closePath();
        return ctx;
    },
    /** @returns {boolean} */
    intersect : function (obj) {
        if (obj.prototype != this.constructor) {
            if (obj.getBoundingRectangle) {
                obj = obj.getBoundingRectangle();
            } else return false;
        }
        return this.from.x < obj.to.x && this.to.x > obj.from.x
            && this.from.y < obj.to.y && this.to.y > obj.from.y;
    },
    getBoundingRectangle: function () {
        return this;
    },
    /** @returns {LibCanvas.Point} */
    getRandomPoint : function (margin) {
        margin = margin || 0;
        return new Point(
            atom.number.random(margin, this.width  - margin),
            atom.number.random(margin, this.height - margin)
        );
    },
    /** @returns {LibCanvas.Shapes.Rectangle} */
    fillToPixel: function () {
        var from = this.from, to = this.to,
            point = function (side, round) {
                return new Point(
                    Math[round](Math[side](from.x, to.x)),
                    Math[round](Math[side](from.y, to.y))
                );
            };

        return new Rectangle(
            point( 'min', 'floor' ),
            point( 'max', 'ceil'  )
        );
    },
    /** @returns {LibCanvas.Shapes.Rectangle} */
    snapToPixel: function () {
        this.from.snapToPixel();
        this.to.snapToPixel().move(MinusOnePoint);
        return this;
    },
    /** @returns {string} */
    dump: function method (name) {
        return method.previous.call(this, name || 'Rectangle');
    },
    /** @returns {LibCanvas.Shapes.Polygon} */
    toPolygon: function () {
        return new Polygon(
            this.from.clone(), this.topRight, this.to.clone(), this.bottomLeft
        );
    }
});

/** @private */
Rectangle.from = function (object) {
    if (object == null) return null;

    return object instanceof Rectangle ? object : new Rectangle(object);
};

/*
---

name: "Shapes.Circle"

description: "Provides circle as canvas object"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Shape

provides: Shapes.Circle

...
*/

/** @class Circle */
var Circle = LibCanvas.declare( 'LibCanvas.Shapes.Circle', 'Circle', Shape, {
    set : function () {
        var
            center, radius,
            a = atom.array.pickFrom(arguments);

        if (a.length >= 3) {
            center = new Point(a[0], a[1]);
            radius = a[2];
        } else if (a.length == 2) {
            center = Point.from(a[0]);
            radius = a[1];
        } else {
            a = a[0];
            radius = a.r == null ? a.radius : a.r;
            if ('x' in a && 'y' in a) {
                center = new Point(a.x, a.y);
            } else if ('center' in a) {
                center = Point.from(a.center);
            } else if ('from' in a) {
                center = new Point(a.from).move({
                    x: this.radius,
                    y: this.radius
                });
            }
        }

        this.center = center;
        this.radius = radius;

        if (center == null) throw new TypeError('center is null');
        if (radius == null) throw new TypeError('radius is null');
    },
    // we need accessors to redefine parent "get center"
    get center ( ) { return this._center; },
    set center (c) { this._center = c; },
    grow: function (size) {
        this.radius += size/2;
        return this;
    },
    getCoords : function () {
        return this.center;
    },
    hasPoint : function (point) {
        return this.center.checkDistanceTo(point, this.radius, true);
    },
    scale : function (factor, pivot) {
        if (pivot) this.center.scale(factor, pivot);
        this.radius *= factor;
        return this;
    },
    getCenter: function () {
        return this.center;
    },
    intersect : function (obj) {
        if (obj instanceof this.constructor) {
            return this.center.checkDistanceTo(obj.center, this.radius + obj.radius, true);
        } else {
            return this.getBoundingRectangle().intersect( obj );
        }
    },
    move : function (distance, reverse) {
        this.center.move(distance, reverse);
        return this;
    },
    processPath : function (ctx, noWrap) {
        if (!noWrap) ctx.beginPath();
        if (this.radius) {
            ctx.arc({
                circle : this,
                angle  : [0, Math.PI * 2]
            });
        }
        if (!noWrap) ctx.closePath();
        return ctx;
    },
    getBoundingRectangle: function () {
        var r = this.radius, center = this.center;
        return new Rectangle(
            new Point(center.x - r, center.y - r),
            new Point(center.x + r, center.y + r)
        );
    },
    clone : function () {
        return new this.constructor(this.center.clone(), this.radius);
    },
    getPoints : function () {
        return { center : this.center };
    },
    equals : function (shape, accuracy) {
        return shape instanceof this.shape &&
            shape.radius == this.radius    &&
            shape.center.equals(this.center, accuracy);
    },
    dump: function () {
        return '[shape Circle(center['+this.center.x+', '+this.center.y+'], '+this.radius+')]';
    }
});

/** @private */
Circle.from = function (object) {
    if (object == null) return null;

    return object instanceof Circle ? object : new Circle(object);
};


/*
---

name: "Core.Canvas"

description: "Provides some Canvas extensions"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas

provides: Core.Canvas

...
*/

atom.core.append(HTMLCanvasElement,
/** @lends HTMLCanvasElement */
{
    /** @private */
    _newContexts: {},
    /** @returns {HTMLCanvasElement} */
    addContext: function (name, ctx) {
        this._newContexts[name] = ctx;
        return this;
    },
    /** @returns {Context2D} */
    getContext: function (name) {
        return this._newContexts[name] || null;
    }
});

atom.core.append(HTMLCanvasElement.prototype,
/** @lends HTMLCanvasElement.prototype */
{
    getOriginalContext: HTMLCanvasElement.prototype.getContext,
    /** @returns {Context2D} */
    getContext: function (type) {
        if (!this.contextsList) {
            this.contextsList = {};
        }

        if (!this.contextsList[type]) {
            var ctx = HTMLCanvasElement.getContext(type);
            if (ctx) {
                ctx = new ctx(this);
            } else try {
                ctx = this.getOriginalContext.apply(this, arguments);
            } catch (e) {
                throw (!e.toString().match(/NS_ERROR_ILLEGAL_VALUE/)) ? e :
                    new TypeError('Wrong Context Type: «' + type + '»');
            }
            this.contextsList[type] = ctx;
        }
        return this.contextsList[type];
    }
});

/*
---

name: "Context.DrawImage"

description: "LibCanvas.Context2D adds new canvas context '2d-libcanvas'"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Size
    - Shapes.Rectangle
    - Shapes.Circle

provides: Context.DrawImage

...
*/

new function () {

var toPoint = Point.from, toRectangle = Rectangle.from;

/** @class LibCanvas.Context.DrawImage */
LibCanvas.declare( 'LibCanvas.Context.DrawImage', {
    initialize: function (context) {
        this.context = context;
        this.ctx2d   = context.ctx2d;
    },

    drawImage: function (args) {
        var a, center, from, draw, crop, scale, image, pivot, angle;

        if (this.checkNonObject(args)) return;

        a = args[0];

        image  = a.image;
        angle  = a.angle;
        scale  = a.scale  && toPoint(a.scale);
        center = a.center && toPoint(a.center);
        from   = a.from   && toPoint(a.from);
        draw   = a.draw   && toRectangle(a.draw);
        crop   = a.crop   && toRectangle(a.crop);

        if (! atom.dom.isElement(image) ) throw new TypeError('Wrong image in Context.DrawImage');
        if (! (center || from || draw)  ) throw new TypeError('Wrong arguments in Context.DrawImage');

        pivot = this.getTransformPivot(
            angle, scale, image,
            center, from, draw
        );

        if (pivot) this.transform(pivot, angle, scale);
        draw ?
            this.drawRect (image, draw, crop  , a.optimize) :
            this.drawPoint(image, from, center, a.optimize);
        if (pivot) this.ctx2d.restore();

        return this.context;
    },

    /** @private */
    run: function (array) {
        this.ctx2d.drawImage.apply( this.ctx2d, array );
    },
    /** @private */
    transform: function (center, angle, scale) {
        this.ctx2d.save();
        if (angle) this.context.rotate(angle, center);
        if (scale) this.context.scale (scale, center);
    },
    /** @private */
    checkNonObject: function (args) {
        var image = args[0], length = args.length, target;
        if (length > 2) {
            this.run(args);
            return true;
        }
        if (length == 2) {
            target = args[1];

            if (target instanceof Point) {
                this.drawPoint(image, target);
                return true;
            }
            if (target instanceof Rectangle) {
                this.drawRect(image, target);
                return true;
            }

            throw new Error('Unknown second argument in Context.DrawImage');
        }

        if (length == 0) {
            throw new Error('Empty arguments in Context.DrawImage');
        }

        if (atom.dom.isElement(image)) {
            this.ctx2d.drawImage(image, 0, 0);
            return true;
        }

        return false;
    },
    /** @private */
    drawPoint: function (image, from, center, optimize) {
        var
            point = center || from,
            fromX = point.x,
            fromY = point.y;

        if (center) {
            fromX -= image.width  / 2;
            fromY -= image.height / 2;
        }

        if (optimize) {
            fromX = Math.round(fromX);
            fromY = Math.round(fromY);
        }

        this.ctx2d.drawImage(image, fromX, fromY);
    },
    /** @private */
    drawRect: function (image, rect, crop, optimize) {
        var deltaX, deltaY, fromX, fromY;

        if (crop) {
            this.ctx2d.drawImage( image,
                crop.from.x, crop.from.y, crop.width, crop.height,
                rect.from.x, rect.from.y, rect.width, rect.height
            );
            return;
        }

        if (optimize) {
            fromX  = Math.round(rect.from.x);
            fromY  = Math.round(rect.from.y);
            deltaX = Math.abs(rect.width  - image.width );
            deltaY = Math.abs(rect.height - image.width );

            if (deltaX < 1.1 && deltaY < 1.1) {
                this.ctx2d.drawImage(image, fromX, fromY);
            } else {
                this.ctx2d.drawImage(image, fromX, fromY,
                    Math.round(rect.width),
                    Math.round(rect.height)
                );
            }
            return;
        }

        this.ctx2d.drawImage( image,
            rect.from.x, rect.from.y,
            rect.width , rect.height
        );
    },
    /** @private */
    getTransformPivot: function (angle, scale, image, center, from, draw) {
        if ( !angle && (!scale || (scale.x == 1 && scale.y == 1)) ) return null;

        if (center) return center;
        if ( draw ) return draw.center;

        return new Point(from.x + image.width/2, from.y + image.height/2);
    }
});

};


/*
---

name: "Context.Gradients"

description: "LibCanvas.Context2D adds new canvas context '2d-libcanvas'"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Size
    - Shapes.Rectangle
    - Shapes.Circle

provides: Context.Gradients

...
*/

new function () {

var toPoint = Point.from, toRectangle = Rectangle.from, toCircle = Circle.from;


var addColorStopSource = document
    .createElement('canvas')
    .getContext('2d')
    .createLinearGradient(0,0,1,1)
    .addColorStop;

var addColorStop = function (colors) {
    if (typeof colors == 'object') {
        for (var position in colors) if (colors.hasOwnProperty(position)) {
            addColorStopSource.call( this, parseFloat(position), colors[position] );
        }
    } else {
        addColorStopSource.apply( this, arguments );
    }
    return this;
};


var fixGradient = function (grad) {
    grad.addColorStop = addColorStop;
    return grad;
};

/** @class LibCanvas.Context.Gradients */
LibCanvas.declare( 'LibCanvas.Context.Gradients', {
    initialize: function (context) {
        this.context = context;
        this.ctx2d   = context.ctx2d;
    },

    /** @returns {CanvasGradient} */
    createGradient: function (from, to, colors) {
        var gradient;
        if ( from instanceof Rectangle ) {
            colors   = to;
            gradient = this.createLinearGradient([ from ]);
        } else if (from instanceof Circle) {
            gradient = this.createRadialGradient([ from, to ]);
        } else if (from instanceof Point) {
            gradient = this.createLinearGradient([ from, to ]);
        } else {
            throw new Error('Unknown arguments in Context.Gradients.createGradient');
        }
        if (typeof colors == 'object') gradient.addColorStop( colors );
        return gradient;
    },
    /** @returns {CanvasGradient} */
    createRectangleGradient: function (rectangle, colors) {
        rectangle = toRectangle( rectangle );

        var from = rectangle.from, line = new Line( rectangle.bottomLeft, rectangle.topRight );

        return this.createGradient( from, line.perpendicular(from).scale(2, from), colors );
    },
    /** @returns {CanvasGradient} */
    createLinearGradient : function (a) {
        var from, to;
        if (a.length != 4) {
            if (a.length == 2) {
                to   = toPoint(a[0]);
                from = toPoint(a[1]);
            } else if (a.length == 1) {
                to   = toPoint(a[0].to);
                from = toPoint(a[0].from);
            } else {
                throw new TypeError('Wrong arguments.length in the Context.createLinearGradient');
            }
            a = [from.x, from.y, to.x, to.y];
        }
        return fixGradient( this.ctx2d.createLinearGradient.apply(this.ctx2d, a) );
    },
    /** @returns {CanvasGradient} */
    createRadialGradient: function (a) {
        var points, c1, c2, length = a.length;
        if (length == 1 || length == 2) {
            if (length == 2) {
                c1 = toCircle( a[0] );
                c2 = toCircle( a[1] );
            } else {
                c1 = toCircle( a.start );
                c2 = toCircle( a.end   );
            }
            points = [c1.center.x, c1.center.y, c1.radius, c2.center.x, c2.center.y, c2.radius];
        } else if (length == 6) {
            points = a;
        } else {
            throw new TypeError('Wrong arguments.length in the Context.createRadialGradient');
        }

        return fixGradient( this.ctx2d.createRadialGradient.apply(this.ctx2d, points) );
    }
});

};


/*
---

name: "Context.Path"

description: "LibCanvas.Context2D adds new canvas context '2d-libcanvas'"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Size
    - Shapes.Circle

provides: Context.Path

...
*/

new function () {

var toPoint = Point.from, toCircle = Circle.from;


/** @class LibCanvas.Context.Path */
LibCanvas.declare( 'LibCanvas.Context.Path', {
    initialize: function (context) {
        this.context = context;
        this.ctx2d   = context.ctx2d;
    },


    /** @returns {Context2D} */
    arc : function (a) {

        if (a.length > 1) {
            return this.ctx2d.arc.apply(this.ctx2d, a);
        } else if (!a[0].circle) {
            throw new TypeError('Wrong arguments in CanvasContext.arc');
        }

        var f = a[0], circle, angle, angleStart, angleEnd, angleSize;
        circle = toCircle(f.circle);
        angle = f.angle;

        if (Array.isArray(angle)) {
            angleStart = angle[0];
            angleEnd   = angle[1];
        } else {
            angleStart = angle.start;
            angleEnd   = angle.end;
            angleSize  = angle.size;

            if (angleSize == null) {
                // do nothing
            } else if (angleEnd == null) {
                angleEnd = angleSize + angleStart;
            } else if (angleStart == null) {
                angleStart = angleEnd - angleSize;
            }
        }
        this.ctx2d.arc(
            circle.center.x, circle.center.y, circle.radius,
            angleStart, angleEnd, !!(f.anticlockwise || f.acw)
        );
        return this.context;
    },

    /** @returns {Context2D} */
    arcTo : function () {
        // @todo Beauty arguments
        this.ctx2d.arcTo.apply(this.ctx2d, arguments);
        return this.context;
    },
    /** @returns {Context2D} */
    curveTo: function (a) {
        var p, l, to, curve = a[0];

        if (typeof curve == 'number') {
            if (a.length === 4) {
                return this.quadraticCurveTo(a);
            } else if (a.length === 6) {
                return this.bezierCurveTo(a);
            }
        } else if (a.length > 1) {
            p  = atom.array.from( a ).map(toPoint);
            to = p.shift()
        } else {
            p  = atom.array.from( curve.points ).map(toPoint);
            to = toPoint(curve.to);
        }

        l = p.length;

        if (l == 2) {
            this.ctx2d.bezierCurveTo(
                p[0].x, p[0].y, p[1].x, p[1].y, to.x, to.y
            );
        } else if (l == 1) {
            this.ctx2d.quadraticCurveTo(
                p[0].x, p[0].y, to.x, to.y
            );
        } else {
            this.ctx2d.lineTo(to.x, to.y);
        }
        return this.context;
    },
    /** @returns {Context2D} */
    quadraticCurveTo : function (a) {
        if (a.length == 4) {
            this.ctx2d.quadraticCurveTo.apply(this.ctx2d, a);
            return this.context;
        } else {
            a = a.length == 2 ? {p:a[0], to:a[1]} : a[0];
            return this.curveTo([{
                to: a.to,
                points: [a.p]
            }]);
        }
    },
    /** @returns {Context2D} */
    bezierCurveTo : function (a) {
        if (a.length == 6) {
            this.ctx2d.bezierCurveTo.apply(this.ctx2d, a);
            return this.context;
        } else {
            a = a.length == 3 ? {p1:a[0], p2:a[1], to:a[2]} : a[0];
            return this.curveTo([{
                to: a.to,
                points: [a.p1, a.p2]
            }]);
        }
    },
    isPointInPath: function (x, y) {
        if (y == null) {
            x = toPoint(x);
            y = x.y;
            x = x.x;
        }
        return this.ctx2d.isPointInPath(x, y);
    }

});

};


/*
---

name: "Context.Pixels"

description: "LibCanvas.Context2D adds new canvas context '2d-libcanvas'"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Size
    - Shapes.Rectangle
    - Shapes.Circle

provides: Context.Pixels

...
*/

new function () {

var toPoint = Point.from, toRectangle = Rectangle.from, size1x1 = new Size(1,1);


/** @class LibCanvas.Context.Pixels */
LibCanvas.declare( 'LibCanvas.Context.Pixels', {
    initialize: function (context) {
        this.context = context;
        this.ctx2d   = context.ctx2d;
    },

    // image data
    /** @returns {CanvasPixelArray} */
    createImageData : function (w, h) {
        if (w == null) {
            w = this.context.width;
            h = this.context.height;
        } else if (h == null) {
            if (w.width == null && w.height == null) {
                throw new TypeError('Wrong argument in the Context.createImageData');
            } else {
                h = w.height;
                w = w.width;
            }
        }

        return this.ctx2d.createImageData(w, h);
    },

    /** @returns {Context2D} */
    putImageData : function (a) {
        var put = {}, args, rect;

        switch (a.length) {
            case 1: {
                if (typeof a != 'object') {
                    throw new TypeError('Wrong argument in the Context.putImageData');
                }

                a = a[0];
                put.image = a.image;
                put.from = toPoint(a.from);

                if (a.crop) put.crop = toRectangle(a.crop);
            } break;

            case 3: {
                put.image = a[0];
                put.from = new Point(a[1], a[2]);
            } break;

            case 7: {
                put.image = a[0];
                put.from = new Point(a[1], a[2]);
                put.crop = new Rectangle(a[3], a[4], a[5], a[6]);
            } break;

            default : throw new TypeError('Wrong args number in the Context.putImageData');
        }

        args = [put.image, put.from.x, put.from.y];

        if (put.crop) {
            rect = put.crop;
            atom.array.append(args, [rect.from.x, rect.from.y, rect.width, rect.height])
        }

        this.ctx2d.putImageData.apply(this.ctx2d, args);
        return this.context;
    },
    /** @returns {CanvasPixelArray} */
    getImageData : function (args) {
        var rect = toRectangle(args.length > 1 ? args : args[0]);

        return this.ctx2d.getImageData(rect.from.x, rect.from.y, rect.width, rect.height);
    },
    getPixels : function (args) {
        var
            rect = toRectangle(args.length > 1 ? args : args[0]),
            data = this.getImageData(rect).data,
            result = [],
            line = [];
        for (var i = 0, L = data.length; i < L; i+=4)  {
            line.push({
                r : data[i],
                g : data[i+1],
                b : data[i+2],
                a : data[i+3] / 255
            });
            if (line.length == rect.width) {
                result.push(line);
                line = [];
            }
        }
        return result;
    },

    getPixel: function (point) {
        var
            rect = new Rectangle(toPoint( point ), size1x1),
            data = slice.call(this.getImageData([rect]).data);

        data[3] /= 255;

        return new atom.Color(data);
    }

});

};


/*
---

name: "Context.Text"

description: "LibCanvas.Context2D adds new canvas context '2d-libcanvas'"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Size
    - Shapes.Rectangle
    - Shapes.Circle

provides: Context.Text

...
*/

new function () {

var toPoint = Point.from, toRectangle = Rectangle.from, size1x1 = new Size(1,1);


/** @class LibCanvas.Context.Text */
LibCanvas.declare( 'LibCanvas.Context.Text', {
    initialize: function (context) {
        this.context = context;
        this.ctx2d   = context.ctx2d;
    },
    // text
    /** @returns {Context2D} */
    method: function (method, text, x, y, maxWidth) {
        var type = typeof x;
        if (type != 'number' && type != 'string') {
            maxWidth = y;
            x = toPoint( x );
            y = x.y;
            x = x.x;
        }
        var args = [text, x, y];
        if (maxWidth) args.push( maxWidth );
        this.ctx2d[method].apply( this.ctx2d, args );
        return this.context;
    },
    fillText : function (text, x, y, maxWidth) {
        return this.method(  'fillText', text, x, y, maxWidth);
    },
    strokeText : function (text, x, y, maxWidth) {
        return this.method('strokeText', text, x, y, maxWidth);
    },
    /** @returns {object} */
    measureText : function (args) {
        return this.ctx2d.measureText.apply(this.ctx2d, args)
    },
    /** @returns {Context2D} */
    text : function (cfg) {
        if (!this.ctx2d.fillText) return this;

        var ctx = this.ctx2d;

        cfg = atom.core.append({
            text   : '',
            color  : null, /* @color */
            wrap   : 'normal', /* no|normal */
            to     : null,
            align  : 'left', /* center|left|right */
            size   : 16,
            weight : 'normal', /* bold|normal */
            style  : 'normal', /* italic|normal */
            family : 'arial,sans-serif', /* @fontFamily */
            lineHeight : null,
            overflow   : 'visible', /* hidden|visible */
            padding : [0,0],
            shadow : null,
            stroke : null,
            lineWidth : null
        }, cfg);

        ctx.save();
        if (typeof cfg.padding == 'number') {
            cfg.padding = [cfg.padding, cfg.padding];
        }
        var method = cfg.stroke ? 'strokeText' : 'fillText';
        var to = cfg.to ? toRectangle(cfg.to) : this.context.rectangle;
        var lh = Math.round(cfg.lineHeight || (cfg.size * 1.15));
        this.context.set('font', atom.string.substitute(
            '{style}{weight}{size}px {family}', {
                style  : cfg.style == 'italic' ? 'italic ' : '',
                weight : cfg.weight == 'bold'  ? 'bold '   : '',
                size   : cfg.size,
                family : cfg.family
            })
        );

        if (cfg.color) {
            this.context.set(cfg.stroke ? 'strokeStyle' : 'fillStyle', cfg.color);
        }

        if (cfg.shadow) this.context.shadow = cfg.shadow;
        if (cfg.overflow == 'hidden') this.context.clip(to);
        if (cfg.lineWidth) this.context.set({ lineWidth: cfg.lineWidth });

        function xGet (lineWidth) {
            var al = cfg.align, pad = cfg.padding[1];
            return Math.round(
                al == 'left'  ? to.from.x + pad :
                al == 'right' ? to.to.x - lineWidth - pad :
                    to.from.x + (to.width - lineWidth)/2
            );
        }
        function measure (text) {
            return Number(ctx.measureText(text).width);
        }
        var lines = String(cfg.text).split('\n');

        if (cfg.wrap == 'no') {
            lines.forEach(function (line, i) {
                if (!line) return;

                ctx[method](line, xGet(cfg.align == 'left' ? 0 : measure(line)), to.from.y + (i+1)*lh);
            });
        } else {
            var lNum = 0;
            lines.forEach(function (line) {
                if (!line) {
                    lNum++;
                    return;
                }

                var words = (line || ' ').match(/.+?(\s|$)/g);
                if (!words) {
                    lNum++;
                    return;
                }
                var L  = '';
                var Lw = 0;
                for (var i = 0; i <= words.length; i++) {
                    var last = i == words.length;
                    if (!last) {
                        var text = words[i];
                        // @todo too slow. 2-4ms for 50words
                        var wordWidth = measure(text);
                        if (!Lw || Lw + wordWidth < to.width) {
                            Lw += wordWidth;
                            L  += text;
                            continue;
                        }
                    }
                    if (Lw) {
                        ctx[method](L, xGet(Lw), to.from.y + (++lNum)*lh + cfg.padding[0]);
                        if (last) {
                            L  = '';
                            Lw = 0;
                        } else {
                            L  = text;
                            Lw = wordWidth;
                        }
                    }
                }
                if (Lw) {
                    ctx[method](L, xGet(Lw), to.from.y + (++lNum)*lh + cfg.padding[0]);
                }
            });

        }
        ctx.restore();
        return this.context;
    }

});

};


/*
---

name: "Context2D"

description: "LibCanvas.Context2D adds new canvas context '2d-libcanvas'"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Size
    - Shapes.Rectangle
    - Shapes.Circle
    - Core.Canvas
    - Context.DrawImage
    - Context.Gradients
    - Context.Path
    - Context.Pixels
    - Context.Text

provides: Context2D

...
*/

/**
 * @class
 * @name Context2D
 * @name LibCanvas.Context2D
 */
var Context2D = function () {

var office = {
    all : function (type, style) {
        this.save();
        if (style) this.set(type + 'Style', style);
        this[type + 'Rect'](this.rectangle);
        this.restore();
        return this;
    },
    rect : function (func, args) {
        var rect = office.makeRect.call(this, args);
        return this.original(func,
            [rect.from.x, rect.from.y, rect.width, rect.height]);
    },
    makeRect: function (args) {
        return args.length ? Rectangle(args) : this.rectangle;
    },
    fillStroke : function (type, args) {
        if (args.length >= 1 && args[0] instanceof Shape) {
            if (args[1]) this.save().set(type + 'Style', args[1]);
            args[0].draw(this, type);
            if (args[1]) this.restore();
        } else {
            if (args.length && args[0]) this.save().set(type + 'Style', args[0]);
            this.original(type);
            if (args.length && args[0]) this.restore();
        }
        
        return this;
    },
    originalPoint : function (func, args) {
        var point = Point(args);
        return this.original(func, [point.x, point.y]);
    }
};

/* In some Mobile browsers shadowY should be inverted (bug) */
var shadowBug = function () {
    // todo: use LibCanvas.buffer
    var ctx = atom.dom
        .create('canvas', { width: 15, height: 15 })
        .first.getContext( '2d' );

    ctx.shadowBlur    = 1;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = -5;
    ctx.shadowColor   = 'green';

    ctx.fillRect( 0, 5, 5, 5 );

    // Color should contains green component to be correct (128 is correct value)
    return ctx.getImageData(0, 0, 1, 1).data[1] < 64;

}();

var constants =
/** @lends LibCanvas.Context2D */
{
    COMPOSITE: {
        SOURCE_OVER: 'source-over',
        SOURCE_IN  : 'source-in',
        SOURCE_OUT : 'source-out',
        SOURCE_ATOP: 'source-atop',

        DESTINATION_OVER: 'destination-over',
        DESTINATION_IN  : 'destination-in',
        DESTINATION_OUT : 'destination-out',
        DESTINATION_ATOP: 'destination-atop',

        LIGHTER: 'lighter',
        DARKER : 'darker',
        COPY   : 'copy',
        XOR    : 'xor'
    },

    LINE_CAP: {
        BUTT  : 'butt',
        ROUND : 'round',
        SQUARE: 'square'
    },

    LINE_JOIN: {
        ROUND: 'round',
        BEVEL: 'bevel',
        MITER: 'miter'
    },

    TEXT_ALIGN: {
        LEFT  : 'left',
        RIGHT : 'right',
        CENTER: 'center',
        START : 'start',
        END   : 'end'
    },

    TEXT_BASELINE: {
        TOP        : 'top',
        HANGING    : 'hanging',
        MIDDLE     : 'middle',
        ALPHABETIC : 'alphabetic',
        IDEOGRAPHIC: 'ideographic',
        BOTTOM     : 'bottom'
    },

    SHADOW_BUG: shadowBug

};

var Context2D = LibCanvas.declare( 'LibCanvas.Context2D', 'Context2D',
/**
 * @lends LibCanvas.Context2D.prototype
 * @property {string} fillStyle
 * @property {string} font
 * @property {number} globalAlpha
 * @property {string} globalCompositeOperation
 * @property {string} lineCap
 * @property {string} lineJoin
 * @property {number} lineWidth
 * @property {number} miterLimit
 * @property {number} shadowOffsetX
 * @property {number} shadowOffsetY
 * @property {number} shadowBlur
 * @property {string} shadowColor
 * @property {string} strokeStyle
 * @property {string} textAlign
 * @property {string} textBaseline
 */
{
    initialize : function (canvas) {
        if (canvas instanceof CanvasRenderingContext2D) {
            this.ctx2d  = canvas;
            this.canvas = this.ctx2d.canvas;
        } else {
            this.canvas = canvas;
            this.ctx2d  = atom.core.isFunction(canvas.getOriginalContext) ?
                canvas.getOriginalContext('2d') :
                canvas.getContext('2d');
        }

        this.helpers = {
            image    : new LibCanvas.Context.DrawImage(this),
            gradients: new LibCanvas.Context.Gradients(this),
            pixels   : new LibCanvas.Context.Pixels   (this),
            text     : new LibCanvas.Context.Text     (this),
            path     : new LibCanvas.Context.Path     (this)
        };
    },
    get width () { return this.canvas.width; },
    get height() { return this.canvas.height; },
    set width (width)  { this.canvas.width  = width; },
    set height(height) { this.canvas.height = height;},
    
    get size () { 
        return new Size(this.width, this.height);
    },
    set size (size) {
        size = Size.from(size);
        this.width  = size.width;
        this.height = size.height;
    },
    

    get shadow () {
        return [this.shadowOffsetX, this.shadowOffsetY, this.shadowBlur, this.shadowColor].join( ' ' );
    },

    set shadow (value) {
        value = value.split( ' ' );
        this.shadowOffsetX = value[0];
        this.shadowOffsetY = value[1];
        this.shadowBlur    = value[2];
        this.shadowColor   = value[3];
    },

    /** @private */
    safeSet: function (property, value) {
        try {
            this.ctx2d[property] = value;
        } catch (e) {
            throw TypeError('Exception while setting «' + property + '» to «' + value + '»: ' + e.message);
        }
    },

    set shadowOffsetY (value) {
        if (shadowBug) value *= -1;
        this.safeSet('shadowOffsetY', value);
    },

    set shadowBlur (value) {
        if (shadowBug && value < 1) value = 1;
        this.safeSet('shadowBlur', value);
    },

    get shadowOffsetY () {
        return this.ctx2d.shadowOffsetY;
    },

    get shadowBlur () {
        return this.ctx2d.shadowBlur;
    },

    get opacity () {
        return this.globalAlpha;
    },

    set opacity (value) {
        this.globalAlpha = value;
    },

    _rectangle: null,
    /** @returns {Rectangle} */
    get rectangle () {
        var rect = this._rectangle;
        if (!rect) {
            this._rectangle = rect = new Rectangle(0, 0, this.width, this.height)
        } else {
            rect.size = this;
        }
        return rect;
    },
    /** @returns {Context2D} */
    original : function (method, args, returnResult) {
        var result = this.ctx2d[method].apply(this.ctx2d, args || []);
        return returnResult ? result: this;
    },
    /** @returns {HTMLCanvasElement} */
    getClone : function (width, height) {
        var resize = !!(width || height), canvas = this.canvas;
        width  = width  || canvas.width;
        height = height || canvas.height;

        var args = [canvas, 0, 0];
        if (resize) args.push(width, height);

        var clone = LibCanvas.buffer(width, height, true);
        clone.ctx.original('drawImage', args);
        return clone;
    },

    // Values
    /** @returns {Context2D} */
    set : function (name, value) {
        if (typeof name == 'object') {
            for (var i in name) this[i] = name[i];
        } else this[name] = value;
        return this;
    },
    /** @returns {string} */
    get : function (name) {
        return this[name];
    },

    // All
    /** @returns {Context2D} */
    fillAll : function (style) {
        return office.all.call(this, 'fill', style);
    },
    /** @returns {Context2D} */
    strokeAll : function (style) {
        return office.all.call(this, 'stroke', style);
    },
    /** @returns {Context2D} */
    clearAll : function () {
        return this.ctx2d.clearRect(0,0,this.canvas.width,this.canvas.height);
    },

    // Save/Restore
    /** @returns {Context2D} */
    save : function () {
        this.ctx2d.save();
        return this;
    },
    /** @returns {Context2D} */
    restore : function () {
        this.ctx2d.restore();
        return this;
    },

    // Fill/Stroke
    /** @returns {Context2D} */
    fill : function (shape) {
        return office.fillStroke.call(this, 'fill', arguments);
    },
    /** @returns {Context2D} */
    stroke : function (shape) {
        return office.fillStroke.call(this, 'stroke', arguments);
    },
    /** @returns {Context2D} */
    clear: function (shape, stroke) {
        return shape instanceof Shape && shape.constructor != Rectangle ?
            this
                .save()
                .set({ globalCompositeOperation: Context2D.COMPOSITE.DESTINATION_OUT })
                [stroke ? 'stroke' : 'fill']( shape )
                .restore() :
            this.clearRect( Rectangle.from(shape) );
    },

    // Path
    /** @returns {Context2D} */
    beginPath : function (moveTo) {
        var ret = this.original('beginPath');
        arguments.length && this.moveTo.apply(this, arguments);
        return ret;
    },
    /** @returns {Context2D} */
    closePath : function () {
        arguments.length && this.lineTo.apply(this, arguments);
        return this.original('closePath');
    },
    /** @returns {Context2D} */
    moveTo : function (point) {
        return office.originalPoint.call(this, 'moveTo', arguments);
    },
    /** @returns {Context2D} */
    lineTo : function (point) {
        return office.originalPoint.call(this, 'lineTo', arguments);
    },
    /** @returns {Context2D} */
    arc : function (x, y, r, startAngle, endAngle, anticlockwise) {
        return this.helpers.path.arc(arguments);
    },
    /** @returns {Context2D} */
    arcTo : function () {
        return this.helpers.path.arcTo(arguments);
    },
    /** @returns {Context2D} */
    curveTo: function (curve) {
        return this.helpers.path.curveTo(arguments);
    },
    /** @returns {Context2D} */
    quadraticCurveTo : function () {
        return this.helpers.path.quadraticCurveTo(arguments);
    },
    /** @returns {Context2D} */
    bezierCurveTo : function () {
        return this.helpers.path.bezierCurveTo(arguments);
    },
    /** @returns {boolean} */
    isPointInPath : function (x, y) {
        return this.helpers.path.isPointInPath(x, y);
    },
    /** @returns {Context2D} */
    clip : function (shape) {
        if (shape && typeof shape.processPath == 'function') {
            shape.processPath(this);
        }
        return this.original('clip');
    },

    // transformation
    /** @returns {Context2D} */
    rotate : function (angle, pivot) {
        if (angle) {
            if (pivot) this.translate(pivot);
            this.original('rotate', [angle]);
            if (pivot) this.translate(pivot, true);
        }
        return this;
    },
    /** @returns {Context2D} */
    translate : function (point, reverse) {
        point = Point(
            (arguments.length === 1 || typeof reverse === 'boolean')
                ? point : arguments
        );
        var multi = reverse === true ? -1 : 1;
        this.original('translate', [point.x * multi, point.y * multi]);
        return this;
    },
    /** @returns {Context2D} */
    scale : function (power, pivot) {
        if (typeof pivot == 'number') {
            power = new Point(power, pivot);
            pivot = null;
        } else {
            power = Point(power);
        }
        if (power.x != 1 || power.y != 1) {
            if (pivot) this.translate(pivot);
            this.original('scale', [power.x, power.y]);
            if (pivot) this.translate(pivot, true);
        }
        return this;
    },
    /** @returns {Context2D} */
    transform : function () {
        // @todo Beauty arguments
        return this.original('transform', arguments);
    },
    /** @returns {Context2D} */
    setTransform : function () {
        // @todo Beauty arguments
        return this.original('setTransform', arguments);
    },

    // Rectangle
    /** @returns {Context2D} */
    fillRect : function (rectangle) {
        return office.rect.call(this, 'fillRect', arguments);
    },
    /** @returns {Context2D} */
    strokeRect : function (rectangle) {
        return office.rect.call(this, 'strokeRect', arguments);
    },
    /** @returns {Context2D} */
    clearRect : function (rectangle) {
        return office.rect.call(this, 'clearRect', arguments);
    },

    // === helpers.text === //

    /** @returns {Context2D} */
    fillText : function (text, x, y, maxWidth) {
        return this.helpers.text.fillText(text, x, y, maxWidth);
    },
    /** @returns {Context2D} */
    strokeText : function (text, x, y, maxWidth) {
        return this.helpers.text.strokeText(text, x, y, maxWidth);
    },
    /** @returns {object} */
    measureText : function (textToMeasure) {
        return this.helpers.text.measureText(arguments);
    },
    /** @returns {Context2D} */
    text : function (cfg) {
        return this.helpers.text.text(cfg);
    },

    // === helpers.drawImage === //

    /** @returns {Context2D} */
    drawImage : function () {
        return this.helpers.image.drawImage(arguments);
    },

    // === helpers.pixels === //

    /** @returns {CanvasPixelArray} */
    createImageData : function (w, h) {
        return this.helpers.pixels.createImageData(w, h);
    },
    /** @returns {Context2D} */
    putImageData : function () {
        return this.helpers.pixels.putImageData(arguments);
    },
    /** @returns {CanvasPixelArray} */
    getImageData : function (rectangle) {
        return this.helpers.pixels.getImageData(arguments);
    },
    getPixels : function (rectangle) {
        return this.helpers.pixels.getPixels(arguments);
    },
    getPixel: function (point) {
        return this.helpers.pixels.getPixel(point);
    },

    // === helpers.gradients === //

    /** @returns {CanvasGradient} */
    createGradient: function (from, to, colors) {
        return this.helpers.gradients.createGradient(from, to, colors);
    },
    /** @returns {CanvasGradient} */
    createRectangleGradient: function (rectangle, colors) {
        return this.helpers.gradients.createRectangleGradient(rectangle, colors);
    },
    /** @returns {CanvasGradient} */
    createLinearGradient : function () {
        return this.helpers.gradients.createLinearGradient(arguments);
    },
    /** @returns {CanvasGradient} */
    createRadialGradient: function () {
        return this.helpers.gradients.createRadialGradient(arguments);
    },

    // === etc === //

    /** @returns {CanvasPattern} */
    createPattern : function () {
        return this.original('createPattern', arguments, true);
    },

    drawWindow : function () {
        return this.original('drawWindow', arguments);
    }

}).own(constants);


[ 'fillStyle','font','globalAlpha','globalCompositeOperation','lineCap',
  'lineJoin','lineWidth','miterLimit','shadowOffsetX','shadowColor',
  'strokeStyle','textAlign','textBaseline'
    // we'll set this values manually because of bug in Mobile Phones
    // 'shadowOffsetY','shadowBlur'
].forEach(function (property) {
    atom.accessors.define(Context2D.prototype, property, {
        set: function (value) {
            this.safeSet(property, value);
        },
        get: function () {
            return this.ctx2d[property];
        }
    })
});

Context2D.office = office;

if (atom.core.isFunction(HTMLCanvasElement.addContext)) {
    HTMLCanvasElement.addContext('2d-libcanvas', Context2D);
}

return Context2D;

}();


/*
---

name: "Point3D"

description: "A X/Y/Z point coordinates encapsulating class"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Geometry

provides: Point3D

...
*/

/** @class Point3D */
var Point3D = LibCanvas.declare( 'LibCanvas.Point3D', 'Point3D', Geometry, {
    x: 0,
    y: 0,
    z: 0,

    /** @private */
    coordinatesArray: ['x', 'y', 'z'],

    /**
     * @constructs
     * @param {Number} x
     * @param {Number} y
     * @param {Number} z
     * @returns {Point3D}
     */
    set: function (x, y, z) {
        if ( arguments.length > 1 ) {
            this.x = Number(x) || 0;
            this.y = Number(y) || 0;
            this.z = Number(z) || 0;
        } else if ( x && typeof x.x  === 'number' ) {
            this.set( x.x, x.y, x.z );
        } else if ( x && typeof x[0] === 'number' ) {
            this.set( x[0], x[1], x[2] );
        } else {
            throw new Error( 'Wrong arguments in Isometric.Point3D' );
        }
        return this;
    },

    /**
     * You can pass callback (function( value, axis, point ){})
     * @param {function} fn
     * @param {object} [context=null]
     * @returns {Point3D}
     */
    map: function (fn, context) {
        var point = this;
        point.coordinatesArray.forEach(function (axis) {
            point[axis] = fn.call( context || point, point[axis], axis, point );
        });
        return this;
    },

    /**
     * @param {Number} factor
     * @returns {Point3D}
     */
    add: function (factor) {
        return this.map(function (c) { return c+factor });
    },

    /**
     * @param {Number} factor
     * @returns {Point3D}
     */
    mul: function (factor) {
        return this.map(function (c) { return c*factor });
    },

    /**
     * @param {Point3D} point3d
     * @returns {Point3D}
     */
    diff: function (point3d) {
        point3d = this.cast( point3d );
        return new this.constructor(
            point3d.x - this.x,
            point3d.y - this.y,
            point3d.z - this.z
        );
    },

    /**
     * @param {Point3D} point3d
     * @returns {Point3D}
     */
    move: function (point3d) {
        point3d = this.cast( arguments );
        this.x += point3d.x;
        this.y += point3d.y;
        this.z += point3d.z;
        return this;
    },

    /**
     * @param {Point3D} point3d
     * @param {Number} accuracy
     * @returns {boolean}
     */
    equals: function (point3d, accuracy) {
        return point3d.x.equals( this.x, accuracy ) &&
               point3d.y.equals( this.y, accuracy ) &&
               point3d.z.equals( this.z, accuracy );
    },

    /** @returns {Point3D} */
    clone: function () {
        return new this.constructor( this );
    },

    /** @returns Array */
    toArray: function () {
        return [this.x, this.y, this.z];
    },

    /** @returns String */
    dump: function () {
        return '[LibCanvas.Point3D(' + this.toArray() + ')]';
    }
});

/*
---

name: "Canvas2DContext"

description: "LibCanvas.Canvas2DContext is similar to original 2d context (and chainable). Can be used for creating your own contexts"

license: "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas

provides: Canvas2DContext

...
*/

new function () {

var object = {
    initialize: function (canvas) {
        if (canvas instanceof CanvasRenderingContext2D) {
            this.ctx2d  = canvas;
            this.canvas = this.ctx2d.canvas;
        } else {
            this.canvas = canvas;
            this.ctx2d  = canvas.getOriginalContext('2d');
        }
    },
    get width () { return this.canvas.width  },
    get height() { return this.canvas.height  },
    set width (width)  { this.canvas.width  = width  },
    set height(height) { this.canvas.height = height }
},

methods = (
    'arc arcTo beginPath bezierCurveTo clearRect clip ' +
    'closePath drawImage fill fillRect fillText lineTo moveTo ' +
    'quadraticCurveTo rect restore rotate save scale setTransform ' +
    'stroke strokeRect strokeText transform translate'
).split(' '),

getterMethods = (
    'createPattern drawFocusRing isPointInPath measureText ' +
    'createImageData createLinearGradient ' +
    'createRadialGradient getImageData putImageData'
).split(' '),

properties = (
    'fillStyle font globalAlpha globalCompositeOperation lineCap ' +
    'lineJoin lineWidth miterLimit shadowOffsetX shadowOffsetY ' +
    'shadowBlur shadowColor strokeStyle textAlign textBaseline'
).split(' ');

properties.forEach(function (property) {
    atom.accessors.define(object, property, {
        set: function (value) {
            try {
                this.ctx2d[property] = value;
            } catch (e) {
                throw TypeError('Exception while setting «' + property + '» to «' + value + '»: ' + e.message);
            }
        },
        get: function () {
            return this.ctx2d[property];
        }
    })
});

methods.forEach(function (method) {
    object[method] = function () {
        this.ctx2d[method].apply(this.ctx, arguments);
        return this;
    };
});

getterMethods.forEach(function (method) {
    object[method] = function () {
        return this.ctx2d[method].apply(this.ctx, arguments);
    };
});

atom.declare( 'LibCanvas.Canvas2DContext', object );

};

/*
---

name: "Plugins.ExtendedCurves"

description: "Curves with dynamic width and color"

license: "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"

authors:
    - "Artem Smirnov <art543484@ya.ru>"
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Context2D

provides: Plugins.ExtendedCurves

...
*/

new function () {

// The following text contains bad code and due to it's code it should not be readed by ANYONE!

var
    Transition = atom.Transition,
    Color = atom.Color,
    EC = {};

/** @returns {atom.Color} */
EC.getColor = function (color) {
    return new Color(color || [0,0,0,1]);
};

EC.getPoints = function (prevPos, pos, width, inverted) {
    var
        w    = pos.x-prevPos.x,
        h    = pos.y-prevPos.y,
        dist = atom.math.hypotenuse(w, h),

        sin = h / dist,
        cos = w / dist,

        dx = sin * width,
        dy = cos * width;
        
    return [
        new Point(pos.x + dx, pos.y + dy*inverted),
        new Point(pos.x - dx, pos.y - dy*inverted)
    ];
};

EC.getGradientFunction = function (attr) {
    switch (typeof attr.gradient) {
        case 'undefined' : 
            return atom.fn.lambda( EC.getColor(attr.color) );
        
        case 'function' :
            return attr.gradient;
        
        default :
            var gradient = { fn: attr.gradient.fn || 'linear' };
            
            if (typeof gradient.fn != 'string') {
                throw new Error('LibCanvas.Context2D.drawCurve -- unexpected type of gradient function');
            }
            
            gradient.from = EC.getColor(attr.gradient.from);
            gradient.to   = EC.getColor(attr.gradient.to  );
            
            var diff = gradient.from.diff( gradient.to );
            
            return function (t) {
                var factor = Transition.get(gradient.fn)(t);
                return gradient.from.shift( diff.clone().mul(factor) ).toString();
            };
    }
};

EC.getWidthFunction = function (attr) {
    attr.width = attr.width || 1;
    switch (typeof attr.width) {
        case 'number'  : return atom.fn.lambda(attr.width);
        case 'function': return attr.width;
        case 'object'  : return EC.getWidthFunction.range( attr.width );
        default: throw new TypeError('LibCanvas.Context2D.drawCurve -- unexpected type of width');
    }
};

EC.getWidthFunction.range = function (width) {
    if(!width.from || !width.to){
        throw new Error('LibCanvas.Context2D.drawCurve -- width.from or width.to undefined');
    }
    var diff = width.to - width.from;
    return function(t){
        return width.from + diff * Transition.get(width.fn || 'linear')(t);
    }
};

EC.curvesFunctions = [
    function (p, t) { // linear
        return {
            x:p[0].x + (p[1].x - p[0].x) * t,
            y:p[0].y + (p[1].y - p[0].y) * t
        };
    },
    function (p,t) { // quadratic
        var i = 1-t;
        return {
            x:i*i*p[0].x + 2*t*i*p[1].x + t*t*p[2].x,
            y:i*i*p[0].y + 2*t*i*p[1].y + t*t*p[2].y
        };
    },
    function (p, t) { // qubic
        var i = 1-t;
        return {
            x:i*i*i*p[0].x + 3*t*i*i*p[1].x + 3*t*t*i*p[2].x + t*t*t*p[3].x,
            y:i*i*i*p[0].y + 3*t*i*i*p[1].y + 3*t*t*i*p[2].y + t*t*t*p[3].y
        };
    }
];

Context2D.prototype.drawCurve = function (obj) {
    var points = atom.array.append( [Point(obj.from)], obj.points.map(Point), [Point(obj.to)] );

    var gradientFunction = EC.getGradientFunction(obj),             //Getting gradient function
        widthFunction    = EC.getWidthFunction(obj),                //Getting width function
        curveFunction    = EC.curvesFunctions[ obj.points.length ]; //Getting curve function

    if (!curveFunction) throw new Error('LibCanvas.Context2D.drawCurve -- unexpected number of points');

    var step = obj.step || 0.02;

    var invertedMultipler = obj.inverted ? 1 : -1;

    var controlPoint, prevContorolPoint,
        drawPoints  , prevDrawPoints   ,
        width , color, prevColor, style;

    prevContorolPoint = curveFunction(points, -step);

    for (var t=-step ; t<1.02 ; t += step) {
        controlPoint = curveFunction(points, t);
        color = gradientFunction(t);
        width = widthFunction(t) / 2;

        drawPoints = EC.getPoints(prevContorolPoint, controlPoint, width, invertedMultipler);

        if (t >= step) {
            // #todo: reduce is part of array, not color
            var diff = EC.getColor(prevColor).diff(color);

            if ( (diff.red + diff.green + diff.blue) > 150 ) {
                style = this.createLinearGradient(prevContorolPoint, controlPoint);
                style.addColorStop(0, prevColor);
                style.addColorStop(1,     color);
            } else {
                style = color;
            }

                this
                    .set("lineWidth",1)
                    .beginPath(prevDrawPoints[0])
                    .lineTo   (prevDrawPoints[1])
                    .lineTo   (drawPoints[1])
                    .lineTo   (drawPoints[0])
                    .fill  (style)
                    .stroke(style);
        }
        prevDrawPoints    = drawPoints;
        prevContorolPoint = controlPoint;
        prevColor         = color;
    }
    return this;
};

};

/*
---

name: "Plugins.Image"

description: "Provides some Image extensions"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Shapes.Rectangle

provides: Plugins.Image

...
*/

var UtilsImage = atom.declare( 'LibCanvas.Utils.Image', {
    canvasCache: null,

    initialize: function (image) {
        this.image = image;
        this.cache = {};
    },

    /**
     * @param {Rectangle} rect
     * #todo: use createPattern
     */
    createSprite: function (rect) {
        var image, buf, xShift, yShift, x, y, xMax, yMax, crop, size, current, from, to;

        if (rect.width <= 0 || rect.height <= 0) {
            throw new TypeError('Wrong rectangle size');
        }

        image = this.image;
        buf = LibCanvas.buffer(rect.width, rect.height, true);

        // если координаты выходят за левый/верхний край картинки
        if (rect.from.x < 0) xShift = Math.ceil(Math.abs(rect.from.x) / rect.width );
        if (rect.from.y < 0) yShift = Math.ceil(Math.abs(rect.from.y) / rect.height);
        if (xShift || yShift) {
            rect = rect.clone().move(new Point(
                xShift * image.width,
                yShift * image.height
            ));
        }

        // для того, чтобы была возможность указывать ректангл, выходящий
        // за пределы картинки. текущая картинка повторяется как паттерн
        xMax = Math.ceil(rect.to.x / image.width );
        yMax = Math.ceil(rect.to.y / image.height);
        for (y = yMax; y-- > 0;) for (x = xMax; x-- > 0;) {
            current = new Point(x * image.width, y * image.height);
            from = current.clone();
            to   = from.clone().move([image.width, image.height]);

            if (from.x < rect.from.x) from.x = rect.from.x;
            if (from.y < rect.from.y) from.y = rect.from.y;
            if (  to.x > rect. to .x)   to.x = rect. to .x;
            if (  to.y > rect. to .y)   to.y = rect. to .y;

            crop = new Rectangle(from, to);
            size = crop.size;
            crop.from.x %= image.width;
            crop.from.y %= image.height;
            crop.size    = size;

            if (x) current.x -= rect.from.x;
            if (y) current.y -= rect.from.y;

            if (size.width && size.height) buf.ctx.drawImage({
                image : image,
                crop  : crop,
                draw  : new Rectangle( current, size )
            });
        }

        return buf;
    },

    toCanvas: function () {
        var cache = this.canvasCache;

        if (!cache) {
            cache = this.canvasCache = LibCanvas.buffer(this, true);
            cache.ctx.drawImage(this);
        }
        return cache;
    },

    isLoaded: function () {
        return this.constructor.isLoaded( this.image );
    },

    sprite: function () {
        if (!this.isLoaded()) throw new Error('Not loaded in Image.sprite, logged');

        if (arguments.length) {
            var
                rect  = Rectangle(arguments),
                index = rect.dump(),
                cache = this.cache[index];

            if (!cache) {
                cache = this.cache[index] = this.createSprite(rect);
            }
            return cache;
        } else {
            return this.toCanvas();
        }
    }
});

UtilsImage.own({
    isLoaded : function (image) {
        return image.complete && ( (image.naturalWidth == null) || !!image.naturalWidth );
    },

    sprite: function (image, rectangle) {
        return this.mix(image).sprite(rectangle);
    },

    toCanvas: function (image) {
        return this.mix(image).toCanvas();
    },

    mix: function (image) {
        var key = 'libcanvas.image';

        if (!image[key]) {
            image[key] = new this(image);
        }

        return image[key];
    }
});

/*
 ---

 name: "ImageBuilder"

 description: "Plugin, that compile image from parts"

 license:
 - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
 - "[MIT License](http://opensource.org/licenses/mit-license.php)"

 authors:
 - Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

 provides: Plugins.ImageBuilder

 requires:
 - LibCanvas
 - Point
 - Shapes.Rectangle

 ...
 */

/** @class ImageBuilder */
var ImageBuilder = LibCanvas.declare(
    'LibCanvas.Plugins.ImageBuilder', 'ImageBuilder', {
        ctx     : null,
        shape   : null,
        images  : [
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ],

        /**
         * @param data
         * @param data.source  - image
         * @param data.widths  - [ left, center, right ]
         * @param data.heights - [ top, middle, bottom ]
         */
        initialize: function (data) {
            this.cropImage( data );
        },

        /** @private */
        renderSingle: function (image, xDir, yDir) {
            if (image != null) this.ctx.drawImage({
                image: image,
                from: this.countShape( xDir, yDir ).from
            });

            return this;
        },
        /** @private */
        renderRepeated: function (image, xDir, yDir) {
            if (image != null) {
                var pattern = this.ctx.createPattern( image, 'repeat' );

                var shape = this.countShape(xDir, yDir);
                this.ctx
                    .translate(shape.from)
                    .fill( new Rectangle(new Point(0,0), shape.size), pattern)
                    .translate(shape.from, true);
            }
            return this;
        },
        /** @private */
        countShape: function (xDir, yDir) {
            var
                size = this.shape.size,
                from = new Point(0,0),
                to   = new Point(0,0);

            from.x = xDir == 'left'   ? 0 :
                this.countBasis( xDir == 'center' ? 'left' : 'right' );

            from.y = yDir == 'top'    ? 0 :
                this.countBasis( yDir == 'middle' ? 'top' : 'bottom' );

            to.x   = xDir == 'right'  ? size.width  :
                this.countBasis( xDir == 'center' ? 'right' : 'left' );

            to.y   = yDir == 'bottom' ? size.height :
                this.countBasis( yDir == 'middle' ? 'bottom' : 'top' );

            return new Rectangle( from, to ).move( this.shape );
        },
        /** @private */
        countBasis: function (basis) {
            var images = this.images, size = this.shape.size;

            switch (basis) {
                case 'left'  : return               images[0].width;
                case 'right' : return size.width  - images[2].width;
                case 'top'   : return               images[0].height;
                case 'bottom': return size.height - images[6].height;
                default: throw new TypeError('Wrong basis: ' + basis);
            }
        },
        /** @private */
        renderParts: function () {
            var images = this.images;
            this
                .renderRepeated( images[1], 'center', 'top'    )
                .renderRepeated( images[3], 'left'  , 'middle' )
                .renderRepeated( images[4], 'center', 'middle' )
                .renderRepeated( images[5], 'right' , 'middle' )
                .renderRepeated( images[7], 'center', 'bottom' )
                .renderSingle  ( images[0], 'left'  , 'top'    )
                .renderSingle  ( images[2], 'right' , 'top'    )
                .renderSingle  ( images[6], 'left'  , 'bottom' )
                .renderSingle  ( images[8], 'right' , 'bottom' );
        },
        /** @private */
        cropImage: function (data) {
            var w, h, x, y, width, height,
                images  = [],
                widths  = data.widths,
                heights = data.heights;

            for (y = 0, h = 0; h < heights.length; h++) {
                height = heights[h];
                for (x = 0, w = 0; w < widths.length; w++) {
                    width = widths[w];

                    images.push(this.createCroppedImage( data.source,
                        new Rectangle(x,y,width,height)
                    ));

                    x += width;
                }
                y += height;
            }

            this.images = images;
        },
        /** @private */
        createCroppedImage: function (source, shape) {
            var buffer = LibCanvas.buffer( shape.size, true );

            buffer.ctx.drawImage({
                image: source,
                draw : buffer.ctx.rectangle,
                crop : shape
            });

            return buffer;
        },

        renderTo: function (ctx, shape) {
            this.ctx   = ctx;
            this.shape = shape;
            this.renderParts();
        }
    }
);

/** @class ImageBuilder.Horisontal */
atom.declare( 'LibCanvas.Plugins.ImageBuilder.Horisontal', ImageBuilder, {
    images: [ 0, 1, 2 ],
    /** @private */
    countBasis: function (basis) {
        var images = this.images, size = this.shape.size;

        switch (basis) {
            case 'left'  : return images[0].width;
            case 'right' : return size.width  - images[2].width;
            case 'top'   : return 0;
            case 'bottom': return size.height;
            default: throw new TypeError('Wrong basis: ' + basis);
        }
    },
    /** @private */
    renderParts: function () {
        var images = this.images;
        this
            .renderRepeated( images[1], 'center', 'middle' )
            .renderSingle  ( images[0], 'left'  , 'middle' )
            .renderSingle  ( images[2], 'right' , 'middle' );
    },
    /** @private */
    cropImage: function (data) {
        var w, x, width,
            images  = [],
            widths  = data.widths;

        this.height = data.source.height;

        for (x = 0, w = 0; w < widths.length; w++) {
            width = widths[w];

            images.push(this.createCroppedImage( data.source,
                new Rectangle(x,0,width,this.height)
            ));

            x += width;
        }

        this.images = images;
    }
});

/** @class ImageBuilder.Vertical */
atom.declare( 'LibCanvas.Plugins.ImageBuilder.Vertical', ImageBuilder, {
    images: [ 0, 1, 2 ],
    /** @private */
    countBasis: function (basis) {
        var images = this.images, size = this.shape.size;

        switch (basis) {
            case 'left'  : return 0;
            case 'right' : return size.width;
            case 'top'   : return images[0].height;
            case 'bottom': return size.height - images[2].height;
            default: throw new TypeError('Wrong basis: ' + basis);
        }
    },
    /** @private */
    renderParts: function () {
        var images = this.images;
        this
            .renderRepeated( images[1], 'center', 'middle' )
            .renderSingle  ( images[0], 'center', 'top'    )
            .renderSingle  ( images[2], 'center', 'bottom' );
    },
    /** @private */
    cropImage: function (data) {
        var h, y, height,
            images  = [],
            heights = data.heights;

        this.width = data.source.width;

        for (y = 0, h = 0; h < heights.length; h++) {
            height = heights[h];

            images.push(this.createCroppedImage( data.source,
                new Rectangle(0,y,this.width,height)
            ));

            y += height;
        }

        this.images = images;
    }
});

/*
---

name: "Plugins.ImagePrototype"

description: "Provides some Image extensions"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Utils.Image

provides: Plugins.ImagePrototype

...
*/

// <image> tag
atom.core.append(HTMLImageElement.prototype, {
    createSprite: function (rect) {
        return UtilsImage.mix(this).createSprite(rect);
    },
    toCanvas: function () {
        return UtilsImage.mix(this).toCanvas();
    },
    sprite : function () {
        var utils = UtilsImage.mix(this);

        return utils.sprite.apply( utils, arguments );
    },
    isLoaded : function () {
        return UtilsImage.isLoaded(this);
    }
});

// mixin from image
atom.core.append(HTMLCanvasElement.prototype, {
    createSprite : HTMLImageElement.prototype.createSprite,
    sprite   : HTMLImageElement.prototype.sprite,
    isLoaded : atom.fn.lambda(true),
    toCanvas : atom.fn.lambda()
});

/*
---

name: "Plugins.ProjectiveTexture"

description: "Provides testing projective textures rendering (more info: http://acko.net/files/projective/index.html)"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Context2D

provides: Plugins.ProjectiveTexture

source: "http://acko.net/blog/projective-texturing-with-canvas"

...
*/

var ProjectiveTexture = function () {

Context2D.prototype.projectiveImage = function (arg) {
    // test
    new ProjectiveTexture(arg.image)
        .setContext(this.ctx2d)
        .setQuality(arg.patchSize, arg.limit)
        .render( arg.to );
    return this;
};

var ProjectiveTexture = declare( 'LibCanvas.Plugins.ProjectiveTexture', {
    initialize : function (image) {
        if (typeof image == 'string') {
            this.image = new Image;
            image.src = image
        } else {
            this.image = image;
        }
        this.patchSize = 64;
        this.limit = 4;
    },
    setQuality : function (patchSize, limit) {
        this.patchSize = patchSize == null ? 64 : patchSize;
        this.limit = limit == null ? 4 : limit;
        return this;
    },
    setContext : function (ctx) {
        this.ctx = ctx;
        return this;
    },
    render : function (polygon) {

        var points = polygon.points;
        points = [
            [points[0].x, points[0].y],
            [points[1].x, points[1].y],
            [points[3].x, points[3].y],
            [points[2].x, points[2].y]
        ];
        
        var tr = getProjectiveTransform(points);

        // Begin subdivision process.
        var ptl = tr.transformProjectiveVector([0, 0, 1]);
        var ptr = tr.transformProjectiveVector([1, 0, 1]);
        var pbl = tr.transformProjectiveVector([0, 1, 1]);
        var pbr = tr.transformProjectiveVector([1, 1, 1]);

        this.transform = tr;
        divide.call(this, 0, 0, 1, 1, ptl, ptr, pbl, pbr, this.limit);

        return this;
    }
});

var divide = function (u1, v1, u4, v4, p1, p2, p3, p4, limit) {

     // See if we can still divide.
    if (limit) {
        // Measure patch non-affinity.
        var d1 = [p2[0] + p3[0] - 2 * p1[0], p2[1] + p3[1] - 2 * p1[1]];
        var d2 = [p2[0] + p3[0] - 2 * p4[0], p2[1] + p3[1] - 2 * p4[1]];
        var d3 = [d1[0] + d2[0], d1[1] + d2[1]];
        var r = Math.abs((d3[0] * d3[0] + d3[1] * d3[1]) / (d1[0] * d2[0] + d1[1] * d2[1]));

        // Measure patch area.
        d1 = [p2[0] - p1[0] + p4[0] - p3[0], p2[1] - p1[1] + p4[1] - p3[1]];
        d2 = [p3[0] - p1[0] + p4[0] - p2[0], p3[1] - p1[1] + p4[1] - p2[1]];
        var area = Math.abs(d1[0] * d2[1] - d1[1] * d2[0]);

        // Check area > patchSize pixels (note factor 4 due to not averaging d1 and d2)
        // The non-affinity measure is used as a correction factor.
        if ((u1 == 0 && u4 == 1) || ((.25 + r * 5) * area > (this.patchSize * this.patchSize))) {
            // Calculate subdivision points (middle, top, bottom, left, right).
            var umid = (u1 + u4) / 2;
            var vmid = (v1 + v4) / 2;
            var tr   = this.transform;
            var pmid = tr.transformProjectiveVector([umid, vmid, 1]);
            var pt   = tr.transformProjectiveVector([umid, v1, 1]);
            var pb   = tr.transformProjectiveVector([umid, v4, 1]);
            var pl   = tr.transformProjectiveVector([u1, vmid, 1]);
            var pr   = tr.transformProjectiveVector([u4, vmid, 1]);
            
            // Subdivide.
            limit--;
            divide.call(this,   u1,   v1, umid, vmid,   p1,   pt,   pl, pmid, limit);
            divide.call(this, umid,   v1,   u4, vmid,   pt,   p2, pmid,   pr, limit);
            divide.call(this,  u1,  vmid, umid,   v4,   pl, pmid,   p3,   pb, limit);
            divide.call(this, umid, vmid,   u4,   v4, pmid,   pr,   pb,   p4, limit);

            return;
        }
    }
    
    var ctx = this.ctx;

    // Render this patch.
    ctx.save();
    // Set clipping path.
    ctx.beginPath();
    ctx.moveTo(p1[0], p1[1]);
    ctx.lineTo(p2[0], p2[1]);
    ctx.lineTo(p4[0], p4[1]);
    ctx.lineTo(p3[0], p3[1]);
    ctx.closePath();
    //ctx.clip();

    // Get patch edge vectors.
    var d12 = [p2[0] - p1[0], p2[1] - p1[1]];
    var d24 = [p4[0] - p2[0], p4[1] - p2[1]];
    var d43 = [p3[0] - p4[0], p3[1] - p4[1]];
    var d31 = [p1[0] - p3[0], p1[1] - p3[1]];

    // Find the corner that encloses the most area
    var a1 = Math.abs(d12[0] * d31[1] - d12[1] * d31[0]);
    var a2 = Math.abs(d24[0] * d12[1] - d24[1] * d12[0]);
    var a4 = Math.abs(d43[0] * d24[1] - d43[1] * d24[0]);
    var a3 = Math.abs(d31[0] * d43[1] - d31[1] * d43[0]);
    var amax = Math.max(Math.max(a1, a2), Math.max(a3, a4));
    var dx = 0, dy = 0, padx = 0, pady = 0;

    // Align the transform along this corner.
    switch (amax) {
        case a1:
            ctx.transform(d12[0], d12[1], -d31[0], -d31[1], p1[0], p1[1]);
            // Calculate 1.05 pixel padding on vector basis.
            if (u4 != 1) padx = 1.05 / Math.sqrt(d12[0] * d12[0] + d12[1] * d12[1]);
            if (v4 != 1) pady = 1.05 / Math.sqrt(d31[0] * d31[0] + d31[1] * d31[1]);
            break;
        case a2:
            ctx.transform(d12[0], d12[1],  d24[0],  d24[1], p2[0], p2[1]);
            // Calculate 1.05 pixel padding on vector basis.
            if (u4 != 1) padx = 1.05 / Math.sqrt(d12[0] * d12[0] + d12[1] * d12[1]);
            if (v4 != 1) pady = 1.05 / Math.sqrt(d24[0] * d24[0] + d24[1] * d24[1]);
            dx = -1;
            break;
        case a4:
            ctx.transform(-d43[0], -d43[1], d24[0], d24[1], p4[0], p4[1]);
            // Calculate 1.05 pixel padding on vector basis.
            if (u4 != 1) padx = 1.05 / Math.sqrt(d43[0] * d43[0] + d43[1] * d43[1]);
            if (v4 != 1) pady = 1.05 / Math.sqrt(d24[0] * d24[0] + d24[1] * d24[1]);
            dx = -1;
            dy = -1;
            break;
        case a3:
            // Calculate 1.05 pixel padding on vector basis.
            ctx.transform(-d43[0], -d43[1], -d31[0], -d31[1], p3[0], p3[1]);
            if (u4 != 1) padx = 1.05 / Math.sqrt(d43[0] * d43[0] + d43[1] * d43[1]);
            if (v4 != 1) pady = 1.05 / Math.sqrt(d31[0] * d31[0] + d31[1] * d31[1]);
            dy = -1;
            break;
    }

    // Calculate image padding to match.
    var du = (u4 - u1);
    var dv = (v4 - v1);
    var padu = padx * du;
    var padv = pady * dv;


    var iw = this.image.width;
    var ih = this.image.height;

    ctx.drawImage(
        this.image,
        u1 * iw,
        v1 * ih,
        Math.min(u4 - u1 + padu, 1) * iw,
        Math.min(v4 - v1 + padv, 1) * ih,
        dx, dy,
        1 + padx, 1 + pady
    );
    ctx.restore();
}

/**
 * Generic matrix class. Built for readability, not for speed.
 *
 * (c) Steven Wittens 2008
 * http://www.acko.net/
 */
var Matrix = function (w, h, values) {
  this.w = w;
  this.h = h;
  this.values = values || allocate(h);
};

var allocate = function (w, h) {
  var values = [];
  for (var i = 0; i < h; ++i) {
    values[i] = [];
    for (var j = 0; j < w; ++j) {
      values[i][j] = 0;
    }
  }
  return values;
}

var cloneValues = function (values) {
    var clone = [];
    for (var i = 0; i < values.length; ++i) {
        clone[i] = [].concat(values[i]);
    }
    return clone;
}

function getProjectiveTransform(points) {
  var eqMatrix = new Matrix(9, 8, [
    [ 1, 1, 1,   0, 0, 0, -points[3][0],-points[3][0],-points[3][0] ],
    [ 0, 1, 1,   0, 0, 0,  0,-points[2][0],-points[2][0] ],
    [ 1, 0, 1,   0, 0, 0, -points[1][0], 0,-points[1][0] ],
    [ 0, 0, 1,   0, 0, 0,  0, 0,-points[0][0] ],

    [ 0, 0, 0,  -1,-1,-1,  points[3][1], points[3][1], points[3][1] ],
    [ 0, 0, 0,   0,-1,-1,  0, points[2][1], points[2][1] ],
    [ 0, 0, 0,  -1, 0,-1,  points[1][1], 0, points[1][1] ],
    [ 0, 0, 0,   0, 0,-1,  0, 0, points[0][1] ]

  ]);

  var kernel = eqMatrix.rowEchelon().values;
  var transform = new Matrix(3, 3, [
    [-kernel[0][8], -kernel[1][8], -kernel[2][8]],
    [-kernel[3][8], -kernel[4][8], -kernel[5][8]],
    [-kernel[6][8], -kernel[7][8],             1]
  ]);
  return transform;
}

Matrix.prototype = {
    add : function (operand) {
        if (operand.w != this.w || operand.h != this.h) {
            throw new Error("Matrix add size mismatch");
        }

        var values = allocate(this.w, this.h);
        for (var y = 0; y < this.h; ++y) {
            for (var x = 0; x < this.w; ++x) {
              values[y][x] = this.values[y][x] + operand.values[y][x];
            }
        }
        return new Matrix(this.w, this.h, values);
    },
    transformProjectiveVector : function (operand) {
        var out = [], x, y;
        for (y = 0; y < this.h; ++y) {
            out[y] = 0;
            for (x = 0; x < this.w; ++x) {
                out[y] += this.values[y][x] * operand[x];
            }
        }
        var iz = 1 / (out[out.length - 1]);
        for (y = 0; y < this.h; ++y) {
            out[y] *= iz;
        }
        return out;
    },
    multiply : function (operand) {
        var values, x, y;
        if (+operand !== operand) {
            // Matrix mult
            if (operand.h != this.w) {
                throw new Error("Matrix mult size mismatch");
            }
            values = allocate(this.w, this.h);
            for (y = 0; y < this.h; ++y) {
                for (x = 0; x < operand.w; ++x) {
                    var accum = 0;
                    for (var s = 0; s < this.w; s++) {
                        accum += this.values[y][s] * operand.values[s][x];
                    }
                    values[y][x] = accum;
                }
            }
            return new Matrix(operand.w, this.h, values);
        }
        else {
            // Scalar mult
            values = allocate(this.w, this.h);
            for (y = 0; y < this.h; ++y) {
                for (x = 0; x < this.w; ++x) {
                    values[y][x] = this.values[y][x] * operand;
                }
            }
            return new Matrix(this.w, this.h, values);
        }
    },
    rowEchelon : function () {
        if (this.w <= this.h) {
            throw new Error("Matrix rowEchelon size mismatch");
        }

        var temp = cloneValues(this.values);

        // Do Gauss-Jordan algorithm.
        for (var yp = 0; yp < this.h; ++yp) {
            // Look up pivot value.
            var pivot = temp[yp][yp];
            while (pivot == 0) {
                // If pivot is zero, find non-zero pivot below.
                for (var ys = yp + 1; ys < this.h; ++ys) {
                    if (temp[ys][yp] != 0) {
                        // Swap rows.
                        var tmpRow = temp[ys];
                        temp[ys] = temp[yp];
                        temp[yp] = tmpRow;
                        break;
                    }
                }
                if (ys == this.h) {
                    // No suitable pivot found. Abort.
                    return new Matrix(this.w, this.h, temp);
                }
                else {
                    pivot = temp[yp][yp];
                }
            }
            // Normalize this row.
            var scale = 1 / pivot;
            for (var x = yp; x < this.w; ++x) {
                temp[yp][x] *= scale;
            }
            // Subtract this row from all other rows (scaled).
            for (var y = 0; y < this.h; ++y) {
                if (y == yp) continue;
                var factor = temp[y][yp];
                temp[y][yp] = 0;
                for (x = yp + 1; x < this.w; ++x) {
                    temp[y][x] -= factor * temp[yp][x];
                }
            }
        }

        return new Matrix(this.w, this.h, temp);
    },
    invert : function () {
        var x, y;

        if (this.w != this.h) {
            throw new Error("Matrix invert size mismatch");
        }

        var temp = allocate(this.w * 2, this.h);

        // Initialize augmented matrix
        for (y = 0; y < this.h; ++y) {
            for (x = 0; x < this.w; ++x) {
                temp[y][x] = this.values[y][x];
                temp[y][x + this.w] = (x == y) ? 1 : 0;
            }
        }

        temp = new Matrix(this.w * 2, this.h, temp);
        temp = temp.rowEchelon();

        // Extract right block matrix.
        var values = allocate(this.w, this.h);
        for (y = 0; y < this.w; ++y) {
            // @todo check if "x < this.w;" is mistake
            for (x = 0; x < this.w; ++x) {
                values[y][x] = temp.values[y][x + this.w];
            }
        }
        return new Matrix(this.w, this.h, values);
    }
};

return ProjectiveTexture;
}();

/*
 ---

 name: "SpriteFont"

 description: "Plugin, that render font from sprite"

 license:
 - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
 - "[MIT License](http://opensource.org/licenses/mit-license.php)"

 authors:
 - Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

 provides: Plugins.SpriteFont

 requires:
 - LibCanvas

 ...
 */

/** @class SpriteFont */
var SpriteFont = LibCanvas.declare(
    'LibCanvas.Plugins.SpriteFont', 'SpriteFont',
    {
        initialize: function (symbols) {
            if (typeof symbols == 'string') {
                symbols = symbols.split('');
            }
            this.symbols = symbols;
            this.normal  = {};
            this.bold    = {};
        },

        make: function (sheet) {
            sheet = new SpriteFont.Sheet(this, sheet);

            var target = sheet.bold ? this.bold : this.normal;

            if (target[sheet.size]) {
                throw new TypeError('Size already exists');
            }

            target[sheet.size] = sheet;

            return sheet;
        },

        get: function (symbol, data) {
            var font = ( data.bold ? this.bold : this.normal )[ data.size ];
            if (font) {
                return font.get(symbol, data.color);
            } else {
                throw new Error('No such sheet in font');
            }
        }
    }
);

/** @class SpriteFont.Sheet */
atom.declare( 'LibCanvas.Plugins.SpriteFont.Sheet', {
    defaultColor: atom.Color.colorNames.black,

    settings: {
        image  : null,
        width  : [],
        symbols: [],
        bold   : false,
        size   : false
    },

    initialize: function (font, data) {
        this.settings = new atom.Settings(this.settings).set(data);
        this.symbols  = font.symbols;
        this.colors   = {};
        this.icons    = {};
    },

    get bold () { return this.settings.get('bold') },
    get size () { return this.settings.get('size') },

    get: function (symbol, color) {
        if (symbol in this.icons) {
            return this.icons[symbol];
        }

        if (!symbol in this.symbols) {
            throw new TypeError('Unknown symbol: ' + symbol);
        }
        if (color == null) {
            color = this.defaultColor;
        }
        color = atom.Color(color).toString('hex');

        var colors = this.colors;

        if (!colors[color]) {
            colors[color] = {};
        }
        if (!colors[color][symbol]) {
            colors[color][symbol] = this.generateSymbol(symbol, color);
        }

        return colors[color][symbol];
    },

    addIcon: atom.core.overloadSetter(function (name, image) {
        this.icons[name] = image;
    }),

    generateSymbol: function (symbol, color) {
        var i, w, h, x, img, buffer,
            width   = this.settings.get('width'),
            found   = false,
            symbols = this.symbols;

        for ( i = 0, x = 0; i < symbols.length; i++ ) {
            w = width[i];
            if (symbols[i] == symbol) {
                found = true;
                break;
            }
            x += w;
        }

        if (!found) {
            throw new Error('No symbol in list: ' + symbol);
        }

        img = this.settings.get('image');
        h   = img.height;
        buffer = LibCanvas.buffer(w, h, true);
        buffer.ctx.drawImage({
            image: img,
            crop : [ x, 0, w, h ],
            draw : buffer.ctx.rectangle
        });

        if (color != this.defaultColor) {
            buffer.ctx
                .save()
                .set({ globalCompositeOperation: Context2D.COMPOSITE.SOURCE_IN })
                .fillAll(color)
                .restore();

        }

        return buffer;
    }
});


/** @class SpriteFont.Render */
atom.declare( 'LibCanvas.Plugins.SpriteFont.Render', {

    /**
     * @param {object}      ctx
     * @param {object}      options
     * @param {number}     [options.size=16]
     * @param {boolean}    [options.bold=false]
     * @param {boolean}    [options.tags=true]
     * @param {string}     [options.text='']
     * @param {SpriteFont}  options.font
     * @param {Rectangle}   options.shape
     * @param {string}     [options.align='left'] - 'left|middle|right'
     */
    initialize: function (ctx, options) {
        this.ctx = ctx;
        this.options = atom.core.append({
            size : 16,
            bold : false,
            text : '',
            tags : '{*}',
            font : null,
            shape: null,
            color: 'black',
            align: 'left',
            lines: null,
            noWrap: false,
            letterSpacing: 0,
            autoRender: true,
            forceSplit: false
        }, options);

        this.options.text = String( this.options.text );

        if (this.options.autoRender) {
            var completeLines = this.parseAndGetLines();
            this.render(completeLines);
        }
    },

    getLinesHeight: function(lines) {
        var height = 0;
        for (var idx = 0; idx < lines.length; idx++) {
            height += lines[idx].height;
        }
        return height;
    },

    parseAndGetLines: function() {
        var steps = new SpriteFont.Steps(this, new SpriteFont.Lexer(
            this.options.text, this.options.tags
        ));

        steps.countSizes(this.options.font, this.options.letterSpacing);

        var lines = this.options.lines;
        if (!lines) lines = new SpriteFont.LinesEnRu();
        lines.setConfig(this.options.font, this.options.noWrap, this.options.forceSplit);

        return lines.run( steps.steps, this.options.shape.width );
    },

    render: function (lines) {
        var x, y, w, l, i, from = this.options.shape.from;

        for (l = 0, y = Math.floor(from.y); l < lines.length; l++) {
            x = Math.floor(from.x);

            if (this.options.align != 'left') {
                w = lines[l].reduce(function (current, elem) { return current + elem.width }, 0);

                if (this.options.align == 'center') {
                    x += parseInt((this.options.shape.width - w) / 2);
                }

                if (this.options.align == 'right') {
                    x += this.options.shape.width - w;
                }
            }

            for (i = 0; i < lines[l].length; i++) {
                this.ctx.drawImage( lines[l][i].image, x, y );
                x += lines[l][i].width;
            }
            y += lines[l].height;
        }
    }
});

/** @class SpriteFont.Steps */
atom.declare( 'LibCanvas.Plugins.SpriteFont.Steps', {
    tags: {
        bold : false,
        size : true,
        color: true
    },

    tagRegExp: /(\w+)(=.*)?/,

    initialize: function (render, lexer) {
        this.steps  = [];
        this.tokens = lexer.tokens;
        this.index  = -1;

        this.split(atom.object.collect(render.options, [ 'color', 'size', 'bold' ]));
    },

    split: function (initialMode) {
        var t,
            i = 0,
            l = this.tokens.length,
            stack = [ initialMode ],
            last  = function () {
                return stack[ stack.length - 1 ];
            };

        for (; i < l; i++) {
            t = this.tokens[i];
            if (t.type == 'string') {
                t.content.split('').forEach(function (l) {
                    this.steps.push({ type: 'symbol', content: l, mode: last() });
                }.bind(this));
            } else if (t.type == 'nl') {
                this.steps.push(t);
            } else if (t.type == 'tag') {
                if (this.isCloseModeTag(t)) {
                    stack.pop();
                } else if (this.isChangeModeTag(t)) {
                    stack.push(this.createMode(t, last()));
                } else {
                    this.steps.push({ type: 'icon', content: t.content, mode: last() });
                }
            } else {
                throw new Error('Unknown type: ' + t.type);
            }
        }
    },

    isChangeModeTag: function (t) {
        return t.content.match( this.tagRegExp )[1] in this.tags;
    },

    isCloseModeTag: function (t) {
        return t.content == '/';
    },

    createMode: function (t, currentMode) {
        var
            parts = t.content.match( this.tagRegExp ),
            tag   = parts[1],
            value = parts[2],
            mode  = atom.core.append({}, currentMode);

        if (this.tags[tag]) {
            if (value) value = value.substr(1);
            if (value == '') throw new Error('Value required in tag ' + tag);
        } else {
            value = true;
        }

        mode[tag] = value;
        return mode;
    },

    countSizes: function (font, letterSpacing) {
        var i, s, img;
        for (i = 0; i < this.steps.length; i++) {
            s = this.steps[i];
            if (s.type == 'symbol' || s.type == 'icon') {
                img = font.get( s.content, s.mode );
                s.image  = img;
                s.width  = img.width + letterSpacing;
                s.height = img.height;
            }
        }
    }
});

/** @class SpriteFont.Lexer */
atom.declare( 'LibCanvas.Plugins.SpriteFont.Lexer', {

    initialize: function (string, tags) {
        this.string = string;
        this.tags   = this.parseTags(tags);
        this.tokens = this.tokenize();
    },

    tokenize: function () {
        var t = this.tags, s = this.string;
        return t ?
            this.parseTaggedText(s, t) :
            this.parsePlainText (s);
    },

    parseTaggedText: function (string, tags) {
        var
            i = 0,
            last,
            symbol = '',
            result = [],
            length = string.length;

        for (; i < length; i++) {
            symbol = string[i];
            if (symbol == '\n') {
                if (last && last.type == 'tag') {
                    throw new Error('Tag started, but not finished at symbol ' + i);
                }
                result.push({ type: 'nl' });
                last = null;
            } else if (symbol == tags[0]) {
                if (last && last.type == 'tag') {
                    throw new Error('Wrong tag opening at symbol ' + i);
                }
                result.push(last = { type: 'tag'   , content: '' });
            } else if (!last) {
                result.push(last = { type: 'string', content: string[i] });
            } else if (symbol == tags[1] && last.type == 'tag') {
                last = null;
            } else {
                last.content += string[i];
            }
        }

        return result;
    },

    parsePlainText: function (string) {
        var
            i = 0,
            last,
            result = [],
            length = string.length;
        for (; i < length; i++) {
            if (string[i] == '\n') {
                last = null;
                result.push({ type: 'nl' });
            } else if (!last) {
                last = { type: 'string', content: string[i] };
                result.push(last);
            } else {
                last.content += string[i];
            }
        }
        return result;
    },

    parseTags: function (tags) {
        if (tags == null) return null;

        function wrong (part) {
            throw new TypeError('String like "[*]" required (' + part + ')');
        }

        if (typeof tags != 'string') wrong('typeof');

        tags = tags.split('*');

        if (tags   .length != 2) wrong('split');
        if (tags[0].length != 1) wrong('left' );
        if (tags[1].length != 1) wrong('right');

        return tags;
    }
});

/** @class SpriteFont.MorphemesFinder */
atom.declare( 'LibCanvas.Plugins.SpriteFont.MorphemesFinder', {
    vowels: 'AEIOUYaeiouyАОУЮИЫЕЭЯЁаоуюиыеэяёьЄІЇЎєіїў',

    initialize: function () {
    },

    isLetter: function(str) {
        return (str >= 'a' && str <= 'z') || (str >= 'A' && str <= 'я') ||
            (str >= 'A' && str <= 'Z') || (str >= '\u00c0' && str <= '\u02a8') ||
            (str >= '0' && str <= '9') || (str >= '\u0386' && str <= '\u04ff');
    },

    isVowel: function(str) {
        return str && str.length == 1 && this.vowels.indexOf(str) > -1;
    },

    isMorpheme: function (str) {
        if (!str || str.length <= 1) return false;

        for (var i = str.length; i--;) if (this.isVowel(str[i])) return true;

        return false;
    },

    findMorphemes: function (line) {
        var i = 0, c, morphemes = [], lastStr = '', last = [], prev;

        var pushLast = function () {
            prev = morphemes[ morphemes.length - 1 ];
            if (Array.isArray(prev)) {
                atom.array.append( prev, last );
            } else {
                morphemes.push(last);
            }
            last = [];
            lastStr = '';

            if (!this.isLetter(c)) {
                morphemes.push( line[i] );
            }
        }.bind(this);

        for (; i < line.length; i++) {
            c = line[i].content;

            if (line[i].type == 'icon') {
                morphemes.push(last);
                last = [];
                lastStr = '';
                morphemes.push( line[i] );
            } else if (line[i].type == 'symbol' && this.isLetter(c)) {
                lastStr += c;
                last.push(line[i]);
                if (this.isMorpheme(lastStr)) {
                    morphemes.push(last);
                    last = [];
                    lastStr = '';
                }
            } else if (lastStr) {
                pushLast();
            } else {
                morphemes.push( line[i] );
            }
        }

        if (lastStr) pushLast();

        return morphemes;
    }
});

/** @class SpriteFont.LinesEnRu */
atom.declare( 'LibCanvas.Plugins.SpriteFont.LinesEnRu', {
    setConfig: function (font, noWrap, forceSplit) {
        this.font = font;
        this.noWrap = noWrap;
        this.forceSplit = forceSplit;
        this.morphemesFinder = new SpriteFont.MorphemesFinder();
    },

    run: function (steps, maxWidth) {
        var i, line = [], morphemes = [], tmpMark = false;

        for (i = 0; i < steps.length; i++) {

            if (this.forceSplit) {
                line.push(steps[i]);
            } else {
                if (steps[i].type == 'icon') tmpMark = true;

                if (steps[i].type == 'nl' || i == steps.length - 1) {
                    if (steps[i].type != 'nl') {
                        line.push(steps[i]);
                    }

                    morphemes.push( this.morphemesFinder.findMorphemes(line) );
                    line = [];
                } else {
                    line.push(steps[i]);
                }
            }
        }

        if (this.forceSplit) {
            morphemes.push(line);
        }

        return this.countLines(morphemes, maxWidth);

    },

    countLines: function (mLines, maxWidth) {
        var lines = [], l, i, line = [], width = 0, mWidth;

        function add (data) {
            if (!Array.isArray(data)) data = [ data ];
            for (var i = 0; i < data.length; i++) {
                line.push(data[i]);
                width += data[i].width;
            }
        }

        for (l = 0; l < mLines.length; l++) {
            for (i = 0; i < mLines[l].length; i++) {
                mWidth = this.countLength(mLines[l][i]);

                if (mWidth > maxWidth) {
                    throw new Error('Morpheme too long');
                }

                if (!this.noWrap && (width + mWidth > maxWidth || (i == 0 && l > 0))) {
                    lines.push(line);
                    line  = [];
                    width = 0;
                }

                add(mLines[l][i]);
            }
        }

        if (line.length > 0) lines.push(line);

        lines.forEach(function (l) {
            l.height = 0;

            l.forEach(function (obj) {
                l.height = Math.max( l.height, obj.height );
            });
        });

        return lines;
    },

    countLength: function (m) {
        if (Array.isArray(m)) {
            return atom.array.reduce(
                m, function (value, sym) { return value + sym.width }, 0
            );
        } else {
            return m.width;
        }
    }
});


/*
---

name: "Shapes.Ellipse"

description: "Provides ellipse as canvas object"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Shapes.Rectangle

provides: Shapes.Ellipse

...
*/

/** @class Ellipse */
var Ellipse = LibCanvas.declare( 'LibCanvas.Shapes.Ellipse', 'Ellipse', Rectangle, {
    set: function () {
        this.bindMethods( 'update' );
        Rectangle.prototype.set.apply(this, arguments);
    },
    _angle : 0,
    get angle () {
        return this._angle;
    },
    set angle (a) {
        if (this._angle == a) return;
        this._angle = atom.math.normalizeAngle(a);
        this.updateCache = true;
    },
    update: function () {
        this.updateCache = true;
    },
    rotate : function (degree) {
        this.angle += degree;
        return this;
    },
    hasPoint : function () {
        var ctx = this.processPath( shapeTestBuffer().ctx );
        return ctx.isPointInPath(Point(arguments));
    },
    cache : null,
    updateCache : true,
    countCache : function () {
        if (this.cache && !this.updateCache) {
            return this.cache;
        }

        if (this.cache === null) {
            this.cache = [];
            for (var i = 12; i--;) this.cache.push(new Point());
        }
        var c = this.cache,
            angle = this._angle,
            kappa = .5522848,
            x  = this.from.x,
            y  = this.from.y,
            xe = this.to.x,
            ye = this.to.y,
            xm = (xe + x) / 2,
            ym = (ye + y) / 2,
            ox = (xe - x) / 2 * kappa,
            oy = (ye - y) / 2 * kappa;
        c[0].set(x, ym - oy); c[ 1].set(xm - ox, y); c[ 2].set(xm, y);
        c[3].set(xm + ox, y); c[ 4].set(xe, ym -oy); c[ 5].set(xe, ym);
        c[6].set(xe, ym +oy); c[ 7].set(xm +ox, ye); c[ 8].set(xm, ye);
        c[9].set(xm -ox, ye); c[10].set(x, ym + oy); c[11].set(x, ym);

        if (angle) {
            var center = new Point(xm, ym);
            for (i = c.length; i--;) c[i].rotate(angle, center);
        }

        return c;
    },
    processPath : function (ctx, noWrap) {
        if (!noWrap) ctx.beginPath();
        var c = this.countCache();
        ctx.beginPath(c[11])
           .bezierCurveTo(c[0], c[1], c[2])
           .bezierCurveTo(c[3], c[4], c[5])
           .bezierCurveTo(c[6], c[7], c[8])
           .bezierCurveTo(c[9], c[10],c[11]);
        if (!noWrap) ctx.closePath();
        return ctx;
    },
    equals : function (shape, accuracy) {
        return Rectangle.prototype.equals.call( this, shape, accuracy ) && shape.angle == this.angle;
    },
    draw : function (ctx, type) {
        this.processPath(ctx)[type]();
        return this;
    },
    dump: function (name) {
        return Rectangle.prototype.dump.call(this, name || 'Ellipse');
    }
});

/*
---

name: "Shapes.Line"

description: "Provides line as canvas object"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Shape

provides: Shapes.Line

...
*/

var Line = function () {

var between = function (x, a, b, accuracy) {
    return atom.number.equals(x, a, accuracy)
        || atom.number.equals(x, b, accuracy)
        || (a < x && x < b)
        || (b < x && x < a);
};

var halfPi = Math.PI/2;

/** @class Line */
return LibCanvas.declare( 'LibCanvas.Shapes.Line', 'Line', Shape, {
    set : function (from, to) {
        var a = atom.array.pickFrom(arguments);

        if (a.length === 4) {
            this.from = new Point( a[0], a[1] );
            this.to   = new Point( a[2], a[3] );
        } else {
            this.from = Point.from(a[0] || a.from);
            this.to   = Point.from(a[1] || a.to);
        }

        return this;
    },
    hasPoint : function (point) {
        var fx = this.from.x,
            fy = this.from.y,
            tx = this.to.x,
            ty = this.to.y,
            px = point.x,
            py = point.y;

        if (!( atom.number.between(point.x, Math.min(fx, tx), Math.max(fx, tx))
            && atom.number.between(point.y, Math.min(fy, ty), Math.max(fy, ty))
        )) return false;

        // if triangle square is zero - points are on one line
        return atom.number.round(((fx-px)*(ty-py)-(tx-px)*(fy-py)), 6) == 0;
    },
    getBoundingRectangle: function () {
        return new Rectangle(this.from, this.to).fillToPixel().grow(2);
    },
    intersect: function (line, point, accuracy) {
        if (line.constructor != this.constructor) {
            return this.getBoundingRectangle().intersect( line );
        }
        var a = this.from, b = this.to, c = line.from, d = line.to, x, y, FALSE = point ? null : false;
        if (atom.number.equals(d.x, c.x, accuracy)) { // DC == vertical line
            if (atom.number.equals(b.x, a.x, accuracy)) {
                if (atom.number.equals(a.x, d.x, accuracy)) {
                    if (atom.number.between(a.y, c.y, d.y)) {
                        return a.clone();
                    } else if (atom.number.between(b.y, c.y, d.y)) {
                        return b.clone();
                    } else {
                        return FALSE;
                    }
                } else {
                    return FALSE;
                }
            }
            x = d.x;
            y = b.y + (x-b.x)*(a.y-b.y)/(a.x-b.x);
        } else {
            x = ((a.x*b.y - b.x*a.y)*(d.x-c.x)-(c.x*d.y - d.x*c.y)*(b.x-a.x))/((a.y-b.y)*(d.x-c.x)-(c.y-d.y)*(b.x-a.x));
            y = ((c.y-d.y)*x-(c.x*d.y-d.x*c.y))/(d.x-c.x);
            x *= -1;
        }

        if (!between(x, a.x, b.x, accuracy)) return FALSE;
        if (!between(y, a.y, b.y, accuracy)) return FALSE;
        if (!between(x, c.x, d.x, accuracy)) return FALSE;
        if (!between(y, c.y, d.y, accuracy)) return FALSE;

        return point ? new Point(x, y) : true;
    },
    perpendicular: function (point) {
        point = Point( point );
        var
            fX = this.from.x,
            fY = this.from.y,
            tX = this.to.x,
            tY = this.to.y,
            pX = point.x,
            pY = point.y,
            dX = (tX-fX) * (tX-fX),
            dY = (tY-fY) * (tY-fY),
            rX = ((tX-fX)*(tY-fY)*(pY-fY)+fX*dY+pX*dX) / (dX+dY),
            rY = (tY-fY)*(rX-fX)/(tX-fX)+fY;

        return new Point( rX, rY );
    },
    distanceTo: function (p, asInfiniteLine) {
        p = Point(p);
        var f = this.from, t = this.to, angle, s, x, y;

        if (!asInfiniteLine) {
            angle = Math.atan2(p.x - t.x, p.y - t.y);
            if ( atom.number.between(angle, -halfPi, halfPi) ) {
                return t.distanceTo( p );
            }

            angle = Math.atan2(f.x - p.x, f.y - p.y);
            if ( atom.number.between(angle, -halfPi, halfPi) ) {
                return f.distanceTo( p );
            }
        }

        s = Math.abs(
            f.x * (t.y - p.y) +
            t.x * (p.y - f.y) +
            p.x * (f.y - t.y)
        ) / 2;

        x = f.x - t.x;
        y = f.y - t.y;
        return 2 * s / Math.sqrt(x*x+y*y);
    },
    get length () {
        return this.to.distanceTo(this.from);
    },
    getLength : function () {
        return this.length;
    },
    draw : function (ctx, type) {
        ctx.beginPath();
        this.processPath(ctx, true)[type]();
        ctx.closePath();
        return this;
    },
    processPath : function (ctx, noWrap) {
        if (!noWrap) ctx.beginPath();
        ctx.moveTo(this.from).lineTo(this.to);
        if (!noWrap) ctx.closePath();
        return ctx;
    },
    dump: function () {
        return Shape.prototype.dump.call(this, 'Line');
    }
});

}();


/*
---

name: "Shapes.Polygon"

description: "Provides user-defined concave polygon as canvas object"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Shape
    - Shapes.Line

provides: Shapes.Polygon

...
*/

/** @class Polygon */
var Polygon = LibCanvas.declare( 'LibCanvas.Shapes.Polygon', 'Polygon', Shape, {
    initialize: function method () {
        this.points = [];
        this._lines = [];
        method.previous.apply(this, arguments);
    },
    set : function (poly) {
        this.points.length = 0;

        var source = Array.isArray(poly) ? poly : atom.core.toArray(arguments);

        atom.array.append( this.points,
            source
                .filter(Boolean)
                .map(Point)
        );

        this._lines.length = 0;

        return this;
    },
    get length () {
        return this.points.length;
    },
    get lines () {
        var
            lines = this._lines,
            p = this.points,
            l = p.length,
            i = 0;

        if (lines.length != l) for (;i < l; i++) {
            lines.push( new Line( p[i], i+1 == l ? p[0] : p[i+1] ) );
        }

        return this._lines;
    },
    get center () {
        return new Point().mean(this.points);
    },
    get: function (index) {
        return this.points[index];
    },
    getCoords : function () {
        return this.points[0];
    },
    processPath : function (ctx, noWrap) {
        var p = this.points, i = 0, l = p.length;

        if (!noWrap) ctx.beginPath();
        for (; i <= l; i++) {
            if (i == 0) {
                ctx.moveTo(p[i]);
            } else {
                ctx.lineTo(p[i == l ? 0 : i]);
            }
        }
        if (!noWrap) ctx.closePath();

        return ctx;
    },

    grow: function () { return this; },

    getBoundingRectangle: function () {
        var p = this.points, l = p.length, from, to;

        if (l == 0) {
            throw new Error('Shape is empty');
        }

        while (l--) {

            if (from) {
                from.x = Math.min( from.x, p[l].x );
                from.y = Math.min( from.y, p[l].y );
                  to.x = Math.max(   to.x, p[l].x );
                  to.y = Math.max(   to.y, p[l].y );
            } else {
                from = p[l].clone();
                to   = p[l].clone();
            }

        }

        return new Rectangle( from, to );
    },

    // points invoking
    move : function (distance, reverse) {
        return this.invoke('move', distance, reverse)
    },
    rotate : function (angle, pivot) {
        return this.invoke('rotate', angle, pivot)
    },
    scale : function (power, pivot) {
        return this.invoke('scale', power, pivot)
    },
    invoke: function (method, args) {
        args = Array.prototype.slice.call(arguments, 1);

        this.points.map(function (point) {
            point[method].apply(point, args);
        });
        return this;
    },
    forEach : function (fn) {
        this.points.forEach(fn);
        return this;
    },
    each: function (fn, context) {
        return this.forEach(context ? fn.bind(context) : fn);
    },

    hasPoint : function (point) {
        point = Point.from(point);

        var result = false, points = this.points;
        for (var i = 0, l = this.length; i < l; i++) {
            var k = (i || l) - 1, I = points[i], K = points[k];
            if (
                (atom.number.between(point.y, I.y , K.y, "L")
                || atom.number.between(point.y, K.y , I.y, "L")
                ) && point.x < (K.x - I.x) * (point.y -I.y) / (K.y - I.y) + I.x
            ) {
                result = !result;
            }
        }
        return result;
    },
    intersect : function (poly) {
        if (poly.constructor != this.constructor) {
            return this.getBoundingRectangle().intersect( poly );
        }

        var tL = this.lines, pL = poly.lines, i = tL.length, k = pL.length;
        while (i-- > 0) for (k = pL.length; k-- > 0;) {
            if (tL[i].intersect(pL[k])) return true;
        }
        return false;
    },
    getPoints : function () {
        return atom.array.toHash(this.points);
    },
    clone: function () {
        return new this.constructor( atom.array.invoke(this.points, 'clone') );
    }
});

/*
---

name: "Shapes.Path"

description: "Provides Path as canvas object"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Shape
    - Shapes.Polygon

provides: Shapes.Path

...
*/

/**
 * @class Path
 * @extends Polygon:
 * get center
 * draw()
 * move(distance, reverse)
 * scale(power, pivot)
 * rotate(angle, pivot)
 * getBoundingRectangle()
 * [empty] grow()
 */
var Path = LibCanvas.declare( 'LibCanvas.Shapes.Path', 'Path', Polygon, {
    parts: [],

    initialize : function (parts) {
        this.parts = [];

        if (parts) this.set(parts);
    },

    set : function (parts) {
        this.parts.length = 0;

        if (Array.isArray(parts)) {
            for (var i = 0, l = parts.length; i < l; i++) {
                this.push(parts[i]);
            }
        }
    },

    get length () {
        return this.parts.length;
    },

    // methods
    moveTo: function (point) {
        return this.push('moveTo', [ Point.from(point) ]);
    },
    lineTo: function (point) {
        return this.push('lineTo', [ Point.from(point) ]);
    },
    curveTo: function (to, cp1, cp2) {
        var points = atom.array.pickFrom(arguments).map(Point);
        return this.push('curveTo', points);
    },

    // queue/stack
    push : function (method, points) {
        this.parts.push(Path.Part.from(method, points));
        return this;
    },
    unshift: function (method, points) {
        this.parts.unshift(Path.Part.from(method, points));
        return this;
    },
    pop : function () {
        return this.parts.pop();
    },
    shift: function () {
        return this.parts.shift();
    },

    processPath : function (ctx, noWrap) {
        if (!noWrap) ctx.beginPath();
        this.forEach(function (part) {
            ctx[part.method].apply(ctx, part.points);
        });
        if (!noWrap) ctx.closePath();
        return ctx;
    },

    intersect: function (obj) {
        return this.getBoundingRectangle()
            .intersect( obj.getBoundingRectangle() );
    },

    forEach: function (fn) {
        var parts = this.parts, i = 0, l = parts.length;
        while (i < l) {
            fn.call( this, parts[i++], i, this );
        }
        return this;
    },

    get points () {
        var points = [];
        this.forEach(function (part) {
            for (var i = 0, l = part.points.length; i < l; i++) {
                atom.array.include(points, part.points[i]);
            }
        });
        return points;
    },

    hasPoint : function (point) {
        var ctx = shapeTestBuffer().ctx;
        this.processPath(ctx);
        return ctx.isPointInPath(Point.from(point));
    },
    clone: function () {
        return new this.constructor(
            this.parts.invoke('clone')
        );
    }
});
/** @class Path.Part */
atom.declare('LibCanvas.Shapes.Path.Part', {
    initialize: function (method, points) {
        this.method = method;
        this.points = points.map(Point);
    },

    clone: function () {
        return new this.constructor(
            this.method,
            this.points.invoke('clone')
        );
    }
}).own({
    from: function (method, args) {
        if (method == null) {
            throw new Error('Empty path method');
        }

        if (typeof method == 'string') {
            return new this(method, args) ;
        } else if (atom.core.isArrayLike(method)) {
            return new this(method[0], args[1]);
        } else {
            return this;
        }
    }
});

/*
---

name: "Shapes.RoundedRectangle"

description: "Provides rounded rectangle as canvas object"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Shapes.Rectangle

provides: Shapes.RoundedRectangle

...
*/

/** @class RoundedRectangle */
var RoundedRectangle = LibCanvas.declare(
    'LibCanvas.Shapes.RoundedRectangle', 'RoundedRectangle', Rectangle, {
        radius: 0,

        setRadius: function (value) {
            this.radius = value;
            return this;
        },
        draw : Shape.prototype.draw,
        processPath : function (ctx, noWrap) {
            var from = this.from, to = this.to, radius = this.radius;
            if (!noWrap) ctx.beginPath();
            ctx
                .moveTo (from.x, from.y+radius)
                .lineTo (from.x,   to.y-radius)
                .curveTo(from.x, to.y, from.x + radius, to.y)
                .lineTo (to.x-radius, to.y)
                .curveTo(to.x,to.y, to.x,to.y-radius)
                .lineTo (to.x, from.y+radius)
                .curveTo(to.x, from.y, to.x-radius, from.y)
                .lineTo (from.x+radius, from.y)
                .curveTo(from.x,from.y,from.x,from.y+radius);
            if (!noWrap) ctx.closePath();
            return ctx;
        },


        clone: function method () {
            return method.previous
                .apply(this, arguments)
                .setRadius(this.radius);
        },

        equals: function (shape, accuracy) {
            return Rectangle.prototype.equals.call( this, shape, accuracy ) && shape.radius == this.radius;
        },

        dump: function () {
            var p = function (p) { return '[' + p.x + ', ' + p.y + ']'; };
            return '[shape RoundedRectangle(from'+p(this.from)+', to'+p(this.to)+', radius='+this.radius+')]';
        }
});

/*
---

name: "App.Behaviors"

description: "DEPRECATED"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas

provides: App.Behaviors

...
*/

/** @class App.Behaviors */
var Behaviors = declare( 'LibCanvas.App.Behaviors', {
    behaviors: {},

    initialize: function (element) {
        this.element   = element;
        this.behaviors = {};
    },

    /** @param [handler=false] */
    getMouse: function (handler) {
        return this.element.layer.app.resources.get(
            handler ? 'mouseHandler' : 'mouse'
        );
    },

    add: function (Behaviour, args) {
        if (typeof Behaviour == 'string') {
            Behaviour = this.constructor[Behaviour];
        }

        return this.behaviors[Behaviour.index] = new Behaviour(this, slice.call( arguments, 1 ));
    },

    get: function (name) {
        return this.behaviors[name] || null;
    },

    startAll: function (arg) {
        this.invoke('start', arguments);
        return this;
    },

    stopAll: function () {
        this.invoke('stop', arguments);
        return this;
    },

    /** @private */
    invoke: function (method, args) {
        var i, b = this.behaviors;
        for (i in b) if (b.hasOwnProperty(i)) {
            b[i][method].apply(b[i], args);
        }
        return this;
    }

}).own({
    attach: function (target, types, arg) {
        target.behaviors = new Behaviors(target);

        types.forEach(function (type) {
            target.behaviors.add(type, arg);
        });

        return target.behaviors;
    }
});


declare( 'LibCanvas.App.Behaviors.Behavior', {
    started: false,

    /** @private */
    eventArgs: function (args, eventName) {
        if (atom.core.isFunction(args[0])) {
            this.events.add( eventName, args[0] );
        }
    },

    /** @private */
    changeStatus: function (status){
        if (this.started == status) {
            return false;
        } else {
            this.started = status;
            return true;
        }
    }
});

/*
---

name: "App.Behaviors.Clickable"

description: "DEPRECATED"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App.Behaviors

provides: App.Behaviors.Clickable

...
*/

new function () {

function setValueFn (name, val) {
    var result = [name, val];
    return function () {
        if (this[name] != val) {
            this[name] = val;
            this.events.fire('statusChange', result);
        }
    };
}

return declare( 'LibCanvas.App.Behaviors.Clickable', App.Behaviors.Behavior, {

    callbacks: {
        'mouseover'   : setValueFn('hover' , true ),
        'mouseout'    : (function () {
            var dehover  = setValueFn('hover' , false),
                deactive = setValueFn('active', false);

            return function (e) {
                dehover .call(this, e);
                deactive.call(this, e);
            };
        })(),
        'mousedown'   : setValueFn('active', true ),
        'mouseup'     : setValueFn('active', false)
    },

    initialize: function (behaviors, args) {
        this.events = behaviors.element.events;
        this.eventArgs(args, 'statusChange');
    },

    start: function () {
        if (!this.changeStatus(true)) return this;

        this.eventArgs(arguments, 'statusChange');
        this.events.add(this.callbacks);
    },

    stop: function () {
        if (!this.changeStatus(false)) return this;

        this.events.remove(this.callbacks);
    }

}).own({ index: 'clickable' });

};

/*
---

name: "App.Behaviors.Draggable"

description: "DEPRECATED"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App.Behaviors

provides: App.Behaviors.Draggable

...
*/

declare( 'LibCanvas.App.Behaviors.Draggable', App.Behaviors.Behavior, {
    stopDrag: [ 'up', 'out' ],

    initialize: function (behaviors, args) {
        this.bindMethods([ 'onStop', 'onDrag', 'onStart' ]);

        this.behaviors = behaviors;
        this.element   = behaviors.element;
        if (!atom.core.isFunction(this.element.move)) {
            throw new TypeError( 'Element ' + this.element + ' must has «move» method' );
        }
        this.events  = behaviors.element.events;
        this.eventArgs(args, 'moveDrag');
    },

    bindMouse: function (method) {
        var mouse = this.mouse, stop = this.stopDrag;

        mouse.events
            [method]( 'move', this.onDrag )
            [method](  stop , this.onStop );

        return mouse;
    },

    start: function () {
        if (!this.changeStatus(true)) return this;

        this.mouse = this.behaviors.getMouse();
        if (!this.mouse) throw new Error('No mouse in element');
        this.eventArgs(arguments, 'moveDrag');
        this.events.add( 'mousedown', this.onStart );
    },

    stop: function () {
        if (!this.changeStatus(false)) return this;

        this.events.remove( 'mousedown', this.onStart );
    },

    /** @private */
    onStart: function (e) {
        if (e.button !== 0) return;

        this.bindMouse('add');
        this.events.fire('startDrag', [ e ]);
    },

    /** @private */
    onDrag: function (e) {
        if (!this.element.layer) {
            return this.onStop(e, true);
        }

        var delta = this.behaviors.getMouse().delta;
        this.element.move( delta );
        this.events.fire('moveDrag', [delta, e]);
    },

    /** @private */
    onStop: function (e, forced) {
        if (e.button === 0 || forced === true) {
            this.bindMouse('remove');
            this.events.fire('stopDrag', [ e ]);
        }
    }
}).own({ index: 'draggable' });

/*
---

name: "App.Light"

description: "LibCanvas.App.Light"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App

provides: App.Light

...
*/

/** @class App.Light */
declare( 'LibCanvas.App.Light', {

    initialize: function (size, settings) {
        var mouse, mouseHandler;

        this.settings = new Settings({
            size    : Size.from(size),
            name    : 'main',
            mouse   : true,
            invoke  : false,
            simple  : true,
            appendTo: 'body',
            intersection: 'auto'
        }).set(settings || {});

        this.app   = new App( this.settings.subset(['size', 'appendTo', 'simple']) );
        this.layer = this.app.createLayer(this.settings.subset(['name','invoke','intersection']));
        if (this.settings.get('mouse') === true) {
            mouse = new Mouse(this.app.container.bounds);
            mouseHandler = new App.MouseHandler({ mouse: mouse, app: this.app });

            this.app.resources.set({ mouse: mouse, mouseHandler: mouseHandler });
        }
    },

    createVector: function (shape, settings) {
        settings = atom.core.append({ shape:shape }, settings || {});
        return new App.Light.Vector(this.layer, settings);
    },

    createText: function (shape, style, settings) {
        settings = atom.core.append({ shape: shape, style: style }, settings);
        return new App.Light.Text(this.layer, settings);
    },

    createImage: function (shape, image, settings) {
        return new App.Light.Image(this.layer, atom.core.append({
            shape: shape, image: image
        }, settings));
    },

    get mouse () {
        return this.app.resources.get( 'mouse' );
    },

    get mouseHandler () {
        return this.app.resources.get( 'mouseHandler' );
    }

});

/*
---

name: "App.Light.Element"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App
    - App.Light

provides: App.Light.Element

...
*/

/** @class App.Light.Vector */
App.Light.Element = atom.declare( 'LibCanvas.App.Light.Element', App.Element, {

    get behaviors () {
        throw new Error( 'Please, use `element.clickable` & `element.draggable` instead' );
    },

    clickable : null,
    draggable : null,
    animatable: null,

    configure: function () {
        this.clickable  = new App.Clickable(this, this.redraw);
        this.draggable  = new App.Draggable(this, this.redraw);
        this.animatable = new atom.Animatable(this);
        this.animate    = this.animatable.animate;

        if (this.settings.get('mouse') !== false) {
            this.listenMouse();
        }
    },

    /**
     * Override by Animatable method
     */
    animate: function(){},

    listenMouse: function (unsubscribe) {
        var method = unsubscribe ? 'unsubscribe' : 'subscribe';
        return this.layer.app.resources.get('mouseHandler')[method](this);
    },

    destroy: function method () {
        this.listenMouse(true);
        return method.previous.call(this);
    }
});

/*
---

name: "App.Light.Image"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App.Light.Element

provides: App.Light.Image

...
*/

/** @class App.Light.Image */
App.Light.Image = atom.declare( 'LibCanvas.App.Light.Image', App.Light.Element, {
    get currentBoundingShape () {
        return this.shape.clone().fillToPixel();
    },

    renderTo: function (ctx) {
        ctx.drawImage({
            image: this.settings.get('image'),
            draw : this.shape
        })
    }
});

/*
---

name: "App.Light.Text"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - App
    - App.Light

provides: App.Light.Text

...
*/

/** @class App.Light.Text */
atom.declare( 'LibCanvas.App.Light.Text', App.Element, {
    get style () {
        return this.settings.get('style') || {};
    },

    get content () {
        return this.style.text || '';
    },

    set content (c) {
        if (Array.isArray(c)) c = c.join('\n');

        if (c != this.content) {
            this.redraw();
            this.style.text = String(c) || '';
        }
    },

    renderTo: function (ctx) {
        var bg    = this.settings.get('background');

        if (bg) ctx.fill( this.shape, bg );
        ctx.text(atom.core.append({
            to  : this.shape
        }, this.style));
    }
});

/*
---

name: "App.Light.Vector"

description: ""

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - App.Light.Element

provides: App.Light.Vector

...
*/

/** @class App.Light.Vector */
App.Light.Vector = atom.declare( 'LibCanvas.App.Light.Vector', App.Light.Element, {
    active: false,
    hover : false,

    configure: function method () {
        method.previous.call(this);

        this.style       = {};
        this.styleActive = {};
        this.styleHover  = {};
    },

    setStyle: function (key, values) {
        if (typeof key == 'object') {
            values = key;
            key = '';
        }
        key = 'style' + atom.string.ucfirst(key);

        atom.core.append( this[key], values );
        return this.redraw();
    },

    getStyle: function (type) {
        if (!this.style) return null;

        var
            active = (this.active || null) && this.styleActive[type],
            hover  = (this.hover  || null)  && this.styleHover [type],
            plain  = this.style[type];

        return active != null ? active :
               hover  != null ? hover  :
               plain  != null ? plain  : null;
    },

    get currentBoundingShape () {
        var
            br = this.shape.getBoundingRectangle(),
            lw = this.getStyle('stroke') && (this.getStyle('lineWidth') || 1);

        return lw ? br.fillToPixel().grow(2 * Math.ceil(lw)) : br;
    },

    renderTo: function (ctx) {
        var fill    = this.getStyle('fill'),
            stroke  = this.getStyle('stroke'),
            lineW   = this.getStyle('lineWidth'),
            opacity = this.getStyle('opacity');

        if (opacity === 0) return this;

        ctx.save();
        if (opacity) ctx.globalAlpha = atom.number.round(opacity, 3);
        if (fill) ctx.fill(this.shape, fill);
        if (stroke) {
            ctx.lineWidth = lineW || 1;
            ctx.stroke(this.shape, stroke);
        }
        ctx.restore();
        return this;
    }
});

/*
---

name: "Engines.Hex"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas

provides: Engines.Hex

...
*/

/** @class HexEngine */
LibCanvas.declare( 'LibCanvas.Engines.Hex', 'HexEngine', { });

/*
---

name: "Engines.Hex.Projection"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Polygon
    - Engines.Hex

provides: Engines.Hex.Projection

...
*/

/** @class HexEngine.Projection */
atom.declare( 'LibCanvas.Engines.Hex.Projection', {
    multipliers: {
        height: Math.cos( Math.PI / 6 ) * 2,
        chord : 1/2 // Math.sin( Math.PI / 6 )
    },

    /**
     * @param {object} settings
     * @param {int} settings.baseLength  - length of top and bottom lines
     * @param {int} settings.chordLength - height of left and right triangle
     * @param {int} settings.hexHeight   - height of the hex (length between top and bottom lines)
     */
    initialize: function (settings) {
        settings = this.settings = new Settings({
            baseLength : 0,
            chordLength: null,
            hexHeight  : null,
            start      : new Point(0, 0)
        }).set(settings);

        if (settings.get('chordLength') == null) {
            settings.set({
                chordLength: settings.get('baseLength') * this.multipliers.chord,
                hexHeight  : settings.get('hexHeight' ) * this.multipliers.height
            });
        }
    },

    /**
     * @param {int} [padding=0]
     * @return LibCanvas.Engines.HexProjection.Sizes
     */
    sizes: function (padding) {
        return new this.constructor.Sizes(this, padding);
    },

    /**
     * @param {int[]} coordinates
     * @return {bool}
     */
    isZero: function (c) {
        return c[0] === 0 && c[1] === 0 && c[2] === 0;
    },

    /**
     * @param {int[]} coordinates
     * @return Point
     */
    rgbToPoint: function (coordinates) {
        var
            red      = coordinates[0],
            green    = coordinates[1],
            blue     = coordinates[2],
            settings = this.settings,
            base     = settings.get('baseLength'),
            chord    = settings.get('chordLength'),
            height   = settings.get('hexHeight'),
            start    = settings.get('start');
        if (red + green + blue !== 0) {
            throw new Error( 'Wrong coordinates: ' + red + ' ' + green + ' ' + blue);
        }

        return new Point(
            start.x + (base + chord) * red,
            start.y + (blue - green) * height / 2
        );
    },

    /**
     * @param {Point} point
     * @return int[]
     */
    pointToRgb: function (point) {
        var
            settings = this.settings,
            base     = settings.get('baseLength'),
            chord    = settings.get('chordLength'),
            height   = settings.get('hexHeight'),
            start    = settings.get('start'),
            // counting coords
            red   = (point.x - start.x) / (base + chord),
            blue  = (point.y - start.y - red * height / 2) / height,
            green = 0 - red - blue;

        var dist = function (c) {
            return Math.abs(c[0] - red) + Math.abs(c[1] - green) + Math.abs(c[2] - blue);
        };

        var
            rF = Math.floor(red  ), rC = Math.ceil(red  ),
            gF = Math.floor(green), gC = Math.ceil(green),
            bF = Math.floor(blue ), bC = Math.ceil(blue );

        return [
            // we need to find closest integer coordinates
            [rF, gF, bF],
            [rF, gC, bF],
            [rF, gF, bC],
            [rF, gC, bC],
            [rC, gF, bF],
            [rC, gC, bF],
            [rC, gF, bC],
            [rC, gC, bC]
        ].filter(function (v) {
            // only correct variants - sum must be equals to zero
            return atom.array.sum(v) == 0;
        })
        .sort(function (left, right) {
            // we need coordinates with the smallest distance
            return dist(left) < dist(right) ? -1 : 1;
        })[0];
    },

    /**
     * @param {Point} center
     * @return LibCanvas.Shapes.Polygon
     */
    createPolygon: function (center) {
        var
            settings   = this.settings,
            halfBase   = settings.get('baseLength') / 2,
            halfHeight = settings.get('hexHeight')  / 2,
            radius     = halfBase + settings.get('chordLength'),

            right  = center.x + halfBase,
            left   = center.x - halfBase,
            top    = center.y - halfHeight,
            bottom = center.y + halfHeight;

        return new Polygon([
            new Point(left , top),                  // top-left
            new Point(right, top),                  // top-right
            new Point(center.x + radius, center.y), // right
            new Point(right, bottom),               // bottom-right
            new Point(left , bottom),               // bottom-left
            new Point(center.x - radius, center.y)  // left
        ]);
    }
});

declare( 'LibCanvas.Engines.Hex.Projection.Sizes', {

    initialize: function (projection, padding) {
        this.projection = projection;
        this.padding    = padding || 0;
        this.centers    = [];
    },

    _limits: null,

    /**
     * @param {int[]} coordinates
     * @return LibCanvas.Engines.HexProjection.Size
     */
    add: function (coordinates) {
        this._limits = null;
        this.centers.push(this.projection.rgbToPoint( coordinates ));
        return this;
    },

    /** @return object */
    limits: function () {
        if (this._limits) return this._limits;

        var min, max, centers = this.centers, i = centers.length, c;

        while (i--) {
            c = centers[i];
            if (min == null) {
                min = c.clone();
                max = c.clone();
            } else {
                min.x = Math.min( min.x, c.x );
                min.y = Math.min( min.y, c.y );
                max.x = Math.max( max.x, c.x );
                max.y = Math.max( max.y, c.y );
            }
        }

        return this._limits = { min: min, max: max };
    },

    /** @return Size */
    size: function () {
        var
            limits   = this.limits(),
            settings = this.projection.settings,
            base     = settings.get('baseLength'),
            chord    = settings.get('chordLength'),
            height   = settings.get('hexHeight'),
            padding  = this.padding;

        return new Size(
            limits.max.x - limits.min.x + base    + 2 * (padding + chord),
            limits.max.y - limits.min.y + height  + 2 *  padding
        );
    },

    /** @return Point */
    center: function () {
        var
            min      = this.limits().min,
            settings = this.projection.settings,
            base     = settings.get('baseLength'),
            chord    = settings.get('chordLength'),
            height   = settings.get('hexHeight'),
            padding  = this.padding;

        return new Point(
            padding + base   /2 + chord - min.x,
            padding + height /2         - min.y
        );
    }


});

/*
---

name: "Engines.Isometric"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas

provides: Engines.Isometric

...
*/

/** @class HexEngine */
LibCanvas.declare( 'LibCanvas.Engines.Isometric', 'IsometricEngine', { });

/*
---

name: "Engines.Isometric.Projection"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point3D
    - Engines.Isometric

provides: Engines.Isometric.Projection

...
*/

/** @class IsometricProjection */
atom.declare( 'LibCanvas.Engines.Isometric.Projection', {

    /**
     * factor (and default factor in proto)
     * @property {Point3D}
     */
    factor: [0.866, 0.5, 0.866],

    /**
     * size (and default size in proto)
     * @property int
     */
    size: 1,

    /**
     * start (and default start in proto)
     * @property {Point}
     */
    start: [0, 0],

    /**
     * @constructs
     * @param {object} settings
     * @param {Point3D} settings.factor
     * @param {Point3D} settings.size
     * @param {Point} settings.start - position of [0,0] coordinate
     */
    initialize: function (settings) {
        this.bindMethods([ 'toIsometric', 'to3D' ]);
        this.settings = new Settings(settings);

        this.factor = Point3D( this.settings.get('factor') || this.factor );
        this.size   = Number ( this.settings.get('size')   || this.size   );
        this.start  = Point  ( this.settings.get('start')  || this.start  );
    },

    /**
     * @param {Point3D} point3d
     * @returns {Point}
     */
    toIsometric: function (point3d) {
        point3d = Point3D( point3d );
        return new Point(
            (point3d.y + point3d.x) * this.factor.x,
            (point3d.y - point3d.x) * this.factor.y - point3d.z * this.factor.z
        )
        .mul(this.size)
        .move(this.start);
    },

    /**
     * @param {Point} point
     * @param {int} [z=0]
     * @returns {Point3D}
     */
    to3D: function (point, z) {
        point = Point(point);
        z = Number(z) || 0;

        var
            size  = this.size,
            start = this.start,
            dXY = ((point.y - start.y) / size + z * this.factor.z) / this.factor.y,
            pX  = ((point.x - start.x) / size / this.factor.x - dXY) / 2;

        return new Point3D( pX, pX + dXY, z );
    }
});

/*
---

name: "TileEngine"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - LibCanvas
    - Point
    - Size
    - Rectangle

provides: Engines.Tile

...
*/

/** @class TileEngine */
var TileEngine = LibCanvas.declare( 'LibCanvas.Engines.Tile', 'TileEngine', {

    /**
     * @param {Object} settings
     * @param {*} settings.defaultValue
     * @param {Size} settings.size
     * @param {Size} settings.cellSize
     * @param {Size} settings.cellMargin
     */
    initialize: function (settings) {
        this.cells   = [];
        this.methods = {};
        this.cellsUpdate = [];

        this.events   = new Events(this);
        this.settings = new Settings(settings).addEvents(this.events);
        this.createMatrix();
    },

    setMethod: atom.core.overloadSetter(function (name, method) {
        if (this.isValidMethod(method)) {
            this.methods[ name ] = method;
        } else {
            throw new TypeError( 'Unknown method: «' + name + '»' );
        }
    }),

    countSize: function () {
        var
            settings   = this.settings,
            cellSize   = settings.get('cellSize'),
            cellMargin = settings.get('cellMargin');

        return new Size(
            (cellSize.x + cellMargin.x) * this.width  - cellMargin.x,
            (cellSize.y + cellMargin.y) * this.height - cellMargin.y
        );
    },

    getCellByIndex: function (point) {
        point = Point.from(point);
        return this.isIndexOutOfBounds(point) ? null:
            this.cells[ this.width * point.y + point.x ];
    },

    getCellByPoint: function (point) {
        var
            settings   = this.settings,
            cellSize   = settings.get('cellSize'),
            cellMargin = settings.get('cellMargin');

        point = Point.from(point);
        
        return this.getCellByIndex(new Point(
            parseInt(point.x / (cellSize.width  + cellMargin.x)),
            parseInt(point.y / (cellSize.height + cellMargin.y))
        ));
    },

    refresh: function (ctx, translate) {
        if (this.requireUpdate) {
            ctx.save();
            if (translate) ctx.translate(translate);
            atom.array.invoke( this.cellsUpdate, 'renderTo', ctx );
            ctx.restore();
            this.cellsUpdate.length = 0;
        }
        return this;
    },

    get width () {
        return this.settings.get('size').width;
    },

    get height () {
        return this.settings.get('size').height;
    },

    get requireUpdate () {
        return !!this.cellsUpdate.length;
    },

    /** @private */
    isValidMethod: function (method) {
        var type = typeof method;

        return type == 'function'
            || type == 'string'
            || atom.dom.isElement(method);
    },

    /** @private */
    createMatrix : function () {
        var x, y,
            settings   = this.settings,
            size       = settings.get('size'),
            value      = settings.get('defaultValue'),
            cellSize   = settings.get('cellSize'),
            cellMargin = settings.get('cellMargin');

        for (y = 0; y < size.height; y++) for (x = 0; x < size.width; x++) {
            this.createMatrixCell(new Point(x, y), cellSize, cellMargin, value);
        }
        return this;
    },

    /** @private */
    createMatrixCell: function (point, size, margin, value) {
        var shape = this.createCellRectangle(point, size, margin);

        this.cells.push(this.createCell(point, shape, value));
    },

    /** @private */
    createCell: function (point, shape, value) {
        return new TileEngine.Cell( this, point, shape, value );
    },

    /** @private */
    createCellRectangle: function (point, cellSize, cellMargin) {
        return new Rectangle({
            from: new Point(
                (cellSize.x + cellMargin.x) * point.x,
                (cellSize.y + cellMargin.y) * point.y
            ),
            size: cellSize
        });
    },

    /** @private */
    isIndexOutOfBounds: function (point) {
        return point.x < 0 || point.y < 0 || point.x >= this.width || point.y >= this.height;
    },

    /** @private */
    updateCell: function (cell) {
        if (!this.requireUpdate) {
            this.events.fire('update', [ this ]);
        }
        atom.array.include( this.cellsUpdate, cell );
        return this;
    }

});

/*
---

name: "TileEngine.Cell"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - Engines.Tile

provides: Engines.Tile.Cell

...
*/
/** @class TileEngine.Cell */
declare( 'LibCanvas.Engines.Tile.Cell', {

    initialize: function (engine, point, rectangle, value) {
        this.engine = engine;
        this.point  = point;
        this.value  = value;
        this.rectangle = rectangle;
    },

    /** @private */
    _value: null,

    get value () {
        return this._value;
    },

    set value (value) {
        this._value = value;
        this.engine.updateCell(this);
    },

    renderTo: function (ctx) {
        var method, value = this.value, rectangle = this.rectangle;

        ctx.clear( rectangle );

        if (value == null) return this;

        method = this.engine.methods[ value ];

        if (method == null) {
            throw new Error( 'No method in tile engine: «' + this.value + '»')
        }

        if (atom.dom.isElement(method)) {
            ctx.drawImage( method, rectangle );
        } else if (typeof method == 'function') {
            method.call( this, ctx, this );
        } else {
            ctx.fill( rectangle, method );
        }
        return this;
    }

});

/*
---

name: "TileEngine.Element"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - Engines.Tile
    - App.Element

provides: Engines.Tile.Element

...
*/
/** @class TileEngine.Element */
declare( 'LibCanvas.Engines.Tile.Element', App.Element, {
    configure: function () {
        this.shape = new Rectangle(
            this.settings.get('from') || new Point(0, 0),
            this.engine.countSize()
        );
        this.engine.events.add( 'update', this.redraw );
    },

    get engine () {
        return this.settings.get('engine');
    },

    clearPrevious: function () {},

    renderTo: function (ctx) {
        this.engine.refresh(ctx, this.shape.from);
    }
}).own({
    app: function (app, engine, from) {
        return new this( app.createLayer({
            name: 'tile-engine',
            intersection: 'manual',
            invoke: false
        }), {
            engine: engine,
            from: from
        });
    }
});



/*
---

name: "TileEngine.Mouse"

license:
    - "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
    - "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
    - "Shock <shocksilien@gmail.com>"

requires:
    - Engines.Tile.Element

provides: Engines.Tile.Mouse

...
*/
/** @class TileEngine.Mouse */
declare( 'LibCanvas.Engines.Tile.Mouse', {
    eventsList: 'mousemove mouseout mousedown mouseup contextmenu'
        .split(' '),

    initialize: function (element, mouse) {
        this.bindMethods(this.eventsList);

        this.events   = new Events(this);

        /** @private */
        this.mouse    = mouse;
        /** @private */
        this.element  = element;
        /** @private */
        this.previous = null;
        /** @private */
        this.lastDown = null;
        this.subscribe(false);
    },

    /** @private */
    subscribe: function (un) {
        var events = atom.object.collect(this, this.eventsList, null);

        this.element.events
            [ un ? 'remove' : 'add' ]
            (events);
    },
    /** @private */
    mousemove: function (e) {
        var cell = this.get();
        if (this.previous != cell) {
            this.outCell(e);
            this.fire( 'over', cell, e );
            this.previous = cell;
        }
    },
    /** @private */
    mouseout: function (e) {
        this.outCell(e);
    },
    /** @private */
    mousedown: function (e) {
        var cell = this.get();
        this.fire( 'down', cell, e );
        this.lastDown = cell;
    },
    /** @private */
    mouseup: function (e) {
        var cell = this.get();
        this.fire( 'up', cell, e );
        if (cell != null && cell == this.lastDown) {
            this.fire( 'click', cell, e );
        }
        this.lastDown = null;
    },
    /** @private */
    contextmenu: function (e) {
        var cell = this.get();
        if (cell != null) {
            this.fire( 'contextmenu', cell, e );
        }
    },
    /** @private */
    get: function () {
        return this.element.engine.getCellByPoint(
            this.mouse.point.clone().move(this.element.shape.from, true)
        );
    },

    /** @private */
    fire: function (event, cell, e) {
        return this.events.fire( event, [ cell, e ]);
    },

    /** @private */
    outCell: function (e) {
        if (this.previous) {
            this.fire( 'out', this.previous, e );
            this.previous = null;
        }
    }
});

/*
---

name: "Plugins.Animation.Core"

description: ""

license:
- "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
- "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
- Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

provides:
- Plugins.Animation
- Plugins.Animation.Core

requires:
- LibCanvas

...
*/

/** @class Animation */
var Animation = LibCanvas.declare( 'LibCanvas.Plugins.Animation', 'Animation', {
    /** @private */
    ownStartTime: null,
    /** @private */
    timeoutId   : 0,
    /** @private */
    synchronizedWith: null,

    initialize: function (settings) {
        this.bindMethods('update');

        this.events = new atom.Events(this);
        this.settings = new atom.Settings(settings).addEvents(this.events);
        this.run();
    },

    stop: function () {
        this.startTime = null;
        return this.update();
    },

    run: function () {
        this.startTime = Date.now();
        return this.update();
    },

    synchronize: function (anim) {
        this.synchronizedWith = anim;
        return this;
    },

    get: function () {
        return this.sheet.get(this.startTime);
    },

    /** @private */
    get sheet () {
        return this.settings.get('sheet');
    },

    /** @private */
    set sheet (sheet) {
        return this.settings.set('sheet', sheet);
    },

    /** @private */
    set startTime (time) {
        this.ownStartTime = time;
    },

    /** @private */
    get startTime () {
        if (this.synchronizedWith) {
            return this.synchronizedWith.startTime;
        } else {
            return this.ownStartTime;
        }
    },

    /** @private */
    update: function () {
        var delay = this.getDelay();

        clearTimeout(this.timeoutId);

        if (delay == null || this.startTime == null) {
            this.events.fire('stop');
        } else {
            this.timeoutId = setTimeout( this.update, delay );
            this.events.fire('update', [ this.get() ]);
        }
        return this;
    },

    /** @private */
    getDelay: function () {
        return this.startTime == null ? null :
            this.sheet.getCurrentDelay(this.startTime);
    }
});

/*
---

name: "Plugins.Animation.Frames"

description: ""

license:
- "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
- "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
- Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

provides:
- Plugins.Animation
- Plugins.Animation.Frames

requires:
- LibCanvas
- Plugins.Animation.Core

...
*/

/** @class Animation.Frames */
atom.declare( 'LibCanvas.Plugins.Animation.Frames', {
    /** @private */
    sprites: [],

    initialize: function (image, width, height) {
        if (image == null) throw new TypeError('`image` cant be null');

        this.sprites = [];
        this.image   = image;
        this.size    = new Size(
            Math.round( width  == null ? image.width  : width  ),
            Math.round( height == null ? image.height : height )
        );

        this.prepare();
    },

    get: function (id) {
        var sprite = this.sprites[id];

        if (!sprite) {
            throw new Error('No sprite with such id: ' + id);
        }

        return sprite;
    },

    get length () {
        return this.sprites.length;
    },

    /** @private */
    prepare: function () {
        var x, y,
            im = this.image,
            w  = this.size.width,
            h  = this.size.height;

        for     (y = 0; y <= im.height - h; y += h) {
            for (x = 0; x <= im.width  - w; x += w) {
                this.sprites.push( this.makeSprite(new Point(x, y)) );
            }
        }

        if (!this.length) {
            throw new TypeError('Animation is empty');
        }
    },

    /** @private */
    makeSprite: function (from) {
        var
            size = this.size,
            buffer = LibCanvas.buffer(size, true);

        buffer.ctx.drawImage({
            image: this.image,
            draw : buffer.ctx.rectangle,
            crop : new Rectangle(from, size)
        });

        return buffer;
    }
});

/*
---

name: "Plugins.Animation.Image"

description: ""

license:
- "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
- "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
- Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

provides:
- Plugins.Animation
- Plugins.Animation.Image

requires:
- LibCanvas
- Plugins.Animation.Core

...
*/

/** @name Animation.Image */
atom.declare( 'LibCanvas.Plugins.Animation.Image', {
    /** @private */
    initialize: function (animation) {
        this.bindMethods('update');

        if (animation instanceof Animation.Sheet) {
            animation = { sheet: animation };
        }
        if (!(animation instanceof Animation)) {
            animation = new Animation(animation);
        }

        this.buffer    = LibCanvas.buffer(animation.sheet.size, true);
        this.element   = atom.dom(this.buffer);
        this.animation = animation;
        this.element.controller = this;

        animation.events.add( 'update', this.update );
    },

    /** @private */
    update: function (image) {
        var ctx = this.buffer.ctx;

        ctx.clearAll();
        if (image) ctx.drawImage(image);
    }
}).own({
    element: function (animation) {
        return new this(animation).element;
    }
});

/*
---

name: "Plugins.Animation.Sheet"

description: ""

license:
- "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
- "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
- Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

provides:
- Plugins.Animation
- Plugins.Animation.Sheet

requires:
- LibCanvas
- Plugins.Animation.Core

...
*/

/** @class Animation.Sheet */
atom.declare( 'LibCanvas.Plugins.Animation.Sheet', {

    initialize: function (options) {
        this.frames = options.frames;
        this.delay  = options.delay;
        this.looped = options.looped;
        if (options.sequence == null) {
            this.sequence = atom.array.range(0, this.frames.length - 1);
        } else {
            this.sequence = options.sequence;
        }
    },

    /** @private */
    get size () {
        return this.frames.size;
    },

    /** @private */
    get: function (startTime) {
        if (startTime == null) return null;

        var id = this.getFrameId(this.countFrames(startTime));
        return id == null ? id : this.frames.get( id );
    },

    /** @private */
    getCurrentDelay: function (startTime) {
        var frames, switchTime;

        frames = this.countFrames(startTime);

        if (this.getFrameId(frames) == null) {
            return null;
        }

        // когда был включён текущий кадр
        switchTime = frames * this.delay + startTime;

        // до следующего кадра - задержка минус время, которое уже показывается текущий
        return this.delay - ( Date.now() - switchTime );
    },

    /** @private */
    getFrameId: function (framesCount) {
        if (this.looped) {
            return this.sequence[ framesCount % this.sequence.length ];
        } else if (framesCount >= this.sequence.length) {
            return null;
        } else {
            return this.sequence[framesCount];
        }
    },

    /** @private */
    countFrames: function (startTime) {
        return Math.floor( (Date.now() - startTime) / this.delay );
    }

});

/*
---

name: "Plugins.Curve"

description: "Provides math base for bezier curves"

license:
- "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
- "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
- Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

provides: Plugins.Curve.Core

requires:
- LibCanvas
- Point

...
*/

/** @name LibCanvas.Plugins.Curve */
atom.declare( 'LibCanvas.Plugins.Curve', {

    step: 0.0001,

    initialize: function (data) {
        var Class = this.constructor.classes[data.points.length];

        if (Class) return new Class(data);

        this.setData(data);
    },

    setData: function (data) {
        this.from = data.from;
        this.to   = data.to;
        this.cp   = data.points;
    },

    getAngle: function (t) {
        var f;

        if (t < this.step) {
            f = t - this.step;
        } else {
            f  = t;
            t += this.step;
        }

        return this.getPoint(t).angleTo(this.getPoint(f));
    }

}).own({
    classes: {},

    addClass: function (points, Class) {
        this.classes[points] = Class;
    }
});

/*
---

name: "Plugins.Curve.Quadratic"

description: "Provides math base for bezier curves"

license:
- "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
- "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
- Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

provides:
- Plugins.Curve
- Plugins.Curve.Quadratic

requires:
- Plugins.Curve.Core

...
*/

/** @name LibCanvas.Plugins.Curve.Quadratic */
atom.declare( 'LibCanvas.Plugins.Curve.Quadratic', LibCanvas.Plugins.Curve, {

    initialize: function (data) {
        this.setData(data);
    },

    getPoint: function (t) {
        var
            from = this.from,
            to   = this.to,
            point= this.cp[0],
            i    = 1 - t;

        return new Point(
            i*i*from.x + 2*t*i*point.x + t*t*to.x,
            i*i*from.y + 2*t*i*point.y + t*t*to.y
        );
    }

});

LibCanvas.Plugins.Curve.addClass(1, LibCanvas.Plugins.Curve.Quadratic);

/*
---

name: "Plugins.Curve.Qubic"

description: "Provides math base for bezier curves"

license:
- "[GNU Lesser General Public License](http://opensource.org/licenses/lgpl-license.php)"
- "[MIT License](http://opensource.org/licenses/mit-license.php)"

authors:
- Pavel Ponomarenko aka Shock <shocksilien@gmail.com>

provides:
- Plugins.Curve
- Plugins.Curve.Qubic

requires:
- Plugins.Curve.Core

...
*/

/** @name LibCanvas.Plugins.Curve.Qubic */
atom.declare( 'LibCanvas.Plugins.Curve.Qubic', LibCanvas.Plugins.Curve, {

    initialize: function (data) {
        this.setData(data);
    },

    getPoint: function (t) {
        var
            from = this.from,
            to   = this.to,
            cp   = this.cp,
            i    = 1 - t;

        return new Point(
            i*i*i*from.x + 3*t*i*i*cp[0].x + 3*t*t*i*cp[1].x + t*t*t*to.x,
            i*i*i*from.y + 3*t*i*i*cp[0].y + 3*t*t*i*cp[1].y + t*t*t*to.y
        );
    }

});

LibCanvas.Plugins.Curve.addClass(2, LibCanvas.Plugins.Curve.Qubic);

}).call(typeof window == 'undefined' ? exports : window, atom, Math);
