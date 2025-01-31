# Port Scanner

## Description
This project is a comprehensive port scanner tool that includes both GUI and CLI modes. It allows users to scan ports on target URLs or IP addresses, identifies open ports, and retrieves service banners. The tool uses multi-threading for enhanced performance and logs detailed information about the scanning process.

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
Sure! Here's the requested portion:

## Usage

### Running the Script
Save the provided code in a file named `main.py`.

Open a terminal or command prompt and navigate to the directory containing `main.py`.

Run the script using Python:

```bash
python3 main.py
```

### Choosing the Mode
When you run the script, you will be prompted to choose between GUI mode and CLI mode:
- To run in GUI mode, type `gui`.
- To run in CLI mode, type `cli`.

### Using GUI Mode
1. Enter your targets in the "Enter Target/s Domain Name or IP" field, separated by commas. Example: `8.8.8.8, 1.1.1.1`
2. Enter the minimum and maximum port numbers.
3. Enter the protocol name (tcp/udp).
4. Click "Start Scan" to begin scanning. The results will be displayed in the GUI and saved in `scannerFile.txt`.

### Using CLI Mode
1. When prompted, enter your targets separated by commas. Example: `8.8.8.8, 1.1.1.1`
2. Enter the minimum and maximum port numbers.
3. Enter the protocol name (tcp/udp).
4. The script will scan each target and display the results in the command line, and save them in `scannerFile.txt`.

## Logging
Logs are stored in `scanner.log` with detailed information about the scanning process, including errors encountered during the scan.

## Results
Scan results are saved in `scannerFile.txt`. The file includes a summary of the scan and details of open ports, services, and banners.

## Acknowledgements
- [IPy](https://github.com/haypo/python-ipy)
- [Tkinter](https://wiki.python.org/moin/TkInter)

---

Feel free to modify this template as needed to best fit your project's details. If you have any questions or need further customization, just let me know! 😊🚀
