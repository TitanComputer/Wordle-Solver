import os
import requests


class DictionaryDownloader:
    def __init__(self, url: str, save_dir: str = "dict", filename: str = "words.txt"):
        self.url = url
        self.save_dir = save_dir
        self.filename = filename
        os.makedirs(self.save_dir, exist_ok=True)

    def download(self):
        save_path = os.path.join(self.save_dir, self.filename)
        try:
            print(f"Downloading dictionary from {self.url} ...")
            response = requests.get(self.url)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Saved dictionary to {save_path}")
        except requests.RequestException as e:
            print(f"Error downloading file: {e}")


if __name__ == "__main__":
    dict_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"

    downloader = DictionaryDownloader(dict_url)
    downloader.download()
