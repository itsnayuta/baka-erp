# BAKAERP - Tài Liệu Chức Năng Phân Hệ Hồ Sơ Cá Nhân (My Profile)

<div align="center">
  <h2>PHÂN HỆ HỒ SƠ CÁ NHÂN & CHẤM CÔNG WIFI (MY PROFILE)</h2>
  <p><b>Trung tâm quản lý hiệu suất nhân sự, chấm công bảo mật WiFi và theo dõi điểm chuyên cần</b></p>
  <p>BAKAERP v15 • Chấm công WiFi • Điểm chuyên cần 8đ/ngày • Điểm đánh giá thi đua</p>
</div>

---

## 1. Giới thiệu tổng quan

Mục **My Profile** (`/app/user-profile`) là phân hệ trung tâm dành cho từng nhân viên và cấp quản lý trong doanh nghiệp BAKAERP. Phân hệ được thiết kế theo triết lý **tinh gọn, trực quan và bảo mật cao**, tích hợp toàn diện:
1. **Chấm công qua WiFi văn phòng độc quyền** (không dùng nút bấm trôi nổi, chỉ chấm công tại My Profile).
2. **Hệ thống Điểm Chuyên cần (Attendance Points)** đo lường chính xác giờ công thực tế.
3. **Hệ thống Điểm Đánh giá (Assessment / Energy Points)** khen thưởng đóng góp và hiệu suất chốt đơn hàng của nhân viên kinh doanh.
4. **Bảng xếp hạng thi đua nội bộ (Leaderboard & Ranking)**.

---

## 2. Cấu trúc giao diện & Chi tiết các khối chức năng

Giao diện My Profile gồm 2 khu vực chính: **Thanh bên hồ sơ (Sidebar)** và **Khu vực hiển thị chính (Main Section)**.

```
┌─────────────────────────────────┬────────────────────────────────────────────────────────┐
│   THANH BÊN HỒ SƠ (SIDEBAR)     │           KHU VỰC HIỂN THỊ CHÍNH (MAIN SECTION)        │
├─────────────────────────────────┼────────────────────────────────────────────────────────┤
│ • Ảnh đại diện (Avatar)         │ [1] Thẻ Chấm Công WiFi BAKA (WiFi Attendance Card)     │
│ • Họ và tên đầy đủ              │     - Trạng thái ca: Chưa chấm / Đang làm / Hoàn thành │
│ • Chức vụ & Phòng ban           │     - Giờ Vào / Giờ Ra / Tổng thời gian đã làm việc    │
│ • Bio (Mô tả trách nhiệm)       │     - Nút Chấm công VÀO / RA / Xem lịch sử chấm công   │
│                                 │                                                        │
│ • Chỉ số thành tích & Thi đua:  │ [2] Biểu Đồ Tổng Quan Chuyên Cần (Heatmap)             │
│   - Điểm đánh giá (X điểm)      │     - 1 giờ làm việc = 1 điểm chuyên cần (Max: 8đ/ngày)│
│   - Điểm chuyên cần (Y điểm)    │     - Càng đủ giờ làm ô càng xanh đậm                  │
│   - Hạng (Rank)                 │     - Tooltip: Di chuột hiển thị "X Điểm chuyên cần"   │
│   - Hạng tháng (Monthly Rank)   │                                                        │
│                                 │ [3] Biểu Đồ Điểm Đánh Giá (Line Chart)                 │
│ • Nút [Đổi người dùng]          │     - Xu hướng điểm thưởng hiệu suất theo thời gian    │
└─────────────────────────────────┴────────────────────────────────────────────────────────┘
```

---

### 2.1. Thanh bên hồ sơ nhân sự (Sidebar Profile)

Nằm ở cột bên trái màn hình, cung cấp thông tin định danh và bảng tổng kết thành tích:

1. **Thông tin nhân sự cơ bản:**
   - **Ảnh đại diện:** Tải lên ảnh cá nhân hoặc sử dụng avatar ký tự viết tắt.
   - **Họ và tên:** Tên nhân sự (liên kết với hồ sơ Employee).
   - **Chức danh:** Vị trí công tác (Giám đốc Vận hành, Chuyên viên Kinh doanh, Quản lý Kho,...).
   - **Bio:** Giới thiệu ngắn về phạm vi phụ trách thị trường, địa bàn hoặc vai trò nhiệm vụ.

