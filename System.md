# BAKAERP - Tài Liệu Chức Năng Phân Hệ Hồ Sơ Cá Nhân (My Profile)

<div align="center">
  <h2>PHÂN HỆ HỒ SƠ CÁ NHÂN & CHẤM CÔNG WIFI (MY PROFILE)</h2>
  <p><b>Trung tâm quản lý hiệu suất nhân sự, chấm công bảo mật WiFi và theo dõi điểm chuyên cần</b></p>
  <p>BAKAERP v15 • Chấm công WiFi • Điểm chuyên cần theo năm (1đ/ngày đủ 8h) • Điểm đánh giá thi đua</p>
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
│ • Họ và tên đầy đủ              │     - 4 Chỉ số: Giờ Vào / Giờ Ra / Hôm nay / Tổng tháng│
│ • Chức vụ & Phòng ban           │     - Nút Chấm công Đan xen theo ca (VÀO / RA)         │
│ • Bio (Mô tả trách nhiệm)       │                                                        │
│                                 │ [2] Biểu Đồ Tổng Quan Chuyên Cần (Heatmap)             │
│ • Chỉ số thành tích & Thi đua:  │     - Đủ 8h/ngày = 1 điểm chuyên cần (Tính theo năm)   │
│   - Điểm đánh giá (X điểm)      │     - Ngày đạt đủ 8h hiển thị ô xanh chuyên cần        │
│   - Điểm chuyên cần (Y điểm)    │     - Tự động reset về 0 điểm sau mỗi hết 1 năm        │
│   - Hạng (Rank)                 │                                                        │
│   - Hạng tháng (Monthly Rank)   │ [3] Biểu Đồ Điểm Đánh Giá (Line Chart)                 │
│                                 │     - Xu hướng điểm thưởng hiệu suất theo thời gian    │
│ • Nút [Đổi người dùng]          │                                                        │
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
   - **Điểm chuyên cần:** Tổng điểm tích lũy theo năm dương lịch (cứ làm đủ 8 tiếng 1 ngày thì tính là 1 điểm, số nguyên không có thập phân; hết 1 năm thì tự động reset về 0).
   - **Hạng (Rank):** Xếp hạng tổng thể của nhân viên trong toàn doanh nghiệp.
   - **Hạng tháng (Monthly Rank):** Thứ hạng thi đua đạt được trong tháng hiện tại.

3. **Chức năng "Đổi người dùng" (Change User):**
   - Cho phép cấp quản lý (COO, Chủ tịch) chuyển đổi nhanh để xem hồ sơ, giờ công và điểm chuyên cần của bất kỳ nhân viên nào trong doanh nghiệp.

---

### 2.2. Thẻ Chấm công WiFi BAKA & Quản lý Ca Đan Xen (Multi-shift)

Nằm tại vị trí trên cùng của khu vực chính, là công cụ ghi nhận thời gian làm việc duy nhất của hệ thống:

1. **Cơ chế xác thực WiFi bảo mật:**
   - Bắt buộc nhân viên phải kết nối đúng mạng WiFi văn phòng (`BAKA-OFFICE-5G`).
   - Hệ thống tự động kiểm tra địa chỉ IP truy cập của thiết bị. Nếu nhân viên ở ngoài văn phòng hoặc dùng mạng 4G/mạng lạ, hệ thống sẽ **từ chối chấm công** và phát cảnh báo yêu cầu kết nối đúng WiFi công ty.

2. **Bảng 4 chỉ số thống kê trực quan:**
   - **Giờ Vào Hôm Nay:** Mốc thời gian bắt đầu ca đầu tiên trong ngày (ví dụ: `08:15:37`).
   - **Giờ Ra Hôm Nay:** Mốc thời gian kết thúc ca gần nhất trong ngày (hoặc `--:--` nếu đang trong ca).
   - **Thời Gian Hôm Nay:** Tổng thời lượng làm việc thực tế đã tích lũy trong ngày (`X giờ Y phút`).
   - **Tổng Giờ Tháng Này:** Tổng số giờ làm việc thực tế tích lũy của nhân viên trong tháng hiện tại (ví dụ: `86.5 giờ`).

3. **Cơ chế Máy trạng thái Đan xen (State-Machine) & Hỗ trợ 2 Ca/Nhiều Ca:**
   - Hỗ trợ linh hoạt cho cả nhân viên làm 1 ca thông thường hoặc làm **2 ca / ca gãy / ca tăng ca** (Ca sáng $\rightarrow$ Ca chiều $\rightarrow$ Tăng ca tối).
   - **Quy trình đan xen tự nhiên:** $\text{VÀO} \rightarrow \text{RA} \rightarrow \text{VÀO} \rightarrow \text{RA}$.
   - **Không cần thời gian chờ (Không cooldown):** Nhân viên có thể chấm công ngay lập tức khi chuyển ca hoặc ra vào văn phòng mà không bị khóa chờ 5 phút như trước.
   - **Chống spam & chống bấm nhầm:**
     - Đang ngoài ca (hoặc đầu ngày): Giao diện chỉ hiển thị duy nhất nút **`Chấm công VÀO`** (hoặc `Chấm công VÀO (Ca tiếp theo)`). Chặn không cho phép bấm RA.
     - Đang trong ca: Giao diện tự động chuyển sang duy nhất nút **`Chấm công RA`**, hiển thị rõ ca đang làm và thời gian làm việc. Chặn không cho phép bấm VÀO tiếp.
     - **Khóa nút bấm tức thì (Click Lock):** Nút bấm lập tức vô hiệu hóa khi chạm chuột/màn hình cảm ứng trong lúc gửi dữ liệu để triệt tiêu lỗi double-click.

