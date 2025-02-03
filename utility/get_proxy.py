import random
import requests

class ProxySelector:
    def __init__(self, file_path):
        self.file_path = file_path
        self.proxies = self.load_proxies()
    
    def load_proxies(self):
        """Loads proxies from a file."""
        with open(self.file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    
    def check_proxy(self, proxy):
        """Checks if a proxy is working by making a test request."""
        url = "https://www.pornxday.com/"  # Test URL to check proxy
        proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            return False
        return False
    
    def get_working_proxy(self):
        """Returns a randomly selected working proxy."""
        random.shuffle(self.proxies)
        for proxy in self.proxies:
            if self.check_proxy(proxy):
                return proxy
        return None  # No working proxy found

# Usage example:
# selector = ProxySelector("proxies.txt")
# working_proxy = selector.get_working_proxy()
# if working_proxy:
#     print(f"Working proxy found: {working_proxy}")
# else:
#     print("No working proxy found.")
