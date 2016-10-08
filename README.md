
## Install & Run
```
pip3 install -r requirements.txt

python3 trans2.py
```

## Fix Audio
```
ffmpeg -i trumpc.mp4 -ar 16000 -ac 1 trump.wav
ffmpeg -ss 200 -t 15 -i trump.wav trumpshort2.wav

```
