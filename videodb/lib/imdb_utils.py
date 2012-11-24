import re, os, time
import imdb
from imdb.helpers import akasLanguages

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

def getMovieTitle(movie):
    akas = akasLanguages(movie)
    #print 'AKAS', akas
    #akasDict = dict(akas)
    
    if 'English' in movie.get('languages', []):
        return movie['title']
    
    eng = filter(lambda x: x[0] == 'English', akas)
    
    if len(eng):
        return eng[0][1]
    
    return movie['title']

def getMovieData(imdbId):
    i = imdb.IMDb()
    movie = i.get_movie(imdbId)
    
    return {
        'id': movie.movieID,
        'title': getMovieTitle(movie),
        'genres': movie.get('genres', []),
        #'cover': movie.get('full-size cover url', None),
        'cover': movie.get('cover url', None),
        'year': movie.get('year', None),
        'runtime': ','.join(movie.get('runtime', []))
    }

def getMovieFullData(imdbId):
    i = imdb.IMDb()
    movie = i.get_movie(imdbId)
    
    #from pprint import pprint
    #pprint(movie.data)
    
    simpleKeys = ['plot', 'plot outline']
    
    out = {
        'id': movie.movieID,
        'title': getMovieTitle(movie),
        'genres': movie.get('genres', []),
        'cover': movie.get('full-size cover url', None),
        'year': movie.get('year', None),
        'runtime': ','.join(movie.get('runtime', [])),
        'imdb url': 'http://imdb.com/title/tt%s' % (movie.movieID),
        #'plot': movie['plot'],
    }
    
    for k in simpleKeys:
        out[k] = movie.get(k, None)
    
    return out

def findByFilename(name):
    print 'IMDB - searching for:', name
    t1 = time.time()
    i = imdb.IMDb()
    t2 = time.time()
    results = i.search_movie(name)
    
    print 'Found', len(results), 'results', '::', (t2-t1)
    
    yield len(results)
    
    #out = []
    for movie in results:
        #print 'PROCESSING', movie
        
        i.update(movie)
        
#        from pprint import pprint
#        pprint(movie.data)
        
        data = {
            'id': movie.movieID,
            #'title': movie['title'],
            'title': getMovieTitle(movie),
            'genres': movie.get('genres', []),
            #'cover': movie.get('full-size cover url', None),
            'cover': movie.get('cover url', None),
            'year': movie.get('year', None),
            'runtime': movie.get('runtime', None)
        }
        
        print 'yielding', data
        
        yield data
        










    
