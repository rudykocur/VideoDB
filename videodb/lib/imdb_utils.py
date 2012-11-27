import re, os
from pprint import pprint
#import imdb
#from imdb.helpers import akasLanguages
from videodb.lib import tmdb

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

#def getMovieTitle(movie):
#    akas = akasLanguages(movie)
#    #print 'AKAS', akas
#    #akasDict = dict(akas)
#    
#    if 'English' in movie.get('languages', []):
#        return movie['title']
#    
#    eng = filter(lambda x: x[0] == 'English', akas)
#    
#    if len(eng):
#        return eng[0][1]
#    
#    return movie['title']

def getMovieData(imdbId):
    #i = imdb.IMDb()
    #movie = i.get_movie(imdbId)
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
#    return {
#        'id': movie.movieID,
#        'title': getMovieTitle(movie),
#        'genres': movie.get('genres', []),
#        #'cover': movie.get('full-size cover url', None),
#        'cover': movie.get('cover url', None),
#        'year': movie.get('year', None),
#        'runtime': ','.join(movie.get('runtime', []))
#    }

def getMovieFullData(imdbId):
    #i = imdb.IMDb()
    #movie = i.get_movie(imdbId)
    
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
#    
#    simpleKeys = ['plot', 'plot outline']
#    
#    out = {
#        'id': movie.movieID,
#        'title': getMovieTitle(movie),
#        'genres': movie.get('genres', []),
#        'cover': movie.get('full-size cover url', None),
#        'year': movie.get('year', None),
#        'runtime': ','.join(movie.get('runtime', [])),
#        'imdb url': 'http://imdb.com/title/tt%s' % (movie.movieID),
#        #'plot': movie['plot'],
#    }
#    
#    for k in simpleKeys:
#        out[k] = movie.get(k, None)
    
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
        
        #print 'yielding', data
        
        yield data
    
    
#    #out = []
#    for movie in results:
#        #print 'PROCESSING', movie
#        
#        i.update(movie)
#        
##        from pprint import pprint
##        pprint(movie.data)
#        
#        data = {
#            'id': movie.movieID,
#            #'title': movie['title'],
#            'title': getMovieTitle(movie),
#            'genres': movie.get('genres', []),
#            #'cover': movie.get('full-size cover url', None),
#            'cover': movie.get('cover url', None),
#            'year': movie.get('year', None),
#            'runtime': movie.get('runtime', None)
#        }
#        
#        print 'yielding', data
#        
#        yield data
        










    
