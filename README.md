# Plant Companion ❄️ aespa Winter Cyber-Frost Edition

[English Version](#english-version) | [繁體中文版本](#繁體中文版本)

---

<a name="繁體中文版本"></a>
## 繁體中文版本

**Plant Companion ❄️（KWANGYA 曠野綠植夥伴）** 是一款融合 **aespa Winter 賽博冰霜美學** 與頂尖 Google 生成式 AI 技術的室內綠植智慧管家。

具備全套 **12 大智慧綠植照護功能**，包含：AI 葉片病害急救診斷、換盆與介質配比精算、季節休眠施肥排程、居家窗台採光方位評估、植物圖鑑水彩拍立得插畫生成、極寒低溫防凍警報、即時天氣防護、本地花市定位、Web Speech 語音對話、虛擬花園儀表板、綠手指成就勳章牆，以及超可愛的 Talking Plant 植物自述模式！

本專案採用 **Google ADK (Agent Development Kit)** 與 **Vertex AI Reasoning Engine (Agent Runtime)** 開發後端大腦，前端以 **Cloud Run** 託管 FastAPI A2A 代理伺服器與響應式 Cyber-Frost Web UI，全面支援 A2A JSON-RPC 協議與 **A2UI** 晶瑩動態卡片渲染。

---

### 🌐 線上展示與即時體驗

- **正式服務體驗網址**：[https://plant-companion-frontend-1038784917896.us-central1.run.app](https://plant-companion-frontend-1038784917896.us-central1.run.app)
- **GitHub 儲存庫**：[https://github.com/KeredStudio/buildwithgemini-my-agent](https://github.com/KeredStudio/buildwithgemini-my-agent)

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

### 🌟 12 大功能完整特色總覽

| 階段 | 編號 | 功能特色 | 說明 |
| :--- | :--- | :--- | :--- |
| **Phase 1** | 1 | 🎧 **冬日 Lyria Lo-Fi 播放器** | 頂部專屬 BGM 按鈕，隨時串流 Vertex AI Lyria 原創輕音樂與動態音波。 |
| | 2 | 🎙️ **Web Speech API 語音輸入** | 專屬麥克風按鈕，免動手用語音進行照護提問與澆水打卡。 |
| | 3 | 🌱 **我的花園儀表板 (Virtual Garden)** | 抽屜選單即時呈現植物水分倒數與「今日已澆水」快捷按鈕。 |
| | 4 | 🎖️ **綠手指成就勳章牆** | 內建抗寒守護者、清泉水行俠、植物神醫等 6 大解鎖徽章。 |
| **Phase 2** | 5 | 🩺 **AI 拍照與病害急救診斷** | 快速診斷葉黃、焦邊、蟲害，並以 A2UI 晶瑩卡片即時提供急救方案。 |
| | 6 | 🪴 **換盆與介質配比計算機** | 輸入盆徑與植物品種，自動精算顆粒石、樹皮與泥炭土黃金比例。 |
| | 7 | 💊 **季節性休眠施肥日程** | 結合 Firestore 記錄施肥，依當前月份智慧提示冬季休眠期減肥建議。 |
| | 8 | ☀️ **居家方位採光評估指南** | 根據東/西/南/北窗戶方向評估日照時數並推薦適配植栽。 |
| **Phase 3** | 9 | 🖼️ **拍立得藝術明信片** | 喚醒 Gemini 繪圖時自動包裝為限量版拍立得卡片，附一鍵高清下載。 |
| | 10 | 💬 **Talking Plant 擬人自述模式** | 點擊切換為植物第一人稱（例如琴葉榕），幽默生動地向主人撒嬌互動。 |
| | 11 | 🏪 **周邊花市與園藝資材推薦** | 整合 Google Maps Geocoding & Places API 定位最近花店與資材行。 |
| **Phase 4** | 12 | ❄️ **極寒低溫防凍警報橫幅** | 全域頂部低溫 Warning Banner，提醒熱帶觀葉植物移離冷風吹襲的窗邊。 |

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
│   ├── static/
│   │   ├── index.html         # 響應式聊天前端（含 12 大功能、A2UI 渲染器、Cyber-Frost 主題）
│   │   └── winter_lofi.mp3    # Vertex AI Lyria 原創 Lo-Fi 背景音軌
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
agents-cli deploy --no-confirm-project
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

**Plant Companion ❄️ (aespa Winter Cyber-Frost Edition)** is an intelligent conversational agent engineered for urban plant lovers, combining **aespa Winter's Cyber-Frost aesthetics** with Google's advanced Generative AI and botanical intelligence.

Featuring a full suite of **12 smart botanical capabilities**: AI pest & disease emergency diagnosis, repotting & custom soil mix calculator, seasonal dormancy fertilizing schedule, room window sunlight orientation assessment, Gemini vintage watercolor Polaroid art generation, severe frost weather alerts, real-time climate advice, Google Maps nursery locator, Web Speech API voice input, Virtual Garden dashboard, Green Thumb achievement badge showcase, and a charming Talking Plant first-person persona!

Built with **Google ADK (Agent Development Kit)** and **Vertex AI Reasoning Engine (Agent Runtime)**, the frontend is hosted on **Cloud Run** serving a FastAPI A2A proxy and a mobile-responsive Cyber-Frost Web UI, fully supporting the A2A JSON-RPC protocol and **A2UI** interactive crystal card rendering.

---

### 🌐 Live Service & Links

- **Live Service URL**: [https://plant-companion-frontend-1038784917896.us-central1.run.app](https://plant-companion-frontend-1038784917896.us-central1.run.app)
- **GitHub Repository**: [https://github.com/KeredStudio/buildwithgemini-my-agent](https://github.com/KeredStudio/buildwithgemini-my-agent)

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

### 🌟 12 Key Features Breakdown

| Phase | # | Feature | Description |
| :--- | :--- | :--- | :--- |
| **Phase 1** | 1 | 🎧 **Winter Lyria Lo-Fi Player** | Dedicated header BGM toggle streaming original Lo-Fi music by Vertex AI Lyria with animated wave bars. |
| | 2 | 🎙️ **Web Speech API Voice Input** | Hands-free voice recognition button to ask plant questions or check in watering. |
| | 3 | 🌱 **Virtual Garden Dashboard** | Drawer panel displaying moisture countdowns and 1-click "Watered Today" logging. |
| | 4 | 🎖️ **Green Thumb Achievement Badges** | Badge wall celebrating Frost Guardian, Aquamancer, Plant Healer, and MY Master milestones. |
| **Phase 2** | 5 | 🩺 **AI Plant Health Diagnosis** | Analyzes yellowing, brown tips, and spider mites, returning treatment actions in crystal A2UI cards. |
| | 6 | 🪴 **Repotting & Soil Mix Calculator** | Calculates ideal upsized pot diameter and tailored soil recipes (peat, perlite, bark ratios). |
| | 7 | 💊 **Seasonal Dormancy Fertilizer Log** | Logs fertilizer application to Firestore with winter dormancy frequency adjustments. |
| | 8 | ☀️ **Window Sunlight Orientation Guide** | Assesses daily sunlight hours based on window orientation (N/S/E/W) and suggests matching plants. |
| **Phase 3** | 9 | 🖼️ **Polaroid Botanical Postcards** | Packages Gemini-generated illustrations into downloadable retro Polaroid cards. |
| | 10 | 💬 **Talking Plant Persona Mode** | Switches conversation to a playful, humorous first-person plant speaking directly to its owner. |
| | 11 | 🏪 **Nursery & Florist Finder** | Integrates Google Maps Geocoding & Places API (New) to locate nearby plant shops. |
| **Phase 4** | 12 | ❄️ **Frost Cold Warning Alert Banner** | Top banner warning users to move tropical foliage away from cold window drafts during winter chills. |

---

### 🏗️ Project Architecture

```
my-agent/
├── app/                       # Core agent implementation
│   ├── agent.py               # ReAct agent, 14 registered tools, callbacks, and A2UI schema
│   ├── a2ui_utils.py          # A2UI callback and message wrapper
│   └── firestore_service.py   # Firestore database CRUD and watering/fertilizer helpers
├── frontend/                  # Web Chat UI & A2A Proxy
│   ├── main.py                # FastAPI proxy communicating over A2A JSON-RPC
│   ├── static/
│   │   ├── index.html         # Responsive UI with 12 features, A2UI renderer & Cyber-Frost theme
│   │   └── winter_lofi.mp3    # Original Lyria Lo-Fi track served locally
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
agents-cli deploy --no-confirm-project
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
