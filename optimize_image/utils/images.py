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

TMP_DIR = '/tmp/'

libraries = {
    'mozjpeg': 'cjpeg'
}


def get_lib_path(name):
    if os.path.exists('./vendor/linux/%s' % name):
        return './vendor/linux/%s' % name
    elif os.path.exists('%s/opt/optimize-images/vendor/linux/%s' % (get_python_lib(), name)):
        return '%s/opt/optimize-images/vendor/linux/%s' % (get_python_lib(), name)
    elif os.path.exists('/opt/optimize-images/vendor/linux/%s' % name):
        return '/opt/optimize-images/vendor/linux/%s' % name
    return None


def format_bytes(value):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if value < 1024.0:
            return value, x
        value /= 1024.0


def get_tmp_dir():
    return '%s%s/' % (TMP_DIR, str(uuid.uuid4())[-10:])


def create_temp_image_from_buffer(image_buffer, path):
    image_file = open(path, 'wb')
    image_file.write(image_buffer.getvalue())
    image_file.close()


def get_buffer_from_file(path, delete=False):
    image_file = open(path, 'rb')
    buffer_image = io.BytesIO(image_file.read())
    image_file.close()

    if delete:
        os.remove(path)

    return buffer_image


def get_file_size(path):
    return os.path.getsize(path)


def run_command(command):
    logger.debug('command: %s', command)
    subprocess.call(command)


def optimize_image(source_path=None, image_buffer=None, filename=None, quality=80):
    if source_path and not os.path.exists(source_path):
        raise ValueError('\'%s\' file path does not exist' % source_path)

    tmp_dir = get_tmp_dir()
    os.mkdir(tmp_dir)

    if source_path is None and image_buffer:
        if not filename:
            raise ValueError('filename is required')

        logger.debug('image_buffer type: %s', type(image_buffer))

        if not isinstance(image_buffer, (io.BytesIO, io.BufferedReader)):
            raise ValueError('image is not Image instance')

        if isinstance(image_buffer, io.BufferedReader):
            image_buffer = io.BytesIO(image_buffer.read())

        filename, extension = os.path.splitext(filename)

        if not extension:
            raise ValueError('filename extension is None')

        source_path = '%s%s%s' % (tmp_dir, filename, extension)
        logger.debug('source_path: %s', source_path)
        create_temp_image_from_buffer(image_buffer, source_path)

    if source_path:
        path, extension = os.path.splitext(source_path)
        content_type = mimetypes.guess_type(source_path)[0]
        file_path, filename = path = path.rsplit('/', 1)

        destination = '%s%s.optimize.%s' % (tmp_dir, filename, extension)

    lib_path = get_lib_path('cjpeg')
    command = [lib_path, '-quality', '%s' % quality, '-optimize', '-progressive', '-outfile', destination, source_path]
    run_command(command)

    original_size = get_file_size(source_path)
    optimize_size = get_file_size(destination)

    logger.debug('quality: %s', quality)
    logger.debug('original filename: %s', filename)
    logger.debug('original size: %3.1f %s', format_bytes(original_size)[0], format_bytes(original_size)[1])
    logger.debug('content-type: %s', content_type)

    logger.debug('optimize filename: %s', destination)
    logger.debug('optimize size: %3.1f %s', format_bytes(optimize_size)[0], format_bytes(original_size)[1])
    logger.debug('%.0f%% smaller', 100 - ((float(optimize_size) / float(original_size)) * 100))

    buffer_image = get_buffer_from_file(destination)

    return {
        'filename': filename, 
        'quality': quality,
        'progressive': True,
        'library': 'mozjpeg',
        'extension': extension, 
        'content_type': content_type,
        'size': optimize_image,
        'image': buffer_image,
    }
