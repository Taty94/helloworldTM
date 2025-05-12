import time
import requests

def check_wiremock():
    url = "http://127.0.0.1:9090/__admin"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("WireMock server is up and running with status code: 200")
                print("Response content:", response.text)
                return True
            else:
                print(f"Received status code: {response.status_code}")
                print("Response content:", response.text)
        except requests.ConnectionError:
            print("WireMock server not ready yet. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    check_wiremock()