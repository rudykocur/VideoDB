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

<ul id="movielist">
% for movie in movies:
	<li>
		${movie.id} :: ${movie.path} :: 
		<a class="identify" href="${tg.url('/identify/%s'%movie.id)}">Identyfikuj</a> ::
		<a class="ignore" href="${tg.url('/ignoreMovie/%s'%movie.id)}">Ignoruj</a>
	</li> 
% endfor
</ul>
