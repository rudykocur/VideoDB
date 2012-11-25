

var MovieIdentifier = (function() {
	
	var pub = {};
	
	var mask;
	
	var runIdentification = function(url) {
		mask.show();
		
		var docScroll = document.getScroll();
		
		var container = new Element('div', {id: 'movieIdentification'});
		
		$(document.body).grab(container);
		
		container.position({
			position: 'leftTop',
			edge: 'leftTop',
			offset: {x: 0, y: 20}
		});
		
		container;//.grab(new Element('span', {text: 'Trwa identyfikacja'}));
		
		var session = new IdentificationSession(container, mask, url);
		session.startIdentify();
	}
	
	
	pub.attach = function(elements) {
		mask = new Mask();
		
		elements.each(function(el) {
			el.addEvent('click', function(ev) {
				ev.stop();
				
				runIdentification(el.get('href'));
			});
		});
	}
	
	return pub;
	
})();

var IdentificationSession = function(container, mask, url) {
	this.container = container;
	this.originalUrl = url;
	this.mask = mask;
	
	this.identificationStatus = new Element('span', {text: 'Trwa identyfikacja: wyszukiwanie ...'});
	this.container.grab(this.identificationStatus);
	
	this.identifyName = new Element('div', {'class': 'identifyName'});
	this.identifyName.addEvent('click', this.customNameSearchHandler.bind(this));
	this.container.grab(this.identifyName);
	
	var closeElement= new Element('a', {'class': 'closeButton', href: '#', text: 'X'});
	closeElement.addEvent('click', this.cancelSession.bind(this));
	container.grab(closeElement);
	
	this.list = new Element('ul');
	this.container.grab(this.list);
}

IdentificationSession.prototype.cancelSession = function(e, callback) {
	if(e) {
		e.stop();
	}
	
	var _fun = function() {
		this.container.destroy();
		this.mask.hide();
		
		if(callback) {
			callback();
		}
	}.bind(this);
	
	if(this.queueId) {
		new Request({
			url: '/cancelIdentifyQueue/'+this.queueId+'/',
			onSuccess: function() {
				_fun();
			}
		}).send();
	}
	else {
		_fun();
	}
	
	
	
	this.cancelIdentification();
	
}

IdentificationSession.prototype.cancelIdentification = function() {
	if(this.currentIdentifyRequest) {
		//this.currentIdentifyRequest.cancel();
		this.currentIdentifyRequest = null;
	}
}

IdentificationSession.prototype.customNameSearchHandler = function(ev) {
	ev.stop();
	
	var nowaNazwa = prompt('Podaj nową nazwę do identyfikacji', this.lastIdentifiedName || '');
	
	if(!nowaNazwa) {
		return;
	}
	
	this.startIdentify(this.originalUrl + '/?customName='+encodeURIComponent(nowaNazwa));
}

IdentificationSession.prototype.startIdentify = function(url) {
	new Request.JSON({
		url: url || this.originalUrl,
		
		onSuccess: function(data) {
			this.identifyData = data;
			this.processQueue(data.queueId, data.resultCount, data.name);
		}.bind(this)
	}).send();
}

IdentificationSession.prototype.processQueue = function(queueId, totalResults, identifyName) {
	this.queueId = queueId;
	this.totalResults = this.resultsLeft = totalResults;
	
	this.lastIdentifiedName = identifyName;
	
	this.identificationStatus.set('text', 'Trwa identyfikacja: '+this.resultsLeft+' pozostało');
	this.identifyName.set('text', 'Wyszukiwanie: ' + identifyName);
	
	this.list.empty();
	this._pool();
}

IdentificationSession.prototype._renderMovie = function(movie) {
	var number = this.totalResults - this.resultsLeft;
	
	var li = new Element('li');
	
	if(number%3 == 0) {
		li.addClass('break');
	}
	
	var img = new Element('img', {src: movie.cover || '/images/preview_unavailable.png'});
	
	img.addEvent('click', function() {
		var _url = '/associate?imdbId='+movie.id+'&movieId='+this.identifyData.movieId;
		this.cancelSession(false, function() {
			window.location = _url;
		})
		//window.location = '/associate?imdbId='+movie.id+'&movieId='+this.identifyData.movieId;
	}.bind(this));
	
	li.grab(new Element('span', {'class':'title', text: movie.title + ' ('+movie.year+')'}));
	li.grab(new Element('div', {'class':'imgwrap'}).grab(img));
	li.grab(new Element('span', {'class': 'genres', text: movie.genres.join(', ')}));
	
	this.list.grab(li);
}

IdentificationSession.prototype._pool = function() {
	if(this.resultsLeft < 1) {
		//console.log('QUEUE', this.queueId, 'DONE');
		this.identificationStatus.set('text', 'Gotowe - ' + this.totalResults + ' wyników');
		this.currentIdentifyRequest = null;
		return;
	}
	
	this.currentIdentifyRequest = new Request.JSON({
		url: '/poolIdentifyQueue/'+this.queueId+'/',
		
		onSuccess: function(data) {
			//console.log("DATA", data);
			this._renderMovie(data.movie);
			
			if(data.movie) {
				this.resultsLeft--;
				
				this.identificationStatus.set('text', 'Trwa identyfikacja: '+this.resultsLeft+' pozostało');
				
				this._pool();
			}
			else {
				alert('STH WRONG:', data, '::', this.resultsLeft);
			}
		}.bind(this)
	}).send();
}













