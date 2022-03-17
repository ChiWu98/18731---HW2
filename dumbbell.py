# CMU 18731 HW2
# Code referenced from: git@bitbucket.org:huangty/cs144_bufferbloat.git
# Edited by: Soo-Jin Moon, Deepti Sunder Prakash

#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os

# Parse arguments

parser = ArgumentParser(description="Shrew tests")
parser.add_argument('--bw-host', '-B',
                    dest="bw_host",
                    type=float,
                    action="store",
                    help="Bandwidth of host links",
                    required=True)
parser.add_argument('--bw-net', '-b',
                    dest="bw_net",
                    type=float,
                    action="store",
                    help="Bandwidth of network link",
                    required=True)
parser.add_argument('--delay',
                    dest="delay",
                    type=float,
                    help="Delay in milliseconds of host links",
                    default='10ms')
parser.add_argument('--n',
                    dest="n",
                    type=int,
                    action="store",
                    help="Number of nodes in one side of the dumbbell.",
                    required=True)

parser.add_argument('--maxq',
                    dest="maxq",
                    action="store",
                    help="Max buffer size of network interface in packets",
                    default=1000)

# Expt parameters
args = parser.parse_args()

class DumbbellTopo(Topo):
    "Dumbbell topology for Shrew experiment"
    def build(self, n=6, bw_net=10, delay='20ms', bw_host=10, maxq=None):
    #TODO: Add your code to create topology
    # n for number of nodes in one side,
    # bw_net for Bandwidth of network link
     # bw_host for Bandwidth of host link
    # delay for delay

    # add 2 swtich for dumbbell
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        a1 = self.addHost('a1')
        a2 = self.addHost('a2')


    # adding S1 dumbnell hosts
        for h in range(n):
            host = self.addHost('hl%s' % (h + 1))
            self.addLink(host, s1, bw = bw_host,delay = delay, max_queue_size = maxq)
        self.addLink(a1, s1, bw = bw_host,delay = delay, max_queue_size = maxq)
    # adding S2 dumbnell hosts
        for h in range(n):
            host = self.addHost('hr%s' % (h + 1))
            self.addLink(host, s2, bw = bw_host,delay = delay, max_queue_size = maxq)
        self.addLink(a2, s2, bw = bw_host,delay = delay, max_queue_size = maxq)

        self.addLink(s1, s2,  bw = bw_net,delay = delay, max_queue_size = maxq)





	
def bbnet():
    "Create network and run shrew  experiment"
    print "starting mininet ...."
    topo = DumbbellTopo(n=args.n, bw_net=args.bw_net,
                    delay='%sms' % (args.delay),
                    bw_host=args.bw_host, maxq=int(args.maxq))

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink,
                  autoPinCpus=True)
    net.start()
    dumpNodeConnections(net.hosts)

    #TODO: Add your code to test reachability of hosts
    net.pingAll()
    #TODO: Add yoour code to start long lived TCP flows
    hl1, hl2, hr1, hr2, a1, a2 = net.get('hl1', 'hl2','hr1', 'hr2','a1','a2')

    
    
    hl1.cmd("iperf -s -p 5001 -t 500 &")
    hl2.cmd("iperf -s -p 5002 -t 500 &")
    a1.cmd("iperf -s -p 5003 -t 500 &")


    a2.cmd("iperf -c 10.0.0.1 -p 5003  -t 500 -i 1 &")
    hr1.cmd("iperf -c 10.0.0.3 -p 5001 -t 500 -i 1 &")
    hr2.cmd("iperf -c 10.0.0.4 -p 5002 -t 500 -i 1 &")


    #net.iperf( ( hl1, hr1 ), l4Type='TCP' , port = 5001)
    #net.iperf( ( hl2, hr2 ), l4Type='TCP' , port = 5002)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    bbnet()
