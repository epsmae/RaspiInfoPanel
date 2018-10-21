# Raspberry Info Panel

Code for a raspberry info panel which shows a endless video.
The video can be copied from usb memory stick.
Video control is available over the keyboard or gpio's.


Uses a modified version from the raspberry hello_video example.

## Convert Videos
### Convert images to .h264 video
```sh
ffmpeg -f image2 -framerate 0.1 -i image%03d.png -c:v libx264 -preset veryslow -qp 18 -pix_fmt yuv420p -r 25 infopanel.h264
```
### Convert video to .h264 video
```sh
ffmpeg -i infopanel.wmv -vcodec libx264 -refs 1 -x264opts b-pyramid=0 -profile:v main -level:v 4.1 -r 25 infopanel.h264
```

