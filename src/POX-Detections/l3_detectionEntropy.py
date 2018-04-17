import os
import datetime
from pox.core import core
import pox

from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.recoco import Timer

import pox.openflow.libopenflow_01 as of

from pox.lib.revent import *
import itertools 
import time

from .detectionUsingEntropy import Entropy

diction = {}
ent_obj = Entropy()   
set_Timer = False     
defendDDOS=False      

log = core.getLogger() 
FLOW_IDLE_TIMEOUT = 10   
ARP_TIMEOUT = 60 * 2    
MAX_BUFFERED_PER_IP = 5      
MAX_BUFFER_TIME = 5

class Entry (object):
  def __init__ (self, port, mac):
    self.timeout = time.time() + ARP_TIMEOUT
    self.port = port
    self.mac = mac

  def __eq__ (self, other):
    if type(other) == tuple:
      return (self.port,self.mac)==other
    else:
      return (self.port,self.mac)==(other.port,other.mac)
  def __ne__ (self, other):
    return not self.__eq__(other)

  def isExpired (self):
    if self.port == of.OFPP_NONE: return False
    return time.time() > self.timeout

def dpid_to_mac (dpid):
  return EthAddr("%012x" % (dpid & 0xffFFffFFffFF,))

class l3_switch (EventMixin):
  def __init__ (self, fakeways = [], arp_for_unknowns = False, wide = False):
    self.fakeways = set(fakeways)

    self.wide = wide

    self.arp_for_unknowns = arp_for_unknowns

    self.outstanding_arps = {}

    self.lost_buffers = {}

    self.arpTable = {}

    self._expire_timer = Timer(5, self._handle_expiration, recurring=True)

    core.listen_to_dependencies(self)

  def _handle_expiration (self):
    empty = []
    for k,v in self.lost_buffers.iteritems():
      dpid,ip = k

      for item in list(v):
        expires_at,buffer_id,in_port = item
        if expires_at < time.time():
          v.remove(item)
          po = of.ofp_packet_out(buffer_id = buffer_id, in_port = in_port)
          core.openflow.sendToDPID(dpid, po)
      if len(v) == 0: empty.append(k)
  
    for k in empty:
      del self.lost_buffers[k]

  def _send_lost_buffers (self, dpid, ipaddr, macaddr, port):
    if (dpid,ipaddr) in self.lost_buffers:
      bucket = self.lost_buffers[(dpid,ipaddr)]
      del self.lost_buffers[(dpid,ipaddr)]
      log.debug("Sending %i buffered packets to %s from %s"
                % (len(bucket),ipaddr,dpid_to_str(dpid)))
      for _,buffer_id,in_port in bucket:
        po = of.ofp_packet_out(buffer_id=buffer_id,in_port=in_port)
        po.actions.append(of.ofp_action_dl_addr.set_dst(macaddr))
        po.actions.append(of.ofp_action_output(port = port))
        core.openflow.sendToDPID(dpid, po)

  def _handle_openflow_PacketIn (self, event):
    dpid = event.connection.dpid
    inport = event.port
    packet = event.parsed
    global set_Timer
    global defendDDOS
    global blockPort
    timerSet =False
    global diction
    def preventing():
      global diction
      global set_Timer
      if not set_Timer:
        set_Timer =True

      if len(diction) == 0:
        print("Empty diction ",str(event.connection.dpid), str(event.port))
        diction[event.connection.dpid] = {}
        diction[event.connection.dpid][event.port] = 1
      elif event.connection.dpid not in diction:
        diction[event.connection.dpid] = {}
        diction[event.connection.dpid][event.port] = 1
      else:
        if event.connection.dpid in diction:
          if event.port in diction[event.connection.dpid]:
            temp_count=0
            temp_count =diction[event.connection.dpid][event.port]
            temp_count = temp_count+1
            diction[event.connection.dpid][event.port]=temp_count
            #print "*****************************************************************************************************************************************************************************"
            print "dpid port and its packet count: ",  str(event.connection.dpid), str(diction[event.connection.dpid]), str(diction[event.connection.dpid][event.port])
            #print "*****************************************************************************************************************************************************************************"
          else:
            diction[event.connection.dpid][event.port] = 1
    
    def _timer_func ():
      global diction
      global set_Timer
      
      if set_Timer==True:
        for k,v in diction.iteritems():
          for i,j in v.iteritems():
            if j >=5:
              print "_____________________________________________________________________________________________"
              print "\n                               DDOS DETECTED                                              \n"
              print "\n",str(diction)
              print "\n",datetime.datetime.now(),": BLOCKED PORT NUMBER  : ", str(i), " OF SWITCH ID: ", str(k)
              print "\n___________________________________________________________________________________________"
              os._exit(0)
              dpid = k
              msg = of.ofp_packet_out(in_port=i)
              core.openflow.sendToDPID(dpid,msg)          
      diction={}
    
    if not packet.parsed:
      log.warning("%i %i ignoring unparsed packet", dpid, inport)
      return

    if dpid not in self.arpTable:
      self.arpTable[dpid] = {}
      for fake in self.fakeways:
        self.arpTable[dpid][IPAddr(fake)] = Entry(of.OFPP_NONE,
         dpid_to_mac(dpid))

    if packet.type == ethernet.LLDP_TYPE:
      return

    if isinstance(packet.next, ipv4):
      log.debug("%i %i IP %s => %s", dpid,inport, packet.next.srcip,packet.next.dstip)
      ent_obj.collectStats(event.parsed.next.dstip)
      print "Entropy : ",str(ent_obj.value)
      if ent_obj.value <1.0:
        preventing()
        if timerSet is not True:
         Timer(1, _timer_func, recurring=True)
         timerSet=False
      else:
        timerSet=False

      self._send_lost_buffers(dpid, packet.next.srcip, packet.src, inport)

      if packet.next.srcip in self.arpTable[dpid]:
        if self.arpTable[dpid][packet.next.srcip] != (inport, packet.src):
          log.info("%i %i RE-learned %s", dpid,inport,packet.next.srcip)
          if self.wide:
            msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
            msg.match.nw_dst = packet.next.srcip
            msg.match.dl_type = ethernet.IP_TYPE
            event.connection.send(msg)
      else:
        log.debug("%i %i learned %s", dpid,inport,packet.next.srcip)
      self.arpTable[dpid][packet.next.srcip] = Entry(inport, packet.src)

      dstaddr = packet.next.dstip
      if dstaddr in self.arpTable[dpid]:

        prt = self.arpTable[dpid][dstaddr].port
        mac = self.arpTable[dpid][dstaddr].mac
        if prt == inport:
          log.warning("%i %i not sending packet for %s back out of the "
                      "input port" % (dpid, inport, dstaddr))
        else:
          log.debug("%i %i installing flow for %s => %s out port %i"
                    % (dpid, inport, packet.next.srcip, dstaddr, prt))

          actions = []
          actions.append(of.ofp_action_dl_addr.set_dst(mac))
          actions.append(of.ofp_action_output(port = prt))
          if self.wide:
            match = of.ofp_match(dl_type = packet.type, nw_dst = dstaddr)
          else:
            match = of.ofp_match.from_packet(packet, inport)

          msg = of.ofp_flow_mod(command=of.OFPFC_ADD,
                                idle_timeout=FLOW_IDLE_TIMEOUT,
                                hard_timeout=of.OFP_FLOW_PERMANENT,
                                buffer_id=event.ofp.buffer_id,
                                actions=actions,
                                match=match)
          event.connection.send(msg.pack())
      elif self.arp_for_unknowns:
        if (dpid,dstaddr) not in self.lost_buffers:
          self.lost_buffers[(dpid,dstaddr)] = []
        bucket = self.lost_buffers[(dpid,dstaddr)]
        entry = (time.time() + MAX_BUFFER_TIME,event.ofp.buffer_id,inport)
        bucket.append(entry)
        while len(bucket) > MAX_BUFFERED_PER_IP: del bucket[0]

        self.outstanding_arps = {k:v for k,v in
         self.outstanding_arps.iteritems() if v > time.time()}

        if (dpid,dstaddr) in self.outstanding_arps:
          return

        self.outstanding_arps[(dpid,dstaddr)] = time.time() + 4

        r = arp()
        r.hwtype = r.HW_TYPE_ETHERNET
        r.prototype = r.PROTO_TYPE_IP
        r.hwlen = 6
        r.protolen = r.protolen
        r.opcode = r.REQUEST
        r.hwdst = ETHER_BROADCAST
        r.protodst = dstaddr
        r.hwsrc = packet.src
        r.protosrc = packet.next.srcip
        e = ethernet(type=ethernet.ARP_TYPE, src=packet.src,
                     dst=ETHER_BROADCAST)
        e.set_payload(r)
        log.debug("%i %i ARPing for %s on behalf of %s" % (dpid, inport,
         r.protodst, r.protosrc))
        msg = of.ofp_packet_out()
        msg.data = e.pack()
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        msg.in_port = inport
        event.connection.send(msg)

    elif isinstance(packet.next, arp):
      a = packet.next
      log.debug("%i %i ARP %s %s => %s", dpid, inport,
       {arp.REQUEST:"request",arp.REPLY:"reply"}.get(a.opcode,
       'op:%i' % (a.opcode,)), a.protosrc, a.protodst)

      if a.prototype == arp.PROTO_TYPE_IP:
        if a.hwtype == arp.HW_TYPE_ETHERNET:
          if a.protosrc != 0:

            if a.protosrc in self.arpTable[dpid]:
              if self.arpTable[dpid][a.protosrc] != (inport, packet.src):
                log.info("%i %i RE-learned %s", dpid,inport,a.protosrc)
                if self.wide:
                  msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
                  msg.match.dl_type = ethernet.IP_TYPE
                  msg.match.nw_dst = a.protosrc
                  event.connection.send(msg)
            else:
              log.debug("%i %i learned %s", dpid,inport,a.protosrc)
            self.arpTable[dpid][a.protosrc] = Entry(inport, packet.src)

            self._send_lost_buffers(dpid, a.protosrc, packet.src, inport)

            if a.opcode == arp.REQUEST:

              if a.protodst in self.arpTable[dpid]:

                if not self.arpTable[dpid][a.protodst].isExpired():

                  r = arp()
                  r.hwtype = a.hwtype
                  r.prototype = a.prototype
                  r.hwlen = a.hwlen
                  r.protolen = a.protolen
                  r.opcode = arp.REPLY
                  r.hwdst = a.hwsrc
                  r.protodst = a.protosrc
                  r.protosrc = a.protodst
                  r.hwsrc = self.arpTable[dpid][a.protodst].mac
                  e = ethernet(type=packet.type, src=dpid_to_mac(dpid),
                               dst=a.hwsrc)
                  e.set_payload(r)
                  log.debug("%i %i answering ARP for %s" % (dpid, inport,
                   r.protosrc))
                  msg = of.ofp_packet_out()
                  msg.data = e.pack()
                  msg.actions.append(of.ofp_action_output(port =
                                                          of.OFPP_IN_PORT))
                  msg.in_port = inport
                  event.connection.send(msg)
                  return

      log.debug("%i %i flooding ARP %s %s => %s" % (dpid, inport,
       {arp.REQUEST:"request",arp.REPLY:"reply"}.get(a.opcode,
       'op:%i' % (a.opcode,)), a.protosrc, a.protodst))

      msg = of.ofp_packet_out(in_port = inport, data = event.ofp,
          action = of.ofp_action_output(port = of.OFPP_FLOOD))
      event.connection.send(msg)

def launch (fakeways="", arp_for_unknowns=None, wide=False):
  fakeways = fakeways.replace(","," ").split()
  fakeways = [IPAddr(x) for x in fakeways]
  if arp_for_unknowns is None:
    arp_for_unknowns = len(fakeways) > 0
  else:
    arp_for_unknowns = str_to_bool(arp_for_unknowns)
  core.registerNew(l3_switch, fakeways, arp_for_unknowns, wide)
  
