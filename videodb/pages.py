
import os
import json


from flask import render_template, jsonify, request, redirect, url_for

from sqlalchemy.orm import joinedload

from videodb.schema import Movie, ImdbData
from videodb import imdb_utils, ffmpeg
from videodb.scheduler import Scheduler

_routerList = []
def router(rule, **options):
    def decorator(f):
        endpoint = options.pop('endpoint', None)
        
        _routerList.append((rule, endpoint, f, options))
        return f
    
    return decorator


@router('/')
def main():
    knownCond = (Movie.disabled==False, Movie.imdbData!=None,)
    
    knownMoviesDb = Movie.query.join(ImdbData).filter(*knownCond).order_by(ImdbData.name).options(joinedload(Movie.imdbData)).all()
    
    knownMovies = []
    for m in knownMoviesDb:
        knownMovies.append([m, ffmpeg.getCachedMovieInfo(m.getFullPath())])
    
    jsonMovies = [];
    for movie, ff in knownMovies:
        jsonMovies.append({
            'id': movie.id,
            'title': movie.imdbData.name,
            'year': movie.imdbData.year,
            'coverUrl': movie.imdbData.coverUrl,
            'frameSize': ff['frameSize'] if ff else None,
            'genres': movie.imdbData.genres,
        })
    
    return render_template('index.html', jsonMovies=json.dumps(jsonMovies))

@router('/identifyList')
def unidentified():
    cond = (Movie.disabled==False, Movie.imdbData==None,)
    movies = Movie.query.filter(*cond).all()
    
    return render_template('unidentified.html', movies=movies)

@router('/associate/<int:movieId>/<imdbId>')
def associate_movie(movieId, imdbId):
    movie = Movie.query.get(int(movieId))
    imdbData = ImdbData.query.get(imdbId)
    
    if imdbData is None:
        data = imdb_utils.getMovieData(imdbId)
        
        imdbData = ImdbData(imdbId=data['id'], name=data['title'], 
            genres=', '.join(data['genres']), coverUrl=data['cover'], year=data['year'],
            runtime=data['runtime'])
        
        #DBSession.add(imdbData)
    
    movie.imdbData = imdbData
    ffmpeg.getMovieInfo(movie.getFullPath())
    
    return redirect(url_for('main'))
    
    

@router('/refresh_unidentified')
def refresh_unidentified():
    Scheduler.rescanLibraries()
    return ''

@router('/identify/<movieId>', methods=['GET','POST'])
def identify_movie(movieId):
    customName = request.args.get('customName', None)
    print 'MOVIE', movieId, '::', repr(customName)
    
    movie = Movie.query.get(int(movieId))
    
    print 'identify_movie:', movie
    
    identifyName = customName or imdb_utils.sanitizeFilename(movie.path)
    queueId, resultCount = Scheduler.findByFilename(identifyName)
    
    return jsonify(name=identifyName, path=movie.path, queueId=queueId, resultCount=resultCount, movieId=movieId)
    
@router('/ignore_movie/<int:movieId>')
def ignore_movie(movieId):
    movie = Movie.query.get(int(movieId))
    movie.disabled = True
    
    return redirect(url_for('unidentified'))

@router('/cancelIdentifyQueue/<int:queueId>', methods=['GET','POST'])
def cancelIdentifyQueue(queueId):
    Scheduler.cancelIdentifyQueue(queueId)
    return ''

@router('/poolIdentifyQueue/<int:queueId>', methods=['GET','POST'])
def poolIdentifyQueue(queueId):
    movie = Scheduler.poolIdentifyQueue(queueId)
    
    return jsonify(movie=movie)
    
@router('/movieCard/<int:movieId>')
def movieCard(movieId):
    movie = Movie.query.get(int(movieId))
    
    ffmpegData = ffmpeg.getMovieInfo(movie.getFullPath())
    data = imdb_utils.getMovieFullData(movie.imdbData.imdbId)
    
    return render_template('movieCard.html', imdb=data, ffmpeg=ffmpegData, movie=movie)


def init_routing(app):
    for rule, endpoint, fun, options in _routerList:
        #print 'Registering', rule#, '::', endpoint, '::', fun, '::', options
        
        app.add_url_rule(rule, endpoint, fun, **options)
    



