import random, string
from shared_lib.utils.models import *

def format_views(count):
    if count >= 1_000_000:
        return f"{count/1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count/1_000:.1f}K"
    else:
        return str(count)


def unique_id():
    characters = string.ascii_uppercase + string.digits

    random_string = ''.join(random.choices(characters, k=20))

    return random_string

def insert_id(id):
    insert = TotalActivity.objects.create()

    return "success"

url = "http://127.0.0.1:8001"

main_url = "http://127.0.0.1:8000"
redirect_link = ""

version = "1.9"
platform = "webiste"


img_link = "https://cdn.ascentracoresolutions.com/sfs/images/"


images = "https://cdn.ascentracoresolutions.com/"
endpoint_url = "https://ab060d1ee8b1175a20056ef065739ffc.r2.cloudflarestorage.com"
aws_access_key_id = "af5a5d1b17972c1c234afe848866f068"
aws_secret_access_key = "8d69c56adbf9374986d35a21c09905dc5e8016448aa408f105949fa479e9411f"


def site_data(request):
    data = {
        "version": version,
        "platform": platform,
        "url": url,
        "main_url": main_url,
        "redirect_link": redirect_link,
        "img_url": img_link,
        "user_id": request.session.get("user_id", None),
        "endpoint_url": endpoint_url,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "images": images,
        
    }

    return data


