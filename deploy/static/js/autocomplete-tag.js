(function ($) {
	$.tagator = function (source_element, options) {
		var defaults = {
			showAllOptionsOnFocus: false,
			allowAutocompleteOnly: false,
			autocomplete: [],
			filter: false,
			tag_container: '',
		};

		var self = this;
		var selected_index = 0;
		var $source_element = $(source_element);
		var $tagator_element = null;
		var $tags_element = null;
		var $input_element = null;
		var $options_element = null;
		var key = {
			backspace: 8,
			enter:     13,
			escape:    27,
			left:      37,
			up:        38,
			right:     39,
			down:      40,
			comma:     188
		};
		self.settings = {};

		// INITIALIZE PLUGIN
		self.init = function () {
			self.settings = $.extend({}, defaults, options);

			//// ================== CREATE ELEMENTS ================== ////
			// box element
			$tagator_element = $(document.createElement('div'));
			if ($source_element[0].id !== undefined) {
				$tagator_element.attr('id', $source_element[0].id);
			}
			$tagator_element.addClass('tag-autocomplete-element options-hidden');
			$tagator_element.css({
				position: 'relative'
			});
			if (self.settings.height === 'element') {
				$tagator_element.css({
					height: $source_element.outerHeight + 'px'
				});
			}
			$source_element.after($tagator_element);
			$source_element.hide();

			// tags element

			$tags_element = $(document.createElement('ul'));
			$tags_element.addClass('tags-container');
			if(self.settings.filter) $(self.settings.tag_container).append($tags_element);
			else $tagator_element.before($tags_element);
			// input element
			$input_element = $(document.createElement('input'));
			$input_element.addClass('tag-input');
			$input_element.attr('placeholder', $source_element.attr('placeholder'))
			$source_element.attr('placeholder', "")
			$input_element.attr('autocomplete', 'false');
			$tagator_element.append($input_element);
			// options element
			$options_element = $(document.createElement('ul'));
			$options_element.addClass('autocomplete-options');

			$tagator_element.append($options_element);

			//// ================== on ELEMENTS EVENTS ================== ////
			// source element
			$source_element.change(function () {
				refreshTags();
			});
			// box element
			$tagator_element.on('focus', function (e) {
				e.preventDefault();
				e.stopPropagation();
				showOptions();
				$input_element.focus();
			});
			$tagator_element.on('mousedown', function (e) {
				e.preventDefault();
				e.stopPropagation();
				$input_element.focus();
				if ($input_element[0].setSelectionRange) {
					$input_element.focus();
					$input_element[0].setSelectionRange($input_element.val().length, $input_element.val().length);
				} else if ($input_element[0].createTextRange) {
					var range = $input_element[0].createTextRange();
					range.collapse(true);
					range.moveEnd('character', $input_element.val().length);
					range.moveStart('character', $input_element.val().length);
					range.select();
				}
			});
			$tagator_element.on('mouseup', function (e) {
				e.preventDefault();
				e.stopPropagation();
			});
			$tagator_element.on('click', function (e) {
				e.preventDefault();
				e.stopPropagation();
				if (self.settings.showAllOptionsOnFocus) {
					showOptions();
					searchOptions();
				}
				$input_element.focus();
			});
			$tagator_element.on('dblclick', function (e) {
				e.preventDefault();
				e.stopPropagation();
				$input_element.focus();
				$input_element.select();
			});
			// input element
			$input_element.on('click', function (e) {
				e.preventDefault();
				e.stopPropagation();
			});
			 $input_element.on('dblclick', function (e) {
			 	e.preventDefault();
			 	e.stopPropagation();
			 });
			$input_element.on('keydown', function (e) {
				e.stopPropagation();
				var keyCode = e.keyCode || e.which;
				switch (keyCode) {
					case key.up:
						e.preventDefault();
						if (selected_index > 0) {
							selected_index = selected_index - 1;
						} else {
							selected_index = $options_element.find('.autocomplete-option').length - 1;
						}
						refreshActiveOption();
						scrollToActiveOption();
						break;
					case key.down:
						e.preventDefault();
						if (selected_index < $options_element.find('.autocomplete-option').length - 1) {
							selected_index = selected_index + 1;
//							console.log('ㅋㅋ', selected_index)
						} else {
							selected_index = 0;
//                            console.log('머임', selected_index, $options_element.find('.autocomplete-option').length - 1)
						}
						refreshActiveOption();
						scrollToActiveOption();
						break;
					case key.escape:
						e.preventDefault();
						break;
					case key.comma:
						e.preventDefault();
						if (selected_index === -1) {
							if ($input_element.val() !== '') {
								addTag($input_element.val());
							}
						}
						break;
					case key.enter:
						e.preventDefault();
						if (selected_index !== -1) {
							selectOption();
						} else {
							if ($input_element.val() !== '') {
								addTag($input_element.val());
							}
						}
						break;
					default:
						break;
				}
			});
			$input_element.on('keyup', function (e) {
				e.preventDefault();
				e.stopPropagation();
				var keyCode = e.keyCode || e.which;
				if (keyCode === key.escape || keyCode === key.enter) {
					hideOptions();
				} else if (keyCode < 37 || keyCode > 40) {
					searchOptions();
				}
				if ($tagator_element.hasClass('options-hidden') && (keyCode === key.left || keyCode === key.right || keyCode === key.up || keyCode === key.down)) {
					searchOptions();
				}
			});
			$input_element.on('focus', function (e) {
				e.preventDefault();
				e.stopPropagation();
				if (!$options_element.is(':empty') || self.settings.showAllOptionsOnFocus) {
					searchOptions();
					showOptions();
				}
			});
			$input_element.on('blur', function (e) {
				e.preventDefault();
				e.stopPropagation();
				hideOptions();
			});
			refreshTags();
		};


		self.autocomplete = function (autocomplete) {
			self.settings.autocomplete = autocomplete !== undefined ? autocomplete : [];
		};


		self.refresh = function () {
			refreshTags();
		};
		var refreshTags = function () {
			$tags_element.empty();
			var tags = $source_element.val().split(',');
			$.each(tags, function (key, value) {
				if (value !== '' && checkAllowedTag(value)) {
					var $tag_element = $(document.createElement('li'));
					$tag_element.addClass('tag-item');
					$tag_element.html(value);
					// remove button
					var $button_remove_element = $(document.createElement('a'));
					$button_remove_element.data('text', value);
					$button_remove_element.addClass('tag-item-remove');
					$button_remove_element.on('mousedown', function (e) {
						e.preventDefault();
						e.stopPropagation();
					});
					$button_remove_element.on('mouseup', function (e) {
						e.preventDefault();
						e.stopPropagation();
						removeTag($(this).data('text'));
						$source_element.trigger('change');
                        if(self.settings.filter) $('.filter-tags').trigger('change');
					});
					$button_remove_element.html('X');
					$tag_element.append($button_remove_element);
					$tags_element.append($tag_element);
				}
			});
			searchOptions();
		};

		// REMOVE TAG FROM ORIGINAL ELEMENT
		var removeTag = function (text) {
			var tagsBefore = $source_element.val().split(',');
			var tagsAfter = [];
			$.each(tagsBefore, function (key, value) {
				if (value !== text && value !== '') {
					tagsAfter.push(value);
				}
			});
			$source_element.val(tagsAfter.join(','));
		};

		// CHECK IF TAG IS PRESENT
		var hasTag = function (text) {
			var tags = $source_element.val().split(',');
			var hasTag = false;
			$.each(tags, function (key, value) {
				if ($.trim(value.toLowerCase()) === $.trim(text.toLowerCase())) {
					hasTag = true;
				}
			});
			return hasTag;
		};

		// CHECK IF TAG IS ALLOWED
		var checkAllowedTag = function (text) {
			if (!self.settings.allowAutocompleteOnly) {
				return true;
			}

			var checkAllowedTag = false;
			$.each(self.settings.autocomplete, function (key, value) {
				if ($.trim(value) === $.trim(text)) {
					checkAllowedTag = true;
				}
			});
			return checkAllowedTag;
		};

		// ADD TAG TO ORIGINAL ELEMENT
		var addTag = function (text, tag=false) {
		    if(tag) text = $(text).text();
		    text = $.trim(text);
		    text = text.replace(/\s\s+/g, ' ');
			if (!hasTag(text) && checkAllowedTag(text)) {
				var isExist = false;
				$.each(self.settings.autocomplete, function (key, value) {
					if ($.trim(value.toLowerCase()) == text.toLowerCase()) isExist = true;
				});
				if(!isExist) {
				    self.settings.autocomplete.push(text);
				    self.settings.autocomplete.sort();
				}
				$source_element.val($source_element.val() + ($source_element.val() !== '' ? ',' : '') + text);
				$source_element.trigger('change');
				if(self.settings.filter) $tags_element.parent().trigger('change');
			}
//			console.log(selected_index, text);
            selected_index = 0;
			$input_element.val('');
			$tagator_element.focus();
			hideOptions();
		};

		// OPTIONS SEARCH METHOD
		var searchOptions = function () {
			$options_element.empty();
			input = $.trim($input_element.val());
			input = input.replace(/\s\s+/g, ' ');
			if (input.replace(/\s/g, '') !== '') {
				var optionsArray = [];
				var isSame = false;
				var cnt = 1;
				$.each(self.settings.autocomplete, function (key, value) {
					if (value.toLowerCase().startsWith(input.toLowerCase())) {
						if (value.toLowerCase() === input.toLowerCase()) {
							isSame = true;
						}
						if (!hasTag(value)) {
							cnt += 1;
							optionsArray.push("<strong>"+value+"</strong>");
						}
					}
				});
				if(!isSame && !self.settings.filter) {
					optionsArray.push("<strong>" + input +"</strong> 추가하기");
				}
				generateOptions(optionsArray);
			}
			if ($input_element.is(':focus')) {
				if (!$options_element.is(':empty')) {
					showOptions();
				} else {
					hideOptions();
				}
			} else {
				hideOptions();
			}
		};

		// GENERATE OPTIONS
		var generateOptions = function (optionsArray) {
			var index = -1;
			$(optionsArray).each(function (key, value) {
				index++;
				var option = createOption(value, index);
				$options_element.append(option);
			});
			refreshActiveOption();
		};

		// CREATE RESULT OPTION
		var createOption = function (text, index) {
			// holder li
			var option = document.createElement('li');
			$(option).data('index', index);
			$(option).data('text', text);
			$(option).html(text);
			$(option).addClass('autocomplete-option');
			if (this.selected) {
				$(option).addClass('active');
			}

			// on EVENTS
			$(option).on('mouseover', function (e) {
				e.stopPropagation();
				e.preventDefault();
				selected_index = index;
				refreshActiveOption();
			});
			$(option).on('mousedown', function (e) {
				e.stopPropagation();
				e.preventDefault();
			});
			$(option).on('click', function (e) {
				e.preventDefault();
				e.stopPropagation();
				selectOption();
			});


			return option;
		};

		// SHOW OPTIONS
		var showOptions = function () {
//		    console.log("showOptions", selected_index);
			$tagator_element.removeClass('options-hidden').addClass('options-visible');
			$options_element.css('top', ($tagator_element.outerHeight - 2) + 'px');
            scrollToActiveOption();
		};

		// HIDE OPTIONS
		var hideOptions = function () {
			$tagator_element.removeClass('options-visible').addClass('options-hidden');
		};

		// REFRESH ACTIVE IN OPTIONS METHOD
		var refreshActiveOption = function () {
			$options_element.find('.active').removeClass('active');
			if (selected_index !== -1) {
				$options_element.find('.autocomplete-option').eq(selected_index).addClass('active');
			}
		};

		// SCROLL TO ACTIVE OPTION IN OPTIONS LIST
		var scrollToActiveOption = function () {
			var $active_element = $options_element.find('.autocomplete-option.active');
			if ($active_element.length > 0) {
				$options_element.scrollTop($options_element.scrollTop() + $active_element.position().top - $options_element.height() / 2 + $active_element.height() / 2);
			}

		};

		// SELECT ACTIVE OPTION
		var selectOption = function () {
//		    console.log('selectOption', selected_index)
			addTag($options_element.find('.autocomplete-option').eq(selected_index).data('text'), true);
		};


		// REMOVE PLUGIN AND REVERT INPUT ELEMENT TO ORIGINAL STATE
		self.destroy = function () {
			$tagator_element.remove();
			$source_element.removeData('tagator');
			$source_element.show();
		};
		// Initialize plugin
		self.init();
	};

	$.fn.tagator = function () {
		var parameters = arguments[0] !== undefined ? arguments : [{}];
	    return jQuery.each(this, function () {
			if (typeof(parameters[0]) === 'object') {
				if (undefined === $(this).data('tagator')) {
					var plugin = new $.tagator(this, parameters[0]);
					$(this).data('tagator', plugin);
				}
			}
			else if ($(this).data('tagator')[parameters[0]]) {
				$(this).data('tagator')[parameters[0]].apply(this, Array.prototype.slice.call(parameters, 1));
			}
			else {
				$.error('Method ' + parameters[0] + ' does not exist in $.tagator');
			}
		});
	};
}(jQuery));


(function($) {
	$('.tagator').each(function () {
		var $this = $(this);
		var options = {};
		$.each($this.data(), function (key, value) {
			if (key.substring(0, 7) === 'tagator') {
				var value_temp = value.toString().replace(/'/g, '"');
				if (typeof value_temp == 'object') {
					value = value_temp;
				}
				options[key.substring(7, 8).toLowerCase() + key.substring(8)] = value;
			}
		});
		$this.tagator(options);
	});
})(jQuery);