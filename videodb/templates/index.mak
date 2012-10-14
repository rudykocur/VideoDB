<%inherit file="local:templates.master"/>

<%def name="title()">
  HOŁMPYJDŻ
</%def>

<%def name="resources()">
<script src="${tg.url('/javascript/movie_identifier.js')}"></script>

<script>
	window.addEvent('domready', function() {
		MovieIdentifier.attach($$('#movielist a.identify'));
	});
</script>
</%def>

HOWDY ${page} :: <a href="${tg.url('/refresh')}">Odśwież</a>

<ul id="knownmovies">
% for movie in known:
	<li>
		<span class="title">${movie.imdbData.name} (${movie.imdbData.year})</span>
		<img src="${movie.imdbData.coverUrl or '/images/preview_unavailable.png'}"/>
		<span class="genres">${movie.imdbData.genres}</span>
	</li>
% endfor
</ul>

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
