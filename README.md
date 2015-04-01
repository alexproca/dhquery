#DHCP command-line query and testing tool 
Automatically exported from [code.google.com/p/dhquery](http://code.google.com/p/dhquery)

##History
I needed some DHCP testing tool for my projects, based on [FreeRADIUS](http://freeradius.org/) dhcp code.

[dhcping](http://c3rb3r.openwall.net/dhcping/) had no DISCOVER packet handling, it couldn't do stress test and didn't allow changing request parameters.

Also, I needed Nagios testing plugin for DHCP cluster testing.

##Features
**dhquery** can send any common packet type, repeat it several times for stress testing or perform cycle testing: **DISCOVER, REQUEST and RELEASE**.

Also it can work as a [Nagios](http://www.nagios.org) plugin.

##Requirements
[Python](http://python.org/) and [pydhcplib](http://pydhcplib.tuxfamily.org/pmwiki/)

Usage

    Usage: dhquery.py [options]
    
    Options:
      -h, --help            show this help message and exit
      -s SERVER, --server=SERVER
                            DHCP server IP (default 0.0.0.0)
      -p PORT, --port=PORT  DHCP server port (default (67)
      -m CHADDR, --mac=CHADDR, --chaddr=CHADDR
                            chaddr: Client's MAC address
      -c CIADDR, --ciaddr=CIADDR
                            ciaddr: Client's desired IP address
      -g GIADDR, --giaddr=GIADDR
                            giaddr: Gateway IP address (if any)
      -t MSGTYPE, --type=MSGTYPE
                            DHCP message type: discover, request, release (default
                            discover)
      -w TIMEOUT, --timeout=TIMEOUT
                            UDP timeout (default 4)
      -r REQUIRED_OPTS, --require=REQUIRED_OPTS
                            Require options by its number
      -y, --cycle           Do full cycle: DISCOVERY, REQUEST, RELEASE
      -n CYCLES, --cycles=CYCLES
                            Do number of cycles (default 1)
      -v, --verbose         Verbose operation
      -q, --quiet           Quiet operation
      --nagios              Nagios mode of operation
