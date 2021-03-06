import asyncio
from aiohttp import ClientSession
import json
from retrying import retry

_blitzer_app_headers = {
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

# eg. https://cdn2.atudo.net/api/3.0/?type=0,1,2,3,4,5,6&z=11&box=48.392979,8.437491,48.753712,9.617148
_url_mask = "https://cdn2.atudo.net/api/3.0/?type=0,1,2,3,4,5,6&z=12&box={},{},{},{}"


async def fetch(url: str, session: ClientSession):
    async with session.get(url, headers=_blitzer_app_headers) as response:
        return await response.read()


def has_speedcams(response: str):
    return not response.startswith('{"pois":[]')


def filter_by_country_code(speedcams, country_code):
    filtered_speedcams = list()

    for speedcam in speedcams:
        if "address" in speedcam:
            if "country" in speedcam["address"]:
                if speedcam["address"]["country"] == country_code:
                    filtered_speedcams.append(speedcam)

    return filtered_speedcams


def sort_by_id(speedcams):
    sorted_speedcams = sorted(speedcams, key=lambda speedcam: int(speedcam["id"]))
    return sorted_speedcams


@retry
async def download_speedcams(tiles, country_code):
    urls = list()
    for tile in tiles:
        urls.append(_url_mask.format(tile.south, tile.west, tile.north, tile.east))

    tasks = []

    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

    speedcams = list()
    for response_bytes in responses:
        response_str: str = response_bytes.decode('unicode_escape')
        if has_speedcams(response_str):
            speedcams += json.loads(response_str)['pois']

    return sort_by_id(filter_by_country_code(speedcams, country_code))
