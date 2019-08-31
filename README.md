# Spacevid
Spacevid is a tool for transcoding large videos to fit a specified file size with minimal adjustment to the bitrate.

# Limitations  
This application was developed specifically for my use case so it only outputs 480p 24FPS WebMs, the only thing that varies is the output bitrate.  
# Prerequisites  

 - FFMPEG  
 - Tensorflow
 - Python3

# Usage
Dump a bunch of videos in `./dataset/videos` then run `./generate_data.py`, for best results you'll want to use videos similar to the ones you're likely to convert (e.g: if you tend to convert alot of YouTube and TikTok clips, use those kinds of videos).

After you've generated a bunch of data (give it a few hours or so) you can use `./convert.py` to convert your video. It takes the following arguments:
 - `filename` - The path to the video file you want to convert
 - `size` - The target file size in bytes
 - `-o` `--output` - The path you'd like to output to
 - `-e` `--epochs` - The amount of training sessions you'd Spacevid to do before converting
 - `-d` `--dont-remember` - By default Spacevid will save the results of every transcode and use it to train itself in future, use this if you'd like to avoid that
 - `-h` `--help` - show the help (it's basically just this tbh)

# Background
I wrote it while on holiday because I had almost no internet and so I started trying to transcode a bunch of video memes I had so that they'd be small enough to post on Spacechan.
The formulas I found would give me bitrates that produced files that were way too small and low quality and I didn't want to figure it out through trial and error. It then occured to me that a neural net would be perfect for this and it'd give me an opportunity to learn Tensorflow so that's what I did.  
Thanks to ∆xel for giving me pointers.
