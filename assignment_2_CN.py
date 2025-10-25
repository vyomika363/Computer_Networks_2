from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class CustomTopo(Topo):
    def build(self):
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        dns = self.addHost('dns', ip='10.0.0.5/24')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        self.addLink(h1, s1, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h2, s2, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h3, s3, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h4, s4, cls=TCLink, bw=100, delay='2ms')

        self.addLink(s1, s2, cls=TCLink, bw=1000, delay='5ms')
        self.addLink(s2, s3, cls=TCLink, bw=1000, delay='8ms')
        self.addLink(s3, s4, cls=TCLink, bw=1000, delay='10ms')

        self.addLink(dns, s2, cls=TCLink, bw=1000, delay='1ms')


def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    print("*** Testing network connectivity")
    net.pingAll()

    print("*** Starting Mininet CLI")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
