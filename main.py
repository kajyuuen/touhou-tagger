import requests
import io
import os
from glob import glob
import sys


from mutagen.id3 import ID3, TIT2, TALB, TPE1, TRCK, APIC, TDRC, TCON, COMM, GRP1
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from src.thb_client import THBClient

class TouhouTagger:
    def __init__(self):
        self.info = {}
        self.client = THBClient()

    def _set_tag(self, audiofile, origin_music):
        audiofile["GRP1"] = GRP1(encoding=3, text=[", ".join(origin_music)])
        audiofile.save()

    def update_tag(self, music_file_path):
        try:
            audiofile = MP3(music_file_path)
            album_name = audiofile["TALB"].text[0]
        except:
            return

        if album_name not in self.info:
            album, songs = self.client.get_album(album_name=album_name)
            if album is None:
                self.info[album_name] = None
            else:
                self.info[album_name] = {}
                self.info[album_name]["songs"] = {}
                for song in songs:
                    song_name = song.name[0]
                    track_num = int(song.properties["trackno"][0])
                    origin_music = song.properties["ogmusic"]
                    self.info[album_name]["songs"][track_num] = {"origin_music": origin_music}

        try:
            music_name = audiofile["TIT2"]
            track_num = int(audiofile["TRCK"].text[0].split("/")[0])
        except:
            return

        if self.info[album_name] is not None and track_num in self.info[album_name]["songs"]:
            origin_music = self.info[album_name]["songs"][track_num]["origin_music"]
            self._set_tag(audiofile, origin_music)

if __name__ == "__main__":
    args = sys.argv

    tagger = TouhouTagger()
    path = args[1]
    for i, music_file_path in enumerate(glob(os.path.join(path, "**/*.mp3"), recursive=True)):
        print(i, music_file_path)
        tagger.update_tag(music_file_path)
