# Intro

simple script to upload instagram reels 'n' many times

# Features:

- random delay and random effect applied using `ffmpeg` to avoid detection
- no need to do anything except provide username and password in `./script.py`

# Tutorial
- download this repo as zip file and extract it
- First run the `dependency.bat` to install all dependencies
- Edit the `username` and `password` field in `./script.py`'s main function
```python
def main():
    username = "username_here"
    password = "pass_here"

```
- Edit `./caption.txt` to edit the caption and edit `./times.txt` to edit how many times to upload
- drag the video u want to upload to the `script.py` or run `script.py` and paste the video's path
