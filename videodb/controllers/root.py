# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context, app_globals
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin import AdminController

from sqlalchemy.orm import joinedload

from videodb.model import DBSession, metadata

from videodb.model import entities
from videodb import model

from videodb.lib.base import BaseController
from videodb.controllers.error import ErrorController

from videodb.lib import imdb_utils

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the videodb application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """

    error = ErrorController()
    admin = AdminController(model, DBSession)

    def _before(self, *args, **kw):
        tmpl_context.project_name = "videodb"

    @expose('videodb.templates.index')
    def index(self):
        """Handle the front-page."""
        
        knownCond = entities.Movie.disabled==False, entities.Movie.imdbData!=None
        knownMovies = DBSession.query(entities.Movie)\
            .join(entities.ImdbData)\
            .filter(*knownCond)\
            .order_by(entities.ImdbData.name)\
            .options(joinedload(entities.Movie.imdbData))\
            .all()
        
        cond = entities.Movie.disabled==False, entities.Movie.imdbData==None
        allmovies = DBSession.query(entities.Movie).filter(*cond).all()
        
        return dict(page='index', movies=allmovies, known=knownMovies)
    
    @expose('json')
    def identify(self, movieId, customName=None):
        print 'MOVIE', movieId, '::', customName
        
        movie = DBSession.query(entities.Movie).get(movieId)
        
        print movie
        
        identifyName = customName or imdb_utils.sanitizeFilename(movie.path)
        queueId, resultCount = app_globals.findByFilename(identifyName)
        
        return dict(name=identifyName, path=movie.path, queueId=queueId, resultCount=resultCount, movieId=movieId)
    
    @expose()
    def associate(self, movieId, imdbId):
        
        movie = DBSession.query(entities.Movie).get(int(movieId))
        
        imdbData = DBSession.query(entities.ImdbData).get(imdbId)
        if imdbData is None:
            data = imdb_utils.getMovieData(imdbId)
            
            imdbData = entities.ImdbData(imdbId=data['id'], name=data['title'], 
                genres=', '.join(data['genres']), coverUrl=data['cover'], year=data['year'],
                runtime=data['runtime'])
            DBSession.add(imdbData)
        
        movie.imdbData = imdbData
        
        redirect('/')
    
    @expose('json')
    def cancelIdentifyQueue(self, queueId):
        app_globals.cancelIdentifyQueue(queueId)
    
    @expose('json')
    def poolIdentifyQueue(self, queueId):
        movie = app_globals.poolIdentifyQueue(queueId)
        
        return dict(movie=movie)
        
    
    @expose('json')
    def refresh(self):
        print 'REFRESH SCHEDULE'
        app_globals.rescanLibraries()
        print 'SCHEDULED !!'
        
        return dict(status=app_globals.rescanStatus)
    
    @expose()
    def ignoreMovie(self, movieId):
        m = DBSession.query(entities.Movie).get(movieId)
        m.disabled = True
        
        #return dict(removed=True, movieId=movieId)
        redirect('/')
    
    @expose('videodb.templates.movieCard')
    def movieCard(self, imdbId):
        data = imdb_utils.getMovieFullData(imdbId)
        return dict(data=data)
    
