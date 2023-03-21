

# Youtube Youtube Mass WEBM MP3 Downloader


So basically, youtube only provides videos as webm files. If you want to download mp3 files you have to make conversion with ffmpeg. And this program does it automatically for you. Release package has the ffmpeg file.

![alt text](https://cdn.discordapp.com/attachments/1080953525737111562/1087691419344449597/3.png)


1. Install python (check ADD to PATH).
2. Run install_libraries.py so it can install required packages.
3. And its done! You have completely **free** mp3 downloader. You don't have to deal with crappy sites filled with ads and can avoid matrix. And works with any amount of lines of Youtube URLs. You can use it to easily download many mp3 files to use it for your SoundPad.

I've made some threading to make the process much faster. Its possible to use GPU cores to make this process much faster. But i was too lazy to research and work with CUDA cores.

Known Issues:

Since its a console program (I was too lazy again to make UI for it) , it might not get the last url so pressing Enter again will make it work.

It will not show any progress when converting file into mp3 from webm. And it might take a bit for it to convert mp3 depending on your pc specs so don't worry when nothing happens on console screen. Just wait for the progress. You can see the progress if you refresh the folder.



