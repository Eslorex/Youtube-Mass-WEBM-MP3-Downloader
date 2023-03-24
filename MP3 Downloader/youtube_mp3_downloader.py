import os
import yt_dlp
import unicodedata
from tqdm import tqdm
from multiprocessing import Pool
import json

CONFIG_FILENAME = 'config.json'

def load_config():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_path, CONFIG_FILENAME)
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    return {}

def save_config(config):
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_path, CONFIG_FILENAME)
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=2)

def check_ffmpeg():
    config = load_config()
    ffmpeg_path = config.get('ffmpeg_path', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ffmpeg', 'bin', 'ffmpeg.exe'))
    while not os.path.exists(ffmpeg_path):
        print("ffmpeg.exe not found at", ffmpeg_path)
        ffmpeg_path = input("Please provide the correct path to ffmpeg.exe: ")
    config['ffmpeg_path'] = ffmpeg_path
    save_config(config)
    return ffmpeg_path

def download_video(url):
    ffmpeg_path = check_ffmpeg()
    ffprobe_path = os.path.join(os.path.dirname(ffmpeg_path), 'ffprobe.exe')

    script_path = os.path.dirname(os.path.realpath(__file__))
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

def download_videos(urls):
    with Pool() as pool:
        filenames = pool.map(download_video, urls)
    return filenames

def main():
    print("Enter YouTube URLs one at a time. Press Ctrl-C to exit.")

    while True:
        try:
            url = input("Enter URL: ")
        except KeyboardInterrupt:
            print("Exiting...")
            break

        filename = download_video(url)
        if filename:
            print(f"Successfully downloaded: {filename}")
        else:
            print(f"Error downloading {url}")

if __name__ == "__main__":
    main()
