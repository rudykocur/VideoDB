



var ViewController = (function() {
	var pub = {};
	
	var viewData = null;
	var views = [];
	var viewsByName = {};
	var currentView = null;
	var target = null;
	var viewContent = null;
	var viewSwitcherContent = null;
	
	var filterControlls = [];
	
	
	
	
	pub.initalize = function(container, data) {
		target = container;
		viewData = data;
		viewContent = new Element('div');
		viewSwitcherContent = new Element('div', {id: 'viewSwitcher'});
		
		filterControlls.push(new LetterFilterControll(this, viewData));
		
		//target.adopt([viewSwitcherContent, letterFilterContent, viewContent]);
		target.grab(viewSwitcherContent);
		target.adopt(filterControlls.map(function(x){return x.getContent()}));
		target.grab(viewContent);
		
		
		
		updateViewSwitcher();
	}
	
	/*
	 * VIEW MANAGEMENT
	 */
	
	pub.addView = function(viewClass) {
		views.push(viewClass);
		viewsByName[viewClass.prototype.name] = viewClass;
		
		if(viewSwitcherContent) {
			updateViewSwitcher();
		}
	}
	
	pub.activateView = function(viewName) {
		
		if(currentView) {
			currentView.destroy();
		}
		
		viewContent.empty();
		
		var viewCls = viewsByName[viewName];
		
		viewSwitcherContent.getElements('.active').removeClass('active');
		viewSwitcherContent.getElements('li')[views.indexOf(viewCls)].addClass('active');
		
		currentView = new viewCls(this, viewContent);
		currentView.show(viewData);
	}
	
	var updateViewSwitcher = function() {
		viewSwitcherContent.empty();
		
		//var ul = new Element('ul', {'class': 'clearfix'});
		var ul = new Element('ul');
		
		views.each(function(v) {
			var li = new Element('li', {text: v.prototype.title});
			li.addEvent('click', function() {
				
				pub.activateView(v.prototype.name)
			});
			
			ul.grab(li);
		});
		
		viewSwitcherContent.grab(ul);
	}
	
	/*
	 * HANDLING FILTERING
	 */
	
	pub.updateFilters = function() {
		var data = viewData;
		
		filterControlls.each(function(fc) {
			data = fc.filterData(data);
		});
		
		currentView.show(data);
	}
	
	return pub;
})();



var LetterFilterControll = function(mainCtrl, data) {
	this.mainCtrl = mainCtrl;
	
	var letters = [], uniqueLetters = [], i;
	
	var aCC = "A".charCodeAt(0);
	var zCC = "Z".charCodeAt(0);
	
	var hasOther = false;
	
	for(i = 0; i < data.length; i++) {
		var l = data[i].title[0].toUpperCase();
		var cc = l.charCodeAt(0);
		
		if(cc < aCC || cc > zCC) {
			hasOther = true;
			continue;
		}
		
		if(uniqueLetters.indexOf(l)<0) {
			uniqueLetters.push(l);
		}
	}
	
	letters.push([LetterFilterControll.prototype.MODE_SHOW_ALL, 'Wszystkie']);
	letters.append(uniqueLetters.sort().map(function(x) {return [x,x];}));
	if(hasOther) {
		letters.push([LetterFilterControll.prototype.MODE_LETTERS_OTHER, 'Inne']);
	}
	
	this.target = new Element('div', {id: 'letterFilterControll'});
	
	this.target.appendText('Wybierz literę: ');
	
	var ul = this.target.grab(new Element('ul'));
	
	for(i = 0; i < letters.length; i++) {
		var li = ul.grab(new Element('li'));
		
		var link = new Element('a', {href:'#', text: letters[i][1]});
		this.wireLetterEvent(link, letters[i]);
		
		li.grab(link);
	}
	
}

LetterFilterControll.prototype = {
	MODE_SHOW_ALL: 1,
	MODE_LETTERS_OTHER: 2,
	
	getContent: function() {return this.target},
	
	filterData: function(data) {
		if(this.selectedLetter == LetterFilterControll.prototype.MODE_SHOW_ALL) {
			return data;
		}
		
		var filterFunction;
		var aCC = "A".charCodeAt(0);
		var zCC = "Z".charCodeAt(0);
		
		if(this.selectedLetter == LetterFilterControll.prototype.MODE_LETTERS_OTHER) {
			filterFunction = function(item) {
				var l = item.title[0].toUpperCase().charCodeAt(0);
				return (l < aCC || l > zCC);
			}
		}
		else {
			filterFunction = function(item) {
				return item.title[0].toUpperCase() == this.selectedLetter;
			}.bind(this);
		}
		
		return data.filter(filterFunction);
	},
	
	wireLetterEvent: function(link, letter) {
		link.addEvent('click', function(e) {
			e.stop();
			
			this.selectedLetter = letter[0];
			
			this.mainCtrl.updateFilters();
		}.bind(this));
	}
}


var GridView = function(controller, container) {
	this.ctrl = controller;
	this.target = container;
}

GridView.prototype = {
	name: 'grid',
	title: 'Grid view',
	
	show: function(items) {
		this.target.empty();
		
		var ul = new Element('ul', {id: 'gridView'});
		this.target.grab(ul);
		
		items.each(function(item) {
			var li = new Element('li');
			
			li.grab(new Element('span', {'class': 'title', text: item.title+' ('+item.year+')'}));
			
			var imgwrap = new Element('div', {'class': 'imgwrap'});
			imgwrap.grab(new Element('img', {src: item.coverUrl}));
			li.grab(imgwrap);
			
			li.grab(new Element('span', {'class': 'genres', text: item.genres}));
			
			
			ul.grab(li);
		});
	},
	
	destroy: function() {}
}






var ListView = function(controller, container) {
	this.ctrl = controller;
	this.target = container;
}

ListView.prototype = {
	name: 'list',
	title: 'List view',
	
	show: function(items) {
		this.target.empty();
		
		var ul = new Element('ul', {id: 'listView'});
		
		items.each(function(item) {
			var li = new Element('li');
			
			li.grab(this.addImgEvents(new Element('img', {src: item.coverUrl})));
			li.grab(new Element('span', {'class': 'title', text: '('+item.year+') '+item.title}));
			
			ul.grab(li);
			
		}.bind(this));
		
		this.target.grab(ul);
	},

	destroy: function() {},
	
	addImgEvents: function(img) {
		// TODO: fill it
		return img;
	}
}







