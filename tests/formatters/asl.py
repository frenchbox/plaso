#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Apple System Log (ASL) event formatter."""

import unittest

from plaso.formatters import asl

from tests.formatters import test_lib


class ASLFormatterTest(test_lib.EventFormatterTestCase):
  """Tests for the Apple System Log (ASL) log event formatter."""

  def testInitialization(self):
    """Tests the initialization."""
    event_formatter = asl.ASLFormatter()
    self.assertIsNotNone(event_formatter)

  def testGetFormatStringAttributeNames(self):
    """Tests the GetFormatStringAttributeNames function."""
    event_formatter = asl.ASLFormatter()

    expected_attribute_names = [
        u'message_id', u'level', u'user_sid', u'group_id', u'read_uid',
        u'read_gid', u'computer_name', u'sender', u'facility', u'message',
        u'extra_information']

    self._TestGetFormatStringAttributeNames(
        event_formatter, expected_attribute_names)

  # TODO: add test for GetMessages.


if __name__ == '__main__':
  unittest.main()