4. **Giới hạn 10 lần chấm công/ngày & Khóa nút an toàn:**
   - Mỗi nhân viên được phép thực hiện tối đa **10 lần chấm công (check-in / check-out)** trong một ngày mà không bị giới hạn cooldown.
   - Giao diện không hiển thị số lần đếm để tránh gây rối mắt cho người dùng.
   - **Khi đạt mốc 10 lần:**
     - Hệ thống lập tức **khóa hoàn toàn nút chấm công** cho ngày hôm đó.
     - Hiển thị banner cảnh báo màu đỏ: *"Bạn đã đạt tối đa 10 lần chấm công trong ngày hôm nay. Vui lòng liên hệ với Ban lãnh đạo để được hỗ trợ xử lý!"*
     - Mọi yêu cầu chấm công vượt quá 10 lần từ API/Backend đều bị từ chối và yêu cầu liên hệ Ban lãnh đạo.

5. **Tính giờ làm việc & Điểm chuyên cần chuẩn xác:**
   - Tổng thời gian làm việc được tính theo tổng độ dài của từng cặp ca thực tế: $\sum (\text{RA}_i - \text{VÀO}_i)$.
   - Tự động loại trừ thời gian nghỉ giữa các ca, bảo đảm dữ liệu minh bạch, chuẩn xác cho cả doanh nghiệp và người lao động.
   - Đã loại bỏ hoàn toàn nút *"Xem lịch sử chi tiết"* rườm rà, tập trung tối đa vào trải nghiệm nhanh gọn của người dùng.

---

### 2.3. Biểu đồ Tổng quan chuyên cần (Attendance Performance Heatmap)

- **Tiêu đề khối:** `Tổng quan chuyên cần`.
- **Cơ chế tính điểm & Đổ màu:**
  - **Chu kỳ tính theo năm:** Điểm chuyên cần được tính lũy kế theo năm dương lịch (từ ngày 01/01 đến 31/12). Hết 1 năm hệ thống sẽ tự động reset về 0 để bắt đầu chu kỳ đánh giá năm mới.
  - **Quy tắc tính điểm chuẩn:** Cứ làm **đủ 8 tiếng trong 1 ngày** thì được tính là **1 điểm**, dưới 8 tiếng là **0 điểm**. Điểm chuyên cần là **số nguyên duy nhất (1 hoặc 0)**, hoàn toàn không có phần thập phân.
  - Đối với ca làm việc $\ge 5$ giờ, hệ thống tự động khấu trừ 1 giờ nghỉ trưa chuẩn để tính thời gian làm việc thực tế.
  - **Hiển thị trên biểu đồ Heatmap:** Ngày đạt đủ 8 tiếng sẽ nhận 1 điểm và hiển thị **ô xanh chuyên cần**. Ngày không đủ 8 tiếng (0 điểm) hoặc không đi làm sẽ có màu xám nhạt/trắng.
  - **Tương tác di chuột (Tooltip):** Khi rê chuột vào từng ô ngày trên biểu đồ, hệ thống hiển thị chính xác:
    $$\text{X Điểm chuyên cần (ngày dd-mm-yyyy)}$$
    *(ví dụ: `1 Điểm chuyên cần (ngày 14-10-2026)` hoặc `0 Điểm chuyên cần`)*.
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
| `get_chuyen_can_summary(user, year)` | `erpnext/setup/wifi_attendance.py` | Tính tổng điểm chuyên cần trong năm dương lịch (đủ 8h = 1đ, số nguyên, reset theo năm), điểm hôm nay và số ngày công. |
| `get_chuyen_can_heatmap_data(user, date)` | `erpnext/setup/wifi_attendance.py` | Trích xuất toàn bộ dữ liệu điểm chuyên cần theo từng ngày (đủ 8h = 1đ, tính theo năm) nạp vào Heatmap chart. |
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
   - Điểm chuyên cần tính theo năm: Cứ làm đủ 8 tiếng 1 ngày sẽ đạt 1 điểm chuyên cần (số nguyên, không có số thập phân). Hết 1 năm hệ thống tự động reset chu kỳ mới.
5. **Thực hiện Chấm công RA (Buổi chiều/tối khi tan sở):**
   - Trước khi rời văn phòng, bấm nút **Chấm công RA**. Hệ thống chốt tổng thời gian làm việc trong ngày và cập nhật ngay vào biểu đồ nhiệt *Tổng quan chuyên cần*.

