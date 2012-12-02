import re, os
from pprint import pprint
from videodb import tmdb

def sanitizeFilename(name):
    name = os.path.splitext(os.path.basename(name))[0]
    
    toDelete = ['XviD', 'aXXo', 'BRRIP', 'x264', '720p', '1080p', '1080P', 'DVDRip', 'ETRG', 'divx']
    
    name = re.sub(r'(www\.[^ ]*)', '', name)
    
    name = name.lower().replace('.', ' ').replace('-', ' ').replace('_', ' ')
    
    for x in toDelete:
        name = name.replace(x.lower(), '')
    
    while name.find('[') != -1:
        name = re.sub(r'(\[[^]]*\])', '', name)
        
    return name

def getMovieData(imdbId):
    movie = tmdb.Movie(imdbId)
    
    data = {
        'id': movie.get_id(),
        'title': movie.get_title(),
        'genres': map(lambda x: x['name'], movie.get_genres()),
        'cover': movie.get_poster('m'),
        'year': movie.get_release_year(),
        'runtime': movie.get_runtime(),
        #'runtime': movie.get('runtime', None)
    }
    
    return data

def getMovieFullData(imdbId):
    movie = tmdb.Movie(imdbId)
    
    out = {
        'id': movie.get_id(),
        'title': movie.get_title(),
        'genres': map(lambda x: x['name'], movie.get_genres()),
        'cover': movie.get_poster(),
        'year': movie.get_release_year(),
        'imdb url': 'http://imdb.com/title/%s' % (movie.get_imdb_id()),
        'plot': movie.get_overview(),
        'plot outline': movie.get_tagline(),
        'runtime': movie.get_runtime(),
        #'runtime': movie.get('runtime', None)
    }
    
    return out

def findByFilename(name):
    print 'TMDB - searching for:', name
    
    tmdbRs = tmdb.Movies(name, True)
    yield tmdbRs.get_total_results()
    
    
    
    for movie in tmdbRs:
        data = {
            'id': movie.get_id(),
            'title': movie.get_title(),
            'genres': map(lambda x: x['name'], movie.get_genres()),
            'cover': movie.get_poster('m'),
            'year': movie.get_release_year(),
            'runtime': movie.get_runtime(),
        }
        
        
        yield data
    
    
        










    
