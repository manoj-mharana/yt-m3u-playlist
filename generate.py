# generate.py (updated)
import pandas as pd
import subprocess
import os

def get_stream_url(url):
    try:
        # yt-dlp -g returns direct media URL(s)
        proc = subprocess.run(['yt-dlp', '-g', '--cookies', 'cookies.txt', url], capture_output=True, text=True, timeout=120)
        out = proc.stdout.strip().splitlines()
        if out:
            # prefer first non-empty line
            for line in out:
                if line.strip():
                    return line.strip()
    except Exception as e:
        print("yt-dlp error for", url, "->", e)
    return None

def generate_m3u(csv_file, output_file):
    df = pd.read_csv(csv_file)
    with open(output_file, "w", encoding="utf-8") as f:
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
    csv_file = os.environ.get("CSV_FILE", "channels.csv")
    output_file = os.environ.get("OUTPUT_FILE", "playlist.m3u")
    generate_m3u(csv_file, output_file)
    print("✅ Playlist generated:", output_file)
