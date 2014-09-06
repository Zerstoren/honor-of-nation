var rect = new Ractive({
    el: document.querySelector('#mech'),
    template: "<span><label>Enter your name:<input value='{{cart}}'></label><label>Enter your name:<input value='{{name}}'></label><p>Hello, {{name}}!</p></span>",
    data: {
        name: 1,
        cart: ''
    }
});


rect.observe('*', function(newVal, oldVal) {
    console.log(arguments);
})