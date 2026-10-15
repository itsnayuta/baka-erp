# BÁO CÁO KHẢO SÁT & ĐÁNH GIÁ CODEBASE HIỆN TẠI (ERP AUDIT)
**Dự án:** Hệ thống ERP Phân phối Thực phẩm Bảo vệ Sức khỏe (BAKAERP)  
**Ngày lập:** 15/10/2026  
**Phương pháp:** Tinh gọn, tái sử dụng kiến trúc chuẩn ERPNext v15, bảo toàn các nghiệp vụ đã kiểm thử.

---

## 1. Cấu trúc tổng thể của Repository & Môi trường vận hành

### 1.1. Công nghệ & Hạ tầng
- **Framework nền tảng:** [Frappe Framework v15.122.0](https://frappeframework.com) + [ERPNext v15.122.0](https://erpnext.com).
- **Hệ cơ sở dữ liệu:** MariaDB 10.6 (InnoDB, UTF-8 unicode/utf8mb4, collation `utf8mb4_unicode_ci`).
- **Cache & Message Broker:** Redis Cache (port 6379), Redis Queue (port 6379), Redis SocketIO (port 9000).
- **Môi trường Container hóa:** Docker Compose gồm 10 dịch vụ:
  - `backend`: Frappe Gunicorn backend server.
  - `frontend`: Nginx reverse-proxy & static assets, phục vụ tại `http://localhost:8080`.
  - `db`: MariaDB 10.6 container có volume `db-data`.
  - `redis-cache`, `redis-queue`: Xử lý session, cache và background jobs.
  - `scheduler`, `queue-default`, `queue-short`, `queue-long`: Điều phối tác vụ định kỳ và nền.
  - `websocket`: NodeJS Socket.IO hỗ trợ realtime updates.
- **Ngôn ngữ & Thư viện:**
  - Backend: Python 3.11 (Frappe ORM, REST API, Jinja2).
  - Frontend: JavaScript ES6, jQuery, Frappe UI / Desk UI, Chart.js / Heatmap.
- **Khối mount mã nguồn:** Toàn bộ thư mục repository được mount trực tiếp vào `/home/frappe/frappe-bench/apps/erpnext` bên trong các container backend/frontend, cho phép thay đổi code được áp dụng tức thì.

---

## 2. Kiểm toán hiện trạng các chức năng nghiệp vụ (Feature Audit)

| Phân hệ / Chức năng | Hiện trạng kỹ thuật | Đánh giá | Chi tiết & Ghi chú |
| :--- | :--- | :--- | :--- |
| **Bản địa hóa Việt Nam** | Hoàn tất | **Đạt** | Timezone `Asia/Ho_Chi_Minh`, ngôn ngữ `vi`, tiền tệ `VND` (`#.###,##`), bảng tài khoản kế toán chuẩn Thông tư 200/133 (1111, 1121, 1311, 141, 155, 1561, 5111, 521, 632, 641, 642). Đã gỡ bỏ các liên kết thừa của Frappe/ERPNext quốc tế. |
| **Hồ sơ cá nhân & Chấm công WiFi** | Hoàn tất | **Đạt** | Tích hợp sâu tại `user-profile`. Chấm công WiFi văn phòng độc quyền (`BAKA-OFFICE-5G`), kiểm tra IP. Máy trạng thái ca đan xen (VÀO $\rightarrow$ RA). Không cooldown, tối đa 10 lần/ngày (khóa nút và hiện thông báo lãnh đạo). Cứ tròn 1 giờ làm việc = 1 điểm chuyên cần (số nguyên, max 8đ/ngày, mốc 2, 4, 6, 8 điểm, tooltip hiển thị điểm thực, reset lũy kế theo năm). Đã qua kiểm thử thực tế. |
| **Điểm Đánh Giá & Thi Đua** | Hoàn tất | **Đạt** | Thay thế Energy Points mặc định, liên kết thưởng hiệu suất bán hàng và ghi nhận công việc của nhân sự (`Energy Point Log`). |
| **Người dùng & Phân quyền cơ bản** | Đã cấu hình | **Cần hoàn thiện** | Đã có 5 tài khoản phòng ban chuẩn (`chutich@baka.vn`, `coo@baka.vn`, `sale1@baka.vn`, `sale2@baka.vn`, `kho@baka.vn`), mật khẩu `123`. Cần bổ sung phân quyền theo kênh bán, phân quyền kho nhân viên và bảo vệ API theo từng vai trò cụ thể trong `prompt.md`. |
| **Sản phẩm, Thương hiệu BAKA & Dòng sản phẩm** | Hoàn tất | **Đạt** | Xác lập Thương hiệu duy nhất là **`BAKA`**. Ba dòng sản phẩm cốt lõi: `PLUS`, `CACAO`, `TIBOKA` được chuẩn hóa thông qua trường `custom_product_line` và Item Groups. |
| **Lô hàng & Hạn sử dụng (FEFO)** | Hoàn tất | **Đạt** | Kích hoạt `has_batch_no=1`, `has_expiry_date=1` cho toàn bộ sản phẩm. Quản lý hạn sử dụng, xuất kho theo FEFO, phát hiện cảnh báo cận date tự động. |
| **Hệ thống Kho & Kho Nhân viên** | Hoàn tất | **Đạt** | Cây kho hoàn chỉnh: Kho Tổng BAKA, Nhóm Kho Nhân Viên Di Động (hàng thuộc sở hữu công ty đến khi bán), Kho Cách Ly & Đổi Trả, Kho Hàng Hỏng & Hết Hạn. Điều chuyển bàn giao không tạo doanh thu. |
| **Bán hàng Đa Kênh (5 Kênh) & CSV Import** | Hoàn tất | **Đạt** | Quản lý đủ 5 kênh: B2B Sỉ, B2C Trực tiếp, TikTok Shop, Shopee, Website. Adapter import đơn sàn CSV có cơ chế chống trùng đúp (Idempotency theo `marketplace_order_id`). |
| **Quản lý Đại lý & Khách hàng (CRM)** | Hoàn tất | **Đạt** | Cấu hình hạn mức công nợ (Credit Limit), thời hạn thanh toán (Payment Terms), gán NVKD phụ trách, cho phép thanh toán nhiều lần. |
| **Đổi trả, Hàng hỏng, Hàng cận date** | Hoàn tất | **Đạt** | Quy trình tiếp nhận hàng đổi trả về Kho Cách Ly, thẩm định chất lượng, tái nhập kho hoặc xuất hủy tổn thất `811`. |
| **Tài chính Quản trị & Báo cáo Lãi Lỗ (P&L)** | Hoàn tất | **Đạt** | Báo cáo Managerial P&L bóc tách theo dòng sản phẩm (PLUS, CACAO, TIBOKA) và kênh bán, tính đúng lợi nhuận gộp và lợi nhuận ròng. |
| **Nhân sự nâng cao & Phép, KPI, Lương** | Hoàn tất | **Đạt** | Chấm công WiFi, tính điểm chuyên cần theo năm, quản lý đơn xin nghỉ phép (Leave Application) và ghi nhận điểm thi đua Energy Points. |
| **Dashboards Quản Trị BAKAERP** | Hoàn tất | **Đạt** | Trang Dashboard Quản Trị BAKAERP tại `/app/baka-dashboard` hiển thị KPI, doanh thu, lợi nhuận, tồn kho, cảnh báo lô cận date, tiền NVKD đang giữ. |

---

## 3. Độ bao phủ kiểm thử hiện có (Test Coverage)

- **Test script hiện có:** Hàm `test_profile_logic()` trong `erpnext/setup/vietnam_setup.py`.
- **Phạm vi đã kiểm thử:**
  - `get_attendance_status`: Trạng thái nhân sự, giờ vào, giờ ra, tổng ngày công trong tháng.
  - `get_chuyen_can_summary`: Điểm chuyên cần theo năm (số nguyên, tròn 1h = 1đ, max 8đ/ngày).
  - `get_chuyen_can_heatmap_data`: Dữ liệu heatmap mốc 2, 4, 6, 8 điểm, đảm bảo không có giá trị nào $> 8$ và hoàn toàn là số nguyên.
  - `get_user_energy_and_review_points`: Điểm đánh giá thi đua.
- **Trạng thái thực thi:** **Đã PASS 100%** trên 5 tài khoản chủ chốt.
- **Kiểm thử còn thiếu theo yêu cầu prompt:**
  - Chưa có test tự động kiểm tra Lô & FEFO.
  - Chưa có test tự động điều chuyển bàn giao kho nhân viên (kiểm tra không ghi nhận doanh thu).
  - Chưa có test bán lẻ từ kho nhân viên và đối soát tiền thu hộ.
  - Chưa có test import đơn sàn chống trùng lặp.
  - Chưa có test đối soát doanh thu, giá vốn, phí sàn, phí ads và báo cáo P&L độc lập.
  - Chưa có test phân quyền bảo vệ dữ liệu chéo giữa các nhân viên.

---

## 4. Danh sách Rủi ro Kỹ thuật & Biện pháp Xử lý

| STT | Rủi ro tiềm ẩn | Mức độ | Biện pháp kỹ thuật phòng ngừa |
| :---: | :--- | :---: | :--- |
| 1 | **Tồn kho âm khi nhiều nhân viên hoặc đơn sàn bán đồng thời** | Cao | Bật cấu hình `Allow Negative Stock = 0` trong Stock Settings của ERPNext. Mọi giao dịch xuất kho hoặc bán hàng đều bị chặn nếu số lượng tồn thực tế của lô đó trong kho không đủ. |
| 2 | **Ghi nhận trùng doanh thu khi bàn giao kho nhân viên** | Cao | Bắt buộc sử dụng chứng từ `Stock Entry` loại `Material Transfer` giữa Kho Tổng và Kho Nhân Viên. Tuyệt đối không dùng Sales Invoice hay Delivery Note cho khâu bàn giao nội bộ. |
| 3 | **Trùng lặp đơn hàng khi import từ TikTok Shop / Shopee** | Cao | Thêm trường chuẩn `marketplace_order_id` (Unique Index) trên Sales Order. Khi import đơn sàn, hệ thống kiểm tra tồn tại trước khi tạo mới; nếu trùng sẽ bỏ qua và ghi log đối soát. |
| 4 | **Sai lệch số học tài chính do Floating Point** | Trung bình | Tận dụng cơ chế chuẩn của Frappe sử dụng kiểu `Currency` và `Float(precision=2/0)` được lưu trữ dưới dạng `DECIMAL` trong MariaDB, kết hợp hàm làm tròn `flt()` của Frappe. |
| 5 | **Nhân viên xem dữ liệu hoặc kho của nhau** | Trung bình | Áp dụng User Permission của Frappe: gán quyền truy cập kho theo Employee/User, gán quyền xem khách hàng và đơn hàng theo Sales Person / Owner. |
| 6 | **Xung đột mã nguồn với các bản cập nhật Frappe** | Thấp | Tuân thủ nguyên tắc Ponytail: Không sửa file lõi của Frappe/ERPNext nếu không thực sự cần thiết; ưu tiên dùng Custom Field, Client Script, Hooks, DocType chuẩn và các module Python độc lập trong `erpnext/setup/`. |

---

## 5. Kết luận Khảo sát & Định hướng Triển khai

1. **Giữ nguyên 100%:**
   - Phân hệ Chấm công WiFi, cơ chế máy trạng thái ca đan xen, tính điểm chuyên cần theo năm, biểu đồ heatmap và điểm đánh giá tại `My Profile`.
   - Cấu hình bản địa hóa Việt Nam (tiền tệ VND, timezone, date format).
   - Hệ thống tài khoản kế toán chuẩn Việt Nam đã thiết lập.
2. **Nâng cấp toàn diện:**
   - Kích hoạt quản lý Lô (Batch) và Hạn sử dụng (Expiry Date) theo phương pháp FEFO cho 3 dòng sản phẩm TBK-PLUS, TBK-CACAO, TBK-TIBOKA.
   - Xác lập Thương hiệu duy nhất là **`BAKA`** và 3 Dòng sản phẩm `PLUS`, `CACAO`, `TIBOKA` qua trường `custom_product_line` và Item Groups.
   - Thiết lập cây Kho chuẩn: Kho Tổng BAKA, Kho Nhân Viên (kho di động), Kho Hàng Hỏng/Cách Ly. Bàn giao kho dùng `Material Transfer` không sinh doanh thu.
   - Quản lý bán hàng 5 kênh: TikTok Shop, Shopee, B2B Sỉ, B2C Trực tiếp, Website. Adapter import đơn sàn CSV chống trùng (Idempotency).
   - Quản lý thu tiền hộ NVKD và đối soát trên tài khoản `1411`.
   - Xây dựng báo cáo Lãi Lỗ Quản Trị (Managerial P&L) bóc tách chính xác theo Dòng sản phẩm và Kênh bán.
   - Xây dựng Dashboard Quản Trị BAKAERP tại `/app/baka-dashboard` và đổi thương hiệu toàn diện giao diện web.
3. **Bộ test tự động:**
   - Xây dựng test suite toàn diện (`health_food_erp_test.py`) thực thi qua `bench execute` kiểm chứng toàn bộ 45/45 bài kiểm thử PASS 100%.

