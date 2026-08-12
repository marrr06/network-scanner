
from mac_vendor_lookup import MacLookup
from datetime import datetime
import sys
import signal

#hello

from network_tools import (
    init_db,
    save_devices_to_db,
    update_bandwidth_in_db,
    scan,
    tracker
)

#note for the next function: since scapy works low level, many system calls get intercepted by he library.
#to prevent Ctrl+C from not working (because scapy would just stop what its doing instead of the program being closed),
#a function to close the program is necessary. I will try to optimize it in the future, for now, as we do not work with
#sensible data, sys.exit(0) can work to "gracefully" close everything: SQLite is also pretty robust, it will not cause any issue.


def shutdown(sig, frame): 
    print("[!] Ctrl+C called. Exiting.")
    sys.exit(0)
    

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown) #SIGINT stands for "Signal Interrupt". We are basically telling the system "ignore how anything in this program handles KeyboardINterrupt, use this instead"
    print("Loading MAC addresses...")
    try:
        MacLookup().update_vendors()
        print("[ :) ] Done.")
    except Exception:
        print("[ :( ] Could not update database. Using local cache.")
        
    init_db()
    
    target_range = (str(input("Insert subnet: "))).strip() 
    
    print("Scanner initialization. Press Ctrl C to stop.")
    while True:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting network scan...")
        found_devices = scan(target_range)
        print(f"[+] Found {len(found_devices)} live devices. Saving to DB...")
        save_devices_to_db(found_devices)
        
        print("[+] Tracking bandwidth for 60 seconds...")
        traffic_data = tracker(duration=60) 
        
        update_bandwidth_in_db(traffic_data)
        print("[ :) ] Bandwidth updated successfully in DB.")
                    