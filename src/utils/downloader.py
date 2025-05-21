import requests

def download_file(url: str, output_path: str) -> bool:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"[Downloader] Failed to download from {url}: {e}")
        return False
