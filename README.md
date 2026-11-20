# Plant Companion 🌿 聖誕暖心綠植夥伴

[English Version](#english-version) | [繁體中文版本](#繁體中文版本)

---

<a name="繁體中文版本"></a>
## 繁體中文版本

**Plant Companion（綠植夥伴）** 是一款專為室內綠植愛好者打造的智慧型對話顧問。具備植物圖鑑檢索、日照澆水照護指南、冬季防寒天氣警報、澆水歷史追蹤、周邊花市花店搜尋，以及運用 Gemini 繪製復古水彩植物插畫等全方位功能。

本專案採用 **Google ADK (Agent Development Kit)** 開發，後端 Agent 部署於 **Vertex AI Agent Platform (Agent Runtime / Reasoning Engine)**，前端採用 **Cloud Run** 託管的 FastAPI 代理伺服器與響應式網頁聊天介面，全面支援 A2A (Agent-to-Agent) JSON-RPC 協議與 **A2UI** 豐富卡片互動渲染。

---

### 🎬 示範影片（Demo Video）

觀看 **Plant Companion** 實際操作示範（含 Google **Lyria** 生成之 Lo-Fi 輕快背景配樂）：

https://github.com/user-attachments/assets/plant-companion-demo (可下載或直接播放 [plant_companion_demo.webm](./plant_companion_demo.webm))

<video src="./plant_companion_demo.webm" controls="controls" width="100%" style="max-width: 800px; border-radius: 8px;">
  您的瀏覽器不支援直接播放 WebM 影片，請點擊下載 <a href="./plant_companion_demo.webm">plant_companion_demo.webm</a>。
</video>

**Demo 兩大亮點：**
1. **Firestore 資料庫查詢與 A2UI 卡片**：查詢龜背竹（*Monstera Deliciosa*）養護指南，包含光照、澆水頻率與寵物毒性，以結構化卡片漂亮排版。
2. **Gemini 多模態圖片生成**：呼叫 `gemini-3.1-flash-lite-image` 生成復古水彩植物插畫並託管於 Google Cloud Storage。
3. **AI 原創配樂**：由 Vertex AI 上的 Google **`lyria-002`** 音樂生成模型專屬譜曲。

---

### 🌟 核心功能特色

- 📖 **植物百科與照護資料庫**：以 Cloud Firestore 為基礎，儲存室內植物詳細養護屬性（日照強度、水分週期、難易度、貓狗寵物毒性）。
- 💧 **澆水登記與週期追蹤**：打卡記錄澆水事件，系統自動依植物特性推算下次最佳澆水日期。
- 🎨 **植物圖鑑水彩插畫生成**：運用 `gemini-3.1-flash-lite-image` 生成精緻古典水彩插圖，自動上傳至 Cloud Storage 公開展示。
- ❄️ **即時天氣與防寒預警**：整合 Open-Meteo API 即時查詢指定城市氣溫與濕度，提供氣候適應與冬季防凍建議。
- 🏪 **花店與園藝中心搜尋**：串接 Google Maps Geocoding API 與 Places API (New) 定位附近的植栽門市。
- 📱 **全平台行動裝置適配 (Mobile Responsive)**：針對手機 Chrome / Safari 全面優化（支援 100dvh 動態高度、防縮放、防跑版、安全邊距 safe-area-inset）。
- 🎄 **溫馨聖誕主題風格與角色頭像**：暖白、松綠與熱紅酒配色，附帶雙方頭像（Agent 🎄 / 使用者 🧑‍🌾）、時間戳記、歡迎卡片與快捷範例按鈕。
- 📂 **對話歷史紀錄抽屜**：左上角漢堡選單隨時開啟側邊欄回顧最近 30 則對話紀錄。

---

### 🏗️ 專案架構目錄

```
my-agent/
├── app/                       # 後端 Agent 核心邏輯
│   ├── agent.py               # ReAct Agent、工具定義、提示詞與 A2UI Schema
│   ├── a2ui_utils.py          # A2UI 回調包裝器 (after_model_callback)
│   └── firestore_service.py   # Firestore 資料庫 CRUD 輔助函式
├── frontend/                  # 前端 Web Chat UI & A2A 代理伺服器
│   ├── main.py                # FastAPI 伺服器，透過 A2A JSON-RPC 與 Agent Runtime 通訊
│   ├── static/index.html      # 響應式聊天前端（含 A2UI 渲染器、聖誕風格、歷史抽屜）
│   ├── requirements.txt       # 前端 Python 相依套件
│   └── Dockerfile             # 前端 Cloud Run 容器打包檔
├── seed_firestore.py          # Firestore 初始植物資料匯入腳本
├── plant_companion_demo.webm  # 示範展示影片（含 Lyria 背景配樂）
├── deployment_metadata.json   # Agent 部署中繼資料記錄
├── agents-cli-manifest.yaml   # agents-cli 專案配置清單
└── pyproject.toml             # Python 專案套件設定檔
```

---

### 🚀 無腦部署與建置指南（零基礎一鍵上手）

跟著以下步驟，任何人都能在自己的 Google Cloud 帳號中完整部署此專案！

#### 步驟 0：前置準備與環境認證
1. 安裝 Google Cloud SDK (`gcloud`) 與 Python 3.11+。
2. 登入 Google Cloud 帳號並設定目標專案：
   ```bash
   gcloud auth login
   gcloud auth application-default login
   gcloud config set project <YOUR_PROJECT_ID>
   ```
3. 啟用必要之 GCP API：
   ```bash
   gcloud services enable \
     aiplatform.googleapis.com \
     firestore.googleapis.com \
     run.googleapis.com \
     artifactregistry.googleapis.com \
     cloudbuild.googleapis.com \
     places.googleapis.com \
     geocoding-backend.googleapis.com
   ```
4. 建立 Firestore 資料庫（預設模式 Native mode）並建立公開 GCS Bucket 用於存放生成的植物插畫。

#### 步驟 1：建立環境變數設定
在專案根目錄複製範本並填入金鑰：
```bash
cp .env.example .env
```
編輯 `.env`：
```ini
PROJECT_ID=<YOUR_PROJECT_ID>
LOCATION=us-east1
GOOGLE_MAPS_API_KEY=<YOUR_GOOGLE_MAPS_API_KEY>
IMAGE_BUCKET_NAME=<YOUR_GCS_BUCKET_NAME>
```

#### 步驟 2：匯入初始植物資料庫
```bash
uv sync   # 或 pip install -r requirements.txt
python3 seed_firestore.py
```

#### 步驟 3：部署 Agent 後端至 Vertex AI Agent Runtime
```bash
agents-cli deploy
```
> 部署完成後，指令列會輸出類似以下格式的資源識別碼：  
> `projects/<PROJECT_NUMBER>/locations/us-east1/reasoningEngines/<REASONING_ENGINE_ID>`  
> （此資訊會自動記錄在 `deployment_metadata.json` 中）

#### 步驟 4：部署前端 Chat UI 至 Cloud Run
進入 `frontend/` 資料夾，執行一鍵建置部署：
```bash
cd frontend

gcloud run deploy plant-companion-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars AGENT_ENGINE_RESOURCE_NAME="<步驟 3 產生的 REASONING_ENGINE_ID 完整路徑>",AGENT_DIRECTORY="app" \
  --quiet
```
完成後終端會顯示 **Service URL**（例如：`https://plant-companion-frontend-xxxx.us-central1.run.app`），即可直接用瀏覽器開啟使用！

#### 步驟 5：本機開發與測試（可選）
如想在本地電腦執行與偵錯：
```bash
# 終端機 1：啟動本機 Agent
agents-cli run

# 終端機 2：啟動本機前端伺服器 (銜接雲端已部署的 Agent)
cd frontend
export AGENT_ENGINE_RESOURCE_NAME="<步驟 3 產生的完整路徑>"
export AGENT_DIRECTORY="app"
uvicorn main:app --port 8080
```
開啟 `http://127.0.0.1:8080` 即可在本地進行調試。

---

<br><hr><br>

<a name="english-version"></a>
## English Version

**Plant Companion** is an intelligent conversational agent engineered for urban plant enthusiasts to care for their indoor greenery with plant care databases, watering logs, seasonal weather advisories, local nursery search, and vintage watercolor illustrations powered by Gemini.

Built with **Google ADK (Agent Development Kit)**, the backend agent is deployed to **Vertex AI Agent Platform (Agent Runtime / Reasoning Engine)**, and served via a **Cloud Run** web chat frontend supporting the A2A (Agent-to-Agent) JSON-RPC protocol and **A2UI** interactive card display.

---

### 🎬 Demo Video

Watch **Plant Companion** in action below (featuring an upbeat lo-fi soundtrack generated by Google's **Lyria** music model):

https://github.com/user-attachments/assets/plant-companion-demo (Download or play [plant_companion_demo.webm](./plant_companion_demo.webm))

<video src="./plant_companion_demo.webm" controls="controls" width="100%" style="max-width: 800px; border-radius: 8px;">
  Your browser does not support the video tag. Download <a href="./plant_companion_demo.webm">plant_companion_demo.webm</a> to view.
</video>

**Highlights in Demo:**
1. **Firestore Query & A2UI**: Querying care guide for *Monstera Deliciosa* (light, watering schedule, toxicity) presented as rich structured cards.
2. **Multimodal Tool Call & Image Generation**: Generating vintage watercolor botanical art using `gemini-3.1-flash-lite-image` hosted on Google Cloud Storage.
3. **AI Soundtrack**: Custom upbeat lo-fi hip hop composed by Google **`lyria-002`** on Vertex AI.

---

### 🌟 Key Features

- 📖 **Plant Care & Inventory Database**: Backed by Cloud Firestore storing indoor plant attributes (light levels, watering frequency, difficulty, pet toxicity).
- 💧 **Watering Log & Tracker**: Records watering events in Firestore and automatically calculates next recommended watering dates.
- 🎨 **Botanical Watercolor Illustrations**: Generates classic botanical watercolor artwork with `gemini-3.1-flash-lite-image` and hosts them on Cloud Storage.
- ❄️ **Real-time Weather & Cold Protection**: Connects to Open-Meteo API for real-time temperature and humidity, providing frost protection advice.
- 🏪 **Nursery & Florist Finder**: Integrates Google Maps Geocoding & Places API (New) to locate nearby garden centers and flower shops.
- 📱 **Fully Mobile Responsive**: Comprehensive support for Mobile Chrome / Safari (`100dvh` dynamic height, safe-area-inset padding, zoom prevention, and layout overflow safeguards).
- 🎄 **Warm Christmas Theme with Avatars**: Cozy forest green, wine red, and cream palette with dedicated avatars (Agent 🎄 / User 🧑‍🌾), timestamps, welcome card, and quick suggestion chips.
- 📂 **Conversation History Drawer**: Accessible via the top-left hamburger menu to inspect recent chat turns.

---

### 🏗️ Project Architecture

```
my-agent/
├── app/                       # Core agent implementation
│   ├── agent.py               # ReAct agent, tools, callbacks, and A2UI schema
│   ├── a2ui_utils.py          # A2UI callback and message wrapper
│   └── firestore_service.py   # Firestore database CRUD helpers
├── frontend/                  # Web Chat UI & A2A Proxy
│   ├── main.py                # FastAPI proxy communicating over A2A JSON-RPC
│   ├── static/index.html      # Responsive UI with A2UI renderer, Christmas theme & drawer
│   ├── requirements.txt       # Frontend dependencies
│   └── Dockerfile             # Cloud Run container definition
├── seed_firestore.py          # Initial plant database seeder
├── plant_companion_demo.webm  # Screen recording demo with Lyria soundtrack
├── deployment_metadata.json   # Agent deployment metadata
├── agents-cli-manifest.yaml   # agents-cli project manifest
└── pyproject.toml             # Python packaging configuration
```

---

### 🚀 Foolproof Step-by-Step Deployment Guide

Follow these exact steps to deploy the entire stack to your Google Cloud project from scratch:

#### Step 0: Prerequisites & GCP Setup
1. Install Google Cloud SDK (`gcloud`) and Python 3.11+.
2. Authenticate and set your active GCP project:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   gcloud config set project <YOUR_PROJECT_ID>
   ```
3. Enable necessary Google Cloud APIs:
   ```bash
   gcloud services enable \
     aiplatform.googleapis.com \
     firestore.googleapis.com \
     run.googleapis.com \
     artifactregistry.googleapis.com \
     cloudbuild.googleapis.com \
     places.googleapis.com \
     geocoding-backend.googleapis.com
   ```
4. Create a Firestore database (Native mode) and a public Google Cloud Storage bucket for hosting generated plant artwork.

#### Step 1: Configure Environment Variables
Copy the template and supply your credentials:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
PROJECT_ID=<YOUR_PROJECT_ID>
LOCATION=us-east1
GOOGLE_MAPS_API_KEY=<YOUR_GOOGLE_MAPS_API_KEY>
IMAGE_BUCKET_NAME=<YOUR_GCS_BUCKET_NAME>
```

#### Step 2: Seed the Firestore Database
```bash
uv sync   # or pip install -r requirements.txt
python3 seed_firestore.py
```

#### Step 3: Deploy Backend Agent to Vertex AI Agent Runtime
```bash
agents-cli deploy
```
> Upon completion, note the returned resource name:  
> `projects/<PROJECT_NUMBER>/locations/us-east1/reasoningEngines/<REASONING_ENGINE_ID>`  
> (This is also recorded in `deployment_metadata.json`).

#### Step 4: Deploy Frontend Chat UI to Cloud Run
Navigate to `frontend/` and trigger Cloud Run build & deployment:
```bash
cd frontend

gcloud run deploy plant-companion-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars AGENT_ENGINE_RESOURCE_NAME="<REASONING_ENGINE_RESOURCE_NAME_FROM_STEP_3>",AGENT_DIRECTORY="app" \
  --quiet
```
Once finished, Cloud Run outputs your live **Service URL** (e.g., `https://plant-companion-frontend-xxxx.us-central1.run.app`).

#### Step 5: Local Development & Debugging (Optional)
To test and develop locally:
```bash
# Terminal 1: Run local agent engine
agents-cli run

# Terminal 2: Run local web proxy connected to deployed agent
cd frontend
export AGENT_ENGINE_RESOURCE_NAME="<YOUR_REASONING_ENGINE_RESOURCE_NAME>"
export AGENT_DIRECTORY="app"
uvicorn main:app --port 8080
```
Open `http://127.0.0.1:8080` in your browser.

---

### 📜 License
This project is open-source under the MIT License.
