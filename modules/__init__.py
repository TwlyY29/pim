#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, sys, importlib

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

__filepath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__filepath)

__themodules = list(filter(lambda p: os.path.isdir(os.path.join(__filepath,p)) and not '__pycache__' in p, os.listdir(__filepath)))

del __filepath

def handle(key,msg):
  if key not in __themodules:
    eprint("module '{}' not installed".format(key))
    return False
  
  _themod = importlib.import_module(key)
  _themod = importlib.import_module('.handle',key)
  return _themod.handle(msg, isreply = False)


def handlereply(key,msg):
  for k in __themodules:
    if k in key:
      _themod = importlib.import_module(key)
      if _themod.HANDLER_ACCEPTS_REPLY:
        _themod = importlib.import_module('.handle',key)
        return _themod.handle(msg, True)
      else:
        eprint("found module '{}' in key '{}' but module doesn't accept replys".format(k,key))
        return False
  return False
        
      
