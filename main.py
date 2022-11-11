import socket
from IPy import IP

f = open("scannerFile.txt", "a")
def scan(target, port_num, protocolName):
    converted_ip = check_ip(target)
    socket.gethostbyname(target)
    print('Target URL: ', target, "\nTarget IP Address : ", socket.gethostbyname(target))
    print('\nScanning....\n')
    print('Open Port \t', '|', '\tServices')

    for port in range(1, port_num):
        scan_port(converted_ip, port, protocolName)


def get_banner(s):
    return s.recv(1024)


def check_ip(ip):
    try:
        IP(ip)
        return (ip)
    except ValueError:
        return socket.gethostbyname(ip)


def scan_port(ipaddress, port, protocolName):
    try:
        try:

            sock = socket.socket()
            sock.settimeout(10)
            sock.connect((ipaddress, port))
            li = socket.getservbyport(port)

            try:
                banner = get_banner(sock)
                l2 = banner.decode().strip('\n').strip('\r')
                print('   ', port, '\t\t\t', socket.getservbyport(port, protocolName), " : ",
                      banner.decode().strip('\n').strip('\r'))

            except:
                print('   ', port, '\t\t\t', socket.getservbyport(port, protocolName), " : ",
                      banner.decode().strip('\n').strip('\r'))

            f.write(f"\nThe service running on port {port} is => {li} : {l2}")

        except:
            pass
    except:
        pass


if __name__ == "__main__":

    targets = input('Enter Target/s URL : ')
    port_number = eval(input('Enter Number Of Ports To Scan: '))
    protocolName = input("Enter protocol name / scan type : ")

    var = socket.gethostbyname(targets)

    f.write(" \n\t\t\t ========================== Port Scanner ========================== \n")

    f.write(f"\nTarget URL         : {targets}")
    f.write(f"\nTarget IP Address  : {var}")
    f.write(f"\nPort range to scan : 0 - {port_number}")
    f.write(f"\nScan type          : {protocolName}")
    f.write(f"\n")

    f.write(" \n\t\t\t ======================== Ports & Services ======================== \n")

    if ',' in targets:

        for ip_add in targets.split(','):
            scan(ip_add.strip(' '), port_number, protocolName)
    else:
        scan(targets, port_number, protocolName)

    f.write(" \n\n\n\t\t\t ================================================================== \n")
