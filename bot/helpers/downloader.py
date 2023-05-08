import os
import aria2p
import asyncio
import glob
import yt_dlp
from yt_dlp import DownloadError
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.helpers.utils import aria2, humanbytes

async def download_file(url, dl_path, gid, sent_message):
    try:
        aria2.add_uris([url], {'dir': dl_path, 'gid': gid})
        while True:
            download = aria2.get_download(gids=[gid])
            download.update()
            if download.completed_length != 0:
              progress = "{:.2f}".format(download.progress)
              progress_bar = "📥 Downloading File...\n"
              progress_bar += f"File name: {download.name}\n"
              progress_bar += f"File size: {humanbytes(download.total_length)}\n"
              progress_bar += f"Speed: {humanbytes(download.download_speed)}/s|ETA: {download.eta}\n"
              progress_bar += f"Processed size: {humanbytes(download.completed_length)}\n"
              progress_bar += f"Progress: {progress}%"
            try:
              await sent_message.edit(progress_bar)
            except:
              pass
            path = download.file.path
            if download.is_complete:
              LOGGER.info("Download complete")
              if os.path.exists(path):
                return True, path
              else:
                return False, path
            elif download.has_failed:
              return False, download.error_message
            await asyncio.sleep(0.5)
    except aria2p.client.ClientException as error:
        return False, error
    except Exception as error:
        return False, error

def utube_dl(link):
  ytdl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_DIRECTORY, '%(title)s'),
    'noplaylist': True,
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
      if path.endswith(('.avi', '.mov', '.flv', '.wmv', '.3gp', '.mpeg', '.webm', '.mp4', '.mkv', '.acc', '.m4a', '.mp3', '.ogg', '.wav')) and \
          path.startswith(ytdl.prepare_filename(meta)):
        return True, path
    return False, 'Something went wrong! No video file exists on server.'
