#!/usr/bin/python
# coding:utf-8
# https://github.com/MtimerCMS/SublimeText-Google-Translate-Plugin

import urllib2
import httplib
import st2_socks
import ssl

class SocksiPyConnection_old(httplib.HTTPConnection):
    def __init__(self, proxytype, proxyaddr, proxyport=None, rdns=True, username=None, password=None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = st2_socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if type(self.timeout) in (int, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

class SocksiPyConnectionS_old(httplib.HTTPSConnection):
    def __init__(self, proxytype, proxyaddr, proxyport=None, rdns=True, username=None, password=None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = st2_socks.socksocket()
        sock.setproxy(*self.proxyargs)
        if type(self.timeout) in (int, float):
            sock.settimeout(self.timeout)
        sock.connect((self.host, self.port))
        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)
            
class SocksiPyHandler_old(urllib2.HTTPHandler, urllib2.HTTPSHandler):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        urllib2.HTTPHandler.__init__(self)

    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):    
            conn = SocksiPyConnection_old(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)

    def https_open(self, req):
        def build(host, port=None, strict=None, timeout=0):    
            conn = SocksiPyConnectionS_old(*self.args, host=host, port=port, strict=strict, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)