#!/usr/bin/env python
# encoding: utf-8
"""
constantes.py
"""
from pickle import *
import signal
import sys
from functools import partial
from socket import *


NETWORK_IP      = '127.0.0.1'
NETWORK_PORT    = 12000
EMISOR_IP       = '127.0.0.1'
EMISOR_PORT     = 12001
RECEPTOR_IP     = '127.0.0.1'
RECEPTOR_PORT   = 12002
LONGITUD_UDP	= 1024
TIMEOUT			= 2
SECUENCE_INIT	= 0