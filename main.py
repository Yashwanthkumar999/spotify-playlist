import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_ID = "042babc43ccc4b959bb4fe0fb1bb1ee1"
SPOTIFY_SECRET_ID = "ac8e8045ce394cca8b9891c606062ac3"
APP_NAME = "personal spotify"

URL = "https://www.billboard.com/charts/hot-100/"
# year = input("which year do you want to travel to? Type the data in t his format YYYY-MM-DD:")
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"{URL}{date}")
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

titles_list = soup.select("li ul li h3")
titles = [title.getText().strip() for title in titles_list]
print(titles)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET_ID,
        show_dialog=True,
        cache_path="token.txt",
        username=APP_NAME

    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_names = ["The list of song", "titles from your", "web scrape"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# song_uris = ["The list of", "song URIs", "you got by", "searching Spotify"]

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
