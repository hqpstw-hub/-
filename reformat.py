import requests

RAW_LIST_URL = 'https://raw.githubusercontent.com/hqpstw-hub/-/main/twTVlist.txt'
DEST_FILE = 'cloud_tv.m3u'

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
            f.write(f'#EXTINF:-1 group-title="{current_grp}",{name}\n')
            f.write(f'{link}\n')
print("✅ 格式工廠任務完成！")
