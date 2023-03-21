import os
import yt_dlp
import unicodedata
from tqdm import tqdm

def download_video(url):
    script_path = os.path.dirname(os.path.realpath(__file__))
    ffmpeg_path = os.path.join(script_path, 'ffmpeg', 'bin', 'ffmpeg.exe')
    ffprobe_path = os.path.join(script_path, 'ffmpeg', 'bin', 'ffprobe.exe')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(script_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,
        'ffprobe_location': ffprobe_path,
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

def main():
    print("Enter YouTube URLs one at a time. Type 'exit' to quit the program.")

    while True:
        url = input("Enter URL: ")

        if url.lower() == 'exit':
            break

        filename = download_video(url)
        if filename:
            print(f"Successfully downloaded: {filename}")
        else:
            print(f"Error downloading {url}")

if __name__ == "__main__":
    main()
