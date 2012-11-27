import json, os, traceback
import subprocess


def formatDuration(number):
    hours = number / float(60*60)
    
    minutesFloat = hours - int(hours)
    minutes = 60*minutesFloat
    
    #secondsFloat = minutes - int(minutes)
    #seconds = 60*secondsFloat
    
    return '%d:%02d' % (int(hours), int(minutes))

def processAudioStreams(streams):
    out = []
    for s in streams:
        tags = s.get('tags', {})
        lang = tags.get('language', '???')
        out.append(lang)
    
    return out

processSubStreams = processAudioStreams

def queryFFProbe(path):
    params = [
        'ffprobe', 
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        path
    ]
    
    #print 'INVOKE', params
    p = subprocess.Popen(params, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    out, err = p.communicate()
    
    return out
    
    

def processJson(out):
    data = json.loads(out)
    
    videoStream = filter(lambda x: x['codec_type'] == 'video', data['streams'])[0]
    audioStreams = filter(lambda x: x['codec_type'] == 'audio', data['streams'])
    subStreams = filter(lambda x: x['codec_type'] == 'subtitle', data['streams'])
    
#    name = data['format']['filename']
    
    dur = formatDuration(float(data['format']['duration']))
    
    videoWidth = videoStream['width']
    videoHeight = videoStream['height']
    
    audioLangs = processAudioStreams(audioStreams)
    subLangs = processSubStreams(subStreams)
    
#    print name
#    print '\tDuration:', dur 
#    print '\tFrame:', videoWidth,'x',videoHeight
#    print '\tAudio:', audioLangs
#    print '\tSubtitles:', subLangs
#    print
    
    return {
        'duration': dur,
        'frameSizeString': '%sx%s' % (videoWidth, videoHeight),
        'frameSize': (videoWidth, videoHeight),
        'audioLang': audioLangs,
        'subLang': subLangs,
    }

def getCacheFilename(path):
    root, filename = os.path.split(path)
    cacheFile = '.%s.videodb' % (filename, )
    
    return os.path.join(root, cacheFile)

def _getCachedMovieInfo(path):
    f = getCacheFilename(path)
    
    if os.path.exists(f):
        with open(f) as fp:
            return json.load(fp)
    
    return None

def _saveMovieInfo(path, info):
    f = getCacheFilename(path)
    
    try:
        with open(f, 'w') as fp:
            json.dump(info, fp)
    except IOError, e:
        print '!!!!!! Unable to cache movie info:', e
        print traceback.format_exc()

def getCachedMovieInfo(path):
    out = _getCachedMovieInfo(path)
    if out is not None:
        return processJson(out)
    
    return None

def getMovieInfo(path, useCache=True):
    #print 'Getting movie info for', path
    
    out = None
    
    if useCache:
        out = _getCachedMovieInfo(path)
    
    if out is None:
        print 'PROBING through ffprobe:', path
        out = queryFFProbe(path)
    
    info = processJson(out)
    
    if useCache:
        _saveMovieInfo(path, out)
    
    return info
    

if __name__ == "__main__":
    processJson(out1)
    processJson(out2)
    processJson(out3)





