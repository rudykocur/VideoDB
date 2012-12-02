
import os
from threading import Thread
from Queue import Queue

from videodb import imdb_utils
from videodb.schema import Library, Movie
from videodb.db import db_session


queueBreak = object()

class Scheduler(object):
    def __init__(self):
        self.identifyQueuesCounter = 1
        self.identifyQueues = {}
        
        self.rescanStatus = 'idle'
        
    def poolIdentifyQueue(self, queueId):
        queueId = int(queueId)
        print 'Waiting in queue', queueId
        data = self.identifyQueues[queueId].get()
        #print 'Got value', data
        
        if data is None:
            print 'QUEUE', queueId,'DONE - removing'
            del self.identifyQueues[queueId]
        
        if data is queueBreak:
            print 'QUEUE', queueId,'BREAK - removing'
            del self.identifyQueues[queueId]
            return
        
        return data
    
    def cancelIdentifyQueue(self, queueId):
        queueId = int(queueId)
        
        q = self.identifyQueues.get(queueId, None)
        
        if q is None:
            print 'CANNOT CANCEL QUEUE', queueId, '- does not exists!'
        else:
            print 'CANCELING QUEUE', queueId,'!!!!'
            q.put(queueBreak)
        #del self.imdbQueues[queueId]
    
    
    def _findByFilenameWorker(self, gen, queueNum):
        q = self.identifyQueues[queueNum]
        
        for movie in gen:
            #print 'ADDING', movie
            
            if queueNum not in self.identifyQueues:
                print 'FINDER BREAK !!!', queueNum
                gen.close()
                return
            
            q.put(movie)
        
        q.put(None)
        
        
        print ' ================ QUEUE', queueNum, 'DONE'
    
    def findByFilename(self, name):
        q = Queue()
        num = self.identifyQueuesCounter
        self.identifyQueuesCounter+=1
        
        self.identifyQueues[num] = q

        #print 'CREATING GENERATOR'        
        gen = imdb_utils.findByFilename(name)
        #print 'WAITING FOR GENERATOR'
        
        results = gen.next()
        
        #print 'FINDER SCHEDULED', results
        
        #self.scheduler.add_single_task(action=self._findByFilenameWorker, args=[gen, num])
        Thread(target=self._findByFilenameWorker, args=[gen, num]).start()
        
        return (num, results)





    def rescanLibraries(self):
        if self.rescanStatus == 'idle':
            #self.scheduler.add_single_task(action=self._doRescan)
            
            Thread(target=self._doRescan).start()
            
            self.rescanStatus = 'running'
    
    def _doRescan(self):
        
        validExtensions = ['mp4', 'mkv', 'avi', ]
        
        for library in Library.query.all():
            print library.root
            
            #knownMovies = Movie.query.select(Movie.path).filter(Movie.library==library).all() 
            knownMovies = db_session.query(Movie.path).filter(Movie.library==library).all()
            
            knownFiles = [m[0] for m in knownMovies]
            
            #print 'ALL KNOWN', knownFiles
            
            files = []
            newMovies = []
            
            libraryRoot = library.root.encode('utf-8')
            
            #tmpcounter = 0
            
            for dirpath, dirnames, filenames in os.walk(libraryRoot):
                for f in filenames:
                    ext = os.path.splitext(f)[1][1:]
                    if ext in validExtensions:
                        #print dirpath, "::", f
                        relpath = unicode(os.path.join(dirpath[len(libraryRoot):], f), 'utf_8', 'replace')
                        
                        if relpath in knownFiles:
                            continue
                        
                        print 'NEW MOVIE:', relpath
                        #else: print relpath
                        
                        #print relpath
                        
                        #tmpcounter += 1
                        #if tmpcounter % 9 == 0:
                        #    continue
                        
                        movie = Movie(library=library, path=relpath)
                        newMovies.append(movie)
                        print 'ADDING MOVIE:', movie
                        db_session.add(movie)
                        
                        #fp = os.path.join(dirpath, f)
                        #files.append(fp)

            #print 'COMMITING', transaction
            #transaction.commit()
            db_session.commit()
            print 'COMMIT DONE', newMovies
        
        self.rescanStatus = 'idle'




Scheduler = Scheduler()