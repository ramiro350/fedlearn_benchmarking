from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def star_topology():
    # Prompt user for the number of hosts
    try:
        num_hosts = int(input("Enter the number of hosts: "))
        if num_hosts < 1:
            print("Number of hosts must be at least 1. Setting to default value (5).")
            num_hosts = 5
    except ValueError:
        print("Invalid input. Setting number of hosts to default value (5).")
        num_hosts = 5

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8',
                   listenPort=5000)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    # Add a switch
    switch1 = net.addSwitch('s1')

    # Add the first host and connect it to the switch
    host1 = net.addNAT('h1')
    net.addLink(host1, switch1)

    # Add the other hosts and connect them to the first host
    for i in range(2, num_hosts + 1):
        host = net.addNAT(f'h{i}')
        net.addLink(host,switch1)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    # Start the network
    net.start()

    # Run the CLI for interaction
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    star_topology()
