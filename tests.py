import unittest
from optimize_image.utils.images import optimize_image
from PIL import Image


class OptimizeImageTestCase(unittest.TestCase):
    def test_optimize_image_from_source_path(self):
        test_path = 'test/diseno-y-estrategia-de-packaging.jpeg'
        test_quality = 80
        image_optimized = optimize_image(source_path=test_path, quality=80)
        self.assertEqual(isinstance(image_optimized['image'], Image.Image), True)
        self.assertEqual(image_optimized['filename'], 'diseno-y-estrategia-de-packaging')
        self.assertEqual(image_optimized['quality'], 80)
        self.assertEqual(image_optimized['progressive'], True)
        self.assertEqual(image_optimized['extension'], '.jpeg')
        self.assertEqual(image_optimized['content_type'], 'image/jpeg')
        self.assertEqual(image_optimized['library'], 'mozjpeg')

    def test_optimize_image_from_image(self):
        test_path = 'test/diseno-y-estrategia-de-packaging.jpeg'
        test_filename = 'diseno-y-estrategia-de-packaging.jpeg'
        test_quality = 80
        image = Image.open(test_path)
        image_optimized = optimize_image(image=image, filename=test_filename, quality=80)
        self.assertEqual(isinstance(image_optimized['image'], Image.Image), True)
        self.assertEqual(image_optimized['filename'], 'diseno-y-estrategia-de-packaging')
        self.assertEqual(image_optimized['quality'], 80)
        self.assertEqual(image_optimized['progressive'], True)
        self.assertEqual(image_optimized['extension'], '.jpeg')
        self.assertEqual(image_optimized['content_type'], 'image/jpeg')
        self.assertEqual(image_optimized['library'], 'mozjpeg')


if __name__ == '__main__':
    unittest.main()
