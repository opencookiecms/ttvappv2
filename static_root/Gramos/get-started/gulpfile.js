var gulp = require("gulp"),
    sass = require("gulp-sass"),
    uglify = require("gulp-uglify"),
    cleanCSS = require('gulp-clean-css'),
    autoprefixer = require('gulp-autoprefixer'),
    rename = require("gulp-rename");

var config = {
    "paths" : {
        "css" : "./assets/css",
        "sass" : "./assets/sass",
        "js" : "./assets/js"
    },
    "autoprefixerBrowsers": [
        "> 0%"
    ]
};

function swallowError (error) {
    console.log(error.toString());
    this.emit('end');
}

gulp.task("sass", function () {
    gulp.src(config.paths.sass + "/app.scss")
        .pipe(sass({outputStyle: "expanded"})).on('error', swallowError)
        .pipe(autoprefixer(config.autoprefixerBrowsers))
        .pipe(gulp.dest(config.paths.css));
});

gulp.task('minify-css', function () {
    gulp.src(config.paths.css + '/app.css')
        .pipe(cleanCSS({compatibility: 'ie8'})).on('error', swallowError)
        .pipe(rename('app.min.css')).on('error', swallowError)
        .pipe(autoprefixer(config.autoprefixerBrowsers))
        .pipe(gulp.dest(config.paths.css));
});

gulp.task("js", function () {
    gulp.src(config.paths.js + '/app.js')
        .pipe(uglify()).on('error', swallowError)
        .pipe(rename({
            suffix: '.min'
        })).on('error', swallowError)
        .pipe(gulp.dest(config.paths.js));
});

gulp.task('default', function () {

    gulp.watch(config.paths.sass + "/**", ["sass"]);

    gulp.watch(config.paths.sass + "/*/*.scss", ["sass"]);

    gulp.watch(config.paths.sass + "/*.scss", ["sass"]);

    gulp.watch(config.paths.css + "/*.css", ["minify-css"]);

    gulp.watch(config.paths.js + "/*", ["js"]);

});