import aiohttp
import asyncio

concurrent = 200

blitzer_app_headers = {
    "Host": "cdn2.atudo.net",
    "Connection": "keep-alive",
    "Origin": "https://map.atudo.com",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; VPN Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, "
                  "like Gecko) Version/4.0 Chrome/74.0.3729.186 Safari/537.36",
    "Accept": "*/*",
    "Referer": "https://map.atudo.com/v3/?infowindow=1",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "de,en-US;q=0.9,en;q=0.8",
    "X-Requested-Width": "de.blitzer.plus"
}


class BlitzerDownloader:
    def __init__(self):
        pass

