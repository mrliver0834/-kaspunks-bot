import requests
import random
import os

TOKEN = "7565680248:AAG0bNUtg_9ZwlhySu8MU-BOEbwpESWY16Y"
CHAT_ID = "-1002493995289"

TOTAL_ITEMS = 3357
METADATA_CID = "bafybeicpypf5l2b6hj5wl5g7dfc5dttjleeg7auddsw76ta5kmo2obgyfu"

LAST_ID_FILE = "last_id.txt"


def ipfs_to_http(ipfs_url: str) -> str:
    if ipfs_url.startswith("ipfs://"):
        return "https://ipfs.io/ipfs/" + ipfs_url.replace("ipfs://", "")
    return ipfs_url


def build_metadata_url(token_id: int) -> str:
    return f"https://ipfs.io/ipfs/{METADATA_CID}/{token_id}.json"


def load_last_id():
    if not os.path.exists(LAST_ID_FILE):
        return None

    with open(LAST_ID_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def save_last_id(token_id: int):
    with open(LAST_ID_FILE, "w", encoding="utf-8") as f:
        f.write(str(token_id))


def pick_random_id():
    last_id = load_last_id()
    token_id = random.randint(1, TOTAL_ITEMS)

    if TOTAL_ITEMS > 1 and str(token_id) == last_id:
        while str(token_id) == last_id:
            token_id = random.randint(1, TOTAL_ITEMS)

    return token_id


def get_metadata(token_id: int):
    metadata_url = build_metadata_url(token_id)

    res = requests.get(metadata_url, timeout=20)
    res.raise_for_status()

    return res.json()


def extract_traits(data: dict) -> list[str]:
    items = data.get("attributes", [])
    trait_list = []

    for item in items:
        trait_type = item.get("trait_type")
        value = item.get("value")

        if value is None:
            continue

        trait_list.append(f"• {trait_type}: {value}")

    return trait_list


def build_caption(name: str, traits: list[str]) -> str:
    if not traits:
        return f"🔥 {name}"

    traits_text = "\n".join(traits[:5])
    return f"🔥 {name}\n\n{traits_text}"


def main():
    token_id = pick_random_id()
    data = get_metadata(token_id)

    image = data.get("image")
    name = data.get("name", f"KasPunk #{token_id}")

    if not image:
        raise ValueError("metadata に image がありません")

    image_url = ipfs_to_http(image)
    traits = extract_traits(data)
    caption = build_caption(name, traits)

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": caption
    }

    send_res = requests.post(telegram_url, data=payload, timeout=30)
    send_res.raise_for_status()

    save_last_id(token_id)

    print("posted:", name, image_url)
    print("traits:", traits)


if __name__ == "__main__":
    main()
