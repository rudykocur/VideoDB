import json, os, traceback
import subprocess

out1 = """
{
    "streams": [
        {
            "index": 0,
            "codec_name": "mpeg4",
            "codec_long_name": "MPEG-4 part 2",
            "codec_type": "video",
            "codec_time_base": "1/25",
            "codec_tag_string": "XVID",
            "codec_tag": "0x44495658",
            "width": 656,
            "height": 368,
            "has_b_frames": 1,
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "41:23",
            "pix_fmt": "yuv420p",
            "level": 5,
            "quarter_sample": "0",
            "divx_packed": "0",
            "r_frame_rate": "25/1",
            "avg_frame_rate": "0/0",
            "time_base": "1/25",
            "start_time": "0.000000",
            "duration": "4837.640000",
            "nb_frames": "120941"
        },
        {
            "index": 1,
            "codec_name": "ac3",
            "codec_long_name": "ATSC A/52A (AC-3)",
            "codec_type": "audio",
            "codec_time_base": "1/48000",
            "codec_tag_string": "[0] [0][0]",
            "codec_tag": "0x2000",
            "sample_fmt": "s16",
            "sample_rate": "48000",
            "channels": 6,
            "bits_per_sample": 0,
            "dmix_mode": "-1",
            "ltrt_cmixlev": "-1.000000",
            "ltrt_surmixlev": "-1.000000",
            "loro_cmixlev": "-1.000000",
            "loro_surmixlev": "-1.000000",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "125/4",
            "time_base": "1/56000",
            "start_time": "0.000000",
            "nb_frames": "270907840"
        }
    ],
    "format": {
        "filename": "Black Sheep/Black sheep KLAXXON.avi",
        "nb_streams": 2,
        "format_name": "avi",
        "format_long_name": "AVI format",
        "start_time": "0.000000",
        "duration": "4837.640000",
        "size": "956291072",
        "bit_rate": "1581417",
        "tags": {
            "encoder": "FairUse Wizard - http://fairusewizard.com"
        }
    }
}
"""


out2 = """
{
    "streams": [
        {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "codec_type": "video",
            "codec_time_base": "1/180000",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "width": 1280,
            "height": 720,
            "has_b_frames": 2,
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "16:9",
            "pix_fmt": "yuv420p",
            "level": 31,
            "is_avc": "1",
            "nal_length_size": "4",
            "r_frame_rate": "24000/1001",
            "avg_frame_rate": "166785000/6959911",
            "time_base": "1/90000",
            "start_time": "0.000000",
            "duration": "6959.911000",
            "nb_frames": "166785",
            "tags": {
                "creation_time": "2012-06-13 18:21:40",
                "language": "und",
                "handler_name": ""
            }
        },
        {
            "index": 1,
            "codec_name": "ac3",
            "codec_long_name": "ATSC A/52A (AC-3)",
            "codec_type": "audio",
            "codec_time_base": "1/48000",
            "codec_tag_string": "ac-3",
            "codec_tag": "0x332d6361",
            "sample_fmt": "s16",
            "sample_rate": "48000",
            "channels": 2,
            "bits_per_sample": 0,
            "dmix_mode": "-1",
            "ltrt_cmixlev": "-1.000000",
            "ltrt_surmixlev": "-1.000000",
            "loro_cmixlev": "-1.000000",
            "loro_surmixlev": "-1.000000",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "125/4",
            "time_base": "1/48000",
            "start_time": "0.000000",
            "duration": "6959.936000",
            "nb_frames": "217498",
            "tags": {
                "creation_time": "2012-06-13 18:21:40",
                "language": "jpn",
                "handler_name": ""
            }
        },
        {
            "index": 2,
            "codec_name": "dvdsub",
            "codec_long_name": "DVD subtitles",
            "codec_type": "subtitle",
            "codec_time_base": "1/90000",
            "codec_tag_string": "mp4s",
            "codec_tag": "0x7334706d",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/90000",
            "start_time": "0.000000",
            "duration": "6959.936000",
            "nb_frames": "2302",
            "tags": {
                "creation_time": "2012-06-13 18:21:40",
                "language": "zho",
                "handler_name": ""
            }
        }
    ],
    "format": {
        "filename": "[youshikibi] Hoshi Wo Ou Kodomo [720p].mp4",
        "nb_streams": 3,
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
        "format_long_name": "QuickTime/MPEG-4/Motion JPEG 2000 format",
        "start_time": "0.000000",
        "duration": "6959.936000",
        "size": "1759514608",
        "bit_rate": "2022449",
        "tags": {
            "major_brand": "mp42",
            "minor_version": "0",
            "compatible_brands": "mp42isomavc1",
            "creation_time": "2012-06-13 18:21:39",
            "encoder": "HandBrake 0.9.6 2012022800",
            "date": "2011",
            "title": "Hoshi Wo Ou Kodomo"
        }
    }
}

"""

out3 = """
{
    "streams": [
        {
            "index": 0,
            "codec_name": "h264",
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10",
            "codec_type": "video",
            "codec_time_base": "1001/48000",
            "codec_tag_string": "avc1",
            "codec_tag": "0x31637661",
            "width": 1920,
            "height": 816,
            "has_b_frames": 2,
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "40:17",
            "pix_fmt": "yuv420p",
            "level": 40,
            "is_avc": "1",
            "nal_length_size": "4",
            "r_frame_rate": "24000/1001",
            "avg_frame_rate": "24000/1001",
            "time_base": "1/24000",
            "start_time": "0.083417",
            "duration": "10256.996750",
            "nb_frames": "245922",
            "tags": {
                "creation_time": "2011-12-09 15:18:04",
                "language": "und",
                "handler_name": "GPAC ISO Video Handler"
            }
        },
        {
            "index": 1,
            "codec_name": "aac",
            "codec_long_name": "Advanced Audio Coding",
            "codec_type": "audio",
            "codec_time_base": "1/16000",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "sample_fmt": "s16",
            "sample_rate": "32000",
            "channels": 2,
            "bits_per_sample": 0,
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/16000",
            "start_time": "0.000000",
            "duration": "10257.280000",
            "nb_frames": "160270",
            "tags": {
                "creation_time": "2011-12-09 15:21:41",
                "language": "eng",
                "handler_name": ""
            }
        }
    ],
    "format": {
        "filename": "Gladiator (2000)/Gladiator.EXTENDED.2000.1080.BrRip.264.YIFY.mp4",
        "nb_streams": 2,
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
        "format_long_name": "QuickTime/MPEG-4/Motion JPEG 2000 format",
        "start_time": "0.000000",
        "duration": "10257.280000",
        "size": "1721883553",
        "bit_rate": "1342955",
        "tags": {
            "major_brand": "isom",
            "minor_version": "1",
            "compatible_brands": "isomavc1",
            "creation_time": "2011-12-09 15:18:04",
            "encoder": "Yamb 2.1.0.0 [http://yamb.unite-video.com]"
        }
    }
}

"""


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





