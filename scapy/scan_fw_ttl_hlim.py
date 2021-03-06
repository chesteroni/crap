#!/usr/bin/env python

# $Id$

from scapy.all import conf,sr1,IP,TCP,UDP
import sys
import random
import time

conf.verb = 0

dhost = "157.166."+str(random.randint(1,255))+"."+str(random.randint(1,255)) # This can also be IPv6

maxvalue = 65534
sport = random.randint(1025,65534)

portrange = range(1,maxvalue)
ttl = 2 

allowed = []

# the same can be done for proto
# in that case proto equals port
# and maxvalue = 255
for i in xrange(1,maxvalue):
  port = random.choice(portrange)
  portrange.remove(port)
  #L3 = IPv6(dst=dhost, hlim=ttl)
  L3 = IP(dst=dhost,flags=2,tos=0,ttl=ttl) #proto=port)
  #L4 = UDP(sport=sport,dport=port)
  L4 = TCP(sport=sport,dport=port,flags=2,urgptr=0)
  
  ans = sr1((L3/L4),timeout=0.5)
  if ans:
    if ans.proto == 1 and ans.payload.type == 11 and ans.payload.code == 0:
      print "Allowed port "+str(port)+" to host "+str(dhost)
      allowed.append(port)

  if i % 10 == 0:
    dhost = "157.166."+str(random.randint(1,255))+"."+str(random.randint(1,255))
    sport = random.randint(1025,65534)
    time.sleep(1)

