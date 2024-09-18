from django.test import TestCase

class FirstTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_equal(self):
        self.assertEqual(1, 1)