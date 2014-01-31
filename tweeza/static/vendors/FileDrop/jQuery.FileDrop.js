(function ($) {
	'use strict';

	//====================================================================
	//Private
	//====================================================================
	
	//Default timer for when to remove the CSS class
	var exitTimer = null;

	function stopEvent(ev){
		ev.stopPropagation();
		ev.preventDefault();
	}

	//The options object is passed in and normalized
	function normalizeOptions(options){
		//If a function was passed in instead of an options object,
		//just use this as the onFileRead options instead
		if($.isFunction(options)){
			var o = {};
			o.onFileRead = options;
			options=o;
		}

		//Create a finalized version of the options
		var opts = $.extend({}, $.fn.fileDrop.defaults, options);

		//If we are decodeing Base64, then we must also remove the data URI Scheme form the beginning of the Base64 string
		if (opts.decodeBase64){
			opts.removeDataUriScheme = true;
		}

		//This allows for string or jQuery selectors to be used
		opts.addClassTo = $(opts.addClassTo);

		//This option MUST be a function or else you can't really do anything...
		if(!$.isFunction(opts.onFileRead)){
			throw('The option "onFileRead" is not set to a function!');
		}

		return opts;
	}

	//
	var events = {
		over : function(ev, $dropArea, opts){
			$(opts.addClassTo).addClass(opts.overClass);
			stopEvent(ev);
		},
		exit : function(ev, $dropArea, opts){
			//Create a timer so that the CSS class is only removed after 100ms
			clearTimeout(exitTimer);
			exitTimer=setTimeout(function(){
				$(opts.addClassTo).removeClass(opts.overClass);
			}, 100);
			stopEvent(ev);
		},
		drop : function(ev, $dropArea, opts){
			$(opts.addClassTo).removeClass(opts.overClass);
			stopEvent(ev);
			var fileList = ev.dataTransfer.files;

			//Create an array of file objects for us to fill in
			var fileArray = [];

			//Loop through each file
			for(var i = 0; i <= fileList.length; i++){

				//Create a new file reader to read the file
				var reader = new window.FileReader();

				//Create a closure so we can properly pass in the file information since this will complete async!
				var completeFn = (handleFile)(fileList[i], fileArray, fileList.length, opts);

				//Different browsers impliment this in different ways, but call the complete function when the file has finished being read
				if(reader.addEventListener) {
					// Firefox, Chrome
					reader.addEventListener('loadend', completeFn, false);
				} else {
					// Safari
					reader.onloadend = completeFn;
				}

				//Actually read the file
				reader.readAsDataURL(fileList[i]);
			}
		}
	};

	//This is called for each initially selected DOM element
	function setEvents(el, opts){
		var $dropArea = $(el);

		//can't bind these events with jQuery!
		el.addEventListener('dragenter', function(ev){
			events.over(ev, $dropArea, opts);
		}, false);
		el.addEventListener('dragover', function(ev){
			events.exit(ev, $dropArea, opts);
		}, false);
		el.addEventListener('drop', function(ev){
			events.drop(ev, $dropArea, opts);
		}, false);
	}

	//This is the complete function for reading a file,
	function handleFile(theFile, fileArray, fileCount, opts) {
		//When called, it has to return a function back up to the listener event
		return function(ev){

			var fileData = ev.target.result;
			
			if(opts.removeDataUriScheme){
				fileData = $.removeUriScheme(fileData);
			}
			
			if(opts.decodeBase64){
				fileData = decodeBase64(fileData);
			}

			//Add the current file to the array
			fileArray.push({
				name: theFile.name,
				size: theFile.size,
				type: theFile.type,
				lastModified: theFile.lastModifiedDate,
				data: fileData
			});
			
			//Once the correct number of items have been put in the array, call the completion function		
			if(fileArray.length === fileCount && $.isFunction(opts.onFileRead)){
				opts.onFileRead(fileArray, opts);
			}
		};
	}

	function decodeBase64(str){
		var decoded = window.atob( str );
		try{
			return decodeURIComponent(window.escape(decoded));
		}catch(ex){
			return '';
		}
	}

	//====================================================================
	//Public
	//====================================================================

	// jQuery plugin initialization
	$.fn.fileDrop = function (options) {

		var opts = normalizeOptions(options);

		//Return the elements & loop though them
		return this.each(function () {
			//Make a copy of the options for each selected element
			var perElementOptions = opts;
			
			//If this option was not set, make it the same as the drop area
			if (perElementOptions.addClassTo.length===0){
				perElementOptions.addClassTo = $(this);
			}

			setEvents(this, perElementOptions);
		});
	};

	$.fn.fileDrop.defaults = {
		overClass: 'state-over',	//The class that will be added to an element when files are dragged over the window
		addClassTo: null,			//Nothing selected by default, in this case the class is added to the selected element
		onFileRead: null,			//A function to run that will read each file
		removeDataUriScheme: true,	//Removes 'data:;base64,' or similar from the beginning of the Base64 string
		decodeBase64: false			//Decodes the Base64 into the raw file data. NOTE: when this is true, removeDataUriScheme will also be true
	};

	//Extend jQuery to allow for this to be a public function
	$.removeUriScheme = function(str){
		return str.replace(/^data:.*;base64,/,'');
	};

	//Extent jQuery.support to detect the support we need here
	$.support.fileDrop = (function () {
		return !! window.FileList;
	})();
		
})(jQuery);


//Add Base64 decode ability if the browser does not support it already
//NOTE: The below code can be removed if you do not plan on targeting IE9!
(function(window){
	//Via: http://phpjs.org/functions/base64_decode/
	function base64_decode (data) {
		/*jshint bitwise: false, eqeqeq:false*/
		var b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
		var o1, o2, o3, h1, h2, h3, h4, bits, i = 0,
		ac = 0,
		dec = '',
		tmp_arr = [];

		if (!data) {
			return data;
		}

		data += '';

		do { // unpack four hexets into three octets using index points in b64
			h1 = b64.indexOf(data.charAt(i++));
			h2 = b64.indexOf(data.charAt(i++));
			h3 = b64.indexOf(data.charAt(i++));
			h4 = b64.indexOf(data.charAt(i++));

			bits = h1 << 18 | h2 << 12 | h3 << 6 | h4;

			o1 = bits >> 16 & 0xff;
			o2 = bits >> 8 & 0xff;
			o3 = bits & 0xff;

			if (h3 == 64) {
				tmp_arr[ac++] = String.fromCharCode(o1);
			} else if (h4 == 64) {
				tmp_arr[ac++] = String.fromCharCode(o1, o2);
			} else {
				tmp_arr[ac++] = String.fromCharCode(o1, o2, o3);
			}
		} while (i < data.length);

		dec = tmp_arr.join('');

		return dec;
	}

	if(!window.atob){
		window.atob = base64_decode;
	}

})(window);