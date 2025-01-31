# Port Scanner

## Description
This project is a comprehensive port scanner tool that includes both GUI mode. It allows users to scan ports on target URLs or IP addresses, identifies open ports, and retrieves service banners. The tool uses multi-threading for enhanced performance and logs detailed information about the scanning process.

## Features
- **GUI Mode**: User-friendly graphical interface for easy operation.
- **Multi-threading**: Scans multiple ports concurrently for faster results.
- **Logging**: Stores detailed logs of the scanning process in `scanner.log`.
- **Result Storage**: Saves scan results in `scannerFile.txt`.
- **Error Handling**: Improved error handling and logging for failed port scans.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/maaviyahrehman/PortScanner.git
    cd PortScanner
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
### GUI Mode
1. Start the GUI mode by running:
    ```bash
    python3 main.py
    ```

2. Enter the target URL(s), number of ports to scan, and protocol (TCP/UDP).

## Logging
Logs are stored in `scanner.log` with detailed information about the scanning process, including errors encountered during the scan.

## Results
Scan results are saved in `scannerFile.txt`. The file includes a summary of the scan and details of open ports, services, and banners.

## Acknowledgements
- [IPy](https://github.com/haypo/python-ipy)
- [Tkinter](https://wiki.python.org/moin/TkInter)

---

Feel free to modify this template as needed to best fit your project's details. If you have any questions or need further customization, just let me know! 😊🚀
