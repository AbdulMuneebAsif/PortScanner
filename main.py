"""

 Name   : Abdul Muneeb Asif
 Sap ID : 29217@students.riphah.edu.pk

"""

import socket
import logging
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
def scan(target, min_port, max_port, protocolName):
    global results
    converted_ip = check_ip(target)
    logging.info(f'Starting scan on {target}')
    update_output(f'Target URL: {target}\nTarget IP Address: {converted_ip}\n\nScanning....\n')
    update_output('Open Port\t| Services\t\t| Banner\n')
    threads = []
    for port in range(min_port, max_port + 1):
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
        f.write("\n\n==================================================================\n")
        f.write(f"|                 Port Scanner Summary - {target}               |\n")
        f.write("==================================================================\n")
        f.write(f"Target Domain Name or IP: {target}\n")
        f.write(f"Target IP Address: {converted_ip}\n")
        f.write(f"Range of Ports Scanned: {min_port}-{max_port}\n")
        f.write(f"Scanned Protocol: {protocolName.upper()}\n")
        f.write("==================================================================\n")
        f.write("Port\t| Service\t| Banner\n")
        f.write("------------------------------------------------------------------\n")
        for result in results:
            f.write(result)
            f.write(f"------------------------------------------------------------------\n")
        f.write("==================================================================\n\n")

# Update Output Function
def update_output(message):
    if gui_mode:
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, message)
        output_text.config(state=tk.DISABLED)
    else:
        print(message.expandtabs(15))

# Check IP Function
def check_ip(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)

# Get Banner Function
def get_banner(sock, protocolName, port, target):
    try:
        if protocolName.lower() == 'tcp':
            if port == 80 or port == 443:  # HTTP or HTTPS
                request = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode()
                sock.send(request)
            else:
                sock.send(b"\r\n")
        elif protocolName.lower() == 'udp':
            sock.send(b"\r\n")
        response = sock.recv(4096).decode()

        # Extract server banner information from response headers
        banner = ""
        for line in response.split('\r\n'):
            if line.lower().startswith("server:"):
                banner = line
                break

        if not banner and response:
            banner = response.split('\r\n')[0]  # Fallback to the first line of the response

        return banner if banner else "No banner"
    except Exception as e:
        logging.error(f"Error retrieving banner: {e}")
        return "No banner"
# Scan Port Function
def scan_port(ipaddress, port, protocolName):
    global results
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocolName.lower() == 'tcp' else socket.SOCK_DGRAM)
        sock.settimeout(10)
        sock.connect((ipaddress, port))
        service = socket.getservbyport(port, protocolName.lower())
        try:
            banner = get_banner(sock, protocolName, port, ipaddress)
        except Exception as e:
            banner = 'No banner'
            logging.error(f'Error retrieving banner for port {port}: {e}')
        result = f'{port}\t| {service}\t\t| {banner}\n------------------------------------------------------------------\n'
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
        min_port = int(min_port_entry.get())
        max_port = int(max_port_entry.get())
        protocolName = protocol_entry.get()
        scan_thread = threading.Thread(target=run_scan, args=(target, min_port, max_port, protocolName))
        scan_thread.start()

    def run_scan(target, min_port, max_port, protocolName):
        if ',' in target:
            for ip_add in target.split(','):
                scan(ip_add.strip(), min_port, max_port, protocolName)
        else:
            scan(target, min_port, max_port, protocolName)

    window = tk.Tk()
    window.title("Port Scanner")

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    window_width = 600
    window_height = 500
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")  # Center the window

    tk.Label(window, text="Enter Target/s Domain Name or IP (e.g., scanme.nmap.org or 64.13.134.52): ").pack()
    target_entry = tk.Entry(window, width=50)
    target_entry.pack()

    tk.Label(window, text="Enter Minimum Port Number:").pack()
    min_port_entry = tk.Entry(window, width=50)
    min_port_entry.pack()

    tk.Label(window, text="Enter Maximum Port Number:").pack()
    max_port_entry = tk.Entry(window, width=50)
    max_port_entry.pack()

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
    targets = input('Enter Target/s URL (e.g., scanme.nmap.org or 64.13.134.52):  ')
    min_port = int(input('Enter Minimum Port Number: '))
    max_port = int(input('Enter Maximum Port Number: '))
    protocolName = input('Enter Protocol Name (tcp/udp): ')
    if ',' in targets:
        for ip_add in targets.split(','):
            scan(ip_add.strip(), min_port, max_port, protocolName)
    else:
        scan(targets, min_port, max_port, protocolName)

if __name__ == "__main__":
    gui_mode = False
    while True:
        mode = input("Choose mode (gui/cli): ").lower()
        if mode == 'gui':
            start_gui()
            break
        elif mode == 'cli':
            start_cli()
            break
        else:
            print("Invalid mode! Please choose 'gui' or 'cli'.")
