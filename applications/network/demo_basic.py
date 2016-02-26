# coding=UTF-8

from urllib.request import urlopen, Request

'''
response = urlopen('http://www.debian.org')
print(response)
print(response.url)
print(response.status)

print(response.getheaders())

req = Request('http://www.debian.org')
req.add_header('Accept-Language', 'sv')
response = urlopen(req)
print(response.getheaders())

req = Request('http://www.python.org')
urlopen(req)
print(req.get_header('User-agent'))
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64;rv:24.0) Gecko/20140722 Firefox/24.0 Iceweasel/24.7.0')
urlopen(req)
print(req.get_header('User-agent'))

from http.cookiejar import CookieJar
cookie_jar = CookieJar()

from urllib.request import build_opener, HTTPCookieProcessor
opener = build_opener(HTTPCookieProcessor(cookie_jar))
opener.open('http://www.github.com')
print(cookie_jar,len(cookie_jar))

cookies = list(cookie_jar)
print(cookies)'''

from urllib.parse import urlparse
result = urlparse('http://www.python.org/dev/peps')
print(result)

from urllib.parse import urljoin
print(urljoin('http://www.debian.org/intro/', 'about'))
# http://www.debian.org/intro/about
print(urljoin('http://www.debian.org/intro', 'about'))
# http://www.debian.org/about
print(urljoin('http://www.debian.org/intro/about', '/News'))
# http://www.debian.org/News

from urllib.parse import parse_qs
result = urlparse('http://docs.python.org/3/search.html?q=urlparse&area=default')
print(parse_qs(result.query))
# {'q': ['urlparse'], 'area': ['default']}

from urllib.parse import quote, urlencode
print(quote('A duck?'))
# A%20duck%3F

req = Request('http://www.google.com', method='HEAD')
response = urlopen(req)
print(response.status)

data_dict = {'P': 'Python'}
data = urlencode(data_dict).encode('utf-8')
req = Request('http://search.debian.org/cgi-bin/omega',data=data)
req.add_header('Content-Type', 'application/x-www-form-urlencode;charset=UTF-8')
response = urlopen(req)
print(response)






