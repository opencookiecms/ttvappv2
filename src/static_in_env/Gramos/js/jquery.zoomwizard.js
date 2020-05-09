(function($){
	function imagesLoaded(srcs, fn, options) {
	   var imgs = [], img;
	   var remaining = srcs.length;
	   for (var i = 0; i < srcs.length; i++) {
	       img = new Image();
	       imgs.push(img);
	       img.onload = function() {
	           --remaining;
	           if (remaining == 0) {
	               fn(options);
	           }
	       };
	       img.src = srcs[i];
	   }
	   return(imgs);
	}
	
	var wrapId = 0, zoomLevel;
	var temp, smallImage = new Image(),largeImage = new Image(),offsetLeft,offsetTop,windowWidth,thumbWidth,thumbHeight,windowHeight,wind,largeImg,ratioX,ratioY,wrap,thumb,distanceLeft,distanceTop,marginLeft,marginTop,dragMode=false,
		dragSlider=false,startedDragging=false,dragTarget,eventX,eventY,initLeft,initTop,initSliderTop,targetSlider,targetSlidebar,targetImg,windowMove = false,activeWindowWrap;
		
	var methods = {
		init : function(options) {
			if (options.settings.mode == 'window') {
				methods.setupHTML				({ el : options.target, settings : options.settings });
				methods.setupStyles				({ el : options.target, settings : options.settings });
				methods.setupEvents				({ settings : options.settings });
			} else if (options.settings.mode == 'inner') {
				methods.setupHTMLInner			({ el : options.target, settings : options.settings });;
				methods.setupStylesInner		({ settings : options.settings });
				methods.setupEventsInner		({ settings : options.settings });
			} else if (options.settings.mode == 'controls') {
				methods.setupHTMLControls		({ el : options.target, settings : options.settings });
				methods.setupStylesControls		({ settings : options.settings });
				methods.setupEventsControls		({ settings : options.settings });
			}
		},

		// "window" functionality
		setupHTML : function(options) {
			var el = options.el;
			var settings = options.settings;
			var next = el.next();
			if (next.hasClass('zoomwizard-large')) {
				var largeImg = '<img class="zoomwizard zoomwizard-large" src="'+next.attr('src')+'" alt="'+next.attr('alt')+'">';
			} else {
				var largeImg = '<img class="zoomwizard zoomwizard-large" src="'+el.attr('src')+'" alt="'+el.attr('alt')+'">';
			}

			var html = '<div class="zoomwizard-wrap zoomwizard-node zoomwizard-wrap-window" id="zoomwizard-wrap-'+wrapId+'">';
			html 	+= '	<div class="zoomwizard-active-area"></div>';
			html 	+= '		<img class="zoomwizard zoomwizard-thumb" src="'+el.attr('src')+'" alt="'+el.attr('alt')+'">';
			html 	+= '		<div class="zoomwizard-window zoomwizard-windowstyle-'+settings.windowstyle+'">';

			if (settings.windowstyle == 3) {
				html += '			<div class="zoomwizard-window-inner"></div>';
			}

			html 	+= 				largeImg;
			html 	+= '		</div>';
			html 	+= '</div>';

			var parent = el.parent();

			el.before(html).remove();
			wrap = $('#zoomwizard-wrap-'+wrapId);
			next.remove();
			wrapId++;
			wrap.data({
				zoom : settings.zoom,
				margin : settings.margin
			});
		},
		setupStyles : function(options) {
			var settings = options.settings;
			var wrapper = wrap;
			var defaultWidth = wrapper.find('img').first().width();
			var defaultHeight = wrapper.find('img').first().height();
			wind = wrapper.find('.zoomwizard-window');
			largeImg = wind.find('img');

			wrapper.find('.zoomwizard-active-area').css({ "width" : defaultWidth, "height" : defaultHeight });
			wrapper	.css({ 	width: defaultWidth, height: defaultHeight });
			wind	.css({ 	width: settings.width, 
							height: settings.height, 
							left: -settings.width/2, 
							top: -settings.height/2,
							"border-radius": settings.radius,
							border: settings.border });

			largeImg.css({ 
							width: defaultWidth * settings.zoom,
							height: defaultHeight * settings.zoom });
			wrapper.find('img').css({ 
										"margin": 0,
										"float": 'none' });

			if (settings.hidecursor) {
				wrapper.find('.zoomwizard-window').css({ "cursor" : 'none' });
				wrapper.find('.zoomwizard-active-area').css({ "cursor" : 'none' });
			}
		},
		setupEvents : function(options) {
			var settings = options.settings;
		
			$('.zoomwizard-wrap-window').unbind('.zoomwizard');
			$(document).unbind('.zoomwizard');
			
			$('.zoomwizard-wrap-window').on('mouseover.zoomwizard', function() {
				zoomLevel = $(this).data('zoom');
				wrap.data({ "windowmove" : true });
				windowMove = true;
				activeWindowWrap = $(this);
				wind = activeWindowWrap.find('.zoomwizard-window');
				windowWidth = settings.width;
				windowHeight = settings.height;
			});
			$(document).on('mousemove.zoomwizard', function(e) {
				if (windowMove) {
					if (!activeWindowWrap.hasClass('init')) {
						methods.initHoverState({ wrapper : activeWindowWrap, settings : settings });
					}
					wind.css({ left: e.pageX - offsetLeft - windowWidth/2,
			 			top: e.pageY - offsetTop - windowHeight/2,
						display: 'block'
					});
					largeImg.css({ 
						left: -((e.pageX - offsetLeft) * zoomLevel -windowWidth/2),
						top: -((e.pageY - offsetTop) * zoomLevel -windowHeight/2)
			 		});
				}
				if (windowMove && !methods.isWithinArea({ ev : e, area : activeWindowWrap })) {
					activeWindowWrap.removeClass('init');
					windowMove = false;
					activeWindowWrap.find('.zoomwizard-window').hide();
				}
			});
		},
		initHoverState : function(options) {
			var wrapper = options.wrapper;
			var settings = options.settings;
			wrapper.addClass('init');
			thumb = wrapper.find('.zoomwizard-thumb');
			largeImg = wrapper.find('.zoomwizard-large');
			thumbWidth = thumb.width();
			thumbHeight = thumb.height();

			largeImg.css({ "width" : thumbWidth*zoomLevel, "height" : thumbHeight*zoomLevel }).show();

			offsetLeft = thumb.offset().left;
			offsetTop = thumb.offset().top;
		},

		// "controls" functionality
		setupHTMLControls : function(options) {
			var el = options.el;
			var settings = options.settings;
			el.parent().find('.zoomwizard-large').remove();
			var html = '<div class="zoomwizard-wrap zoomwizard-wrap-controls" id="zoomwizard-wrap-'+wrapId+'">';
			html 	+= '	<div class="zoomwizard-controls-wrap zoomwizard-style-'+settings.controlstyle+'">';
			if (settings.slider == true) {
				html 	+= '		<div class="zoomwizard-controls-block zoomwizard-controls-block-slider">';
				html	+= '			<div class="zoomwizard-slidebar">';
				html	+= '				<div class="zoomwizard-slidebar-skin"></div>';
				html	+= '				<div class="zoomwizard-slider"></div>';
				html 	+= '			</div>';
				html	+= '		</div>';
			}
			if (settings.movegizmo == true) {
				html	+= '		<div class="zoomwizard-controls-block">';
				html 	+= '			<div class="zoomwizard-moveup zoomwizard-button"></div>';
				html 	+= '			<div class="zoomwizard-movedown zoomwizard-button"></div>';
				html 	+= '			<div class="zoomwizard-moveleft zoomwizard-button"></div>';
				html 	+= '			<div class="zoomwizard-moveright zoomwizard-button"></div>';
				html 	+= '		</div>';
			}
			if (settings.zoombuttons == true) {
				html 	+= '		<div class="zoomwizard-controls-block zoomwizard-controls-block-zoom">';
				html	+= '			<div class="zoomwizard-plus zoomwizard-button"></div>';
				html	+= '			<div class="zoomwizard-minus zoomwizard-button"></div>';
				html 	+= '		</div>';			
			}

			html 	+= '	</div>';			
			html 	+= '	<img class="'+el.attr('class')+' zoomwizard-img" src="'+el.attr('src')+'" alt="'+el.attr('alt')+'">';
			html 	+= '</div>';

			el.before(html).remove();
			wrap = $('#zoomwizard-wrap-'+wrapId);
			wrapId++;
		},	
		setupStylesControls : function(options) {
			var settings = options.settings;
			var wrapper = wrap;
			var img = wrapper.find('.zoomwizard-img');

			wrapper.css({ "overflow" : 'hidden', "width" : img.width(), "height" : img.height() });
			img.css({ 
				position: 'absolute',
				"z-index": 9998,
				left: 0,
				top: 0,
				cursor: 'move'
			});
			if (settings.autohide) {
				wrapper.find('.zoomwizard-controls-wrap').hide();
			}

			wrapper.find('.zoomwizard-button');
			wrapper.find('.zoomwizard-slider').css({
				"top" : wrapper.find('.zoomwizard-slidebar').height()
			});
		},
		setupEventsControls : function(options) {
			var settings = options.settings;
			// unbind old events
			$('.zoomwizard-wrap-controls').unbind('.zoomwizard');
			
			// setup data
			$('.zoomwizard-wrap-controls').find('img').each(function() {
				targetSlidebar = $(this).closest('.zoomwizard-wrap').find('.zoomwizard-slidebar');
				$(this).data({ 
					'zoom' : 1,
					'width' : $(this).width(),
					'height' : $(this).height(),
					'factor-left' : 1,
					'factor-top' : 1,
					'zoomfactor' : targetSlidebar.height()/(settings.zoom-1),
					'offset-left' : 0,
					'offset-top' : 0 });
			});
			// setup events
			$('.zoomwizard-wrap-controls').mousewheel(function(e, delta) {
				var img = $(this).find('img');
				img.data({ 'zoom' : methods.lim.call(this, { val : img.data('zoom')+delta*0.1, min : 1, max : parseInt(settings.zoom)}) });
				methods.zoomImg({ target : img, settings : settings });
				methods.updateSliderPosition({ img : img, animated : settings.animated });
				return false;
			});
			$('.zoomwizard-wrap-controls').on('mousedown.zoomwizard', function(e) {
				dragTarget = $(this).find('img');
				if (dragTarget.data('zoom') != 1) {
					dragMode = true;
					eventX = e.pageX;
					eventY = e.pageY;
					initLeft = dragTarget.position().left;
					initTop = dragTarget.position().top;
					windowWidth = dragTarget.closest('.zoomwizard-wrap').width();
					windowHeight = dragTarget.closest('.zoomwizard-wrap').height();
				}
					return false;
			});
			$('.zoomwizard-wrap-controls').on('mousemove.zoomwizard', function(e) {
				$(this).find('.zoomwizard-controls-wrap').fadeIn(200);

				if (dragMode && !dragSlider) {
					offsetLeft = methods.lim.call(this, { val : initLeft + (e.pageX - eventX), min : -dragTarget.width() + windowWidth, max : 0});
					offsetTop = methods.lim.call(this, { val : initTop + (e.pageY - eventY), min : -dragTarget.height() + windowHeight, max : 0});
					dragTarget.css({
						"left" : offsetLeft,
						"top" : offsetTop
					});
					dragTarget.data({ "factor-left" : (2*(-offsetLeft))/(dragTarget.width()-dragTarget.data('width')) });
					dragTarget.data({ "factor-top" : (2*(-offsetTop))/(dragTarget.height()-dragTarget.data('height')) });
				}

				if (dragSlider) {
					startedDragging = true;
					targetSlider.css({
						top: methods.lim.call(this, { val : initSliderTop + (e.pageY - eventY), min : 0, max : targetSlidebar.height()})
					});
					targetImg.data({ 'zoom' : 1 + (((targetSlidebar.height()-targetSlider.position().top)) / (targetImg.data('zoomfactor'))) });
					methods.zoomImg({ target : targetImg, settings : settings });
				}

				return false;
			});
			$('.zoomwizard-wrap-controls').on('mouseup.zoomwizard', function(e) {
				dragMode = false;
				dragSlider = false;
				startedDragging = false;
			});

			if (settings.autohide) {
				$('.zoomwizard-wrap-controls').on('mouseout.zoomwizard', function(e) {
					if (!methods.isWithinArea.call(this, { ev : e, area : $('.zoomwizard-wrap') })) {
						$(this).find('.zoomwizard-controls-wrap').fadeOut(200);
					}
				});
			}
			$(document).on('mouseup.zoomwizard', function() {
				dragSlider = false;
				dragMode = false;
			})

			if (settings.movegizmo == true) {
				wrap.find('.zoomwizard-button').on('click.zoomwizard', function() {

					var target = $(this).closest('.zoomwizard-wrap').find('img');
					if ($(this).hasClass('zoomwizard-moveup')) {
						methods.moveImg.call(this, { target: target, directionLeft : 0, directionTop : 1, settings : settings });
					} else if ($(this).hasClass('zoomwizard-movedown')) {
						methods.moveImg.call(this, { target: target, directionLeft : 0, directionTop : -1, settings : settings });
					} else if ($(this).hasClass('zoomwizard-moveleft')) {
						methods.moveImg.call(this, { target: target, directionLeft : 1, directionTop : 0, settings : settings });
					} else if ($(this).hasClass('zoomwizard-moveright')) {
						methods.moveImg.call(this, { target: target, directionLeft : -1, directionTop : 0, settings : settings });
					}
				});
			}

			if (settings.zoombuttons == true) {
				wrap.find('.zoomwizard-button').on('click.zoomwizard', function() {
					var target = $(this).closest('.zoomwizard-wrap').find('img');
					if ($(this).hasClass('zoomwizard-plus')) {
						target.data({ 'zoom' : target.data('zoom')*1.33 });

						if (target.data('zoom')*1.33 < settings.zoom) {
							target.data({ 'zoom' : target.data('zoom')*1.33 });					
							methods.zoomImg({ target : target, settings : settings });					
						} else {
							target.data({ 'zoom' : settings.zoom });					
							methods.zoomImg({ target : target, settings : settings });
						}
					} else if ($(this).hasClass('zoomwizard-minus')) {
						target.data({ 'zoom' : target.data('zoom')*0.66 });

						if (target.data('zoom')*0.66 > 1) {
							target.data({ 'zoom' : target.data('zoom')*0.66 });					
							methods.zoomImg({ target : target, settings : settings });					
						} else {
							target.data({ 'zoom' : 1 });
							methods.zoomImg({ target : target, settings : settings });
						}
					}
					methods.updateSliderPosition.call(this, { img : $(this).closest('.zoomwizard-wrap').find('img').first(), animated : settings.animated});
				});
			}

			if (settings.slider == true) {
				wrap.find('.zoomwizard-slidebar').on('mousedown.zoomwizard', function(e) {
					dragSlider = true;
					eventY = e.pageY;
					targetSlider = $(this).find('.zoomwizard-slider');
					targetImg = $(this).closest('.zoomwizard-wrap').find('img');
					// initSliderTop = targetSlider.position().top;
					targetSlider.css({ "top" : eventY - targetSlider.parent().offset().top - targetSlider.height()/2 });

					if (dragSlider) {
						targetImg.data({ 'zoom' : 1 + (((targetSlidebar.height()-targetSlider.position().top)+5) / (targetImg.data('zoomfactor'))) });
						methods.zoomImg({ target: targetImg, settings : settings });
					}

					initSliderTop = targetSlider.position().top;
					return false;
				});
				wrap.find('.zoomwizard-slider').on('mousedown.zoomwizard', function(e) {
					dragSlider = true;
					eventY = e.pageY;
					targetSlider = $(this);
					targetImg = $(this).closest('.zoomwizard-wrap').find('img');
					initSliderTop = targetSlider.position().top;
					return false;
				});
				wrap.find('.zoomwizard-slider').on('mouseup.zoomwizard', function(e) {
					dragSlider = false;
					dragMode = false;
				});
			}
		},
		updateSliderPosition : function(options) {
			var img = options.img, animated = options.animated;
			var slider = img.siblings('.zoomwizard-controls-wrap').find('.zoomwizard-slider');
			if (animated) {
				slider.stop().animate({ "top" : (slider.parent().height())+img.data('zoomfactor')*(1-img.data('zoom')) }, 200);
			} else {
				slider.css({ "top" : (slider.parent().height())+img.data('zoomfactor')*(1-img.data('zoom')) });
			}
		},

		// "inner scale" functionality
		setupHTMLInner : function(options) {
			var el = options.el;
			var next = el.next();
			if (next.hasClass('zoomwizard-large')) {
				var html = '<div class="zoomwizard-inner-wrap" id="zoomwizard-wrap-'+wrapId+'">';
				html 	+= '	<div class="zoomwizard-inner-active-area"></div>';
				html 	+= '	<img class="'+el.attr('class')+' zoomwizard-thumb" src="'+el.attr('src')+'" alt="'+el.attr('alt')+'">';
				html 	+= '	<img class="'+next.attr('class')+' zoomwizard-large" src="'+next.attr('src')+'" alt="'+next.attr('alt')+'">';
				html 	+= '</div>';

			} else {
				var largeImg = '<img class="'+el.attr('class')+' zoomwizard-large" src="'+el.attr('src')+'" alt="'+el.attr('alt')+'">';
				var html = '<div class="zoomwizard-inner-wrap" id="zoomwizard-wrap-'+wrapId+'">';
				html 	+= '	<div class="zoomwizard-inner-active-area"></div>';
				html 	+= '	<img class="'+el.attr('class')+' zoomwizard-thumb zoomwizard-large" src="'+el.attr('src')+'" alt="'+el.attr('alt')+'">';
				html 	+= '</div>';
			}

			el.before(html).remove();
			next.remove();
			wrap = $('#zoomwizard-wrap-'+wrapId);
			wrapId++;
		},
		setupStylesInner : function(options) {
			var settings = options.settings;
			var wrapper = wrap;
			thumb = wrapper.find('.zoomwizard-thumb');
			wrapper.css	({ 	overflow: 'hidden', 
							position: 'relative', 
							width: thumb.width(), 
							height: thumb.height(),
							background: 'red'
						});
			thumb.css({ "position" : 'absolute', "left" : 0, "top" : 0 });
			thumb.prev().css({ 	width: thumb.width() - settings.margin*2,
			 					height: thumb.height() - settings.margin*2,
								position: 'absolute',
								"z-index": 9999,
								left: settings.margin,
								top: settings.margin
							});
			wrapper.find('.zoomwizard-large').css({
				position: 'absolute',
				"z-index": 9998,
				left: 0,
				top: 0
			});
		},
		setupEventsInner : function(options) {
			var settings = options.settings;
			
			$('.zoomwizard-inner-wrap').unbind('.zoomwizard');
			
			$('.zoomwizard-inner-wrap').on('mousemove.zoomwizard', function(e) {
				var wrapper = $(this);
				if (!wrapper.hasClass('init')) {
					methods.initHoverStateInner({ wrapper : wrapper, settings : settings });
				}

				if (settings.margin == 0) {
					largeImg.css	({ 
									left: -((e.pageX - offsetLeft) * factorX),
									top: -((e.pageY - offsetTop) * factorY)
						 		});
				} else {
					distanceLeft = e.pageX - offsetLeft - settings.margin;
					distanceLeft = (distanceLeft < 0) ? 0 : distanceLeft;
					distanceTop = e.pageY - offsetTop - settings.margin;
					distanceTop = (distanceTop < 0) ? 0 : distanceTop;

					marginLeft = -distanceLeft * factorX;
					marginLeft = (-marginLeft > thumbWidth*settings.zoom - thumbWidth) ? -(thumbWidth*settings.zoom - thumbWidth) : marginLeft;
					marginTop = -distanceTop * factorY;
					marginTop = (-marginTop > thumbHeight*settings.zoom - thumbHeight) ? -(thumbHeight*settings.zoom - thumbHeight) : marginTop;

					largeImg.css	({ 
									left: marginLeft,
									top: marginTop
						 		});
				}
			});
			$('.zoomwizard-inner-wrap').on('mouseout.zoomwizard', function(e) {
				$(this).removeClass('init');
				thumb.css	({ 
								left: 0,
								top: 0,
								width: thumbWidth,
								height: thumbHeight
					 		});
				// for IE8
				largeImg.hide();
			});
		},
		initHoverStateInner : function(options) {
			var wrapper = options.wrapper;
			var settings = options.settings;
			
			wrapper.addClass('init');
			thumb = wrapper.find('.zoomwizard-thumb');
			largeImg = wrapper.find('.zoomwizard-large');
			thumbWidth = thumb.width();
			thumbHeight = thumb.height();

			largeImg.css({ "width" : thumbWidth*settings.zoom, "height" : thumbHeight*settings.zoom }).show();

			if (settings.margin == 0) {
				offsetLeft = thumb.offset().left + settings.margin;
				offsetTop = thumb.offset().top + settings.margin;

				factorX = (3*(thumbWidth*settings.zoom - thumbWidth))/(thumbWidth*settings.zoom);
				factorY = (3*(thumbHeight*settings.zoom - thumbHeight))/(thumbHeight*settings.zoom);
			} else {
				offsetLeft = thumb.offset().left;
				offsetTop = thumb.offset().top;
				factorX = (settings.zoom - 1)*(thumbWidth/(thumbWidth - settings.margin*2));
				factorY = (settings.zoom - 1)*(thumbHeight/(thumbHeight - settings.margin*2));
			}
		},

		// utility
		zoomImg : function(options) {
			var settings = options.settings;
			var target = options.target;
			offsetLeft = -(target.data('width')*target.data('zoom') - target.data('width'))/2;
			offsetLeft = offsetLeft * target.data('factor-left');
			offsetTop = -(target.data('height')*target.data('zoom') - target.data('height'))/2;
			offsetTop = offsetTop * target.data('factor-top');

			if (settings.animated && !startedDragging) {
				target.stop().animate({ 
					"width" : target.data('width')*target.data('zoom'),
					"height" : target.data('height')*target.data('zoom'),
					"left" : offsetLeft,
					"top" : offsetTop
				}, 200);
			} else {
				target.css({ 
					"width" : target.data('width')*target.data('zoom'),
					"height" : target.data('height')*target.data('zoom'),
					"left" : offsetLeft,
					"top" : offsetTop
				});
			}

			if (target.data('zoom') == 1) {
				target.data({ 'factor-left': 1 });
				target.data({ 'factor-top' : 1 });
			}
		},
		moveImg : function(options) {
			var target = options.target, directionLeft = options.directionLeft, directionTop = options.directionTop, settings = options.settings;
			if (target.data('zoom') > 1 && directionLeft != 0) {
				offsetLeft = target.position().left + ((target.data('width')/6) * directionLeft);
				offsetLeft = (offsetLeft > 0) ? 0 : offsetLeft;
				offsetLeft = (offsetLeft < target.closest('.zoomwizard-wrap').width() - target.width()) ? target.closest('.zoomwizard-wrap').width() - target.width() : offsetLeft;
			} else if (target.data('zoom') > 1 && directionTop != 0) {
				offsetTop = target.position().top + ((target.data('height')/6) * directionTop);
				offsetTop = (offsetTop > 0) ? 0 : offsetTop;
				offsetTop = (offsetTop < target.closest('.zoomwizard-wrap').height() - target.height()) ? target.closest('.zoomwizard-wrap').height() - target.height() : offsetTop;
			}

			if (target.data('zoom') > 1) {
				target.data({ "offset-left" : offsetLeft, "offset-top" : offsetTop })
				target.data({ "factor-left" : (2*(-offsetLeft))/(target.width()-target.data('width')) });
				target.data({ "factor-top" : (2*(-offsetTop))/(target.height()-target.data('height')) });


				if (settings.animated) {
					target.animate({ "left" : offsetLeft, "top" : offsetTop }, 200);
				} else {
					target.css({ "left" : offsetLeft, "top" : offsetTop });
				}
			}
		},
		lim : function(options) {
			if (options.val < options.min) {
				options.val = options.min;
			} else if (options.val > options.max) {
				options.val = options.max;
			}

			return options.val;
		},
		isWithinArea : function(options) {
			if (options.ev.pageX < options.area.offset().left + options.area.width() && 
				options.ev.pageX > options.area.offset().left &&
				options.ev.pageY < options.area.offset().top + options.area.height() && 
				options.ev.pageY > options.area.offset().top) {
					return true;
				} else { return false; }
		}
	};
 	$.fn.extend({
 		zoomwizard: function(options) {
			var settings = $.extend( {
				mode: 'window',
				movegizmo: true,
				slider: true,
				zoombuttons: true,
				animated: false,
				// zoom: 4,
		        width: 250,
				height: 250,
				zoom: 4,
				margin: 20,
				autohide: false,
				hidecursor: true,
				controlstyle: 1,
				windowstyle: 2
			}, options);
			
			
			
    		return this.each(function() {
				$('.zoomwizard-large').hide();
				if ($(this).next().hasClass('zoomwizard-large')) {
					imagesLoaded([$(this).attr('src'), $(this).next().attr('src')], methods.init, { target : $(this), settings : settings });	
				} else {
					imagesLoaded([$(this).attr('src')], methods.init, { target : $(this), settings : settings });	
				}
    		});
			
			
    	}
	});
	
	
	// Free plugin for the 'mousewheel' event listener
	// Licensed under MIT

	(function(d){function e(a){var b=a||window.event,c=[].slice.call(arguments,1),f=0,e=0,g=0,a=d.event.fix(b);a.type="mousewheel";b.wheelDelta&&(f=b.wheelDelta/120);b.detail&&(f=-b.detail/3);g=f;void 0!==b.axis&&b.axis===b.HORIZONTAL_AXIS&&(g=0,e=-1*f);void 0!==b.wheelDeltaY&&(g=b.wheelDeltaY/120);void 0!==b.wheelDeltaX&&(e=-1*b.wheelDeltaX/120);c.unshift(a,f,e,g);return(d.event.dispatch||d.event.handle).apply(this,c)}var c=["DOMMouseScroll","mousewheel"];if(d.event.fixHooks)for(var h=c.length;h;)d.event.fixHooks[c[--h]]=
	d.event.mouseHooks;d.event.special.mousewheel={setup:function(){if(this.addEventListener)for(var a=c.length;a;)this.addEventListener(c[--a],e,!1);else this.onmousewheel=e},teardown:function(){if(this.removeEventListener)for(var a=c.length;a;)this.removeEventListener(c[--a],e,!1);else this.onmousewheel=null}};d.fn.extend({mousewheel:function(a){return a?this.bind("mousewheel",a):this.trigger("mousewheel")},unmousewheel:function(a){return this.unbind("mousewheel",a)}})})(jQuery);
	
})(jQuery);




