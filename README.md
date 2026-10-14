# BAKAERP - Hệ Thống Quản Trị Doanh Nghiệp (ERP) Ngành Thức Uống Dinh Dưỡng

<div align="center">
  <h2>BAKAERP v15</h2>
  <p><b>Hệ thống ERP tối ưu hóa cho doanh nghiệp Việt Nam, ngành hàng đồ uống dinh dưỡng & tinh bột kháng</b></p>
  <p>Chuẩn hóa Kế toán TT 200/133 • Chấm công WiFi • Điểm chuyên cần 8đ/ngày • Quản lý Đơn hàng & Kho vận khép kín</p>
</div>

---

## 1. Giới thiệu tổng quan & Mô hình tinh gọn

**BAKAERP** là giải pháp ERP tối giản hóa chuyên sâu trên nền tảng **ERPNext / Frappe v15 (Docker Container)**, thiết kế chính xác theo mô hình kinh doanh tinh gọn của doanh nghiệp:
- **Ngành hàng:** Chuyên doanh thức uống dinh dưỡng đóng hộp (không bán dịch vụ, không sản xuất hay mua bán nguyên vật liệu thô):
  - **Tinh bột kháng PLUS** (365.000 đ)
  - **Tinh bột kháng CACAO** (265.000 đ)
  - **Tinh bột kháng TIBOKA** (250.000 đ)
- **Kênh phân phối:** Chỉ phục vụ 2 nhóm đối tượng khách hàng:
  - **Đại lý (B2B):** Các đại lý phân phối, nhà thuốc, chuỗi thực phẩm sạch.
  - **Khách hàng cuối (B2C):** Khách hàng lẻ mua sản phẩm tiêu dùng trực tiếp.
- **Quản lý nhân sự & Tiếp thị:** Tập trung vào đội ngũ Sale tiếp thị và Quản lý vận hành (Chấm công WiFi văn phòng, Điểm chuyên cần 8đ/ngày, Thi đua doanh số đơn hàng).
- **Tối giản hóa triệt để (Ultra-minimal):**
  - **Workspaces:** Ẩn toàn bộ 22 phân hệ không dùng (Sản xuất, Mua hàng nguyên liệu, Dự án, Y tế, Dịch vụ,...), hệ thống chỉ giữ đúng **6 Không gian làm việc cốt lõi** (`Trang chủ`, `Bán hàng`, `Kho vận`, `Khách hàng & Tiếp thị`, `Kế toán`, `Nhân sự`).
  - **Danh mục Nhóm sản phẩm:** Duy nhất **Thức uống dinh dưỡng** (loại bỏ Raw Material, Services, Consumable).
  - **Danh mục Nhóm khách hàng:** Chuẩn hóa chỉ gồm **Đại lý** và **Khách hàng cuối** (loại bỏ Commercial, Individual, Government,...).
  - **Giao diện làm việc:** Dọn sạch các thẻ và liên kết thừa (loại bỏ bảo trì thiết bị, yêu cầu mua nguyên liệu, hợp đồng gia công).
  - **Tiền tệ chuẩn:** Chỉ kích hoạt **VND** (cơ sở) và **USD** (tỷ giá quy đổi 25.400 VND/USD).
  - **Kế toán chuẩn:** Hệ thống tài khoản theo **Thông tư 200/133** (1111, 1121, 1311, 1561, 3311, 5111,...).

---

## 2. Cơ cấu tổ chức & Danh sách tài khoản thử nghiệm

Tất cả tài khoản trong hệ thống sử dụng **mật khẩu chung:** `123`

