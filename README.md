# 熱門新聞爬蟲與 MongoDB 整合系統 
### Taiwan News Crawler with MongoDB Integration

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB%20Atlas-green)](https://www.mongodb.com/cloud/atlas)

這是一個自動化新聞擷取與儲存系統，專責抓取台灣主要媒體（聯合報、中時新聞網）的即時熱門新聞，並將非結構化資料轉化為 JSON 格式後，存入 MongoDB Atlas 雲端資料庫。

## Core Features
- **多來源爬蟲**：整合 Requests 與 BeautifulSoup4，同步擷取 UDN 與 Chinatimes 資料。
- **NoSQL 資料持久化**：串接 MongoDB Atlas，雲端儲存與管理新聞資料。
- **進階資料分析**：用 MongoDB Aggregation Pipeline 即時統計資料庫端報表。
- **安全性設計**：用 `.env` 環境變數管理資料庫密碼等資訊，避免 API 金鑰與資料庫密碼外洩。
- **SSL 安全連線**：用 `certifi` 套件讓不同作業系統都可以建立加密連線。

## CI/CD
整合 **GitHub Actions** 無人值守自動化爬蟲，流程：
- **定時執行**：設定於每天台北時間 08:00 (UTC 00:00) 自動啟動。
- **雲端同步**：執行成功後將自動更新 MongoDB Atlas 雲端資料庫之內容。
- **狀態監控**：可至 [Actions](../../actions) 頁籤查看每日執行狀態與 Log。

## Tech Stack
- **語言**: Python 3.x
- **爬蟲**: Requests, BeautifulSoup4
- **資料庫**: MongoDB Atlas (NoSQL)
- **環境管理**: python-dotenv, certifi

## Project Structure
.
├── .github/workflows/
│   └── main.yml         # GitHub Actions 自動化腳本
├── main.py              # 爬蟲主程式 (含 MongoDB 聚合統計)
├── requirements.txt     # 環境依賴清單
└── .env.example         # 環境變數範本

## Getting Started

### 1. 複製專案
```bash
git clone [https://github.com/ycchenn/News-Crawler-MongoDB.git](https://github.com/ycchenn/News-Crawler-MongoDB.git)
cd News-Crawler-MongoDB
```

### 2. 安裝必要套件
```bash
pip install -r requirements.txt
```

### 3. 設定環境變數
```bash
MONGO_URI=mongodb+srv://<USER>:<PASSWORD>@your-cluster.mongodb.net/
```

### 4. 執行程式
```bash
python main.py
