import requests
import time

def ping_backend():
    while True:
        try:
            response = requests.get('http://backend:8000')
            print("Response from backend:", response.text)
            break
        except requests.exceptions.ConnectionError:
            print("Backend not available yet, retrying in 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    ping_backend()
