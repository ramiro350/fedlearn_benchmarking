#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8',
                   listenPort=5000)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    # h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    # h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    # h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h1 = net.addNAT(name='h1', connect=True, inNamespace=False)
    h2 = net.addNAT(name='h2', connect=True, inNamespace=False)
    h3 = net.addNAT(name='h3', connect=True, inNamespace=False)
    h4 = net.addNAT(name='h4', connect=True, inNamespace=False)

    info( '*** Add links\n')
    net.addLink(h1, s1,port1=5001,cls=TCLink,bw=10,delay=10)
    net.addLink(h2, s1,port1=5002)
    net.addLink(h3, s1,port1=5003)
    net.addLink(h4, s1,port1=5003)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
