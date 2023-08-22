import requests
import os, io
from dotenv import load_dotenv

# From  https://github.com/rfrlcode/Public/blob/main/mastodon.py   (22.8.2023)

dotenv_path = os.path.join('.env')  # Path to .env file
load_dotenv(dotenv_path)

# Replace these with your instance's domain, email, and password
instance_domain = os.getenv('MASTODON_SERVER') 
mastodon_email = os.getenv('MASTODON_EMAIL')
mastodon_password = os.getenv('MASTODON_PASSWORD')
client_id = os.getenv('MASTODON_CLIENT_ID')
client_secret = os.getenv('MASTODON_CLIENT_SECRET')

# Log in and obtain an access token
def log_in(client_id, client_secret):
    token_data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": mastodon_email,
        "password": mastodon_password,
        "scope": "read write",
    }
    response = requests.post(f"https://{instance_domain}/oauth/token", data=token_data)
    response_data = response.json()
    return response_data["access_token"]


def download_image(url):
    response = requests.get(url)
    return io.BytesIO(response.content)


# TODO : Chk this!
def upload_image(access_token, image_url):
    headers = {"Authorization": f"Bearer {access_token}"}
    image_data = download_image(image_url)
    files = {"file": image_data}
    response = requests.post(
        f"https://{instance_domain}/api/v2/media", headers=headers, files=files
    )
    response_data = response.json()
    print(response_data)

    return response_data["id"]

def post_status(access_token, status_text, media_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"status": status_text
#            "visibility": 'public'}   #Public (default), Unlisted, Followers only¨
    }
    data["media_ids[]"] = media_id

    response = requests.post(
        f"https://{instance_domain}/api/v1/statuses", headers=headers, data=data
    )
    if response.status_code != 200:
        raise Exception


def post_to_mastodon(content, image_url=""):

    ## access_token = log_in(client_id, client_secret)

    access_token = os.getenv('ACCESS_TOKEN')

    # TODO 
    media_id = "" # upload_image(access_token, image_url)

    post_status(access_token, content, media_id)


##post_to_mastodon('test test\nhttps://commons.wikimedia.org/wiki/File:Kit_socks_juventude1718gk1.png')

