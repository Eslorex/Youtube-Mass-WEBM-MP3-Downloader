import subprocess

libraries = ['yt-dlp', 'tqdm']

for library in libraries:
    subprocess.check_call(['pip', 'install', library])
