import requests
import argparse
import json

from random import sample
from http.client import responses
from enum import IntEnum
from bs4 import BeautifulSoup

class SERIES_STATUS(IntEnum):
	CURRENT_WATCHING = 1
	COMPLETED = 2
	ON_HOLD = 3
	DROPPED = 4
	PLANNED = 6
	ALL = 7

def get_list(username: str, status:SERIES_STATUS):
	url = f"https://myanimelist.net/animelist/{username}?status={status.value}"
	res = requests.get(url)
	if res.status_code == 200:
		raw_text = res.text
		soup = BeautifulSoup(raw_text, "html.parser")
		series_data = json.loads(soup.find("table")['data-items'])
		series_names = [i['anime_title'] for i in series_data]
		return sample(series_names, k=1)[0]
	else:
		print(f"we done goofed fam. {res.status_code} {response[res.status_code]}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog="get_random_watched_anime",
		description="Get a random anime from a MAL account"
	)
	parser.add_argument("username", help="username of account to pull")
	parser.add_argument("-s", "--status", choices=[i.name for i in SERIES_STATUS], help="Return a series from a watching status. Default to ALL", default="ALL")
	args = parser.parse_args()

	print(get_list(args.username, SERIES_STATUS[args.status]))