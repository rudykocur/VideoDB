



var ViewController = (function() {
	var pub = {};
	
	var viewData = null;
	var views = [];
	var viewsByName = {};
	var currentView = null;
	var target = null;
	var viewContent = null;
	var viewSwitcherContent = null;
	
	
	pub.initalize = function(container, data) {
		target = container;
		viewData = data;
		viewContent = new Element('div');
		viewSwitcherContent = new Element('div', {id: 'viewSwitcher'});
		target.adopt([viewSwitcherContent, viewContent]);
		
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
		currentView = new viewCls(this, viewContent);
		
		currentView.show(viewData);
	}
	
	var updateViewSwitcher = function() {
		viewSwitcherContent.empty();
		
		//var ul = new Element('ul', {'class': 'clearfix'});
		var ul = new Element('ul');
		
		views.each(function(v) {
			var li = new Element('li', {text: v.prototype.title});
			li.addEvent('click', function() {pub.activateView(v.prototype.name)});
			
			ul.grab(li);
		});
		
		viewSwitcherContent.grab(ul);
	}
	
	/*
	 * 
	 */
	
	return pub;
})();


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







