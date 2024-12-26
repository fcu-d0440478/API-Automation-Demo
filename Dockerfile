# 基於 Python 3.10 Slim 版本的基礎映像
FROM python:3.10-slim

# 設置工作目錄
WORKDIR /app

# 預先複製 requirements.txt，這樣當它沒有變更時，Docker 可以重用這一層
COPY requirements.txt .

# 只在 requirements.txt 變更時重新安裝依賴
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 複製其餘項目文件
COPY . .

# 運行應用程式
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
