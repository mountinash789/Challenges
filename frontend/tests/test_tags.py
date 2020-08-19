from django.test import TestCase

from frontend.templatetags.formatting import decode_plotline


class FormattingTagsTestCase(TestCase):

    def test_decode_plotline_with_none(self):
        plotline = None
        self.assertEquals(None, decode_plotline(plotline))

    def test_decode_plotline(self):
        plotline = 'this\\is\\a\\test'
        self.assertEquals('this\\\\is\\\\a\\\\test', decode_plotline(plotline))
