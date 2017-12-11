# (c) 2012, Jeroen Hoekx <jeroen@hoekx.be>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import base64
import crypt
import glob
import hashlib
import itertools
import json
import ntpath
import os.path
import re
import string
import sys
import time
import uuid
import yaml

from collections import MutableMapping, MutableSequence
from datetime import datetime
from functools import partial
from random import Random, SystemRandom, shuffle

from jinja2.filters import environmentfilter, do_groupby as _do_groupby

try:
    import passlib.hash
    HAS_PASSLIB = True
except:
    HAS_PASSLIB = False

from ansible import errors
from ansible.module_utils.six import iteritems, string_types, integer_types
from ansible.module_utils.six.moves import reduce, shlex_quote
from ansible.module_utils._text import to_bytes, to_text
from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.utils.hashing import md5s, checksum_s
from ansible.utils.unicode import unicode_wrap
from ansible.utils.vars import merge_hash
from ansible.vars.hostvars import HostVars


UUID_NAMESPACE_ANSIBLE = uuid.UUID('361E6D51-FAEC-444A-9079-341386DA8E2E')


class AnsibleJSONEncoder(json.JSONEncoder):
    '''
    Simple encoder class to deal with JSON encoding of internal
    types like HostVars
    '''
    def default(self, o):
        if isinstance(o, HostVars):
            return dict(o)
        else:
            return super(AnsibleJSONEncoder, self).default(o)

def reverse_upper(string):
    ''' Reverse and upper string. '''
    return string[::-1].upper()


class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
            # reverse_upper
            'reverse_upper': reverse_upper
        }
