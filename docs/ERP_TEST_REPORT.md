# BÁO CÁO KẾT QUẢ KIỂM THỬ HỆ THỐNG (ERP TEST REPORT)
**Dự án:** Hệ thống ERP Phân phối Thực phẩm Bảo vệ Sức khỏe (BAKAERP)  
**Ngày kiểm thử:** 15/10/2026  
**Môi trường:** Docker Multi-Container (Frappe v15 + MariaDB 10.6)  
**Trạng thái kiểm thử:** **PASS 41/41 BÀI KIỂM THỬ (100%)**

---

## 1. Tóm tắt Kết quả Thực thi Kiểm thử

```
==================================================================
=== BẮT ĐẦU CHẠY TOÀN BỘ BỘ KIỂM THỬ TỰ ĐỘNG (ERP TEST SUITE) ===
==================================================================

1. Nhóm Sản phẩm & Nhãn hàng:      5/5 PASS
2. Nhóm Kho vận & Lô hàng FEFO:     7/7 PASS
3. Nhóm Bán hàng Đa Kênh & Dedup:   7/7 PASS
4. Nhóm Đối soát Tiền thu hộ:      1/1 PASS
5. Nhóm Tài chính & Báo cáo P&L:    6/6 PASS
6. Nhóm Nhân sự, WiFi & Chuyên cần:15/15 PASS
------------------------------------------------------------------
TỔNG CỘNG:                         41/41 BÀI KIỂM THỬ ĐÃ PASS 100%
==================================================================
```

---

## 2. Chi tiết Từng Hạng mục Kiểm thử Nghiệp vụ (Section 18 Test Details)

### 2.1. Kiểm thử Sản phẩm & 3 Nhãn hàng (Brands & Items)
- **Bài kiểm thử 1:** Tồn tại đủ 3 Nhãn hàng (`PLUS`, `CACAO`, `TIBOKA`) $\rightarrow$ **PASS**.
- **Bài kiểm thử 2:** Tồn tại đủ 3 Sản phẩm cốt lõi (`TBK-PLUS`, `TBK-CACAO`, `TBK-TIBOKA`) $\rightarrow$ **PASS**.
- **Bài kiểm thử 3:** Bật chế độ quản lý Lô (`has_batch_no=1`) và Hạn sử dụng (`has_expiry_date=1`) cho cả 3 sản phẩm $\rightarrow$ **PASS**.
- **Bài kiểm thử 4:** Đơn vị tính cơ sở chuẩn hóa là `Hộp` (số nguyên) $\rightarrow$ **PASS**.
- **Bài kiểm thử 5:** Gán chính xác Nhãn hàng tương ứng cho từng SKU (`TBK-PLUS` $\rightarrow$ PLUS, `TBK-CACAO` $\rightarrow$ CACAO, `TBK-TIBOKA` $\rightarrow$ TIBOKA) $\rightarrow$ **PASS**.

### 2.2. Kiểm thử Kho vận, Lô hàng & Bàn giao Kho Nhân Viên (FEFO)
- **Bài kiểm thử 6:** Tổng tồn kho toàn hệ thống phản ánh đúng số liệu nhập kho thực tế (3.273 hộp thành phẩm) $\rightarrow$ **PASS**.
- **Bài kiểm thử 7:** Tồn kho tại Kho Tổng BAKA (`Finished Goods - B` / `Kho Tổng BAKA - B`): 1.933 hộp $\rightarrow$ **PASS**.
- **Bài kiểm thử 8:** Tồn kho tại Kho Nhân Viên Di Động (`Kho Nhân Viên - B`): 135 hộp $\rightarrow$ **PASS**.
- **Bài kiểm thử 9:** Kho NVKD Nguyễn Văn Nam có cả 2 mặt hàng PLUS và CACAO $\rightarrow$ **PASS**.
- **Bài kiểm thử 10:** Tồn kho NVKD Nguyễn Văn Nam giảm chính xác sau bán lẻ trực tiếp: Nhận bàn giao 40 hộp PLUS, bán 5 hộp cho khách lẻ $\rightarrow$ Còn lại chính xác **35 hộp** (Giá trị tồn: 7.000.000 đ) $\rightarrow$ **PASS**.
- **Bài kiểm thử 11:** Hệ thống tự động phát hiện và cảnh báo Lô cận date: Lô `LOT-PLUS-NEAR` (HSD: 20/11/2026, còn 36 ngày) được gắn nhãn `CẬN DATE (Còn 36 ngày)` mức cảnh báo `warning` màu vàng $\rightarrow$ **PASS**.
- **Bài kiểm thử 12:** Bàn giao hàng sang kho nhân viên thực hiện bằng `Material Transfer` nội bộ, **xác nhận không tạo doanh thu, không phát sinh công nợ** $\rightarrow$ **PASS**.

