import os
import yt_dlp
import unicodedata
from tqdm import tqdm
from multiprocessing import Pool

def download_video(url):
    script_path = os.path.dirname(os.path.realpath(__file__))
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(script_path, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            with tqdm(total=info['filesize'], unit='B', unit_scale=True, desc=filename) as pbar:
                ydl_opts['progress_hooks'] = [lambda d: pbar.update(d['downloaded_bytes']) if d['status'] == 'downloading' else None]
                ydl.download([url])
            return filename
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def download_videos(urls):
    with Pool() as pool:
        filenames = pool.map(download_video, urls)
    return filenames

def main():
    print("Enter YouTube URLs. Type 'exit' to quit the program.")

    while True:
        urls = input("Enter URLs: ")

        if urls.lower() == 'exit':
            break

        urls = urls.split(",")
        filenames = download_videos(urls)

        for filename in filenames:
            if filename:
                normalized_filename = unicodedata.normalize('NFC', filename)
                os.rename(filename, normalized_filename)
                print(f"Successfully downloaded: {normalized_filename}")
            else:
                print(f"Error downloading {url}")

if __name__ == "__main__":
    main()
