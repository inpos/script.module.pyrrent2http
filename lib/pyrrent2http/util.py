import sys
import socket
import chardet
import os
from . import MediaType
import mimetypes

SUBTITLES_FORMATS = ['.aqt', '.gsub', '.jss', '.sub', '.ttxt', '.pjs', '.psb', '.rt', '.smi', '.stl',
                         '.ssf', '.srt', '.ssa', '.ass', '.usf', '.idx']

class Struct(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value

def detect_media_type(name):
    ext = os.path.splitext(name)[1]
    if ext in SUBTITLES_FORMATS:
        return MediaType.SUBTITLES
    else:
        mime_type = mimetypes.guess_type(name)[0]
        if not mime_type:
            return MediaType.UNKNOWN
        mime_type = mime_type.split("/")[0]
        if mime_type == 'audio':
            return MediaType.AUDIO
        elif mime_type == 'video':
            return MediaType.VIDEO
        else:
            return MediaType.UNKNOWN

def localize_path(path):
    path = path.decode(chardet.detect(path)['encoding'])
    if not sys.platform.startswith('win'):
        path = path.encode(True and sys.getfilesystemencoding() or 'utf-8')
    return path

def can_bind(host, port):
    """
    Checks we can bind to specified host and port

    :param host: Host
    :param port: Port
    :return: True if bind succeed
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.close()
    except socket.error:
        return False
    return True


def find_free_port(host):
    """
    Finds free TCP port that can be used for binding

    :param host: Host
    :return: Free port
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, 0))
        port = s.getsockname()[1]
        s.close()
    except socket.error:
        return False
    return port


def ensure_fs_encoding(string):
    if isinstance(string, str):
        string = string.decode('utf-8')
    return string.encode(sys.getfilesystemencoding() or 'utf-8')
