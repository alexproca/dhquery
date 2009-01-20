#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
# vim:tabstop=2

from random import Random
from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
from pydhcplib.type_hw_addr import hwmac
from pydhcplib.type_ipv4 import ipv4
from time import sleep
import socket
from optparse import OptionParser

r = Random()
r.seed()


class silentClient(DhcpClient):
	
	def HandleDhcpAck(self,p):
		print "Get ACK fo MAC %s and IP %s"%(str2mac(p.GetOption('chaddr')[:p.GetOption('hlen')[0]]), str2ip(p.GetOption('yiaddr')))
	
	def HandleDhcpNack(self,p):
		print "Get NAK fo MAC %s"%(str2mac(p.GetOption('chaddr')[:p.GetOption('hlen')[0]]))
	
	def HandleDhcpOffer(self,p):
		print "Get OFFER fo MAC %s and IP %s; (%s)"%(str2mac(p.GetOption('chaddr')[:p.GetOption('hlen')[0]]), str2ip(p.GetOption('yiaddr')), str2ascii(p.GetOption('host_name')))
	
	def HandleDhcpUnknown(self,p):
		message_type = ans.GetOption('dhcp_message_type')[0]
		if message_type == 13:
			print "Get LEASEACTIVE fo MAC %s and IP %s; (%s)"%(str2mac(p.GetOption('chaddr')[:p.GetOption('hlen')[0]]), str2ip(p.GetOption('yiaddr')), str2ascii(p.GetOption('host_name')))
		if message_type == 11:
			print "Get LEASEUNASSIGNED fo MAC %s and IP %s; (%s)"%(str2mac(p.GetOption('chaddr')[:p.GetOption('hlen')[0]]), str2ip(p.GetOption('yiaddr')), str2ascii(p.GetOption('host_name')))
		if message_type == 12:
			print "Get LEASEUNKNOWN fo MAC %s"%(str2mac(p.GetOption('chaddr')[:p.GetOption('hlen')[0]]))
	

#server = silentClient(client_listen_port=67, server_listen_port=67)
#server.dhcp_socket.settimeout(4)
#server_ip = '192.168.133.94'


def gethostname():
	hn = []
	for i in xrange(r.randint(2,8)):
		ch = r.randint(97,122)
		hn.append(ch)
	return hn + [0]

def getmac():
	mac = r.randint(0x0, 0xffffffffffff)
	m = []
	for i in xrange(6):
		m.insert(0,mac & 0xff)
		mac = mac >> 8
	return m
		

def str2mac(l):
	return ':'.join(map(lambda x:"%x"%int(x),l))

def str2ip(l):
	return '.'.join(map(str,l))

def str2ascii(l):
	return ''.join(map(chr,l))


def sendLeaseQuery(mac):
	req = DhcpPacket()
	req.SetOption('op',[1])
	req.SetOption('htype',[1])
	req.SetOption('hlen',[6])
	req.SetOption('hops',[1])
	req.SetOption('xid',getxid())
