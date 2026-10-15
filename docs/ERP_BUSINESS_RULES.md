# QUY TẮC NGHIỆP VỤ HỆ THỐNG ERP (ERP BUSINESS RULES)
**Dự án:** Hệ thống ERP Phân phối Thực phẩm Bảo vệ Sức khỏe (BAKAERP)  
**Thương hiệu duy nhất:** BAKA  
**Dòng sản phẩm:** PLUS (Cao cấp), CACAO (Hương vị), TIBOKA (Đại trà)  
**Kênh bán:** TikTok Shop, Shopee, Đại lý B2B, Bán lẻ B2C trực tiếp, Website  

---

## 1. Quy tắc Quản lý Sản phẩm, Lô hàng & Xuất kho FEFO

### 1.1. Phân cấp Thương hiệu & Dòng sản phẩm
- **Thương hiệu duy nhất là BAKA.** PLUS, CACAO, TIBOKA là các dòng sản phẩm (Product Lines) cốt lõi của BAKA, không phải thương hiệu riêng biệt.
- Mỗi sản phẩm (`Item`) thuộc Thương hiệu duy nhất `BAKA` và gắn với một Dòng sản phẩm chuẩn:
  - `PLUS`: Dòng tinh bột kháng BAKA cao cấp (Giá bán lẻ: 365.000 đ/hộp; Giá vốn: 200.000 đ/hộp).
  - `CACAO`: Dòng tinh bột kháng BAKA hương vị ca cao tự nhiên (Giá bán lẻ: 265.000 đ/hộp; Giá vốn: 150.000 đ/hộp).
  - `TIBOKA`: Dòng tinh bột kháng BAKA dinh dưỡng đại trà (Giá bán lẻ: 250.000 đ/hộp; Giá vốn: 140.000 đ/hộp).
- Bắt buộc đơn vị tính gốc (`Stock UOM`): **`Hộp`** (số nguyên, không cho phép số lẻ).

### 1.2. Quy tắc Lô (Batch) & Hạn sử dụng (Expiry Date)
- Mọi nghiệp vụ nhập kho thành phẩm (Material Receipt / Purchase Receipt) đều phải gắn với một Mã lô (`batch_id`) và Hạn sử dụng (`expiry_date`) cụ thể.
- **Nguyên tắc xuất kho FEFO (First Expired, First Out):** Khi tạo lệnh xuất kho bán hàng (`Delivery Note`) hoặc điều chuyển (`Stock Entry`), hệ thống ưu tiên chọn lô hàng có ngày hết hạn sớm nhất còn tồn trong kho chỉ định.
- **Chặn xuất lô hết hạn:** Tuyệt đối không cho phép xuất kho đối với lô hàng có `expiry_date < ngày hiện tại` vào các đơn bán hàng cho khách. Các lô quá hạn chỉ được phép điều chuyển sang `Kho Hàng Hỏng & Hết Hạn` để lập biên bản tiêu hủy.
- **Ngưỡng cảnh báo cận hạn (Near-Expiry Alert):**
  - Cận date cấp độ 1: Còn dưới 60 ngày đến hạn sử dụng $\rightarrow$ Bật cảnh báo vàng trên Dashboard kho để ưu tiên đẩy bán hoặc khuyến mãi.
  - Cận date cấp độ 2: Còn dưới 30 ngày đến hạn sử dụng $\rightarrow$ Bật cảnh báo đỏ, cách ly hoặc xin phê duyệt xử lý đặc biệt.

---

## 2. Quy tắc Kho vận & Bàn giao Kho Nhân Viên Di Động

### 2.1. Cấu trúc kho vận
- **Kho Tổng BAKA (`Finished Goods - B`):** Nơi tiếp nhận thành phẩm sản xuất, cung ứng cho toàn bộ đơn sỉ B2B, đơn sàn Shopee/TikTok và đơn Website.
- **Kho Nhân Viên Di Động (`Kho NVKD - [Tên NV] - B`):** Mỗi nhân viên kinh doanh thị trường được cấp một kho di động riêng để chứa hàng mang đi chào bán trực tiếp.
- **Kho Cách Ly & Đổi Trả (`Quarantine - B`):** Nơi tiếp nhận toàn bộ hàng hoàn/đổi trả từ khách hàng hoặc sàn để kiểm tra phân loại.
- **Kho Hàng Hỏng & Hết Hạn (`Damaged - B`):** Chứa hàng lỗi, rách bao bì, quá hạn để chờ xuất hủy.

