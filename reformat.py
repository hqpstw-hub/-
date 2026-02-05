import requests

# --- 設定 ---
RAW_LIST_URL = 'https://raw.githubusercontent.com/hqpstw-hub/-/main/twTVlist.txt'
DEST_FILE = 'cloud_tv.m3u'

# 1. 抓取清單
resp = requests.get(RAW_LIST_URL)
lines = resp.text.splitlines()

# 2. 生成 M3U (純格式轉換)
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
            # 格式工廠：不做解析，直接排版輸出
            f.write(f'#EXTINF:-1 group-title="{current_grp}",{name}\n')
            f.write(f'{link}\n')

print("✅ 格式工廠任務完成，純 M3U 已產出！")
