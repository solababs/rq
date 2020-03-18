# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import dill
from rq.serializers import resolve_serializer, DefaultSerializer, CustomSerializer

try:
    import unittest
except ImportError:
    import unittest2 as unittest  # noqa


class TestSerializers(unittest.TestCase):
    def test_resolve_serializer(self):
        """Ensure function parse_timeout works correctly"""
        serializer = resolve_serializer(None)
        self.assertIsNotNone(serializer)
        self.assertIsInstance(serializer, DefaultSerializer)

        self.assertTrue(hasattr(serializer, 'serialize'))
        self.assertTrue(hasattr(serializer, 'deserialize'))

        serializer = resolve_serializer(dill)
        self.assertIsNotNone(serializer)
        self.assertIsInstance(serializer, CustomSerializer)

        self.assertTrue(hasattr(serializer, 'serialize'))
        self.assertTrue(hasattr(serializer, 'deserialize'))
