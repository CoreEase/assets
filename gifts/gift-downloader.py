import os
import sys
from pathlib import Path
from urllib.request import urlretrieve, Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = "https://cdn.changes.tg/gifts/originals/{gift_id}/{filename}"

FILENAMES = [
    "Original.png",
    "Original.json",
    "Original.tgs",
]

GIFT_IDS = [
    "5974210632977745012",
    "6026193266406327981",
    "5969796561943660080",
    "5935895822435615975",
    "5893356958802511476",
    "5866352046986232958",
    "5800655655995968830",
    "5801108895304779062",
    "5956217000635139069",
    "5922558454332916696",
]

OUTPUT_DIR = Path("gifts")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; GiftDownloader/1.0)"
}

def download_file(url: str, dest: Path) -> bool:
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=30) as response:
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                f.write(response.read())
        print(f"  ✅ {dest.name}")
        return True
    except HTTPError as e:
        print(f"  ❌ HTTP {e.code}: {dest.name}")
    except URLError as e:
        print(f"  ❌ Network error: {dest.name} → {e.reason}")
    except Exception as e:
        print(f"  ❌ {dest.name}: {e}")
    return False

def main():
    print("🚀 Starting gift download...\n")
    OUTPUT_DIR.mkdir(exist_ok=True)

    total = 0
    success = 0

    for gift_id in GIFT_IDS:
        gift_dir = OUTPUT_DIR / gift_id
        print(f"📦 Gift ID: {gift_id}")

        for filename in FILENAMES:
            total += 1
            url = BASE_URL.format(gift_id=gift_id, filename=filename)
            dest = gift_dir / filename

            if download_file(url, dest):
                success += 1

        print()

    print("=" * 40)
    print(f"Finished: {success}/{total} files downloaded")
    print(f"Output folder: {OUTPUT_DIR.resolve()}")

    if success == 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
