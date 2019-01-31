import os
import uuid
import logging
import mimetypes
import subprocess
import StringIO
from distutils.sysconfig import get_python_lib

from PIL import Image

DEBUG = os.getenv('DEBUG', False)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_PATH = './vendor/linux/' if DEBUG else '%s/opt/optimize-images/vendor/linux/' % get_python_lib()
TMP_DIR = '/tmp/'

libraries = {
    'mozjpeg': 'cjpeg'
}


def format_bytes(value):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if value < 1024.0:
            return value, x
        value /= 1024.0


def get_tmp_dir():
    return '%s%s/' % (TMP_DIR, str(uuid.uuid4())[-10:])


def optimize_image(source, quality=80):
    if not os.path.exists(source):
        raise ValueError('\'%s\' file does not exist' % source)

    path, extension = os.path.splitext(source)
    content_type = mimetypes.guess_type(source)
    file_path, filename = path = path.rsplit('/', 1)

    file_tmp_dir = get_tmp_dir()
    destination = '%s%s%s' % (file_tmp_dir, filename, extension)

    command = ['%scjpeg' % BASE_PATH, '-quality', '%s' % quality, '-optimize', '-progressive', '-outfile', destination, source]
    logger.debug('command: %s', command)

    os.mkdir(file_tmp_dir)
    subprocess.call(command)

    original_size = os.path.getsize(source)
    optimize_size = os.path.getsize(destination)

    logger.debug('original filename: %s', filename)
    logger.debug('original size: %3.1f %s', format_bytes(original_size)[0], format_bytes(original_size)[1])
    logger.debug('content-type: %s', content_type)

    logger.debug('optimize filename: %s', destination)
    logger.debug('optimize size: %3.1f %s', format_bytes(optimize_size)[0], format_bytes(original_size)[1])
    logger.debug('%.0f%% smaller', 100 - ((float(optimize_size) / float(original_size)) * 100))

    buffer_image = file(destination).read()
    os.remove(destination)
    image = Image.open(StringIO.StringIO(buffer_image))

    return {
        'filename': filename, 
        'quality': quality,
        'progressive': True,
        'library': 'mozjpeg',
        'extension': extension, 
        'content_type': content_type,
        'size': optimize_image,
        'image': image
    }
