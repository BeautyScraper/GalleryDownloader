import random
import requests
import os
from urllib.parse import urlparse

class ProxySelector:
    def __init__(self, file_path, test_url="https://www.pornxday.com"):
        self.file_path = file_path
        self.test_url = test_url
        self.cache_file = self.get_cache_filename()
        self.proxies = self.load_proxies()
    
    def get_cache_filename(self):
        """Generates a cache file name based on the test URL domain."""
        domain = urlparse(self.test_url).netloc.replace(':', '_')
        return f"last_working_proxy_{domain}.txt"
    
    def load_proxies(self):
        """Loads proxies from a file."""
        with open(self.file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    
    def check_proxy(self, proxy):
        """Checks if a proxy is working by making a test request."""
        # proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}", "socks": f"socks://{proxy}"}
        proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}", "socks": f"//{proxy}"}
        try:
            response = requests.get(self.test_url, proxies=proxies, timeout=50)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            return False
        return False
    
    def get_last_working_proxy(self):
        """Retrieves the last working proxy from the cache file."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                proxy = file.read().strip()
                if proxy:
                    return proxy
        return None
    
    def save_last_working_proxy(self, proxy):
        """Saves the last working proxy to the cache file."""
        # breakpoint()
        with open(self.cache_file, 'w') as file:
            file.write(proxy)
    
    def get_working_proxy(self):
        """Returns a working proxy, prioritizing the last known working one."""
        last_proxy = self.get_last_working_proxy()
        # breakpoint()
        if last_proxy and self.check_proxy(last_proxy):
            return last_proxy
        
        # random.shuffle(self.proxies)
        for proxy in self.proxies:
            if self.check_proxy(proxy):
                proxy = f'http://{proxy}'
                self.save_last_working_proxy(proxy)
                return proxy
        return None  # No working proxy found

# Usage example:
# selector = ProxySelector("proxies.txt", "http://httpbin.org/ip")
# working_proxy = selector.get_working_proxy()
# if working_proxy:
#     print(f"Working proxy found: {working_proxy}")
# else:
#     print("No working proxy found.")