### 2.3. Kiểm thử Bán hàng Đa Kênh & Chống trùng đơn sàn (Idempotency)
- **Bài kiểm thử 13:** Kênh **B2B Sỉ** phát sinh doanh thu thực tế: 147.725.000 đ (485 hộp) $\rightarrow$ **PASS**.
- **Bài kiểm thử 14:** Kênh **B2C Trực tiếp** phát sinh doanh thu: 1.825.000 đ (5 hộp) xuất từ Kho NVKD $\rightarrow$ **PASS**.
- **Bài kiểm thử 15:** Kênh **TikTok Shop** phát sinh doanh thu: 6.300.000 đ (20 hộp), khấu trừ phí sàn 504.000 đ và phí vận chuyển 120.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 16:** Kênh **Shopee** phát sinh doanh thu: 10.475.000 đ (35 hộp), khấu trừ phí sàn 942.750 đ và phí vận chuyển 150.000 đ $\rightarrow$ **PASS**.
- **Bài kiểm thử 17:** Kênh **Website** phát sinh doanh thu: 4.245.000 đ (13 hộp) thanh toán chuyển khoản ngân hàng $\rightarrow$ **PASS**.
- **Bài kiểm thử 18:** Import lại đơn sàn đã có (`TIKTOK-20261010-001`): Adapter tự động phát hiện mã đơn đã tồn tại trong database, lập tức từ chối và ghi log `"Duplicate order skipped"`, **chống tạo trùng đơn bán, chống xuất kho đúp và chống ghi nhận thừa doanh thu** $\rightarrow$ **PASS**.

### 2.4. Kiểm thử Đối soát Tiền thu hộ của Nhân viên (Tài khoản 1113)
- **Bài kiểm thử 19:** NVKD Nguyễn Văn Nam bán lẻ đơn 1.825.000 đ (thu tiền mặt), đã làm ủy nhiệm chi nộp 1.500.000 đ về tài khoản ngân hàng công ty `1121`. Số dư nợ còn lại trên tài khoản `1113 - Tiền thu hộ của NVKD - B` là chính xác **325.000 đ** $\rightarrow$ **PASS**.

### 2.5. Kiểm thử Tài chính Quản trị & Báo cáo P&L Đa Chiều
- **Bài kiểm thử 20:** Lợi nhuận gộp tính toán chuẩn xác độc lập:
  $$\text{Doanh thu thuần } (170.570.000 \text{ đ}) - \text{Giá vốn COGS } (94.700.000 \text{ đ}) = \text{Lợi nhuận gộp } (75.870.000 \text{ đ})$$
  Biên lợi nhuận gộp đạt **44,48%** $\rightarrow$ **PASS**.
- **Bài kiểm thử 21:** Lợi nhuận ròng quản trị khớp phương trình độc lập:
  $$\text{Lợi nhuận gộp } (75.870.000) - \text{Phí sàn } (1.446.750) - \text{Phí ship } (270.000) - \text{Ads } (6.000.000) - \text{Lương } (31.000.000) - \text{Thuê kho/VP } (8.000.000) = \mathbf{29.153.250 \text{ đ}}$$
  Tỷ suất lợi nhuận ròng đạt **17,09%** $\rightarrow$ **PASS**.
- **Bài kiểm thử 22:** Báo cáo P&L bóc tách theo Nhãn hàng `PLUS`: Doanh thu 90.520.000 đ, Giá vốn 49.600.000 đ, Lãi gộp 40.920.000 đ (Biên lãi 45,2%) $\rightarrow$ **PASS**.
- **Bài kiểm thử 23:** Báo cáo P&L bóc tách theo Nhãn hàng `CACAO`: Doanh thu 45.050.000 đ, Giá vốn 25.500.000 đ, Lãi gộp 19.550.000 đ (Biên lãi 43,4%) $\rightarrow$ **PASS**.
- **Bài kiểm thử 24:** Báo cáo P&L bóc tách theo Nhãn hàng `TIBOKA`: Doanh thu 35.000.000 đ, Giá vốn 19.600.000 đ, Lãi gộp 15.400.000 đ (Biên lãi 44,0%) $\rightarrow$ **PASS**.
- **Bài kiểm thử 25:** Tổng doanh thu 3 Nhãn hàng khớp chính xác Tổng doanh thu toàn hệ thống ($90.520.000 + 45.050.000 + 35.000.000 = 170.570.000 \text{ đ}$) $\rightarrow$ **PASS**.

### 2.6. Kiểm thử Nhân sự, Chấm công WiFi & Điểm Chuyên Cần
- **Bài kiểm thử 26-30:** Kiểm tra chấm công WiFi hoạt động bình thường, định danh đúng Employee ID cho cả 5 tài khoản chủ chốt (`chutich@baka.vn`, `coo@baka.vn`, `sale1@baka.vn`, `sale2@baka.vn`, `kho@baka.vn`) $\rightarrow$ **PASS**.
- **Bài kiểm thử 31-35:** Kiểm tra Điểm chuyên cần theo năm của từng nhân sự luôn là **số nguyên (integer)**, không có phần thập phân $\rightarrow$ **PASS**.
- **Bài kiểm thử 36-40:** Kiểm tra Điểm chuyên cần từng ngày trên Heatmap không vượt quá **8 điểm/ngày** theo đúng quy định $\rightarrow$ **PASS**.
- **Bài kiểm thử 41:** Tạo và phê duyệt thành công Đơn xin nghỉ phép (`Employee Leave Request`) cho NVKD Nguyễn Văn Nam $\rightarrow$ **PASS**.

---

## 3. Lệnh Tự Động Kiểm Thử Định Kỳ (Regression Command)

Bất kỳ lúc nào, quản trị viên có thể chạy lệnh sau để xác minh tính toàn vẹn hệ thống:
```bash
docker compose exec backend bench --site frontend execute erpnext.setup.health_food_erp_test.run_all_tests
```
