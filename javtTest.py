import scrapy
from scrapy.http import Request

def curl_to_request(curl_command):
    headers = {}
    url = None

    # Split the cURL command into individual parts
    parts = curl_command.split()

    # Extract URL
    for i, part in enumerate(parts):
        if part.startswith('http'):
            url = part.strip("'")
            break

    # Extract headers
    for i, part in enumerate(parts):
        if part.startswith('-H'):
            header_name = parts[i+1].strip("'")
            header_value = parts[i+2].strip("'")
            headers[header_name] = header_value

    # Create Scrapy Request object
    yield Request(url, headers=headers,callback=parse_url)

    return request
def parse_url(response):
    print(response.url)
    breakpoint()
# Example usage:
curl_command = '''curl 'https://jt-static-assets.b-cdn.net/videos/tmb/56757/1.jpg' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0' -H 'Accept: image/avif,image/webp,*/*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Connection: keep-alive' -H 'Referer: https://javtiful.com/' -H 'Sec-Fetch-Dest: image' -H 'Sec-Fetch-Mode: no-cors' -H 'Sec-Fetch-Site: cross-site' '''

request = curl_to_request(curl_command)
# breakpoint()
print(request.url)
print(request.headers)