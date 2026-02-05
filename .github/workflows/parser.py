import subprocess
import os

# 這裡填入你的原始清單網址
RAW_LIST_URL = "https://raw.githubusercontent.com/你的帳號/你的倉庫/main/twTVlist.txt"

def get_real_url(link):
    try:
        # 在 GitHub 環境下，yt-dlp 通常能解出 4GTV 或是 YouTube
        result = subprocess.check_output(
            ["yt-dlp", "-g", "--user-agent", "Mozilla/5.0", link], 
            stderr=subprocess.STDOUT, timeout=30
        )
        return result.decode('utf-8').strip()
    except:
        return link # 失敗就回傳原始網址

# 讀取清單並產生 M3U (邏輯同你之前的 cmd.txt，但改成 Python 版更穩)
# ... (此處省略部分寫檔代碼，我會在你確認後提供完整版)
