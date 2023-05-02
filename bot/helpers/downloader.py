import os
import aria2p
import asyncio
import glob
import yt_dlp
from yt_dlp import DownloadError
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.helpers.utils import aria2

async def download_file(url, dl_path, gid, sent_message):
    try:
        aria2.add_uris([url], {'dir': dl_path,  'gid': gid})
        while True:
            downloads = aria2.get_downloads(gids=[gid])
            for download in downloads:
                status = download.status
                progress = download.progress
                progress_bar = f'{download.download_speed}\n{download.completed_length}\n{download.name}\n{download.total_length}'
                LOGGER.info(f'{progress_bar}')
                for file in download.files:
                    path = file.path
                if status == "complete":
                    LOGGER.info("Download complete")
                    if os.path.exists(path):
                        return True, path
                    else:
                        return False, path
                elif status == "error":
                    return False, download.error_message
            await asyncio.sleep(2)
    except aria2p.client.ClientException as error:
        return False, error
    except Exception as error:
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
