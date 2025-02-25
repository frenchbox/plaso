#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the JSON output module."""

import json
import os
import sys
import unittest

from plaso.lib import timelib
from plaso.output import json_out

from tests.cli import test_lib as cli_test_lib
from tests.output import test_lib


class JSONOutputTest(test_lib.OutputModuleTestCase):
  """Tests for the JSON output module."""

  def setUp(self):
    """Makes preparations before running an individual test."""
    output_mediator = self._CreateOutputMediator()
    self._output_writer = cli_test_lib.TestOutputWriter()
    self._output_module = json_out.JSONOutputModule(output_mediator)
    self._output_module.SetOutputWriter(self._output_writer)
    self._event_object = test_lib.TestEventObject()

  def testWriteHeader(self):
    """Tests the WriteHeader function."""
    expected_header = b'{'

    self._output_module.WriteHeader()

    header = self._output_writer.ReadOutput()
    self.assertEqual(header, expected_header)

  def testWriteFooter(self):
    """Tests the WriteFooter function."""
    expected_footer = b'}'

    self._output_module.WriteFooter()

    footer = self._output_writer.ReadOutput()
    self.assertEqual(footer, expected_footer)

  def testWriteEventBody(self):
    """Tests the WriteEventBody function."""
    self._output_module.WriteEventBody(self._event_object)

    # The dict comparison is very picky on Windows hence we
    # have to make sure the UUID is a Unicode string.
    expected_uuid = u'{0:s}'.format(self._event_object.uuid)
    expected_timestamp = timelib.Timestamp.CopyFromString(
        u'2012-06-27 18:17:01')

    if sys.platform.startswith(u'win'):
      # The dict comparison is very picky on Windows hence we
      # have to make sure the drive letter is in the same case.
      expected_os_location = os.path.abspath(u'\\{0:s}'.format(
          os.path.join(u'cases', u'image.dd')))
    else:
      expected_os_location = u'{0:s}{1:s}'.format(
          os.path.sep, os.path.join(u'cases', u'image.dd'))

    expected_json_dict = {
        u'event_0': {
            u'__type__': u'EventObject',
            u'data_type': u'test:output',
            u'display_name': u'OS: /var/log/syslog.1',
            u'hostname': u'ubuntu',
            'inode': 12345678,
            'pathspec': {
                u'__type__': u'PathSpec',
                u'type_indicator': u'TSK',
                u'location': u'/var/log/syslog.1',
                u'inode': 15,
                u'parent': {
                    u'__type__': u'PathSpec',
                    u'type_indicator': u'OS',
                    u'location': expected_os_location,
                }
            },
            u'text': (
                u'Reporter <CRON> PID: |8442| (pam_unix(cron:session): '
                u'session\n closed for user root)'),
            u'timestamp': expected_timestamp,
            u'username': u'root',
            u'uuid': expected_uuid
        }
    }
    event_body = self._output_writer.ReadOutput()

    # We need to compare dicts since we cannot determine the order
    # of values in the string.
    json_string = u'{{ {0:s} }}'.format(event_body)
    json_dict = json.loads(json_string)
    self.assertEqual(json_dict, expected_json_dict)


if __name__ == '__main__':
  unittest.main()
