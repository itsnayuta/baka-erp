# HƯỚNG DẪN CÀI ĐẶT, TRIỂN KHAI & VẬN HÀNH (ERP DEPLOYMENT)
**Dự án:** Hệ thống ERP Phân phối Thực phẩm Bảo vệ Sức khỏe (BAKAERP)  
**Nền tảng:** Docker Compose, Frappe Framework v15, ERPNext v15, MariaDB 10.6  

---

## 1. Môi trường Yêu cầu & Cấu hình Docker

### 1.1. Yêu cầu Hệ thống
- **Hệ điều hành:** Linux (Ubuntu 22.04 LTS khuyến nghị cho máy chủ sản xuất) hoặc Windows 10/11 có WSL 2 (môi trường phát triển).
- **Phần mềm:** Docker Engine $\ge 24.0$, Docker Compose V2 $\ge 2.20$.
- **Tài nguyên tối thiểu:** 4 Core CPU, 8GB RAM, 40GB SSD khả dụng.

### 1.2. Các Dịch vụ Trong `docker-compose.yml`
- `backend`: Frappe Gunicorn app server.
- `frontend`: Nginx reverse-proxy & file server phục vụ cổng `8080`.
- `db`: MariaDB 10.6 lưu trữ dữ liệu tại volume `db-data`.
- `redis-cache`, `redis-queue`: Bộ nhớ đệm và hàng đợi.
- `scheduler`: Tiến trình cron định kỳ của Frappe.
- `queue-default`, `queue-short`, `queue-long`: Worker xử lý tiến trình ngầm.
- `websocket`: NodeJS hỗ trợ giao tiếp Socket.IO realtime.

---

## 2. Hướng dẫn Khởi chạy Môi trường Local

### 2.1. Khởi động hệ thống
Từ thư mục gốc dự án:
```powershell
# Khởi động toàn bộ container ở chế độ nền
docker compose up -d

# Kiểm tra trạng thái các container
docker compose ps
```

Khi toàn bộ các container ở trạng thái `Up` (và `db` ở trạng thái `healthy`), truy cập giao diện hệ thống tại:
- **Địa chỉ:** `http://localhost:8080`
- **Tài khoản mặc định:**
  - Chủ tịch HĐQT: `chutich@baka.vn` (Mật khẩu: `123`)
  - Giám đốc Vận hành: `coo@baka.vn` (Mật khẩu: `123`)
  - Quản lý Kho: `kho@baka.vn` (Mật khẩu: `123`)
  - Nhân viên Kinh doanh 1: `sale1@baka.vn` (Mật khẩu: `123`)
  - Nhân viên Kinh doanh 2: `sale2@baka.vn` (Mật khẩu: `123`)
  - Quản trị viên hệ thống: `Administrator` (Mật khẩu: `admin` hoặc `123`)

### 2.2. Khởi tạo & Cập nhật Dữ liệu Mẫu Toàn Diện
Để chạy kịch bản khởi tạo hệ thống hoàn chỉnh (3 nhãn hàng, cây kho, lô hàng FEFO, bán hàng đa kênh, báo cáo P&L):
```bash
docker compose exec backend bench --site frontend execute erpnext.setup.health_food_erp_setup.run
```

---

## 3. Quy trình Sao lưu & Khôi phục Dữ liệu (Backup & Restore)

### 3.1. Quy trình Sao lưu (Backup)
Frappe hỗ trợ công cụ backup an toàn bao gồm cả cơ sở dữ liệu và file đính kèm:
```bash
# Thực hiện backup site frontend
docker compose exec backend bench --site frontend backup --with-files
```
File backup sẽ được lưu trữ tự động trong volume `sites/frontend/private/backups/`.

### 3.2. Quy trình Khôi phục (Restore)
Khi cần khôi phục lại dữ liệu từ file backup `.sql.gz`:
```bash
docker compose exec backend bench --site frontend restore /path/to/backup-database.sql.gz \
  --mariadb-root-password admin \
  --with-private-files /path/to/backup-private-files.tar \
  --with-public-files /path/to/backup-files.tar
```

---

## 4. Hướng dẫn Triển khai Máy chủ Trực tuyến (Production Deployment)

### 4.1. Cấu hình Tên miền & SSL (HTTPS)
Trên máy chủ Production (ví dụ: `erp.baka.vn`):
1. Trỏ DNS A Record của tên miền về địa chỉ IP Public của máy chủ.
2. Thiết lập Nginx host hoặc Traefik / Caddy để cấp phát chứng chỉ SSL Let's Encrypt tự động và forward traffic về cổng `8080`.
3. Cấu hình biến môi trường an toàn trong file `.env`:
   - `MYSQL_ROOT_PASSWORD`: Mật khẩu root mạnh.
   - `ADMIN_PASSWORD`: Mật khẩu Administrator mới.
   - `FRAPPE_SITE_NAME_HEADER`: Tên domain chính thức (ví dụ: `erp.baka.vn`).

### 4.2. Khởi động lại khi cập nhật mã nguồn
Mỗi khi có cập nhật code mới từ Git:
```bash
git pull origin main
docker compose exec backend bench --site frontend migrate
docker compose restart backend frontend websocket
```

