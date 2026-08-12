from scapy.all import Ether, ARP, srp, sniff, IP
from mac_vendor_lookup import MacLookup
import sqlite3
from datetime import datetime

def init_db(): #gets the database file, creates it if it doesn't exist 
    connections = sqlite3.connect("devices.db")
    cursor = connections.cursor()
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS devices (
                       mac TEXT PRIMARY KEY,
                       ip TEXT,
                       vendor TEXT,
                       bandwidth INTEGER DEFAULT 0,
                       first_seen TEXT,
                       last_seen TEXT
                       )""")
    connections.commit()
    connections.close()
    
def save_devices_to_db(devices_list):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for device in devices_list:
        cursor.execute("""INSERT INTO devices (mac, ip, vendor, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(mac) DO UPDATE SET
                ip = excluded.ip,
                last_seen = excluded.last_seen
        """, (device["mac"], device["ip"], device["vendor"], current_time, current_time))
    conn.commit()
    conn.close()
    
def update_bandwidth_in_db(traffic_dict):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()
    
    for ip, counted_bytes in traffic_dict.items():
        cursor.execute("""UPDATE devices
                       SET bandwidth = bandwidth + ?
                       WHERE ip = ?
                       """, (counted_bytes, ip))
    conn.commit()
    conn.close()
    


def scan(ip_range): 
        
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    result = srp(packet, timeout=3, verbose=0)[0]
    devices = []
    
    for sent, received in result:
        mac_address = received.hwsrc
        try:
            vendor = MacLookup().lookup(mac_address)
        except:
            vendor = "Unkown vendor"
            
        devices.append({"ip": received.psrc, 
                        "mac": mac_address,
                        "vendor": vendor
                        })
    return devices

def tracker(duration=60):
    traffic = {}
    def _capture(pkt):
        if IP in pkt: #necessary to check if the packet has IP layer protocols to avioid excetions, as documentation says
            src = pkt[IP].src
            traffic[src] = traffic.get(src, 0) + len(pkt)
    sniff(prn=_capture, store=False, timeout=duration)
    return traffic