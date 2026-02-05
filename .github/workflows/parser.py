import subprocess
import requests
import re

# --- 設定 ---
RAW_LIST_URL = 'https://raw.githubusercontent.com/hqpstw-hub/-/main/twTVlist.txt' # 確保路徑正確
DEST_FILE = 'cloud_tv.m3u'
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_real_url(name, link):
    print(f"正在處理: {name}")
    try:
        # 針對 YouTube 或 4GTV 使用 yt-dlp 硬攻
        cmd = ["yt-dlp", "-g", "--user-agent", UA, link]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=45)
        return result.decode('utf-8').strip()
    except Exception as e:
        print(f"⚠️ {name} 解析失敗: {e}")
        # 如果是 4GTV 且解析失敗，回退到標頭注入模式
        if "4gtv" in link.lower():
            return f"{link}|User-Agent={UA}&Referer=https://www.4gtv.tv/"
        return link

# 1. 下載原始清單
resp = requests.get(RAW_LIST_URL)
lines = resp.text.splitlines()

# 2. 開始產出 M3U
with open(DEST_FILE, 'w', encoding='utf-8') as f:
    f.write("#EXTM3U\n")
    current_grp = "未分類"
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # 處理分組
        if line.startswith("#") and "," not in line:
            current_grp = line.replace("#", "")
            continue
        
        # 處理頻道
        if "," in line:
            parts = line.split(',', 1)
            name = parts[0]
            link = parts[1]
            
            # 只有 YouTube 和 4GTV 需要解析，其餘直連
            if "youtube.com" in link.lower() or "4gtv" in link.lower():
                real_link = get_real_url(name, link)
            else:
                real_link = link
                
            f.write(f'#EXTINF:-1 group-title="{current_grp}",{name}\n')
            f.write(f'{real_link}\n')

print("✨ 雲端清單製作完成！")
