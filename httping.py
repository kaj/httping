#! /usr/bin/env python
# -*- encoding: utf-8 -*-
description = """
A simple utility to periodically measure time to access a few urls.
"""
from optparse import OptionParser
from datetime import datetime
from urllib2 import urlopen
from re import sub
from time import time, sleep
from socket import socket
from sys import exit

opt = OptionParser(usage='usage: %prog [options] url ...',
                 description=description)
opt.add_option('--base', dest='base', default='httping',
               help='Prefix for metric series name [%default]')
opt.add_option('-v', '--verbose', dest='verbose', action='store_true')
opt.add_option('-n', '--nocarbon', dest='nocarbon', action='store_true',
               help='Disable carbon, only show measurments on stdout')
opt.add_option('--server', dest='server', default='localhost',
               help='Carbon server to send messages to [%default]')
opt.add_option('--port', dest='port', default=2003,
               help='Carbon port to send messages to [%default]')
opt.add_option('--delay', dest='delay', default=60,
               help='Seconds to wait between measurments [%default]')
(options, urls) = opt.parse_args()

def openCarbon():
    if options.nocarbon:
        return None
    try:
        sock.connect( (options.server,options.port) )
    except:
        print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':options.server, 'port':options.port }
        exit(1)

sock = openCarbon()

def getname(url):
    '''Get time series name for a given url'''
    return '.'.join(
        sub(r'[^a-z0-9]', '-', s) for s in url.lower().split('/')[1:] if s)

def getstats(urls):
    lines = []
    for url in urls:
        try:
            start = time()
            length = sum(len(row) for row in urlopen(url))
            elapsed = time() - start
            lines.append('%s.%s.%s %s %d' % (options.base, 'time', getname(url),
                                             elapsed, int(start)))
            lines.append('%s.%s.%s %s %s' % (options.base, 'size', getname(url),
                                             length, int(start)))
        except Exception as err:
            print "Failed to get %s: %s" % (url, err)
    return lines

if __name__ == '__main__':
    while True:
        message = '\n'.join(getstats(urls)) + '\n' #all lines must end in a newline
        if options.verbose or not sock:
            print "sending message"
            print '-' * 80
            print message
            print
        if sock:
            sock.sendall(message)
        sleep(options.delay)
