from urllib.parse import urlparse, urljoin

parsed1 = 'wfw.ch'
parsed2 = 'www.wfw.ch'
parsed3 = 'www.wfw.ch'
parsed4 = 'https://www.wfw.ch/'
parsed5 = 'https://femtonics.eu/uploads/MES/MES7.2_released.zip'


print(urlparse(parsed1))
print(urlparse(parsed2))
print(urlparse(parsed3))
print(urlparse(parsed4))
print(urlparse(parsed5))

print(urlparse(parsed5).path.lower().split('.')[-1] in ['exe', 'zip', 'png', 'jpg', 'pdf'])