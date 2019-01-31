#!/usr/bin/env python
import sys
import logging
from utils.images import optimize_image

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    quality = sys.argv[2] if len(sys.argv) >= 3 else 80
    optimize_image = optimize_image(sys.argv[1], quality)
    image = optimize_image['image']
    image.save('%s%s' % (optimize_image['filename'], optimize_image['extension']))
