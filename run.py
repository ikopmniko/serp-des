import requests
import time
from concurrent.futures import ThreadPoolExecutor

# API Serper
API_KEY = "f8e2f001d14f486ff378ab9a421d90bbfd32e60e"
URL_API = "https://google.serper.dev/search"

# Endpoint PHP kamu
PHP_ENDPOINT = "https://leamarie-yoga.de/save_serper.php"

# Rentang baris
mulai = 22500
endnya = 25000

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def search_url(idx, target_url):
    query = f"site:{target_url}"
    payload = {"q": query}

    try:
        response = requests.post(URL_API, headers=headers, json=payload, timeout=30)
        data = response.json()

        if "organic" in data and len(data["organic"]) > 0:
            top_result = data["organic"][0]
            title = top_result.get("title", "")
            link = top_result.get("link", "")
            snippet = top_result.get("snippet", "").strip()
            if not snippet:
                snippet = "snipet nya kosong"
            print(f"[{idx}] ✔ {title} -> {link}")
            return {"title": title, "url": link}
        else:
            print(f"[{idx}] ❌ Tidak ditemukan: {target_url}")
            return None

    except Exception as e:
        print(f"[{idx}] ⚠ Error: {e}")
        return None

    finally:
        time.sleep(1.2)

def send_to_php(data):
    """
    Kirim data ke API PHP (save_serper.php) dalam bentuk JSON:
    { "url": "...", "title": "..." }
    """
    try:
        res = requests.post(PHP_ENDPOINT, json=data, timeout=15)
        if res.status_code == 200:
            print(f"✔ Terkirim ke PHP: {data['url']}")
        else:
            print(f"⚠ Gagal kirim ke PHP ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"⚠ Error kirim ke PHP: {e}")

def worker(idx, url):
    result = search_url(idx, url)
    if result:
        send_to_php(result)

def main(start_line=1, end_line=None):
    with open("list_url.csv", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    urls = urls[start_line - 1 : end_line]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(worker, idx + start_line, url) for idx, url in enumerate(urls)]
        for f in futures:
            f.result()

if __name__ == "__main__":
    main(start_line=mulai, end_line=endnya)










