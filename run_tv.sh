cat << 'EOF' > ~/run_tv.sh
#!/data/data/com.termux/files/usr/bin/bash
# 確保環境路徑，讓腳本找得到系統工具
export PATH=$PATH:/data/data/com.termux/files/usr/bin

# 指向你的雲端指令網址 (Raw 連結)
CMD_URL="https://raw.githubusercontent.com/hqpstw-hub/-/refs/heads/main/cmd.txt"

echo "📡 正在從雲端同步指令並洗滌格式..."

# 核心技術：使用 tr -d '\r' 徹底濾掉 Windows 換行符號
# 確保從 GitHub 抓下來的指令在 Linux 環境下不會因字元錯誤而當機
curl -s -L "$CMD_URL" | tr -d '\r' | bash

echo "🚀 本地執行序列結束。"
rm -rf ~/.cache/yt-dlp/*
EOF

# 賦予執行權限
chmod +x ~/run_tv.sh

