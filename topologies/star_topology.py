from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def modified_topology():
    # Prompt user for the number of hosts
    try:
        num_hosts = int(input("Enter the number of hosts: "))
        if num_hosts < 1:
            print("Number of hosts must be at least 1. Setting to default value (5).")
            num_hosts = 5
    except ValueError:
        print("Invalid input. Setting number of hosts to default value (5).")
        num_hosts = 5

    # Create a Mininet instance
    net = Mininet(controller=Controller, switch=OVSSwitch)

    # Add a controller
    controller = net.addController('c0')

    # Add a switch
    switch = net.addSwitch('s1')

    # Add the first host and connect it to the switch
    host1 = net.addHost('h1')
    net.addLink(host1, switch)

    # Add the other hosts and connect them to the first host
    for i in range(2, num_hosts + 1):
        host = net.addHost(f'h{i}')
        net.addLink(host, host1)  # Connect other hosts to the first host

    # Start the network
    net.start()

    # Run the CLI for interaction
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    modified_topology()
