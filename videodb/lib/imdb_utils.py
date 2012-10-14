import re, os
import imdb

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

def findByFilename(name):
    print 'IMDB - searching for:', name
    
    i = imdb.IMDb()
    results = i.search_movie(name)
    
    print 'Found', len(results), 'results'
    
    yield len(results)
    
    #out = []
    for movie in results:
        #print 'PROCESSING', movie
        
        i.update(movie)
        #i.update(movie, 'genres')
        
        #print movie.summary()
        
        data = {
            'id': movie.movieID,
            'title': movie['title'],
            'genres': movie.get('genres', []),
            'cover': movie.get('full-size cover url', None),
            'year': movie.get('year', None),
        }
        
        print 'yielding', data
        
        yield data
        
        #out.append(data)
    
    #print out
    #return out
    
#    first = results[0]
#    
#    i.update(first, 'all')
#    
#    import sys;sys.path.append(r'/home/ivan/apps/eclipse-4.2/plugins/org.python.pydev_2.6.0.2012062818/pysrc')
#    import pydevd;pydevd.settrace()
#    
#    print first