import pycurl

# As long as the file is opened in binary mode, both Python 2 and Python 3
# can write response body to it without decoding.
with open('out.html', 'wb') as f:
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://allporncomic.com/porncomic/au-naturel-pegasus-smith/7-au-naturel/')
    c.setopt(c.WRITEDATA, f)
    c.perform()
    c.close()