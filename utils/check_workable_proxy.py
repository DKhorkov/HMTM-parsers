from typing import List

import requests

def load_proxy() -> list[str]:
    with open('../proxylist.txt', 'r') as f:
        return [proxy for proxy in f.read().splitlines()]

proxylist: List[str] = load_proxy()
url = 'https://www.etsp.ru/'


for pr in proxylist:
    proxies = {
        "http": f"http://{pr}/",
        # "https": f"http://{pr}/"
    }

    response = requests.get(url, proxies=proxies)
    if response.status_code == 200:
        print('workable')
    else:
        print('doest not working')