### 2.2. Quy trình Bàn giao hàng sang Kho Nhân viên
- Bàn giao hàng từ Kho Tổng cho NVKD **bắt buộc dùng `Stock Entry` (loại `Material Transfer`)**.
- **Nguyên tắc bất di bất dịch:** Việc bàn giao hàng này **tuyệt đối KHÔNG ghi nhận doanh thu, KHÔNG phát sinh công nợ khách hàng**, chỉ chuyển giao trách nhiệm quản lý vật chất giữa Thủ kho và Nhân viên kinh doanh.
- Khi NVKD bán được hàng cho khách lẻ trực tiếp: Thực hiện xuất kho (`Delivery Note` hoặc `Sales Invoice`) từ chính **Kho NVKD của nhân viên đó**.
- Khi NVKD nộp lại hàng chưa bán về công ty: Tạo chứng từ `Material Transfer` điều chuyển ngược từ Kho NVKD về Kho Tổng BAKA.

---

## 3. Quy tắc Bán hàng Đa Kênh, Công Nợ & Thu tiền hộ

### 3.1. Kênh Bán Sỉ B2B (Đại lý & Nhà phân phối)
- Đơn hàng xuất từ Kho Tổng BAKA.
- **Hạn mức công nợ (Credit Limit):** Mỗi đại lý có hạn mức nợ cụ thể (ví dụ: 50.000.000 đ hoặc 100.000.000 đ). Nếu tổng nợ vượt hạn mức, hệ thống cảnh báo hoặc yêu cầu cấp quản lý (COO) phê duyệt.
- **Thời hạn công nợ (Payment Terms):** Thời hạn thanh toán chuẩn từ 15 đến 30 ngày. Quá hạn hệ thống đánh dấu nợ quá hạn.
- **Thu tiền nhiều lần (Partial Payments):** Cho phép ghi nhận nhiều phiếu thu (`Payment Entry`) cho cùng một hóa đơn bán hàng cho đến khi hết công nợ.

### 3.2. Kênh Bán lẻ Trực tiếp B2C & Đối soát Tiền Thu Hộ
- Khi NVKD bán lẻ trực tiếp thu tiền mặt hoặc khách chuyển khoản vào tài khoản cá nhân của NVKD:
  - Hóa đơn ghi nhận thanh toán vào tài khoản **`1411 - Tiền thu hộ của NVKD`** mang tên nhân viên đó.
  - Doanh thu được ghi nhận cho công ty, nhưng dòng tiền thực tế đang nằm tại NVKD.
- **Quy trình Nộp tiền & Đối soát (Reconciliation):**
  - Định kỳ (hàng ngày hoặc hàng tuần), NVKD nộp tiền mặt vào quỹ hoặc chuyển khoản về tài khoản ngân hàng công ty (`1121`).
  - Kế toán lập `Payment Entry` chuyển tiền từ tài khoản `1411 - Tiền thu hộ của NVKD` sang `1121 - Tiền gửi ngân hàng (VND)`.
  - Số dư nợ còn lại trên tài khoản `1411` chính là số tiền NVKD còn phải nộp về công ty.

### 3.3. Kênh Sàn TMĐT (Shopee & TikTok Shop) & Chống trùng đơn
- Tiếp nhận đơn qua bộ chuyển đổi dữ liệu (Adapter).
- **Quy tắc chống trùng đơn (Idempotency):**
  - Mỗi đơn hàng sàn có mã duy nhất `marketplace_order_id` (ví dụ: `SHOPEE-20261015-001`, `TIKTOK-20261015-002`).
  - Hệ thống kiểm tra: Nếu đơn hàng có mã này đã tồn tại trong cơ sở dữ liệu, thao tác import sẽ lập tức từ chối và ghi log, **tuyệt đối không tạo trùng đơn bán, không xuất kho hai lần và không ghi nhận đúp doanh thu**.
- **Quy tắc chi phí sàn:**
  - Tiền hàng thanh toán của khách: Ghi nhận doanh thu gộp.
  - Phí hoa hồng sàn + Phí thanh toán sàn: Hạch toán vào tài khoản `6413 - Phí sàn TMĐT`.
  - Phí vận chuyển sàn tài trợ/thu hộ: Hạch toán theo số liệu quyết toán thực tế.
  - Số tiền sàn chuyển về tài khoản ngân hàng công ty sau khi trừ phí = Doanh thu - Phí sàn - Chiết khấu sàn.

