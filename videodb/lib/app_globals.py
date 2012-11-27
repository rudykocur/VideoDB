# -*- coding: utf-8 -*-

"""The application's Globals object"""

__all__ = ['Globals']

import os
import tg
import tgscheduler
import transaction

from Queue import Queue

from videodb.model import DBSession
from videodb.model import entities

from videodb.lib import imdb_utils, tmdb


queueBreak = object()


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """

    def __init__(self):
        """Do nothing, by default."""
        self.scheduler = tgscheduler
        self.scheduler.start_scheduler()
        
        self.rescanStatus = 'idle'
        
        self.imdbQueueCounter = 1
        self.imdbQueues = {}
        
        api_key = tg.config.get('tmdb_api_key')
        tmdb.configure(api_key)
    
    def poolIdentifyQueue(self, queueId):
        queueId = int(queueId)
        print 'Waiting in queue', queueId
        data = self.imdbQueues[queueId].get()
        #print 'Got value', data
        
        if data is None:
            print 'QUEUE', queueId,'DONE - removing'
            del self.imdbQueues[queueId]
        
        if data is queueBreak:
            print 'QUEUE', queueId,'BREAK - removing'
            del self.imdbQueues[queueId]
            return
        
        return data
    
    def cancelIdentifyQueue(self, queueId):
        queueId = int(queueId)
        
        q = self.imdbQueues[queueId]
        
        print 'CANCELING QUEUE', queueId,'!!!!'
        q.put(queueBreak)
        #del self.imdbQueues[queueId]
    
    def _findByFilenameWorker(self, gen, queueNum):
        q = self.imdbQueues[queueNum]
        
        for movie in gen:
            #print 'ADDING', movie
            
            if queueNum not in self.imdbQueues:
                print 'FINDER BREAK !!!', queueNum
                gen.close()
                return
            
            q.put(movie)
        
        q.put(None)
        
        
        print ' ================ QUEUE', queueNum, 'DONE'
    
    def findByFilename(self, name):
        q = Queue()
        num = self.imdbQueueCounter
        self.imdbQueueCounter+=1
        
        self.imdbQueues[num] = q

        #print 'CREATING GENERATOR'        
        gen = imdb_utils.findByFilename(name)
        #print 'WAITING FOR GENERATOR'
        
        results = gen.next()
        
        #print 'FINDER SCHEDULED', results
        
        self.scheduler.add_single_task(action=self._findByFilenameWorker, args=[gen, num])
        
        return (num, results)
    
    def rescanLibraries(self):
        if self.rescanStatus == 'idle':
            self.scheduler.add_single_task(action=self._doRescan)
            self.rescanStatus = 'running'
    
    def _doRescan(self):
        
        validExtensions = ['mp4', 'mkv', 'avi', ]
        
        for library in DBSession.query(entities.Library).all():
            print library.root
            
            knownMovies = DBSession.query(entities.Movie.path).filter(entities.Movie.library==library).all()
            
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
                        
                        movie = entities.Movie(library=library, path=relpath)
                        newMovies.append(movie)
                        print 'ADDING MOVIE:', movie
                        DBSession.add(movie)
                        
                        #fp = os.path.join(dirpath, f)
                        #files.append(fp)

            print 'COMMITING', transaction
            transaction.commit()
            print 'COMMIT DONE', newMovies
        
        self.rescanStatus = 'idle'
