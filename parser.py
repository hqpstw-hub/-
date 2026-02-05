import subprocess
import requests
import re

# --- 設定 ---
RAW_LIST_URL = 'https://raw.githubusercontent.com/hqpstw-hub/-/main/twTVlist.txt'
DEST_FILE = 'cloud_tv.m3u'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_youtube_url(name, link):
    print(f"解析 YouTube: {name}")
    try:
        # 只對 YouTube 進行解析，因為 YouTube 對 GitHub 的包容度較高
        cmd = ["yt-dlp", "-g", "-f", "best", link]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=45)
        return result.decode('utf-8').strip()
    except Exception as e:
        print(f"⚠️ {name} YouTube 解析失敗: {e}")
        return link

# 1. 獲取原始清單
resp = requests.get(RAW_LIST_URL)
lines = resp.text.splitlines()

with open(DEST_FILE, 'w', encoding='utf-8') as f:
    f.write("#EXTM3U\n")
    current_grp = "未分類"
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#EXT"): continue
        
        if line.startswith("#") and "," not in line:
            current_grp = line.replace("#", "")
            continue
        
        if "," in line:
            name, link = line.split(',', 1)
            
            # --- 核心修正邏輯 ---
            if "youtube.com" in link.lower() or "youtu.be" in link.lower():
                # YouTube 繼續讓 GitHub 幫忙解析
                real_link = get_youtube_url(name, link)
            elif "4gtv.tv" in link.lower():
                # 4GTV 不解析，直接生成帶標頭的格式，避開 429 封鎖
                # 這是 TiviMate 認得的注入格式
                real_link = f"{link}|User-Agent={UA}&Referer=https://www.4gtv.tv/"
            else:
                real_link = link
                
            f.write(f'#EXTINF:-1 group-title="{current_grp}",{name}\n')
            f.write(f'{real_link}\n')
