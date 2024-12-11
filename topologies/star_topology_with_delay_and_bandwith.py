from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink  # Import for traffic control links

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

    # Prompt user for delay and bandwidth
    try:
        delay = input("Enter link delay (e.g., 10ms): ").strip()
        if not delay:
            print("No delay provided. Setting default to 5ms.")
            delay = '5ms'
        bandwidth = float(input("Enter link bandwidth in Mbps (e.g., 10): ").strip())
        if bandwidth <= 0:
            print("Invalid bandwidth. Setting default to 10 Mbps.")
            bandwidth = 10.0
    except ValueError:
        print("Invalid input. Using default delay (5ms) and bandwidth (10 Mbps).")
        delay = '5ms'
        bandwidth = 10.0

    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/8',
                  link=TCLink)  # Use TCLink for bandwidth and delay control

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    # Add a switch
    switch1 = net.addSwitch('s1')

    # Add the first host and connect it to the switch
    host1 = net.addHost('h1')
    net.addLink(host1, switch1, delay=delay, bw=bandwidth)

    # Add the other hosts and connect them to the switch
    for i in range(2, num_hosts + 1):
        host = net.addHost(f'h{i}')
        net.addLink(host, switch1, delay=delay, bw=bandwidth)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
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
