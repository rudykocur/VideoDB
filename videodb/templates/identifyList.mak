<%inherit file="local:templates.master"/>

<%def name="title()">
  VideoDB - Unidentified movies
</%def>

<%def name="resources()">
<script src="${tg.url('/javascript/movie_identifier.js')}"></script>

<script>
	window.addEvent('domready', function() {
		MovieIdentifier.attach($$('#movielist a.identify'));
		
		$('refreshIdentifyList').addEvent('click', function(e) {
			e.stop();
			
			new Request({
				url: e.target.href,
				onSuccess: function() {
					window.location = window.location;
				},
				onFailure: function(xhr) {
					alert('Ooops, unable to refresh');
					console.log('xhr');
				}
			}).get();
		});
	});
</script>
</%def>


<ul id="nav">
	<li>
		<a href="${tg.url('/index')}">Biblioteka</a>
	</li>
	<li>
		<strong>Niezidentyfikowane</strong>	
	</li>
	<li>
		<a id="refreshIdentifyList" href="${tg.url('/refresh')}">Odśwież</a>
	</li>
</ul>

<ul id="movielist">
% for movie in movies:
	<li>
		<a class="identify" href="${tg.url('/identify/%s'%movie.id)}">Identyfikuj</a> ::
		<a class="ignore" href="${tg.url('/ignoreMovie/%s'%movie.id)}">Ignoruj</a> ::
		${'/'.join(movie.path.split('/')[:-1])}${'/' if movie.path.find('/')>0 else ''}<strong>${movie.path.split('/')[-1]}</strong>
	</li> 
% endfor
</ul>