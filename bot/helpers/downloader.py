import os
import wget
import glob
import yt_dlp
from urllib.error import HTTPError
from yt_dlp import DownloadError
from bot import DOWNLOAD_DIRECTORY, LOGGER
import aria2p

# initialization, these are the default values
aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)

def download_file(url, dl_path):
  try:
    download = aria2.add_uris([url], options={"dir": dl_path})
    download.wait()
    return True, download.files()[0].path
  except aria2p.client.ClientException as error:
    return False, error

def download_fb(url, dl_path):
  try:
    filename = wget.download(url, dl_path)
    return True, os.path.join(f"{DOWNLOAD_DIRECTORY}/{filename}")
  except HTTPError as error:
    return False, error


def utube_dl(link):
  ytdl_opts = {
    'outtmpl' : os.path.join(DOWNLOAD_DIRECTORY, '%(title)s'),
    'noplaylist' : True,
    'logger': LOGGER,
    'format': 'bestvideo+bestaudio/best',
    'geo_bypass_country': 'IN',
    'verbose': True,
    'update': True
  }
  with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
    try:
      meta = ytdl.extract_info(link, download=True)
    except DownloadError as e:
      return False, str(e)
    for path in glob.glob(os.path.join(DOWNLOAD_DIRECTORY, '*')):
      if path.endswith(('.avi', '.mov', '.flv', '.wmv', '.3gp','.mpeg', '.webm', '.mp4', '.mkv', '.acc', '.m4a', '.mp3', '.ogg', '.wav')) and \
          path.startswith(ytdl.prepare_filename(meta)):
        return True, path
    return False, 'Something went wrong! No video file exists on server.'
