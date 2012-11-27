<div>

<div class="cover">
	<img src="${imdb['cover'] or '/images/preview_unavailable.png'}"/>
</div>

<div class="infoPanel">
	<ul>
		<li><strong>IMDB</strong>: <a href="${imdb['imdb url']}" target="_blank">link</a> 
		<li><strong>Tytuł</strong>: ${imdb['title']}</li>
		<li><strong>Gatunki</strong>: ${', '.join(imdb['genres'])}</li>
		<li><strong>Fabuła</strong>: ${imdb['plot']}</li>
		<li><strong>Czas</strong>: ${ffmpeg['duration']}</li>
		<li><strong>Rozdzielczość</strong>: ${ffmpeg['frameSizeString']}</li>
		<li><strong>Języki</strong>: ${', '.join(ffmpeg['audioLang'])}</li>
		<li><strong>Napisy</strong>: ${', '.join(ffmpeg['subLang']) or 'Brak'}</li>
		<li><strong>Ścieżka</strong>: <pre>${movie.library.name}:${movie.path}</pre></li>
	</ul>
</div>

</div>