| Email đăng nhập | Họ và tên | Chức danh | Quyền hạn & Phân hệ phụ trách |
| :--- | :--- | :--- | :--- |
| **`chutich@baka.vn`** | Bùi Chủ Tịch | Chủ tịch HĐQT | Toàn quyền Quản trị & Giám sát cấp cao (`System Manager`) |
| **`coo@baka.vn`** | Trần Vận Hành | Giám đốc Vận hành | Điều hành toàn diện hệ thống, duyệt đơn hàng, phê duyệt chính sách (`System Manager`) |
| **`sale1@baka.vn`** | Nguyễn Văn Nam | Chuyên viên Kinh doanh 1 | Phụ trách thị trường Miền Bắc & Đại lý (`Sales User`, `Stock User`, `Desk User`) |
| **`sale2@baka.vn`** | Trần Thị Mai | Chuyên viên Kinh doanh 2 | Phụ trách thị trường Miền Nam & Chuỗi bán lẻ (`Sales User`, `Stock User`, `Desk User`) |
| **`kho@baka.vn`** | Phạm Quản Kho | Quản lý Kho | Quản lý kho `Finished Goods - B`, Nhập/Xuất kho (`Stock Manager`, `Stock User`, `Desk User`) |

---

## 3. Danh mục sản phẩm & Bảng giá niêm yết

Tất cả sản phẩm là hàng hóa tồn kho quản lý theo đơn vị tính **Hộp**, thuộc nhóm mặt hàng **Thức uống dinh dưỡng**:

| Mã sản phẩm | Tên sản phẩm | Đơn vị tính | Giá bán niêm yết (VND) | Giá vốn định mức (VND) |
| :--- | :--- | :---: | :---: | :---: |
| **`TBK-PLUS`** | Tinh bột kháng PLUS | Hộp | **365.000** | 200.000 |
| **`TBK-CACAO`** | Tinh bột kháng CACAO | Hộp | **265.000** | 150.000 |
| **`TBK-TIBOKA`** | Tinh bột kháng TIBOKA | Hộp | **250.000** | 140.000 |

- **Bảng giá chuẩn:** `Standard Selling` (bán ra) và `Standard Buying` (mua vào) đều sử dụng đơn vị tiền tệ **VND**.
- **Tỷ giá quy đổi:** Tích hợp bảng tỷ giá tự động giữa `USD` và `VND` (1 USD = 25.400 VND).

---

## 4. Các tính năng & Phân hệ cốt lõi

### 4.1. Chấm công WiFi Văn phòng & Điểm Chuyên cần
Module chấm công thế hệ mới được tích hợp trực tiếp vào màn hình **My Profile** của nhân viên:
- **Xác thực kết nối WiFi:** Bắt buộc kết nối đúng WiFi công ty (`BAKA-OFFICE-5G`) để ghi nhận thời gian vào/ra; tự động phát hiện IP và cảnh báo nếu sử dụng mạng ngoài.
- **Điểm chuyên cần (Attendance Points):**
  - Công thức tính: **1 giờ làm việc thực tế = 1 điểm chuyên cần** (tối đa **8.0 điểm/ngày**).
  - Biểu đồ nhiệt (Heatmap) trong hồ sơ cá nhân tự động tính theo Điểm chuyên cần: làm đủ ca chuẩn 8 tiếng sẽ hiển thị **ô xanh đậm tối đa**.
  - Di chuột vào ô xanh trên biểu đồ hiển thị chính xác nhãn: `X Điểm chuyên cần`.
- **Điểm đánh giá (Assessment Points):** Ghi nhận điểm thưởng, hiệu suất và đóng góp công việc của từng nhân sự trong tháng.

### 4.2. Quản lý Bán hàng & Phân phối (Selling & Distribution)
- Quản lý danh bạ phân nhóm rõ ràng: **Đại lý** (B2B: cửa hàng thực dưỡng, nhà thuốc, chuỗi thực phẩm) và **Khách hàng cuối** (B2C: khách lẻ tiêu dùng).
- Tạo và phê duyệt Đơn đặt hàng bán (`Sales Order`), tự động áp dụng Bảng giá niêm yết VND.
- Liên kết khép kín: Đơn bán hàng $\rightarrow$ Quản lý kho duyệt Phiếu xuất kho $\rightarrow$ Kế toán xuất Hóa đơn & Thu tiền.

