# BÁO CÁO KẾT QUẢ KIỂM THỬ HỆ THỐNG (ERP TEST REPORT)
**Dự án:** Hệ thống ERP Phân phối Thực phẩm Bảo vệ Sức khỏe (BAKAERP)  
**Ngày kiểm thử:** 15/10/2026  
**Môi trường:** Docker Multi-Container (Frappe v15 + MariaDB 10.6)  
**Trạng thái kiểm thử:** **PASS 45/45 BÀI KIỂM THỬ (100%)**

---

## 1. Tóm tắt Kết quả Thực thi Kiểm thử

```
==================================================================
=== BẮT ĐẦU CHẠY TOÀN BỘ BỘ KIỂM THỬ TỰ ĐỘNG (ERP TEST SUITE) ===
==================================================================

1. Nhóm Sản phẩm, Thương hiệu BAKA & Dòng SP:  7/7 PASS
2. Nhóm Kho vận, Lô hàng & Bàn giao Kho NV:    7/7 PASS
3. Nhóm Bán hàng Đa Kênh & Chống trùng & CSV:  8/8 PASS
4. Nhóm Đối soát Tiền thu hộ:                  1/1 PASS
5. Nhóm Tài chính Quản trị & Báo cáo P&L:      7/7 PASS
6. Nhóm Nhân sự, WiFi & Chuyên cần:           15/15 PASS
------------------------------------------------------------------
TỔNG CỘNG:                                     45/45 BÀI KIỂM THỬ ĐÃ PASS 100%
==================================================================
{"status": "success", "total_tests": 45, "passed": 45}
```

---

## 2. Chi tiết Từng Hạng mục Kiểm thử Nghiệp vụ (Section 18 Test Details)

### 2.1. Kiểm thử Sản phẩm, Thương hiệu BAKA & Dòng sản phẩm (Brands & Items)
- **Bài kiểm thử 1:** Thương hiệu duy nhất là **`BAKA`** (`Brand.name = 'BAKA'`) $\rightarrow$ **PASS**.
- **Bài kiểm thử 2:** Tồn tại đủ 3 Dòng sản phẩm (`PLUS`, `CACAO`, `TIBOKA`) thuộc cây Item Group $\rightarrow$ **PASS**.
- **Bài kiểm thử 3:** Tồn tại đủ 3 Sản phẩm cốt lõi (`TBK-PLUS`, `TBK-CACAO`, `TBK-TIBOKA`) $\rightarrow$ **PASS**.
- **Bài kiểm thử 4:** Tất cả sản phẩm thuộc Thương hiệu duy nhất `BAKA` $\rightarrow$ **PASS**.
- **Bài kiểm thử 5:** Gán đúng Dòng sản phẩm (`custom_product_line`) cho từng SKU $\rightarrow$ **PASS**.
- **Bài kiểm thử 6:** Bật chế độ quản lý Lô (`has_batch_no=1`) và Hạn sử dụng (`has_expiry_date=1`) cho cả 3 sản phẩm (FEFO) $\rightarrow$ **PASS**.
- **Bài kiểm thử 7:** Đơn vị tính cơ sở chuẩn hóa là `Hộp` (số nguyên) $\rightarrow$ **PASS**.

### 2.2. Kiểm thử Kho vận, Lô hàng & Bàn giao Kho Nhân Viên (FEFO)
- **Bài kiểm thử 8:** Tổng tồn kho toàn hệ thống phản ánh đúng số liệu nhập kho thực tế (3.271 hộp thành phẩm) $\rightarrow$ **PASS**.
- **Bài kiểm thử 9:** Tồn kho tại Kho Tổng BAKA (`Finished Goods - B` / `Kho Tổng BAKA - B`): 1.931 hộp $\rightarrow$ **PASS**.
- **Bài kiểm thử 10:** Tồn kho tại Kho Nhân Viên Di Động (`Kho Nhân Viên - B`): 135 hộp $\rightarrow$ **PASS**.
- **Bài kiểm thử 11:** Kho NVKD Nguyễn Văn Nam có cả 2 mặt hàng PLUS và CACAO $\rightarrow$ **PASS**.
- **Bài kiểm thử 12:** Tồn kho NVKD Nguyễn Văn Nam giảm chính xác sau bán lẻ trực tiếp: Nhận bàn giao 40 hộp PLUS, bán 5 hộp cho khách lẻ $\rightarrow$ Còn lại chính xác **35 hộp** (Giá trị tồn: 7.000.000 đ) $\rightarrow$ **PASS**.
- **Bài kiểm thử 13:** Hệ thống tự động phát hiện và cảnh báo Lô cận date: Lô `LOT-PLUS-NEAR` (HSD: 20/11/2026, còn 36 ngày) được gắn nhãn `CẬN DATE (Còn 36 ngày)` mức cảnh báo `warning` màu vàng $\rightarrow$ **PASS**.
- **Bài kiểm thử 14:** Bàn giao hàng sang kho nhân viên thực hiện bằng `Material Transfer` nội bộ, **xác nhận không tạo doanh thu, không phát sinh công nợ** (hàng thuộc sở hữu công ty đến khi bán) $\rightarrow$ **PASS**.

