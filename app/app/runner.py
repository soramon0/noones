import logging

from django.test.runner import DiscoverRunner


class TestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        # Disbale logging for tests
        logging.disable(logging.CRITICAL)
        return super().run_tests(test_labels, extra_tests=extra_tests, **kwargs)
