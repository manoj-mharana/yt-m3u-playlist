# generate.py
import pandas as pd
import subprocess
import os

def run_yt_dlp(args):
    """Helper to run yt-dlp and return stdout lines"""
    try:
        proc = subprocess.run(
            ["yt-dlp"] + args,
            capture_output=True, text=True, timeout=60
        )
        return proc.stdout.strip().splitlines()
    except Exception as e:
        print("yt-dlp error:", e)
        return []

def get_live_stream_url(url):
    """
    1. If URL is /@channel/live → get actual video ID
    2. Then extract direct playable URL
    """
    # Step 1: resolve video ID
    vid_id = None
    if "/live" in url:
        out = run_yt_dlp(["--get-id", url])
        if out:
            vid_id = out[0].strip()
    else:
        # assume it's already a direct video link
        if "watch?v=" in url:
            vid_id = url.split("watch?v=")[-1].split("&")[0]

    if not vid_id:
        print("⚠️ Could not resolve video ID for", url)
        return None

    # Step 2: get streamable URL
    out = run_yt_dlp(["-g", f"https://www.youtube.com/watch?v={vid_id}"])
    if out:
        return out[0].strip()
    return None

def generate_m3u(csv_file, output_file):
    df = pd.read_csv(csv_file)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for _, row in df.iterrows():
            name = row.get("name", "").strip()
            url = (row.get("url", "") or "").strip()
            if not url:
                continue
            stream = url
            if "youtube.com" in url or "youtu.be" in url:
                s = get_live_stream_url(url)
                if s:
                    stream = s
                else:
                    print(f"⚠️ Warning: could not extract stream for {name}")
            f.write(f"#EXTINF:-1,{name}\n{stream}\n")

if __name__ == "__main__":
    csv_file = os.environ.get("CSV_FILE", "channels.csv")
    output_file = os.environ.get("OUTPUT_FILE", "playlist.m3u")
    generate_m3u(csv_file, output_file)
    print("✅ Playlist generated:", output_file)
