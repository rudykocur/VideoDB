<%inherit file="local:templates.master"/>

<%def name="title()">
  VideoDB
</%def>

<%def name="resources()">
<script src="${tg.url('/javascript/movie_card.js')}"></script>
<script src="${tg.url('/javascript/index_view.js')}"></script>

<script>
window.addEvent('domready', function() {
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

<!--
<a href="${tg.url('/refresh')}">Odśwież</a> || <a href="${tg.url('/identifyList')}">Niezidentyfikowane</a>
-->


<div id="mainContent"></div>

<!--
<ul id="knownmovies">
% for movie, ffmpeg in known:
	<li id="movie-${movie.id}">
		<span class="title">${movie.imdbData.name} (${movie.imdbData.year})</span>
		<div class="imgwrap">
			<a href="/movieCard/${movie.id}">
				<img src="${movie.imdbData.coverUrl or '/images/preview_unavailable.png'}"/>
			</a>
		% if ffmpeg:
			<span class="frameSize ${'720p' if ffmpeg['frameSize'][1] >= 720 else '' }">${ffmpeg['frameSizeString']}</span>
		% endif
		</div>
		<span class="genres">${movie.imdbData.genres}</span>
	</li>
% endfor
</ul>


<script>
window.addEvent('domready', function() {

	MovieCard.initalize();
% for movie, ffmpeg in known:
	MovieCard.attach('${movie.id}');
% endfor
});
</script>

-->
