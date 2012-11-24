<div>

<div class="cover">
	<img src="${data['cover'] or '/images/preview_unavailable.png'}"/>
</div>

<div class="infoPanel">
	<ul>
		<li><strong>IMDB</strong>: <a href="${data['imdb url']}" target="_blank">link</a> 
		<li><strong>Tytuł</strong>: ${data['title']}</li>
		<li><strong>Gatunki</strong>: ${', '.join(data['genres'])}</li>
		<li><strong>Fabuła</strong>: ${data['plot outline']}</li>
	</ul>
</div>

</div>