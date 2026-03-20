import requests
import random
import os

TOKEN = os.environ["TOKEN_YONAMAXI"]
CHAT_ID = os.environ["CHAT_ID"]
THREAD_ID = int(os.environ["THREAD_ID_YONAMAXI"])

TOTAL_ITEMS = 250
METADATA_CID = "bafybeifxmoqrza4cybkmalknqpouy5vu4x3nm3vzuhikskwzli2vo4ewpe"


def ipfs_to_http(url):
    if url.startswith("ipfs://"):
        return "https://ipfs.io/ipfs/" + url.replace("ipfs://", "")
    return url


def get_metadata(token_id):
    url = f"https://ipfs.io/ipfs/{METADATA_CID}/{token_id}.json"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()


def main():
    token_id = random.randint(1, TOTAL_ITEMS)
    data = get_metadata(token_id)

    image = ipfs_to_http(data["image"])
    name = data.get("name", f"YONAMAXI #{token_id}")

    traits = []
    for t in data.get("attributes", []):
        traits.append(f"• {t.get('trait_type')}: {t.get('value')}")

    caption = f"🔥 {name}\n\n" + "\n".join(traits[:5])

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": THREAD_ID,
        "photo": image,
        "caption": caption
    }

    requests.post(url, data=payload)


if __name__ == "__main__":
    main()