### 4.3. Quản lý Kho vận & Tồn kho (Stock & Warehouse)
- Quản lý kho hàng thành phẩm trung tâm: `Finished Goods - B`.
- Nhập kho ban đầu (`Material Receipt`), Xuất kho giao hàng (`Delivery Note`).
- Kiểm soát tồn kho tức thời (Real-time Stock Balance), chặn xuất âm kho, đảm bảo số liệu thực tế khớp 100% với kế toán hàng tồn kho (Tài khoản 1561).

### 4.4. Kế toán Tài chính theo Thông tư 200/133
- Xuất Hóa đơn bán hàng (`Sales Invoice`) tự động hạch toán Nợ TK 1311 / Có TK 5111.
- Thu tiền bán hàng qua Chuyển khoản ngân hàng (`Payment Entry`) hạch toán Nợ TK 1121 / Có TK 1311.
- Theo dõi công nợ chi tiết theo từng đối tác khách hàng và hóa đơn phát sinh.

---

## 5. Dữ liệu kinh doanh mô phỏng (Tháng 10/2026)

Hệ thống đã nạp sẵn kịch bản kinh doanh thống nhất trong tháng 10/2026 để kiểm thử trực quan luồng vận hành:

1. **Nhập kho ban đầu (01/10/2026):**
   - 500 hộp `TBK-PLUS` + 500 hộp `TBK-CACAO` + 600 hộp `TBK-TIBOKA` (Tổng giá trị kho ban đầu: 259.000.000 VND).
2. **7 Đơn đặt hàng bán luân phiên giữa 2 chuyên viên kinh doanh:**
   - **Đơn 1 đến 5 (02/10 – 12/10):** Đã hoàn tất 100% chu trình (Sales Order $\rightarrow$ Quản lý kho duyệt xuất kho Delivery Note $\rightarrow$ Sales Invoice $\rightarrow$ Thu tiền ngân hàng qua Payment Entry).
   - **Đơn 6 (13/10 - Healthy Mart):** 80 PLUS + 60 CACAO (45.100.000 VND) — Trạng thái **Chờ xuất kho** (để Quản lý kho đăng nhập thực hiện xuất kho).
   - **Đơn 7 (14/10 - Đại lý Dinh Dưỡng Xanh):** 50 TIBOKA (12.500.000 VND) — Trạng thái **Mới tạo trong ngày**.
3. **Số lượng tồn kho thực tế hiện tại:**
   - `TBK-PLUS`: **340 Hộp**
   - `TBK-CACAO`: **385 Hộp**
   - `TBK-TIBOKA`: **480 Hộp**
4. **Chấm công thực tế tháng 10:**
   - Đã chấm công đủ ca từ 01/10 đến 13/10 (~8.3h/ngày $\rightarrow$ Đạt mức tối đa **8.0 Điểm chuyên cần/ngày**, hiển thị đầy đủ ô xanh đậm).
   - **Hôm nay (14/10):** Đã check-in lúc ~08:20, **chưa check-out** để người dùng trực tiếp bấm nút "Chấm công RA" trải nghiệm.

---

## 6. Hướng dẫn vận hành & Lệnh kỹ thuật

### Khởi động hệ thống
```bash
docker compose up -d
```
Hệ thống sẽ chạy trên cổng `http://localhost:8080`.

### Cấu hình chuẩn hóa Việt Nam (Chạy khi cần cập nhật cài đặt hệ thống)
```bash
docker compose exec backend bench --site frontend execute erpnext.setup.vietnam_setup.run
```

### Nạp lại toàn bộ dữ liệu mô phỏng tháng 10
```bash
docker compose exec backend bench --site frontend execute erpnext.setup.sample_data.run
```

### Xóa bộ nhớ đệm (Clear cache)
```bash
docker compose exec backend bench --site frontend clear-cache
```

### Biên dịch lại giao diện và tài nguyên tĩnh (Build assets)
```bash
docker compose exec backend bench build --app erpnext
```
