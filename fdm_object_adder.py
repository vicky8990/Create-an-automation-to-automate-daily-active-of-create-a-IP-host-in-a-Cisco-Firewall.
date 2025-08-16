#!/usr/bin/env python3
import requests
import getpass
import sys
from pathlib import Path
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FDMClient:
    def __init__(self, host):
        self.base_url = f"https://{host}"
        self.token = None
        self.session = requests.Session()
        self.session.verify = False
        
    def authenticate(self, username, password):
        try:
            response = self.session.post(
                f"{self.base_url}/api/fdm/latest/fdm/token",
                json={"grant_type": "password", "username": username, "password": password},
                timeout=30
            )
            response.raise_for_status()
            self.token = response.json()['access_token']
            print("Authentication successful")
        except Exception as e:
            print(f"Authentication failed: {e}")
            sys.exit(1)
           def create_object(self, endpoint, payload):
        response = self.session.post(
            f"{self.base_url}/api/fdm/v6/object/{endpoint}",
            json=payload,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

def sanitize_name(value, is_ip_addr):
    if is_ip_addr:
        return f"Block-IP_{value.replace('.', '_')}"
    clean = value.replace('https://', '').replace('http://', '')
    return ''.join(c if c.isalnum() or c in '-_.' else '_' for c in clean)[:50]

def get_user_inputs():
    host = input("FDM IP: ").strip()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    return host, username, password

def read_file(filepath):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def process_files(client, files, file_type):
    total_success = 0
    for file_path in files:
        entries = read_file(file_path)
        print(f"\nProcessing {file_path.name}: {len(entries)} {file_type}s")
        
        for entry in entries:
            name = sanitize_name(entry, file_type == "IP")
            
            try:
                if file_type == "URL":
                    payload = {"name": name, "url": entry, "type": "urlobject"}
                    client.create_object("urls", payload)
                else:  # IP
                    payload = {"name": name, "subType": "HOST", "value": entry, "type": "networkobject"}
                    client.create_object("networks", payload)
                
                print(f"SUCCESS: {name}")
                total_success += 1
                
            except Exception as e:
                print(f"FAILED: {name}: {e}")
    
    return total_success
  def main():
    print("=" * 60)
    print("║" + " " * 58 + "║")
    print("║" + " " * 18 + "FDM Object Adder" + " " * 24 + "║")
    print("║" + " " * 58 + "║")
    print("║  • Creates URL objects from url.txt" + " " * 22 + "║")
    print("║  • Creates Network objects from ip.txt" + " " * 19 + "║")
    print("║" + " " * 58 + "║")
    print("=" * 60)
    print()
    
    host, username, password = get_user_inputs()
    
    client = FDMClient(host)
    client.authenticate(username, password)
    
    url_files = list(Path('.').glob('url.txt'))
    ip_files = list(Path('.').glob('ip.txt'))
    
    if not url_files and not ip_files:
        print("No URL or IP files found")
        sys.exit(1)
    
    total_success = 0
    total_success += process_files(client, url_files, "URL")
    total_success += process_files(client, ip_files, "IP")
    
    print(f"\nCompleted: {total_success} objects created")

    # Add this line to create the group after adding IPs
    if ip_files:
        create_ip_group(client, ip_files[0], "All_Block_IPs_Sep2025")

if __name__ == "__main__":
    main()
