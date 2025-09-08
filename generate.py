import pandas as pd
import subprocess
import os

# CSV read
channels = pd.read_csv("channels.csv")

playlist_lines = ["#EXTM3U\n"]

# Get YTDLP_OPTS (if set in workflow)
yt_dlp_opts = os.environ.get("YTDLP_OPTS", "")

for _, row in channels.iterrows():
    name = row["name"]
    url = row["url"]

    try:
        # yt-dlp command
        cmd = f"yt-dlp -g {yt_dlp_opts} {url}"
        result = subprocess.check_output(cmd, shell=True, text=True).strip()

        if result:
            stream_url = result.split("\n")[-1]  # last URL
            playlist_lines.append(f"#EXTINF:-1,{name}\n{stream_url}\n")
        else:
            print(f"⚠️ Warning: no stream extracted for {name}")

    except Exception as e:
        print(f"⚠️ Warning: could not extract stream for {name} ({e})")

# Write playlist
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.writelines(playlist_lines)

print("✅ Playlist generated: playlist.m3u")
