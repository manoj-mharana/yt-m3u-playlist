import pandas as pd
import sys

def generate_m3u(csv_file, output_file):
    df = pd.read_csv(csv_file)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for _, row in df.iterrows():
            name, url = row["name"], row["url"]
            if pd.notna(url) and url.strip():
                f.write(f"#EXTINF:-1,{name}\n{url}\n")

if __name__ == "__main__":
    csv_file = "channels.csv"
    output_file = "playlist.m3u"
    generate_m3u(csv_file, output_file)
    print(f"✅ Playlist generated: {output_file}")
