import os
import requests
import re


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


class WordFilter:
    def __init__(self, input_path="dict/words.txt", output_path="dict/words_filtered.txt"):
        self.input_path = input_path
        self.output_path = output_path
        self.pattern = re.compile(r"^[a-z]{5}$")

    def filter_and_save(self):
        if not os.path.exists(self.input_path):
            print(f"File {self.input_path} not found!")
            return

        words_set = set()

        with open(self.input_path, "r", encoding="utf-8") as infile:
            for line in infile:
                word = line.strip().lower()
                if self.pattern.match(word):
                    words_set.add(word)

        sorted_words = sorted(words_set)

        with open(self.output_path, "w", encoding="utf-8") as outfile:
            for word in sorted_words:
                outfile.write(word + "\n")

        print(f"Filtered words saved to {self.output_path}, total {len(sorted_words)} words.")


class WordleSolver:
    def __init__(self, words):
        self.words = words

    def filter_candidates(self, known_pattern, unknowns, excluded_letters):
        pattern = "".join([ch if ch else "." for ch in known_pattern])
        print(f"Regex Pattern: {pattern}")
        regex = re.compile(pattern)

        candidates = [w for w in self.words if regex.match(w)]
        print(f"After Known Positions: {len(candidates)} words")

        for idx, letter in unknowns:
            candidates = [w for w in candidates if letter in w and w[idx] != letter]
        if unknowns:
            print(f"After Unknown Positions: {len(candidates)} words")

        if excluded_letters:
            candidates = [w for w in candidates if all(ch not in w for ch in excluded_letters)]
            print(f"Excluded Letters: {excluded_letters}")

        return candidates


if __name__ == "__main__":
    dict_url = "https://raw.githubusercontent.com/tabatkins/wordle-list/refs/heads/main/words"

    downloader = DictionaryDownloader(dict_url)
    downloader.download()
    wf = WordFilter()
    wf.filter_and_save()
