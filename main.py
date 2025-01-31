"""

 Name   : Abdul Muneeb Asif
 Sap ID : 29217@students.riphah.edu.pk

"""

import socket
from IPy import IP
import threading
import logging
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Configure Logging
logging.basicConfig(filename='scanner.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize Results List
results = []

# Scan Function
def scan(target, port_num, protocolName):
    global results
    converted_ip = check_ip(target)
    logging.info(f'Starting scan on {target}')
    update_output(f'Target URL: {target}\nTarget IP Address: {converted_ip}\n\nScanning....\n')
    update_output('Open Port\t| Services\n')

    threads = []
    for port in range(1, port_num + 1):
        t = threading.Thread(target=scan_port, args=(converted_ip, port, protocolName))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    completion_message = '\nScan complete! Check the scannerFile.txt for details.\n'
    update_output(completion_message)
    
    if gui_mode:
        messagebox.showinfo("Scan Complete", "Port scanning is complete. Check the output for details.")

    # Write summary and results to the file
    with open("scannerFile.txt", "a") as f:
        f.write("\n\n============================================\n")
        f.write(f"|         Port Scanner Summary - {target}  |\n")
        f.write("============================================\n")
        f.write(f"Target URL/IP: {target}\n")
        f.write(f"Target IP Address: {converted_ip}\n")
        f.write(f"Number of Ports Scanned: {port_num}\n")
        f.write(f"Scanned Protocol: {protocolName.upper()}\n")
        f.write("============================================\n")
        f.write("Port\t| Service\t| banner\n")
        for result in results:
            f.write(result + '\n')
        f.write("=============================================\n\n")

# Update Output Function
def update_output(message):
    if gui_mode:
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, message)
        output_text.config(state=tk.DISABLED)
    else:
        print(message)

# Get Banner Function
def get_banner(s):
    return s.recv(1024)

# Check IP Function
def check_ip(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)

# Scan Port Function
def scan_port(ipaddress, port, protocolName):
    global results
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocolName.lower() == 'tcp' else socket.SOCK_DGRAM)
        sock.settimeout(10)
        sock.connect((ipaddress, port))
        service = socket.getservbyport(port, protocolName.lower())
        banner = get_banner(sock).decode().strip('\n').strip('\r')
        result = f'{port}\t| {service}\t\t| {banner}'
        update_output(result + '\n')
        results.append(result)
    except Exception as e:
        logging.error(f'Error scanning port {port} on {ipaddress}: {e}')

# GUI
def start_gui():
    global gui_mode
    gui_mode = True

    def start_scan():
        target = target_entry.get()
        port_num = int(port_entry.get())
        protocolName = protocol_entry.get()
        scan_thread = threading.Thread(target=run_scan, args=(target, port_num, protocolName))
        scan_thread.start()

    def run_scan(target, port_num, protocolName):
        if ',' in target:
            for ip_add in target.split(','):
                scan(ip_add.strip(), port_num, protocolName)
        else:
            scan(target, port_num, protocolName)

    window = tk.Tk()
    window.title("Port Scanner")
    window.geometry("600x500")

    tk.Label(window, text="Enter Target/s URL:").pack()
    target_entry = tk.Entry(window, width=50)
    target_entry.pack()

    tk.Label(window, text="Enter Number of Ports to Scan:").pack()
    port_entry = tk.Entry(window, width=50)
    port_entry.pack()

    tk.Label(window, text="Enter Protocol Name (tcp/udp):").pack()
    protocol_entry = tk.Entry(window, width=50)
    protocol_entry.pack()

    start_button = tk.Button(window, text="Start Scan", command=start_scan)
    start_button.pack()

    global output_text
    output_text = scrolledtext.ScrolledText(window, width=70, height=20, state=tk.DISABLED)
    output_text.pack()

    window.mainloop()

# CLI
def start_cli():
    global gui_mode
    gui_mode = False

    targets = input('Enter Target/s URL: ')
    port_number = int(input('Enter Number of Ports to Scan: '))
    protocolName = input('Enter Protocol Name (tcp/udp): ')
    if ',' in targets:
        for ip_add in targets.split(','):
            scan(ip_add.strip(), port_number, protocolName)
    else:
        scan(targets, port_number, protocolName)

if __name__ == "__main__":
    gui_mode = False
    mode = input("Choose mode (gui/cli): ").lower()
    if mode == 'gui':
        start_gui()
    elif mode == 'cli':
        start_cli()
    else:
        print("Invalid mode! Please choose 'gui' or 'cli'.")
