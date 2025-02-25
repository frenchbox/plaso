#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for Keychain password database parser."""

import unittest

from plaso.formatters import mac_keychain as _  # pylint: disable=unused-import
from plaso.lib import eventdata
from plaso.lib import timelib
from plaso.parsers import mac_keychain

from tests.parsers import test_lib


class MacKeychainParserTest(test_lib.ParserTestCase):
  """Tests for keychain file parser."""

  def setUp(self):
    """Makes preparations before running an individual test."""
    self._parser = mac_keychain.KeychainParser()

  def testParse(self):
    """Tests the Parse function."""
    test_file = self._GetTestFilePath([u'login.keychain'])
    event_queue_consumer = self._ParseFile(self._parser, test_file)
    event_objects = self._GetEventObjectsFromQueue(event_queue_consumer)

    self.assertEqual(len(event_objects), 5)

    event_object = event_objects[0]

    expected_timestamp = timelib.Timestamp.CopyFromString(
        u'2014-01-26 14:51:48')
    self.assertEqual(event_object.timestamp, expected_timestamp)

    self.assertEqual(
        event_object.timestamp_desc,
        eventdata.EventTimestamp.CREATION_TIME)
    self.assertEqual(event_object.entry_name, u'Secret Application')
    self.assertEqual(event_object.account_name, u'moxilo')
    expected_ssgp = (
        u'b8e44863af1cb0785b89681d22e2721997ccfb8adb8853e726aff94c8830b05a')
    self.assertEqual(event_object.ssgp_hash, expected_ssgp)
    self.assertEqual(event_object.text_description, u'N/A')
    expected_msg = u'Name: Secret Application Account: moxilo'
    expected_msg_short = u'Secret Application'
    self._TestGetMessageStrings(event_object, expected_msg, expected_msg_short)
    event_object = event_objects[1]
    self.assertEqual(
        event_object.timestamp_desc,
        eventdata.EventTimestamp.MODIFICATION_TIME)

    expected_timestamp = timelib.Timestamp.CopyFromString(
        u'2014-01-26 14:52:29')
    self.assertEqual(event_object.timestamp, expected_timestamp)

    event_object = event_objects[2]

    expected_timestamp = timelib.Timestamp.CopyFromString(
        u'2014-01-26 14:53:29')
    self.assertEqual(event_object.timestamp, expected_timestamp)

    self.assertEqual(event_object.entry_name, u'Secret Note')
    self.assertEqual(event_object.text_description, u'secure note')
    self.assertEqual(len(event_object.ssgp_hash), 1696)
    expected_msg = u'Name: Secret Note'
    expected_msg_short = u'Secret Note'
    self._TestGetMessageStrings(event_object, expected_msg, expected_msg_short)

    event_object = event_objects[3]

    expected_timestamp = timelib.Timestamp.CopyFromString(
        u'2014-01-26 14:54:33')
    self.assertEqual(event_object.timestamp, expected_timestamp)

    self.assertEqual(event_object.entry_name, u'plaso.kiddaland.net')
    self.assertEqual(event_object.account_name, u'MrMoreno')
    expected_ssgp = (
        u'83ccacf55a8cb656d340ec405e9d8b308fac54bb79c5c9b0219bd0d700c3c521')
    self.assertEqual(event_object.ssgp_hash, expected_ssgp)
    self.assertEqual(event_object.where, u'plaso.kiddaland.net')
    self.assertEqual(event_object.protocol, u'http')
    self.assertEqual(event_object.type_protocol, u'dflt')
    self.assertEqual(event_object.text_description, u'N/A')

    expected_msg = (
        u'Name: plaso.kiddaland.net '
        u'Account: MrMoreno '
        u'Where: plaso.kiddaland.net '
        u'Protocol: http (dflt)')
    expected_msg_short = u'plaso.kiddaland.net'
    self._TestGetMessageStrings(event_object, expected_msg, expected_msg_short)


if __name__ == '__main__':
  unittest.main()
