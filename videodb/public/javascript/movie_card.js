

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
	
	pub.attach = function(imdbId) {
		var li = $('imdb-'+imdbId);
		li.getElement('img').addEvent('click', function() {
			console.log('click !!');
			
			mask.show();
			
			container = new Element('div', {id: 'movieCard'});
			$(document.body).grab(container);
			
			container.position({
				position: 'leftTop',
				edge: 'leftTop',
				offset: {x: 0, y: 20}
			});
			
			new Request.HTML({
				url: '/movieCard/'+imdbId,
				update: container,
				
				onSuccess: function() {
					var img = $('movieCard').getElement('img');
					img.addEvent('click', closeCard);
					
					
					var widthDiff = $('movieCard').getWidth() - img.getWidth();
					var maxWidth = $(document.body).getWidth() - widthDiff - 20;
					img.setStyle('max-width', maxWidth);
				}
			}).get();
		})
	}
	
	return pub;
})();