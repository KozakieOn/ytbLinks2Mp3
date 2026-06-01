import yt_dlp
import urllib.request
import threading
from mutagen.id3 import ID3, APIC, ID3NoHeaderError


def download(url, output_name, output_dir="output/", on_progress=None, on_finish=None):
    thread = threading.Thread(target=_download, args=(url, output_name, output_dir, on_progress, on_finish))
    thread.start()

def _download(url, output_name, output_dir, on_progress, on_finish):
    def progress_hook(d):
        if d["status"] == "downloading" and on_progress:
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                percent = (downloaded / total) * 100
                on_progress(percent)

    info = {}
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    thumbnail_url = info.get("thumbnail")
    if not output_name:
        output_name = info.get("title", "output")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}{output_name}.%(ext)s",
        "progress_hooks": [progress_hook],
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    _embed_cover(f"{output_dir}{output_name}.mp3", thumbnail_url)

    if on_finish:
        on_finish()

def _embed_cover(mp3_path, thumbnail_url):
    try:
        with urllib.request.urlopen(thumbnail_url) as response:
            cover_data = response.read()

        try:
            tags = ID3(mp3_path)
        except ID3NoHeaderError:
            tags = ID3()

        tags["APIC"] = APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=cover_data,
        )
        tags.save(mp3_path, v2_version=3)

    except Exception as e:
        print(f"Cover error: {e}")