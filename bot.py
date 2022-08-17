import httpx
import json
import time

def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        stop = time.time() - start
        print(f"time taken {stop}")
    return wrapper

class FantasyBot:
    def __init__(self):
        self.base_url = "https://fantasy.premierleague.com/api/"
        self.standings = "{}leagues-classic/{}/standings/"
    
    def get_overall_standings(self, page):
        params = {"page":page}
        data = httpx.get(self.standings.format(self.base_url, 314), params=params).json()
        data = json.dumps(data, indent=4)
        return data
    
    @timed
    def get_all_pages_overall_standings(self):
        for page in range(1,21):
            print(f"geting page {page}")
            data = self.get_overall_standings(page)


if __name__ == "__main__":
    print(FantasyBot().get_all_pages_overall_standings())