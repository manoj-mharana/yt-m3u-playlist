# generate.py (Hostinger version)
import pandas as pd
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "channels.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "playlist.m3u")
COOKIES_FILE = os.path.join(BASE_DIR, "cookies.txt")

def get_stream_url(url):
    try:
        cmd = ['yt-dlp', '-g']
        if os.path.exists(COOKIES_FILE):
            cmd += ['--cookies', COOKIES_FILE]
        cmd.append(url)

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        out = proc.stdout.strip().splitlines()
        if out:
            for line in out:
                if line.strip():
                    return line.strip()
    except Exception as e:
        print("yt-dlp error for", url, "->", e)
    return None

def generate_m3u():
    df = pd.read_csv(CSV_FILE)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for _, row in df.iterrows():
            name = row.get("name", "") or ""
            url = (row.get("url", "") or "").strip()
            if not url:
                continue
            stream = url
            if "youtube.com" in url or "youtu.be" in url:
                s = get_stream_url(url)
                if s:
                    stream = s
                else:
                    print("Warning: could not extract stream for", name)
            f.write(f"#EXTINF:-1,{name}\n{stream}\n")

if __name__ == "__main__":
    generate_m3u()
    print("✅ Playlist updated:", OUTPUT_FILE)
