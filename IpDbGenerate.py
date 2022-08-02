#!/usr/bin/env python

"""Generate the ipdb for Python."""

import pprint
from operator import itemgetter
from socket import inet_aton
from struct import unpack
from urllib import urlopen
import sys

pp = pprint.PrettyPrinter(indent=4, width=50)
iplist = {}


if len(sys.argv) > 1:
    fp = open(sys.argv[1], 'r')
else:
    # fetch remote datacenter list and convert to searchable datastructure
    external_list = \
        'https://raw.github.com/client9/ipcat/master/datacenters.csv'
    fp = urlopen(external_list)

fp.readline()
for line in fp:
    line = line.strip()
    if not line or line[0] == '#':
        continue

    parts = line.split(",")
    newrow = (
        unpack("!L", inet_aton(parts[0]))[0],
        unpack("!L", inet_aton(parts[1]))[0],
        parts[3],
    )
    iplist[newrow[0]] = newrow

# return the list of entries, sorted by the lowest ip in the range
iplist = tuple(v for (k, v) in sorted(iplist.iteritems(),
                                      key=itemgetter(0)))
