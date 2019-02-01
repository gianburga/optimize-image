import os
import uuid
import logging
import mimetypes
import subprocess
import io
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


def optimize_image(source_path=None, image=None, filename=None, quality=80):
    if source_path and not os.path.exists(source_path):
        raise ValueError('\'%s\' file path does not exist' % source_path)

    if source_path is None and image and isinstance(image, Image.Image):
        if not filename:
            raise ValueError('filename is required')

        filename, extension = os.path.splitext(filename)
        content_type = mimetypes.guess_type(filename)[0]
        tmp_dir_source = get_tmp_dir()
        source_path = '%s%s%s' % (tmp_dir_source, filename, extension)
        os.mkdir(tmp_dir_source)
        image.save(source_path)

    if source_path:
        path, extension = os.path.splitext(source_path)
        content_type = mimetypes.guess_type(source_path)[0]
        file_path, filename = path = path.rsplit('/', 1)

        file_tmp_dir = get_tmp_dir()
        destination = '%s%s%s' % (file_tmp_dir, filename, extension)

    command = ['%scjpeg' % BASE_PATH, '-quality', '%s' % quality, '-optimize', '-progressive', '-outfile', destination, source_path]
    logger.debug('command: %s', command)

    os.mkdir(file_tmp_dir)
    subprocess.call(command)

    original_size = os.path.getsize(source_path)
    optimize_size = os.path.getsize(destination)

    logger.debug('original filename: %s', filename)
    logger.debug('original size: %3.1f %s', format_bytes(original_size)[0], format_bytes(original_size)[1])
    logger.debug('content-type: %s', content_type)

    logger.debug('optimize filename: %s', destination)
    logger.debug('optimize size: %3.1f %s', format_bytes(optimize_size)[0], format_bytes(original_size)[1])
    logger.debug('%.0f%% smaller', 100 - ((float(optimize_size) / float(original_size)) * 100))

    f = open(destination, 'rb')
    buffer_image = io.BytesIO(f.read())
    f.close()

    os.remove(destination)

    image = Image.open(buffer_image)

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
