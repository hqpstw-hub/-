import subprocess
import requests
import os

# --- 設定 ---
RAW_LIST_URL = 'https://raw.githubusercontent.com/hqpstw-hub/-/main/twTVlist.txt'
DEST_FILE = 'cloud_tv.m3u'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_youtube_url(name, link):
    print(f"正在解析 YouTube: {name}")
    try:
        # 加上 --no-check-certificates 增加成功率
        cmd = ["yt-dlp", "-g", "-f", "best", "--no-check-certificates", link]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=60)
        return result.decode('utf-8').strip()
    except Exception as e:
        print(f"⚠️ {name} 解析失敗，保留原樣")
        return link

# 1. 抓取清單
resp = requests.get(RAW_LIST_URL)
lines = resp.text.splitlines()

# 2. 開始生成 M3U
with open(DEST_FILE, 'w', encoding='utf-8') as f:
    f.write("#EXTM3U\n")
    current_grp = "未分類"
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#EXT"): continue
        
        # 分組處理
        if line.startswith("#") and "," not in line:
            current_grp = line.replace("#", "")
            continue
        
        # 頻道處理
        if "," in line:
            name, link = line.split(',', 1)
            
            # 判斷平台
            if "youtube.com" in link.lower() or "youtu.be" in link.lower():
                real_link = get_youtube_url(name, link)
            elif "4gtv.tv" in link.lower():
                # --- 重點：4GTV 直接改用注入格式，不給 GitHub 伺服器碰網頁的機會 ---
                real_link = f"{link}|User-Agent={UA}&Referer=https://www.4gtv.tv/"
            else:
                real_link = link
                
            f.write(f'#EXTINF:-1 group-title="{current_grp}",{name}\n')
            f.write(f'{real_link}\n')

print("✨ 任務完成，避開了 4GTV 偵測！")
