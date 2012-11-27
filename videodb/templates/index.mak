<%inherit file="local:templates.master"/>

<%def name="title()">
  VideoDB
</%def>

<%def name="resources()">
<script src="${tg.url('/javascript/movie_card.js')}"></script>
<script src="${tg.url('/javascript/index_view.js')}"></script>

<script>
window.addEvent('domready', function() {
	MovieCard.initalize();
	

	ViewController.addView(GridView);
	ViewController.addView(ListView);
	
	var jsonMovies = '${jsonMovies}'.replace(/&#34;/g, "'");
	var jsonMovies = JSON.decode(jsonMovies);
	
	ViewController.initalize($('mainContent'), jsonMovies);
	
	ViewController.activateView('grid');
	//ViewController.activateView('list');
});
</script>
</%def>

<ul id="nav">
	<li>
		<strong class="current">Biblioteka</strong>
	</li>
	<li>
		<a href="${tg.url('/identifyList')}">Niezidentyfikowane</a>	
	</li>
</ul>


<div id="mainContent"></div>

