 # Sử dụng base image Python
FROM python:3.10

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép tệp tin requirements.txt vào container
COPY requirements.txt .

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn của bot vào container
COPY . .

# Chạy bot Discord
CMD [ "python", "nightguardian.py" ]
