import os
import sys
from pathlib import Path
from urllib.request import urlretrieve, Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = "https://cdn.changes.tg/gifts/originals/{gift_id}/{filename}"

GIFT_IDS = [
 "6046178578163303744", 
]

FILE_EXTENSIONS = [".png", ".json", ".tgs"]

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
    print(f"📦 Total gifts: {len(GIFT_IDS)}")
    print(f"📁 Output folder: {OUTPUT_DIR}\n")
    
    OUTPUT_DIR.mkdir(exist_ok=True)

    total = 0
    success = 0

    for gift_id in GIFT_IDS:
        gift_dir = OUTPUT_DIR / gift_id
        print(f"📦 Gift ID: {gift_id}")

        for ext in FILE_EXTENSIONS:
            total += 1
            filename = f"{gift_id}{ext}"
            url = BASE_URL.format(gift_id=gift_id, filename=f"Original{ext}")
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
