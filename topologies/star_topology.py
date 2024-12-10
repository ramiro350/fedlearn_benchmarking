from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

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

    # Create a Mininet instance
    net = Mininet(controller=Controller, switch=OVSSwitch)

    # Add a controller
    controller = net.addController('c0')

    # Add a switch (central node in the star)
    switch = net.addSwitch('s1')

    # Add hosts and connect them to the switch
    for i in range(1, num_hosts + 1):
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
