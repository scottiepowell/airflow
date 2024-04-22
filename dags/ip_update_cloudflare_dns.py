import os
import requests

# Constants
CLOUDFLARE_API_BASE_URL = "https://api.cloudflare.com/client/v4"
API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')
DIR_PATH = os.path.dirname(os.path.realpath(__file__))  # Get the directory where the script is located
SUBDOMAIN_FILE = os.path.join(DIR_PATH, 'subdomains.txt')

# Function to get current public IP address
def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

# Function to get current IP address of a subdomain from Cloudflare
def get_cloudflare_ip(subdomain):
    url = f"{CLOUDFLARE_API_BASE_URL}/zones/{ZONE_ID}/dns_records?type=A&name={subdomain}"
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get(url, headers=headers).json()
    records = response.get('result', [])
    if records:
        return records[0]['id'], records[0]['content']  # Return record ID and IP
    return None, None

# Function to update the DNS record in Cloudflare
def update_cloudflare_ip(record_id, subdomain, new_ip):
    url = f"{CLOUDFLARE_API_BASE_URL}/zones/{ZONE_ID}/dns_records/{record_id}"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',
        'name': subdomain,
        'content': new_ip
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Main function
def main():
    public_ip = get_public_ip()
    print(f"Current public IP: {public_ip}")
    
    with open(SUBDOMAIN_FILE, 'r') as file:
        for line in file:
            subdomain = line.strip()
            record_id, cloudflare_ip = get_cloudflare_ip(subdomain)
            if cloudflare_ip != public_ip:
                print(f"Updating IP for {subdomain} from {cloudflare_ip} to {public_ip}")
                response = update_cloudflare_ip(record_id, subdomain, public_ip)
                print(response)
            else:
                print(f"No update needed for {subdomain}")

if __name__ == '__main__':
    main()
