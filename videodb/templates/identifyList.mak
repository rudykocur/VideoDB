<%inherit file="local:templates.master"/>

<%def name="title()">
  VideoDB - Unidentified movies
</%def>

<%def name="resources()">
<script src="${tg.url('/javascript/movie_identifier.js')}"></script>

<script>
	window.addEvent('domready', function() {
		MovieIdentifier.attach($$('#movielist a.identify'));
	});
</script>
</%def>


<a href="${tg.url('/refresh')}">Odśwież</a> || <a href="${tg.url('/index')}">Biblioteka</a>

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