'use strict';

module.exports = function(grunt) {

	grunt.initConfig({
		compass:{
			dist:{
				options:{
					sassDir:'sass',
					cssDir: 'css',
					outputStyle: 'compressed'
				}
			}
		},

		watch:{
			compass:{
				files:[ 'sass/**/*.scss' ],
				tasks:[ 'compass' ]
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-imagemin');
	grunt.loadNpmTasks('grunt-contrib-compass');
};