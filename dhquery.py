#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
# vim:tabstop=2

from random import Random
from optparse import OptionParser
from pydhcplib.dhcp_packet import DhcpPacket
from pydhcplib.dhcp_network import DhcpClient
from pydhcplib.type_hw_addr import hwmac
from pydhcplib.type_ipv4 import ipv4
import socket

r = Random()
r.seed()

dhcpTypes = {
	1: 'DISCOVER',
	2: 'OFFER',
	3: 'REQUEST',
	4: 'DECLINE',
	5: 'ACK',
	6: 'NACK',
	7: 'RELEASE',
	8: 'INFORM',

}

class SilentClient(DhcpClient):
	
	def HandleDhcpAck(self,p):
		return
	
	def HandleDhcpNack(self,p):
		return
	
	def HandleDhcpOffer(self,p):
		return
	
	def HandleDhcpUnknown(self,p):
		return
	
def genxid():
	decxid = r.randint(0,0xffffffff)
	xid = []
	for i in xrange(4):
		xid.insert(0, decxid & 0xff)
		decxid = decxid >> 8
	return xid

def receivePacket(serverip, serverport, timeout, req):
	server = SilentClient(client_listen_port=67, server_listen_port=serverport)
	server.dhcp_socket.settimeout(timeout)
	if serverip == '0.0.0.0': req.SetOption('flags',[128, 0])
	server.SendDhcpPacketTo(serverip,req)
	if req.GetOption('dhcp_message_type')[0] in [7,]:
		return None
	return server.GetNextDhcpPacket()

def preparePacket(xid=None,giaddr='0.0.0.0',chaddr='00:00:00:00:00:00',ciaddr='0.0.0.0',msgtype='discover',required_opts=[]):
	req = DhcpPacket()
	req.SetOption('op',[1])
	req.SetOption('htype',[1])
	req.SetOption('hlen',[6])
	req.SetOption('hops',[0])
	if not xid: xid = genxid()
	req.SetOption('xid',xid)
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
#	req.SetOption('parameter_request_list',1)
	return req


def main():
	parser =  OptionParser()
	parser.add_option("-s","--server", dest="server", help="DHCP server IP")
	parser.add_option("-p","--port", type="int", dest="port", default=67, help="DHCP server port")
	parser.add_option("-m","--mac","--chaddr", dest="chaddr", default='00:00:00:00:00:00', help="chaddr: Client's MAC address")
	parser.add_option("-c","--ciaddr", dest="ciaddr", default='0.0.0.0', help="ciaddr: Client's desired IP address")
	parser.add_option("-g","--giaddr", dest="giaddr", default='0.0.0.0', help="giaddr: Gateway IP address (if any)")
	parser.add_option("-t","--type", dest="msgtype", type="choice", choices=["discover","request","release"],
			default="discover", help="DHCP message type: discover, request, release (default %default)")
	parser.add_option("-w","--timeout", dest="timeout", type="int", default=4, help="UDP timeout (default %default)")
	parser.add_option("-r","--require", action="append", type="int", default=[1,3,6,51], dest="required_opts", help="Require options by its number")
	parser.add_option("-v","--verbose", action="store_true", dest="verbose", help="Verbose operation")
	parser.add_option("-q","--quiet", action="store_false", dest="verbose", help="Quiet operation")
	parser.add_option("-y","--cycle", action="store_true", dest="docycle", help="Do full cycle: DISCOVERY, REQUEST, RELEASE")
	parser.add_option("-n","--cycles", dest="cycles", type="int", default="1", help="Do submitten number of cycles")
	(opts, args) = parser.parse_args()
	verbose = opts.verbose

	if opts.docycle:
		request_dhcp_message_type = "discover"
	else:
		request_dhcp_message_type = opts.msgtype

	request_ciaddr = opts.ciaddr 
	serverip = opts.server 
	cycleno = 1
	
	while True:
		
		if opts.verbose is not False:
			print "="*100
			print "| Cycle %s"%cycleno
			print "="*100

		req = preparePacket(giaddr=opts.giaddr, chaddr=opts.chaddr, ciaddr=request_ciaddr, msgtype=request_dhcp_message_type, required_opts=opts.required_opts)
		if verbose != False:
			print "Sending %s [%s] packet to %s"%(request_dhcp_message_type.upper(),opts.chaddr, opts.server)
		if verbose == True:
			print "-"*100
			req.PrintHeaders()
			req.PrintOptions()
			print "="*100
			print "\n"
		
		try:
			res = receivePacket(serverip=serverip, serverport=opts.port, timeout=opts.timeout, req=req)
		except socket.timeout:
			res = None
			if verbose != False: print "Timed out."
			pass
	
		if res:
			dhcp_message_type = res.GetOption('dhcp_message_type')[0]
			server_identifier = ipv4(res.GetOption('server_identifier'))
			chaddr = hwmac(res.GetOption('chaddr')[:6])
			yiaddr = ipv4(res.GetOption('yiaddr'))
	
			if verbose != False:
				print "Received %s packet from %s; [%s] was bound to %s"%(dhcpTypes.get(dhcp_message_type,'UNKNOWN'), server_identifier, chaddr, yiaddr )
			if verbose == True:
				print "-"*100
				res.PrintHeaders()
				res.PrintOptions()
				print "="*100
				print "\n"

			if opts.docycle:
				if dhcp_message_type == 2:
					request_dhcp_message_type = 'request'
					request_ciaddr = yiaddr.str()
					serverip = server_identifier.str()
					continue
				
				if dhcp_message_type == 5:
					request_dhcp_message_type = 'release'
					request_ciaddr = yiaddr.str()
					serverip = server_identifier.str()
					continue
		
		cycleno += 1
		if cycleno > opts.cycles:
				break
		

		if opts.docycle:
			request_dhcp_message_type = 'discovery'
			request_ciaddr = opts.ciaddr 
			serverip = opts.server 


if __name__ == '__main__':
	main()



