#!/usr/bin/env python3
# generate.py
import csv
import subprocess
import shlex
import os

CSV = "channels.csv"
OUT = "playlist.m3u"
COOKIES = "cookies.txt" if os.path.exists("cookies.txt") else None

def run_yt_dlp(url):
    # Try a few fallback commands to extract a playable URL
    cmds = [
        ["yt-dlp","-f","best","-g", url],
        ["yt-dlp","-f","best[protocol^=m3u8]/best","-g", url],
        ["yt-dlp","-f","bv*+ba/best","-g", url]  # fallback
    ]
    for cmd in cmds:
        cmd_use = cmd.copy()
        if COOKIES:
            cmd_use += ["--cookies", COOKIES]
        try:
            out = subprocess.check_output(cmd_use, stderr=subprocess.DEVNULL, timeout=35)
            text = out.decode().strip()
            if text:
                # sometimes yt-dlp returns multiple URLs separated by newline; take first
                return text.splitlines()[0].strip()
        except Exception:
            continue
    return None

def safe(s):
    return s.strip()

with open(OUT,"w",encoding="utf-8") as outf:
    outf.write("#EXTM3U\n")
    with open(CSV, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: 
                continue
            # handle header if present
            if len(row) >= 2 and row[0].strip().lower() == "name" and row[1].strip().lower().startswith("http"):
                # header detected because first col is "name" and second looks like url; still process (but skip if header row)
                pass
            if len(row) < 2:
                continue
            name = safe(row[0])
            url = safe(row[1])
            if not name or not url:
                continue
            print(f"Processing: {name} -> {url}")
            stream = run_yt_dlp(url)
            if stream:
                outf.write(f'#EXTINF:-1 tvg-name="{name}",{name}\n')
                outf.write(stream + "\n")
            else:
                print(f"Warning: no URL found for {name}")
