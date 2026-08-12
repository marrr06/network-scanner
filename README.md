Lightweight home network security monitor written in Python. Built with Scapy, Streamlit and SQLite3. 
!!!! REMINDER: ONLY run this on networks you own or have explicit authorization to test !!!

[ + ] Overview

- What it does: Monitors your local network (LAN) in real time to keep track of connected devices and their data traffic.
- How it works: Performs ARP scans to discover active hosts, identifies device vendors, passively sniffs IP network packets using Scapy to measure bandwidth for each device found, saves everything into a local SQLite database (devices.db, it will be created automatically by the program).
- you will get interactive web dashboard featuring a live device inventory table and a bandwidth usage bar chart.

[ + ] How to Run

For Linux users {

Because Scapy acts at low level, the scanner script must be run with superuser privileges. You cannot run it directly from an IDE without root access.

0. If not done yet, install dependencies:
pip install scapy mac-vendor-lookup pandas streamlit

You will need two terminals. One of them will run the scanner (scan.py), the other will run the dashboard. 

1. Run the Scanner (Terminal 1):
sudo python3 scan.py
Enter your subnet when prompted (e.g. 192.168.1.0/24). Press Ctrl+C to stop.

2. Launch the Dashboard (Terminal 2):
streamlit run dashboard.py
A dedicated window should open automatically, if not: open http://localhost:8501 (default network port sed by Streamlit) in your browser to view the statistics.
} 

For non-Linux users {
why?
}