### 3.4. Xử lý Đổi trả Hàng (Returns)
- Khi khách hàng hoặc sàn hoàn trả hàng:
  - Lập chứng từ trả hàng (`Sales Invoice Return` hoặc `Delivery Note Return`).
  - Hàng hoàn trả **bắt buộc nhập vào `Kho Cách Ly & Đổi Trả - B`**, chưa được nhập ngay về Kho Tổng.
  - Thủ kho kiểm định chất lượng:
    - Nếu hàng còn nguyên tem/hộp/đạt chất lượng: Lập phiếu `Material Transfer` chuyển từ Kho Cách Ly về Kho Tổng để tiếp tục bán.
    - Nếu hàng bị rách hộp, móp méo, hỏng hoặc quá hạn: Lập phiếu `Material Transfer` chuyển sang `Kho Hàng Hỏng & Hết Hạn`, sau đó xuất hủy vào chi phí tổn thất `811`.

---

## 4. Quy tắc Kế toán Quản trị & Báo cáo Lãi Lỗ (Managerial P&L)

### 4.1. Công thức Lãi Lỗ Quản Trị Đa Chiều
$$\text{Doanh thu thuần} = \text{Doanh thu gộp (5111)} - \text{Chiết khấu thương mại (5211)} - \text{Hàng bán trả lại (5213)}$$
$$\text{Lợi nhuận gộp (Gross Profit)} = \text{Doanh thu thuần} - \text{Giá vốn hàng bán (COGS 632)}$$
$$\text{Lợi nhuận kinh doanh trực tiếp} = \text{Lợi nhuận gộp} - \text{Phí sàn TMĐT (6413)} - \text{Chi phí vận chuyển (6412)}$$
$$\text{Lợi nhuận sau Marketing} = \text{Lợi nhuận kinh doanh trực tiếp} - \text{Chi phí Quảng cáo Ads (6414)}$$
$$\text{Lợi nhuận ròng quản trị (Net Profit)} = \text{Lợi nhuận sau Marketing} - \text{Chi phí Nhân viên (6411 + 6421)} - \text{Chi phí Vận hành chung (6426 + 6428)}$$

### 4.2. Nguyên tắc phân bổ chi phí
- **Doanh thu & Giá vốn:** Phân bổ trực tiếp theo từng sản phẩm, Dòng sản phẩm (`PLUS`, `CACAO`, `TIBOKA`) thuộc thương hiệu duy nhất `BAKA` và Kênh bán.
- **Phí sàn:** Phân bổ trực tiếp cho kênh TikTok Shop và Shopee.
- **Chi phí Quảng cáo Ads:** Phân bổ theo chiến dịch của từng kênh và dòng sản phẩm tương ứng.
- **Chi phí Lương & Vận hành:** Phân bổ chung cho doanh nghiệp hoặc chia theo tỷ trọng doanh thu giữa các dòng sản phẩm.

---

## 5. Quy tắc Nhân sự, Chấm công WiFi & Đánh giá KPI

### 5.1. Quy tắc Chấm công WiFi (Bảo toàn 100%)
- **Địa điểm & Mạng:** Chỉ chấm công tại trang `My Profile` khi kết nối đúng WiFi văn phòng `BAKA-OFFICE-5G` (kiểm tra dải IP hợp lệ).
- **Máy trạng thái ca đan xen:** $\text{VÀO} \rightarrow \text{RA} \rightarrow \text{VÀO} \rightarrow \text{RA}$. Hỗ trợ làm 2 ca/nhiều ca trong ngày.
- **Giới hạn số lần:** Không giới hạn cooldown; tối đa 10 lần chấm công/ngày. Quá 10 lần hệ thống tự động khóa nút và hiển thị cảnh báo liên hệ Ban lãnh đạo.
- **Điểm chuyên cần:**
  - Cứ tròn 1 tiếng làm việc thực tế = 1 điểm chuyên cần (số nguyên, không lấy thập phân, tối đa 8 điểm/ngày).
  - Chu kỳ tính theo năm dương lịch: Hết năm tự động reset chu kỳ mới.
  - Biểu đồ nhiệt (Heatmap): Đổ màu theo 4 mốc (Mốc 2: Level 1, Mốc 4: Level 2, Mốc 6: Level 3, Mốc 8: Level 4). Tooltip hiển thị đúng số điểm chuyên cần thực tế của ngày hôm đó (ví dụ 3, 5, 7 điểm).

### 5.2. Đánh giá KPI Bán hàng & Thưởng Thi Đua
- **Điểm Đánh Giá (Energy Points):**
  - Đạt chỉ tiêu doanh thu sỉ B2B trong tuần: +20 đến +50 điểm.
  - Chốt thành công đại lý phân phối mới: +30 điểm.
  - Đạt điểm chuyên cần tối đa trong tuần (không đi muộn): +10 điểm.
- Bảng xếp hạng thi đua nhân sự (Leaderboard) được cập nhật tự động hàng tuần/tháng.

