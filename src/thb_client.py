from typing import Optional
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from src.album import Album
from src.song import Song
from src.utils import allowed_album_property
from src.utils import allowed_music_property

class THBClient:
    def __init__(self):
        self.base_url = "https://thwiki.cc/album.php"

    def search_album(self,
                     search_string: str,
                     is_returned_circle: bool = False,
                     limit_num: Optional[int] = None) -> Optional[List[Album]]:
        params = {}
        params["m"] = "sa"
        params["d"] = "kv"
        params["v"] = search_string
        if is_returned_circle:
            params["o"] = "1"
        if limit_num:
            params["l"] = str(limit_num)

        r = requests.get(self.base_url, params=params)
        try:
            return_json = r.json()
        except:
            return None
        if len(return_json) == 0:
            return None

        albums = []
        for smw_id, name in return_json.items():
            albums.append(Album(name, smw_id))
        return albums

    def search_track(self,
                     search_string: str, # v
                     is_returned_album_name: bool = False) -> Optional[List[Song]]:
        params = {}
        params["m"] = "st"
        params["d"] = "kv"
        params["v"] = search_string
        if is_returned_album_name:
            params["o"] = "1"

        r = requests.get(self.base_url, params=params)
        try:
            return_json = r.json()
        except:
            return None
        if len(return_json) == 0:
            return None

        songs = []
        for smw_id, name in return_json.items():
            songs.append(Song(name, smw_id))
        return songs

    def get_album(self,
                  album_property: Optional[list] = None,
                  music_property: Optional[list] = None,
                  smw_id: Optional[int] = None,
                  album_name: Optional[str] = None) -> Optional[Tuple[Album, List[Song]]]:
        params = {}
        params["m"] = "ga"
        params["d"] = "kv"
        params["f"] = " ".join(allowed_album_property)
        params["p"] = " ".join(allowed_music_property)
        if smw_id:
            params["a"] = str(smw_id)
        if album_name:
            params["t"] = album_name

        r = requests.get(self.base_url, params=params)
        try:
            return_json = r.json()
        except:
            return None, None

        if len(return_json) == 2:
            album = Album.from_params(return_json[0])
        songs = []
        for string_smw_id, song_params in return_json[1].items():
            songs.append(Song.from_params(string_smw_id, song_params))

        return album, songs

    # gt
    def get_track(self,
                  music_property: Optional[list] = None,
                  smw_id: Optional[int] = None) -> Optional[Song]:
        params = {}
        params["m"] = "gt"
        params["d"] = "kv"
        params["p"] = " ".join(allowed_music_property)
        if smw_id:
            params["i"] = str(smw_id)
        r = requests.get(self.base_url, params=params)
        try:
            return_json = r.json()
        except:
            return None
        if len(return_json) == 1:
            string_smw_id = list(return_json.keys())[0]
        song = Song.from_params(string_smw_id, return_json[string_smw_id])
        return song


if __name__ == "__main__":
    client = THBClient()
    print(client.search_album("東方乙女囃子"))
    print(client.search_track("sky drive"))
    print(client.get_album(smw_id=96293))
    print(client.get_track(smw_id=136124))

    print(client.search_album("a"*1000))
    print(client.search_track("a"*1000))
    print(client.get_album(smw_id=962438993))
    print(client.get_track(smw_id=13612438434))
