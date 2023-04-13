import os
import wget
import glob
import yt_dlp
from urllib.error import HTTPError
from yt_dlp import DownloadError
from bot import DOWNLOAD_DIRECTORY, LOGGER
import aria2p
import time

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
        while True:
            status = download.status
            if status == "complete":
                LOGGER.info("Download complete")
                file = download.files[0].path
                cwd = os.getcwd()  # Get current working directory
                path = os.path.join(cwd, file)  # Concatenate cwd and filename
                return True, path
            elif status == "active":
                LOGGER.info("Download is active...")
                download.update()
                time.sleep(5) # wait for 1 second and check status again
            elif status == "error":
                # code to run when download encounters an error
                LOGGER.info("Download failed: {}".format(download.error_message))
                return False, download.error_message
    except aria2p.client.ClientException as error:
        # code to run when aria2p client raises an exception
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
