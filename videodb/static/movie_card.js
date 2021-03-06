

var MovieCard = (function() {
	var pub = {};
	
	var mask, container;
	
	var closeCard = function() {
		container.destroy();
		container = null;
		
		mask.hide();
	}
	
	pub.initalize = function() {
		mask = new Mask();
	}
	
	pub.openCard = function(url) {
		//var li = $('movie-'+movieId);
		mask.show();
		
		container = new Element('div', {id: 'movieCard'});
		$(document.body).grab(container);
		
		container.position({
			position: 'leftTop',
			edge: 'leftTop',
			offset: {x: 0, y: 20}
		});
		
		new Request.HTML({
			//url: '/movieCard/'+movieId,
			//url: li.getElement('a').href,
			url: url,
			update: container,
			
			onSuccess: function() {
				var img = $('movieCard').getElement('img');
				img.addEvent('click', closeCard);
				
				
				var widthDiff = $('movieCard').getWidth() - img.getWidth();
				var maxWidth = $(document.body).getWidth() - widthDiff - 20;
				img.setStyle('max-width', maxWidth);
			}
		}).get();
	}
	
	pub.attach = function(movieId) {
		var li = $('movie-'+movieId);
		li.getElement('img').addEvent('click', function(e) {
			e.stop();
			
			pub.openCard(li.getElement('a').href);
		})
	}
	
	return pub;
})();