### 2.3. Kiểm thử Bán hàng Đa Kênh, CSV Import & Chống trùng đơn sàn (Idempotency)
- **Bài kiểm thử 15:** Kênh **B2B Sỉ** phát sinh doanh thu thực tế: 147.725.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 16:** Kênh **B2C Trực tiếp** phát sinh doanh thu: 1.825.000 đ (xuất từ Kho NVKD) $\rightarrow$ **PASS**.
- **Bài kiểm thử 17:** Kênh **TikTok Shop** phát sinh doanh thu: 7.030.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 18:** Kênh **Shopee** phát sinh doanh thu: 10.475.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 19:** Kênh **Website** phát sinh doanh thu: 4.245.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 20:** Adapter tự động nhận diện và chặn đơn sàn trùng (Idempotent theo `marketplace_order_id = TIKTOK-20261010-001`): Bỏ qua để chống trùng lặp dữ liệu $\rightarrow$ **PASS**.
- **Bài kiểm thử 21:** Import đơn hàng đa kênh từ CSV và chống trùng đúp dữ liệu (`import_orders_from_csv`): Bỏ qua đơn `TIKTOK-CSV-DEMO-01` nếu đã có $\rightarrow$ **PASS**.
- **Bài kiểm thử 22:** Tích hợp kế thừa và xử lý chính xác phí sàn (`custom_platform_fee`) và phí ship (`custom_shipping_fee`) $\rightarrow$ **PASS**.

### 2.4. Kiểm thử Đối soát Tiền thu hộ của Nhân viên (Tài khoản 1411)
- **Bài kiểm thử 23:** NVKD Nguyễn Văn Nam bán lẻ đơn 1.825.000 đ (thu tiền mặt), đã làm ủy nhiệm chi nộp 1.500.000 đ về tài khoản ngân hàng công ty `1121`. Số dư nợ còn lại trên tài khoản `1411 - Tiền thu hộ của NVKD - B` là chính xác **325.000 đ** $\rightarrow$ **PASS**.

### 2.5. Kiểm thử Tài chính Quản trị & Báo cáo P&L Đa Chiều
- **Bài kiểm thử 24:** Báo cáo P&L xác định Thương hiệu duy nhất **`BAKA`** $\rightarrow$ **PASS**.
- **Bài kiểm thử 25:** Lợi nhuận gộp tính toán chuẩn xác độc lập:
  $$\text{Doanh thu thuần } (171.300.000 \text{ đ}) - \text{Giá vốn COGS } (95.100.000 \text{ đ}) = \text{Lợi nhuận gộp } (76.200.000 \text{ đ})$$
  Biên lợi nhuận gộp đạt **44,48%** $\rightarrow$ **PASS**.
- **Bài kiểm thử 26:** Lợi nhuận ròng quản trị khớp phương trình độc lập:
  $$\text{Lợi nhuận gộp } (76.200.000) - \text{Phí sàn } (1.500.150) - \text{Phí ship } (300.000) - \text{Ads } (6.000.000) - \text{Lương } (31.000.000) - \text{Thuê kho/VP } (8.000.000) = \mathbf{29.399.850 \text{ đ}}$$
  Tỷ suất lợi nhuận ròng đạt **17,16%** $\rightarrow$ **PASS**.
- **Bài kiểm thử 27:** Báo cáo P&L bóc tách theo Dòng sản phẩm `PLUS`: Doanh thu 91.250.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 28:** Báo cáo P&L bóc tách theo Dòng sản phẩm `CACAO`: Doanh thu 45.050.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 29:** Báo cáo P&L bóc tách theo Dòng sản phẩm `TIBOKA`: Doanh thu 35.000.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 30:** Tổng doanh thu 3 Dòng sản phẩm khớp chính xác Tổng doanh thu toàn hệ thống ($91.250.000 + 45.050.000 + 35.000.000 = 171.300.000 \text{ đ}$) $\rightarrow$ **PASS**.

### 2.6. Kiểm thử Nhân sự, Chấm công WiFi & Điểm Chuyên Cần
- **Bài kiểm thử 31-35:** Kiểm tra chấm công WiFi hoạt động bình thường, định danh đúng Employee ID cho cả 5 tài khoản chủ chốt (`chutich@baka.vn`, `coo@baka.vn`, `sale1@baka.vn`, `sale2@baka.vn`, `kho@baka.vn`) $\rightarrow$ **PASS**.
- **Bài kiểm thử 36-40:** Kiểm tra Điểm chuyên cần theo năm của từng nhân sự luôn là **số nguyên (integer)**, không có phần thập phân $\rightarrow$ **PASS**.
- **Bài kiểm thử 41-45:** Kiểm tra Điểm chuyên cần từng ngày trên Heatmap không vượt quá **8 điểm/ngày** theo đúng quy định $\rightarrow$ **PASS**.
- **Bổ sung:** Đơn xin nghỉ phép hợp lệ được phê duyệt (`coo@baka.vn` duyệt cho `sale1@baka.vn`) $\rightarrow$ **PASS**.

---

## 3. Lệnh Tự Động Kiểm Thử Định Kỳ (Regression Command)

Bất kỳ lúc nào, quản trị viên có thể chạy lệnh sau để xác minh tính toàn vẹn hệ thống:
```bash
docker compose exec backend bench --site frontend execute erpnext.setup.health_food_erp_test.run_all_tests
```
