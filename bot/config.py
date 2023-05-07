class config:
    BOT_TOKEN = "6177070670:AAF4XMqVka2P0pboli9g9CWKOg-Y-cwqTdQ"
    APP_ID = "10112326"
    API_HASH = "76b4e277c75aaf991589d78eca42946a"
    DATABASE_URL = "mongodb://mongo:TpghbMFn6sO3JyPFzrRP@containers-us-west-148.railway.app:6601"
    SUDO_USERS = "5227230295" # Sepearted by space.
    SUPPORT_CHAT_LINK = ""
    DOWNLOAD_DIRECTORY = "/usr/src/app/downloads/"
    G_DRIVE_CLIENT_ID = "564756005768-5vf0hs66doiptjr9304u9busj2kf4p8d.apps.googleusercontent.com"
    G_DRIVE_CLIENT_SECRET = "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"


class BotCommands:
    Start = 'start'
    Download = 'download'
    Authorize = 'auth'
    SetFolder = 'setfolder'
    Revoke = 'revoke'
    Clone = 'clone'
    Delete = 'delete'
    EmptyTrash = 'emptytrash'
    YtDl = 'ytdl'
    Storage = 'storage'
    Speed = 'speedtest'
    Ping = 'ping'
    Stats = 'stats'

class Messages:
    START_MSG = """**Hi there {}.**\n__I'm Google Drive Uploader Bot V3.You can use me to upload any file / video to Google Drive from direct link or Telegram Files.__\n__You can know more from /help.__ \n***Supported Direct Link***\nFacebook Video\nGoogle Drive\nYoutube\nSolidfiles\nAnonfiles\nMediafire\nZippyshare\n[Yt-dlp support sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)\nOne Drive\nTera Box\nGdtot"""

    HELP_MSG = [
        ".",
        """**Google Drive Uploader**\n__I can upload files from link or Telegram Files to your Google Drive. All i need is to authenticate me to your Google Drive Account and send a link or Telegram File.__\n\nI have more features... ! Wanna know about it ? Just walkthrough this tutorial and read the messages carefully.""",

        f"**Authenticating Google Drive**\n__Send the /{BotCommands.Authorize} commmand and you will receive a URL, visit URL and follow the steps and send the received code here. Use /{BotCommands.Revoke} to revoke your currently logged Google Drive Account.__\n\n**Note: I will not listen to any command or message (except /{BotCommands.Authorize} command) until you authorize me.\nSo, Authorization is mandatory !**",

        f"**Telegram Files**\n__To Upload telegram files in your Google drive Account just send me the file and i will download and upload it to your Google Drive Account.__\n\n**YouTube-DL Support**\n__Download files via yt-dlp.\nUse /{BotCommands.YtDl} (YouTube Link/ytdlp Supported site link)__",

        f"**Custom Folder for Upload**\n__Want to upload in custom folder or in__ **TeamDrive** __ ?\nUse /{BotCommands.SetFolder} (Folder URL) to set custom upload folder.\nAll the files are uploaded in the custom folder you provide.__",

        f"**Delete Google Drive Files**\n__Delete google drive files. Use /{BotCommands.Delete} (File/Folder URL) to delete file or reply /{BotCommands.Delete} to bot message.\nYou can also empty trash files use /{BotCommands.EmptyTrash}\nNote: Files are deleted permanently. This process cannot be undone.\n\n**Copy Google Drive Files**\n__Yes, Clone or Copy Google Drive Files.\n__Use /{BotCommands.Clone} (File id / Folder id or URL) to copy Google Drive Files in your Google Drive Account.__",

        "**Join Channel @drivetalkchannel**"
        ]

    RATE_LIMIT_EXCEEDED_MESSAGE = """❗ **Rate Limit Exceeded.**\n__User rate limit exceeded try after 24 hours.__"""

    FILE_NOT_FOUND_MESSAGE = """❗ **File/Folder not found.**\n__File id - {} Not found. Make sure it\'s exists and accessible by the logged account.__"""

    INVALID_GDRIVE_URL = """❗ **Invalid Google Drive URL**\nMake sure the Google Drive URL is in valid format."""

    COPIED_SUCCESSFULLY = """✅ **Copied successfully.**\n[{}]({}) __({})__"""

    NOT_AUTH = f"""🔑 **You have not authenticated me to upload to any account.**\n__Send /{BotCommands.Authorize} to authenticate.__"""

    DOWNLOADED_SUCCESSFULLY = '📤 **Uploading File...**\n**Filename:** {}\n**Size:** {}'

    UPLOADED_SUCCESSFULLY = """✅ **Uploaded Successfully.**\n[{}]({}) __({})__"""

    DOWNLOAD_ERROR = """❗**Downloader Failed**\n{}\n__Link - {}__"""

    CLONE_ERROR = """❗**Clone Failed**\n{}\n__Link - {}__"""

    DOWNLOADING = """📥 **Downloading File...\nLink:** {}"""

    ALREADY_AUTH = """🔒 **Already authorized your Google Drive Account.**\n__Use /revoke to revoke the current account.__\n__Send me a direct link or File to Upload on Google Drive__"""

    FLOW_IS_NONE = f"""❗ **Invalid Code**\n__Run {BotCommands.Authorize} first.__"""

    AUTH_SUCCESSFULLY = """🔐 **Authorized Google Drive account Successfully.**"""

    INVALID_AUTH_CODE = """❗ **Invalid Code**\n__The code you have sent is invalid or already used before. Generate new one by the Authorization URL__"""

    AUTH_TEXT = """⛓️ **To Authorize your Google Drive account visit this [URL]({}) and send the generated code here.**\n__Visit the URL > Allow permissions > you will get a code > copy it > Send it here__"""

    DOWNLOAD_TG_FILE = """📥 Downloading File...\nFilename: {}\nSize: {}\nFile Type: {}"""

    PARENT_SET_SUCCESS = '🆔✅ **Custom Folder link set successfully.**\n__Your custom folder id - {}\nUse__ ```/{} clear``` __to clear it.__'

    PARENT_CLEAR_SUCCESS = f"""🆔🚮 **Custom Folder ID Cleared Successfuly.**\n__Use /{BotCommands.SetFolder} (Folder Link)to set it back__."""

    CURRENT_PARENT = '🆔 **Your Current Custom Folder ID - {}**\n__Use__ /{} (Folder link) __to change it.__'

    REVOKED = f"""🔓 **Revoked current logged account successfully.**\n__Use /{BotCommands.Authorize} to authenticate again and use this bot.__"""

    NOT_FOLDER_LINK = """❗ **Invalid folder link.**\n__The link you send its not belong to a folder.__"""

    CLONING = """🗂️ **Cloning into Google Drive...**\n__G-Drive Link - {}__"""

    PROVIDE_GDRIVE_URL = """**❗ Provide a valid Google Drive URL along with commmand.**\n__Usage - /{} (GDrive Link)__"""

    INSUFFICIENT_PERMISSONS = """❗ **You have insufficient permissions for this file.**\n__File id - {}__"""

    DELETED_SUCCESSFULLY = """🗑️✅ **File Deleted Successfully.**\n__File deleted permanently !\nFile id - {}__"""

    WENT_WRONG = """⁉️ **ERROR: SOMETHING WENT WRONG**\n__Please try again later.__"""

    EMPTY_TRASH = """🗑️🚮**Trash Emptied Successfully !**"""

    PROVIDE_YTDL_LINK = """❗**Provide a valid YouTube-DL supported link.**"""