2. **Bảng thống kê thành tích & Xếp hạng (`User Stats`):**
   - **Điểm đánh giá:** Tổng số điểm đánh giá được ghi nhận từ cấp quản lý hoặc điểm thưởng hệ thống tự động khi tạo/chốt đơn hàng thành công (thay thế cho Điểm năng lượng cũ).
   - **Điểm chuyên cần:** Tổng điểm tích lũy từ thời gian làm việc thực tế tại văn phòng (cứ 1 giờ làm việc = 1 điểm, tối đa 8.0 điểm/ngày).
   - **Hạng (Rank):** Xếp hạng tổng thể của nhân viên trong toàn doanh nghiệp.
   - **Hạng tháng (Monthly Rank):** Thứ hạng thi đua đạt được trong tháng hiện tại.

3. **Chức năng "Đổi người dùng" (Change User):**
   - Cho phép cấp quản lý (COO, Chủ tịch) chuyển đổi nhanh để xem hồ sơ, giờ công và điểm chuyên cần của bất kỳ nhân viên nào trong doanh nghiệp.

---

### 2.2. Thẻ Chấm công WiFi BAKA (WiFi Attendance Card)

Nằm tại vị trí trên cùng của khu vực chính, là công cụ ghi nhận thời gian làm việc duy nhất của hệ thống:

1. **Cơ chế xác thực WiFi bảo mật:**
   - Bắt buộc nhân viên phải kết nối đúng mạng WiFi văn phòng (`BAKA-OFFICE-5G`).
   - Hệ thống tự động kiểm tra địa chỉ IP truy cập của thiết bị. Nếu nhân viên ở ngoài văn phòng hoặc dùng mạng 4G/mạng lạ, hệ thống sẽ **từ chối chấm công** và phát cảnh báo yêu cầu kết nối đúng WiFi công ty.

2. **Các trạng thái làm việc trong ngày:**
   - **Chưa chấm công:** Hiển thị nhãn cảnh báo màu vàng, nút `Chấm công VÀO` sẵn sàng.
   - **Đang làm việc:** Hiển thị nhãn màu xanh lá, ghi nhận thời điểm VÀO (ví dụ: `08:15:30`), đồng hồ đếm tổng thời gian làm việc tính đến hiện tại (`X giờ Y phút`), nút `Chấm công RA` sẵn sàng.
   - **Đã hoàn thành ca:** Hiển thị nhãn màu xanh đậm, tổng kết giờ VÀO, giờ RA và tổng thời lượng làm việc trong ngày.

3. **Các nút tương tác:**
   - **`Chấm công VÀO` (Check-in):** Ghi nhận bắt đầu ca làm việc buổi sáng.
   - **`Chấm công RA` (Check-out):** Ghi nhận kết thúc ca làm việc buổi chiều/tối.
   - **`Xem lịch sử chấm công`:** Chuyển nhanh sang màn hình danh sách nhật ký chấm công chi tiết (`Employee Checkin`).

---

### 2.3. Biểu đồ Tổng quan chuyên cần (Attendance Performance Heatmap)

- **Tiêu đề khối:** `Tổng quan chuyên cần`.
- **Cơ chế tính điểm & Đổ màu:**
  - **Công thức:** `1 giờ làm việc thực tế = 1 điểm chuyên cần` (tối đa **8.0 điểm/ngày**).
  - Đối với ca làm việc $\ge 5$ giờ, hệ thống tự động khấu trừ 1 giờ nghỉ trưa chuẩn để tính giờ làm việc thực tế.
  - **Mức độ xanh (Color Intensity):** Ô ngày làm việc càng nhiều điểm thì màu xanh càng đậm. Nhân viên làm đủ 8 tiếng sẽ đạt mức điểm tối đa và hiển thị **ô xanh đậm nhất**.
  - **Tương tác di chuột (Tooltip):** Khi rê chuột vào từng ô ngày trên biểu đồ, hệ thống hiển thị chính xác:
    $$\text{X.X Điểm chuyên cần (ngày dd-mm-yyyy)}$$
- **Bộ lọc thời gian:** Cho phép xem biểu đồ nhiệt theo từng năm dương lịch.

---

### 2.4. Biểu đồ Điểm đánh giá (Assessment Points Line Chart)

- **Tiêu đề khối:** `Điểm đánh giá`.
- **Nội dung:** Biểu đồ đường (Line Chart) thể hiện biến động và xu hướng tích lũy Điểm đánh giá của nhân viên qua các tuần/tháng.
- **Nguồn dữ liệu:** Đồng bộ từ sổ nhật ký điểm thưởng (`Energy Point Log`), bao gồm các điểm cộng thưởng khi hoàn thành xuất sắc nhiệm vụ, chốt đơn hàng bán vượt chỉ tiêu.

