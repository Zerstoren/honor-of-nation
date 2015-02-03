//Стандартный экспорт модуля в nodejs
module.exports = function(grunt) {

    var execSync = require('exec-sync');
    var commitHash = execSync('git rev-parse HEAD');

    var deploySassFiles = {};
    deploySassFiles['public/deploy/' + commitHash + '/css.css'] = 'sass/init.scss';

    //Загрузка модулей, которые предварительно установлены
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-html-build');

    grunt.registerTask('_default', '', function () {
        // Инициализация конфига GruntJS
        grunt.initConfig({
            //Например проверка кода javascript с помощью утилиты jshint
            jshint: {
                options: {
                    globals: {
                        jQuery: true,
                        console: true,
                        module: true
                    }
                },

                files: [
                    'public/js/**/*.js',
                    '!public/js/libs/alertify.js',
                    '!public/js/libs/backbone.js',
                    '!public/js/libs/bootstrap.js',
                    '!public/js/libs/jquery.js',
                    '!public/js/libs/ractive.js',
                    '!public/js/libs/ractive-backbone-adapter.js',
                    '!public/js/libs/underscore.js',
                    '!public/js/libs/require.js'
                ]
            },

            //Склеивание файлов
            concat: {
                js: {
                    src: [
                        'public/js/libs/require.js',
                        'public/js/libs/underscore.js',
                        'public/js/libs/alertify.js',
                        'public/js/libs/jquery.js',
                        'public/js/libs/bootstrap.js',
                        'public/js/libs/backbone.js',
                        'public/js/libs/ractive.js',
                        'public/js/libs/ractive-backbone-adapter.js',
                        'public/js/libs/socket.js',
                        'public/js/libs/defferedTrigger.js',
                        'public/js/libs/bootstrap.js',

                        'public/deploy/' + commitHash + '/view.js',

                        'public/js/libs/abstract/**/*.js',
                        'public/js/collection/**/*.js',
                        'public/js/controller/**/*.js',
                        'public/js/factory/**/*.js',
                        'public/js/gateway/**/*.js',
                        'public/js/model/**/*.js',
                        'public/js/service/**/*.js',
                        'public/js/view/**/*.js',

                        'public/js/system/config.js',
                        'public/js/system/preStart.js',
                        'public/js/system/router.js',
                        'public/js/system/template.js',
                        'public/js/system/bootstrap.js'
                    ],
                    dest: 'public/deploy/' + commitHash + '/js.js'
                }
            },

            sass: {
                dist: {
                    options: {},
                    files: deploySassFiles
                }
            },

            cssmin: {
                minify: {
                    expand: true,
                    cwd: 'public/deploy/' + commitHash + '/',
                    src: ['css.css'],
                    dest: 'public/deploy/' + commitHash + '/',
                    ext: '.min.css'
                }
            },

            uglify: {
                dist: {
                    src: ['<%= concat.js.dest %>'],
                    dest: 'public/deploy/' + commitHash + '/js.min.js'
                }
            },

            htmlbuild: {
                dist: {
                    src: 'public/deploy/index.release.html',
                    dest: 'public/deploy/' + commitHash + '/index.release.html'
                },

                options: {
                    data: {
                        commit: commitHash
                    }
                }
            }
        });
    });

    grunt.registerTask('tpls', 'Concat all tpl files', function () {
        var fs = require('fs');
        var results = {};

        var options = {
            listeners: {
                file: function (root, fileStats, next) {
                    data = fs.readFileSync(root + '/' + fileStats.name).toString();
                    results[(root + '/' + fileStats.name).replace('public/js/tpl/', '').replace('.tpl', '')] =
                        data.replace(/\n/gmi, '').replace(/  /gmi, "");

                    next();
                }
            }
        };

        require('walk').walkSync("public/js/tpl", options);
        fs.writeFileSync('public/deploy/' + commitHash + '/view.js', "define('tpls', function() { return " + JSON.stringify(results) + "; });");
    });

    grunt.registerTask('clean', 'Clean up project', function () {
        execSync('rm public/deploy/' + commitHash + '/view.js');
    });


    grunt.registerTask('_release', 'Release commit apply on server', function() {
         try {
             execSync("rm public/index.html");
         } catch(Error) {}

         execSync("ln public/deploy/" + commitHash + "/index.release.html public/index.html");
    });

    grunt.registerTask('_deploy', 'Deploy last commit', function () {

        // Инициализация конфига GruntJS
        grunt.initConfig({
            htmlbuild: {
                dist: {
                    src: 'public/deploy/index.deploy.html',
                    dest: 'public/deploy/' + commitHash + '/index.deploy.html'
                },

                options: {
                    data: {
                        commit: commitHash
                    }
                }
            }
        });
    });

    grunt.registerTask('_deploy_clean', '', function () {
         try {
            execSync("rm public/index.html");
        } catch(Error) {}

        execSync("ln public/deploy/" + commitHash + "/index.deploy.html public/index.html");
        execSync("rm public/deploy/" + commitHash + "/css.css");
        execSync("rm public/deploy/" + commitHash + "/js.js");
        execSync("rm public/deploy/" + commitHash + "/index.release.html");
        execSync("rm -rf public/js");
        execSync("rm -rf public/css");
    });

    //Эти задания будут выполнятся сразу же когда вы в консоли напечатание grunt, и нажмете Enter
    grunt.registerTask('default', ['_default', 'jshint', 'htmlbuild', 'sass', 'cssmin', 'tpls', 'concat', 'uglify', 'clean']);
    grunt.registerTask('rebuild', ['_default', 'htmlbuild', 'sass', 'tpls', 'concat', 'clean']);
    grunt.registerTask('release', ['_release']);
    grunt.registerTask('deploy',  ['_deploy', 'htmlbuild', '_deploy_clean']);
    grunt.registerTask('hint', ['_default', 'jshint']);
};
