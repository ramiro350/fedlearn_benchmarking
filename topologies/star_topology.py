from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def star_topology():
    # Create a Mininet instance
    net = Mininet(controller=Controller, switch=OVSSwitch)

    # Add a controller
    controller = net.addController('c0')

    # Add a switch (central node in the star)
    switch = net.addSwitch('s1')

    # Add hosts and connect them to the switch
    for i in range(1, 6):  # Change range for more hosts
        host = net.addHost(f'h{i}')
        net.addLink(host, switch)

    # Start the network
    net.start()

    # Run the CLI for interaction
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    star_topology()
