from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class CustomTopo(Topo):
    def build(self):
        
        H1 = self.addHost('H1', ip='10.0.0.1/24')
        H2 = self.addHost('H2', ip='10.0.0.2/24')
        H3 = self.addHost('H3', ip='10.0.0.3/24')
        H4 = self.addHost('H4', ip='10.0.0.4/24')
        DNS = self.addHost('DNS', ip='10.0.0.5/24')

        #adding switches
        S1 = self.addSwitch('S1')
        S2 = self.addSwitch('S2')
        S3 = self.addSwitch('S3')
        S4 = self.addSwitch('S4')

        #addinf host to switch links with bw=100Mbps and delay=2ms
        self.addLink(H1, S1, bw=100, delay='2ms')
        self.addLink(H2, S2, bw=100, delay='2ms')
        self.addLink(H3, S3, bw=100, delay='2ms')
        self.addLink(H4, S4, bw=100, delay='2ms')

        #adding switch to switch links
        self.addLink(S1, S2, bw=1000, delay='5ms')
        self.addLink(S2, S3, bw=1000, delay='8ms')
        self.addLink(S3, S4, bw=1000, delay='10ms')

        #linking DNS resolver to s2 
        self.addLink(DNS, S2, bw=1000, delay='1ms')

def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    print("Testing network connectivity")
    net.pingAll()

    #starting CLI for manual testing
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