#	req.SetOption('giaddr',[172,22,12,2])
	req.SetOption('ciaddr',[192,168,133,100])
	req.SetOption('chaddr', mac + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	req.SetOption('dhcp_message_type',[10])
	server.SendDhcpPacketTo(server_ip,req)
	try:
		ans = server.GetNextDhcpPacket()
	except socket.timeout:
		print "Timeout"

#while True:
#	for mac in macs:
#		req = DhcpPacket()
#		req.SetOption('op',[1])
#		req.SetOption('htype',[1])
#		req.SetOption('hlen',[6])
#		req.SetOption('hops',[1])
#		req.SetOption('xid',getxid())
#		req.SetOption('giaddr',[172,22,12,2])
#		req.SetOption('chaddr', mac[0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
#		req.SetOption('host_name',mac[3])
#		if mac[2]: req.SetOption('ciaddr',mac[2])
#
#		if not mac[2]:
#			# Запрашиваем DHCPDISCOVERY
#			print "Sending DISCOVERY for MAC %s; (%s)"%(str2mac(mac[0]), str2ascii(mac[3]))
#			req.SetOption('dhcp_message_type',[1])
#		elif mac[2] and mac[1] < 20:
#			# Запрашиваем DHCPREQUEST
#			print "Sending REQUEST for MAC %s / IP %s; (%s)"%(str2mac(mac[0]), str2ip(mac[2]), str2ascii(mac[3]))
#			req.SetOption('dhcp_message_type',[3])
#		else:
#			# Запрашиваем DHCPRELEASE (чтоыбы на следующем цикле снова спросить DISCOVERY, чтоб сервер не расслаблялся :) )
#			print "Sending RELEASE for MAC %s / IP %s; (%s)"%(str2mac(mac[0]), str2ip(mac[2]), str2ascii(mac[3]))
#			req.SetOption('dhcp_message_type',[7])
#			mac[1:2] = [0,None]
#
#		server.SendDhcpPacketTo(server_ip,req)
#		try:
#			ans = server.GetNextDhcpPacket()
#		except socket.timeout:
#			print "Timeout"
#			continue
#		
#		if ans.GetOption('dhcp_message_type') == [2]:
#			# Прислали OFFER. Надо не зевать и забить IP адрес REQUEST'ом
#			sleep(0.2)
#			req.SetOption('dhcp_message_type',[3])
#			req.SetOption('ciaddr',ans.GetOption('yiaddr'))
#			server.SendDhcpPacketTo(server_ip,req)
#			print "Sending REQUEST for MAC %s / IP %s; (%s)"%(str2mac(mac[0]), str2ip(ans.GetOption('yiaddr')), str2ascii(mac[3]))
#			try:
#				ans = server.GetNextDhcpPacket()
#			except socket.timeout:
#				print "Timeout"
#				continue
#			if ans.GetOption('dhcp_message_type') == [5]:
#				mac[2] = ans.GetOption('yiaddr')
#		mac[1] += 1
#		packetcount += 1
#		if packetcount > 30:
#			sendLeaseQuery(mac[0])
#			packetcount = 0
#		sleep(0.1)
	

def genxid():
	decxid = r.randint(0,0xffffffff)
	xid = []
	for i in xrange(4):
		xid.insert(0, decxid & 0xff)
		decxid = decxid >> 8
	return xid


def preparePacket(xid=None,giaddr='0.0.0.0',chaddr='00:00:00:00:00:00',ciaddr='0.0.0.0',msgtype='discovery'):
	req = DhcpPacket()
	req.SetOption('op',[1])
	req.SetOption('htype',[1])
	req.SetOption('hlen',[6])
	req.SetOption('hops',[0])
	if not xid: xid = genxid()
	req.SetOption('xid',xid)
	print giaddr
	print chaddr
	req.SetOption('giaddr',ipv4(giaddr).list())
	req.SetOption('chaddr',hwmac(chaddr).list() + [0] * 10)
	req.SetOption('ciaddr',ipv4(ciaddr).list())
	if msgtype == 'request':
		mt = 3
	elif msgtype == 'release':
		mt = 7
	else:
		mt = 1
	req.SetOption('dhcp_message_type',[mt])
	return req


def main():
	parser =  OptionParser()
	parser.add_option("-s","--server", dest="server", help="DHCP server IP")
	parser.add_option("-p","--port", type="int", dest="port", default=67, help="DHCP server port")
	parser.add_option("-m","--mac","--chaddr", dest="chaddr", default='00:00:00:00:00:00', help="chaddr: Client's MAC address")
	parser.add_option("-c","--ciaddr", dest="ciaddr", default='0.0.0.0', help="ciaddr: Client's desired IP address")
	parser.add_option("-g","--giaddr", dest="giaddr", default='0.0.0.0', help="giaddr: Gateway IP address (if any)")
	parser.add_option("-t","--type", dest="msgtype", type="choice", choices=["discovery","request","release"],
			default="discovery", help="DHCP message type: discovery, request, release (default %default)")
	parser.add_option("-w","--timeout", dest="udptimeout", type="int", default=4, help="UDP timeout (default %default)")
	parser.add_option("-y","--cycle", action="store_true", dest="docycle", help="Do full cycle: DISCOVERY, REQUEST, RELEASE")
	parser.add_option("-r","--require", action="append", type="int", dest="required_opts", help="Reuire options by its number")
	(opts, args) = parser.parse_args()
	print opts
	print preparePacket(giaddr=opts.giaddr, chaddr=opts.chaddr, ciaddr=opts.ciaddr, msgtype=opts.msgtype).PrintHeaders()

	#server = silentClient(client_listen_port=67, server_listen_port=67)
	#server.dhcp_socket.settimeout(4)
	#server_ip = '192.168.133.94'

if __name__ == '__main__':
	main()



