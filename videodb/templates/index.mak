<%inherit file="local:templates.master"/>

<%def name="title()">
  VideoDB
</%def>

<%def name="resources()">
<script src="${tg.url('/javascript/movie_identifier.js')}"></script>
<script src="${tg.url('/javascript/movie_card.js')}"></script>

<script>
	window.addEvent('domready', function() {
		MovieIdentifier.attach($$('#movielist a.identify'));
	});
</script>
</%def>

HOWDY ${page} :: <a href="${tg.url('/refresh')}">Odśwież</a>

<ul id="knownmovies">
% for movie in known:
	<li id="imdb-${movie.imdbData.imdbId}">
		<span class="title">${movie.imdbData.name} (${movie.imdbData.year})</span>
		<div class="imgwrap">
			<img src="${movie.imdbData.coverUrl or '/images/preview_unavailable.png'}"/>
		</div>
		<span class="genres">${movie.imdbData.genres}</span>
	</li>
% endfor
</ul>


<script>
window.addEvent('domready', function() {

	MovieCard.initalize();
% for movie in known:
	MovieCard.attach('${movie.imdbData.imdbId}');
% endfor
});
</script>

<br/><br/><br/>

<ul id="movielist">
% for movie in movies:
	<li>
		${movie.id} :: ${movie.path} :: 
		<a class="identify" href="${tg.url('/identify/%s'%movie.id)}">Identyfikuj</a> ::
		<a class="ignore" href="${tg.url('/ignoreMovie/%s'%movie.id)}">Ignoruj</a>
	</li> 
% endfor
</ul>