---

## 3. Các thành phần đã loại bỏ & Tối ưu hóa (Ultra-Minimal)

Theo định hướng tinh gọn, tránh gây xao nhãng và tăng tốc độ xử lý:

1. **Loại bỏ phần "Phân phối loại" (Type Distribution):**
   - Biểu đồ hình tròn phân phối loại điểm năng lượng mặc định của ERPNext đã được **loại bỏ hoàn toàn**.
   - Triệt tiêu các hàm tính toán `render_percentage_chart` và các lệnh gọi API truy vấn liên quan.

2. **Loại bỏ phần "Hoạt động gần đây" (Recent Activity):**
   - Danh sách dòng thời gian hoạt động xã hội (Like, Share, Comment) đã được **loại bỏ hoàn toàn** khỏi trang My Profile.
   - Triệt tiêu hàm `setup_user_activity_timeline` nhằm giảm tải dữ liệu, giúp trang tải tức thì.

3. **Loại bỏ nút Chấm công trên Navbar:**
   - Không đặt nút chấm công trên thanh menu trên cùng để tránh tình trạng hiển thị trùng lặp (duplicate) hoặc thao tác nhầm lẫn. Mọi thao tác chấm công đều thực hiện tập trung, chuẩn mực trong **My Profile**.

---

## 4. Bảng tổng hợp API & Logic kỹ thuật

| Hàm / Endpoint | File mã nguồn | Chức năng kỹ thuật |
| :--- | :--- | :--- |
| `get_attendance_status(user)` | `erpnext/setup/wifi_attendance.py` | Kiểm tra kết nối WiFi/IP, lấy trạng thái ca làm việc hôm nay và thống kê số ngày đi làm, đúng giờ trong tháng. |
| `checkin(log_type)` | `erpnext/setup/wifi_attendance.py` | Thực hiện xác thực IP mạng WiFi và tạo bản ghi `Employee Checkin` (IN hoặc OUT). |
| `get_chuyen_can_summary(user)` | `erpnext/setup/wifi_attendance.py` | Tính tổng điểm chuyên cần lũy kế của nhân viên, số điểm hôm nay và số ngày công thực tế. |
| `get_chuyen_can_heatmap_data(user, date)` | `erpnext/setup/wifi_attendance.py` | Trích xuất toàn bộ dữ liệu điểm chuyên cần theo từng ngày (1h = 1đ, max 8đ) nạp vào Heatmap chart. |
| `get_user_energy_and_review_points(user)` | `frappe/social/.../energy_point_log.py` | Trả về tổng Điểm đánh giá (Energy Points) của nhân viên. |
| `setup_profile_hook()` | `erpnext/public/js/wifi_attendance.js` | Tùy biến Frontend: Render thẻ chấm công WiFi, đổi tiêu đề biểu đồ, gán nhãn tooltip `Điểm chuyên cần`, loại bỏ Type Distribution & Recent Activity. |

---

## 5. Hướng dẫn nhân viên sử dụng

1. **Đăng nhập vào hệ thống:**
   - Truy cập `http://localhost:8080`, đăng nhập bằng tài khoản được cấp (Mật khẩu mặc định: `123`).
2. **Vào mục Hồ sơ cá nhân:**
   - Bấm vào Avatar góc trên cùng bên phải $\rightarrow$ Chọn **My Profile** (hoặc truy cập thẳng `/app/user-profile`).
3. **Thực hiện Chấm công VÀO (Buổi sáng):**
   - Đảm bảo thiết bị (Laptop/Điện thoại) đã kết nối mạng WiFi văn phòng (`BAKA-OFFICE-5G`).
   - Bấm nút **Chấm công VÀO**. Hệ thống báo xanh thành công, chuyển sang trạng thái *Đang làm việc*.
4. **Theo dõi điểm số trong ngày:**
   - Hệ thống tự động tích lũy 1 điểm chuyên cần cho mỗi 1 giờ làm việc thực tế.
5. **Thực hiện Chấm công RA (Buổi chiều/tối khi tan sở):**
   - Trước khi rời văn phòng, bấm nút **Chấm công RA**. Hệ thống chốt tổng thời gian làm việc trong ngày và cập nhật ngay vào biểu đồ nhiệt *Tổng quan chuyên cần*.
