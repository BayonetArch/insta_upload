from pathlib import Path
from instagrapi import Client
import os
import sys
import random
import time
import subprocess
import tempfile
from instagrapi.exceptions import LoginRequired


def fatal(e):
    print(f"[Error]: {e}")
    input("Press Enter to exit...")
    exit(1)


def info(s):
    print(f"[INFO]: {s}")


def login(username, password):
    cl = Client()
    session_path = convert_path("./session.json")

    if os.path.exists(session_path):
        info(f"session.json found!")
        cl.load_settings(session_path)
        cl.login(username, password)
        try:
            cl.get_timeline_feed()
        except LoginRequired:
            info("Session expired, doing fresh login...")
            cl.set_settings({})
            cl.login(username, password)
            cl.dump_settings(session_path)

    else:
        info(f"session.json not found,doing fresh login...")
        try:
            cl.login(username, password)
        except Exception as e:
            fatal(f"Login failed.\nReason: {e}\ndid u provide correct username and password?")

        cl.dump_settings(session_path)

    info("Logged in as " + str(cl.username))
    return cl


def convert_path(path):
    path = path.strip().strip('"').strip("'")

    if os.name == "nt":
        if path.startswith("/mnt/"):
            parts = path.split("/")
            drive = parts[2].upper()
            rest = "\\".join(parts[3:])
            return Path(f"{drive}:\\{rest}")
        else:
            return Path(path)
    else:
        return path


def get_caption():
    caption = "Caption was not retrieved"
    caption_path = Path(convert_path("./caption.txt"))

    try:
        with open(caption_path) as f:
            caption = f.read()
    except Exception as e:
        fatal(e)
    return caption


def get_times():
    times = 10
    times_path = Path(convert_path("./times.txt"))

    try:
        with open(times_path) as f:
            times = int(f.read())
    except Exception as e:
        fatal(e)
    return times


def get_video():
    video = ""

    if len(sys.argv) < 2:
        print("[Error]: Video file was not provided as an argument")
        video = input("Enter path to video: ")
        if not video:
            fatal("empty path to video!")
    else:
        video = sys.argv[1]

    return Path(convert_path(video))


def upload_reel(cl, path, caption):
    try:
        cl.clip_upload(path=path, caption=caption)
    except Exception as e:
        fatal(e)

    info("Upload Success")


def main():
    username = "username_here"
    password = "pass_here"

    cl = login(username, password)
    caption = get_caption()
    path = get_video()
    times = get_times()

    for i in range(times):

        temp = Path(tempfile.gettempdir()) / f"varied_{i}.mp4"
        brightness = round(random.uniform(-0.05, 0.05), 3)
        contrast = round(random.uniform(0.95, 1.05), 3)

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(path),
                "-vcodec",
                "libx264",
                "-crf",
                "18",
                "-vf",
                f"eq=brightness={brightness}:contrast={contrast}",
                "-acodec",
                "aac",
                str(temp),
                "-y",
            ]
        )
        info(f"Uploading \x1b[0;32m{i+1}/{times}\x1b[0m...")
        upload_reel(cl, temp, caption)

        temp.unlink()

        if i < times - 1:
            delay = random.uniform(5, 7)
            info(
                f"Waiting \x1b[0;32m{delay:.1f}\x1b[0m seconds before another upload...."
            )
            time.sleep(delay)


if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
