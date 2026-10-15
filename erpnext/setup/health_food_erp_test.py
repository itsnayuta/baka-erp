# Copyright (c) 2026, BAKA and contributors
# Comprehensive Test Suite for Health Food ERP (BAKAERP)
# Covers all 18 criteria required in Section 18 of prompt.md

import frappe
from frappe import _
from frappe.utils import flt, cint, nowdate
from erpnext.setup.health_food_erp_setup import (
    get_managerial_pnl_report,
    get_warehouse_dashboard_data,
    import_marketplace_order,
    COMPANY,
    CENTRAL_WAREHOUSE,
    SALE1_WAREHOUSE,
    SALE2_WAREHOUSE,
    QUARANTINE_WAREHOUSE,
    DAMAGED_WAREHOUSE
)
from erpnext.setup.wifi_attendance import (
    get_attendance_status,
    get_chuyen_can_summary,
    get_chuyen_can_heatmap_data
)

def run_all_tests():
    print("==================================================================")
    print("=== BẮT ĐẦU CHẠY TOÀN BỘ BỘ KIỂM THỬ TỰ ĐỘNG (ERP TEST SUITE) ===")
    print("==================================================================")

    test_results = []

    def record_test(name, passed, detail=""):
        status_str = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} [{status_str}] {name} {f'({detail})' if detail else ''}")
        test_results.append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            raise AssertionError(f"Test Failed: {name} - {detail}")

    # ------------------------------------------------------------------
    # 1. KIỂM THỬ SẢN PHẨM & 3 NHÃN HÀNG
    # ------------------------------------------------------------------
    print("\n--- 1. Kiểm thử Sản phẩm & 3 Nhãn hàng (Brands & Items) ---")
    brands = frappe.db.get_all("Brand", filters={"name": ["in", ["PLUS", "CACAO", "TIBOKA"]]}, pluck="name")
    record_test("Tồn tại đủ 3 Nhãn hàng (PLUS, CACAO, TIBOKA)", len(brands) == 3, f"Found: {brands}")

    items = frappe.db.get_all("Item", filters={"name": ["in", ["TBK-PLUS", "TBK-CACAO", "TBK-TIBOKA"]]}, fields=["name", "brand", "has_batch_no", "has_expiry_date", "stock_uom"])
    record_test("Đủ 3 Sản phẩm cốt lõi", len(items) == 3)
    record_test("Sản phẩm bật quản lý Lô & Hạn sử dụng (FEFO)", all(it.has_batch_no == 1 and it.has_expiry_date == 1 for it in items))
    record_test("Đơn vị tính chuẩn là Hộp", all(it.stock_uom == "Hộp" for it in items))
    record_test("Gán đúng Nhãn hàng cho từng SKU", {it.name: it.brand for it in items} == {"TBK-PLUS": "PLUS", "TBK-CACAO": "CACAO", "TBK-TIBOKA": "TIBOKA"})

    # ------------------------------------------------------------------
    # 2. KIỂM THỬ KHO VẬN & QUẢN LÝ LÔ (FEFO)
    # ------------------------------------------------------------------
    print("\n--- 2. Kiểm thử Kho vận, Lô hàng & Bàn giao Kho Nhân Viên ---")
    wh_data = get_warehouse_dashboard_data()
    record_test("Tổng tồn kho có số liệu thực tế", wh_data["summary"]["total_items_in_stock"] > 0, f"Total: {wh_data['summary']['total_items_in_stock']} hộp")
    record_test("Có tồn kho tại Kho Tổng BAKA", wh_data["summary"]["central_warehouse_qty"] > 0, f"Central: {wh_data['summary']['central_warehouse_qty']} hộp")
    record_test("Có tồn kho tại Kho Nhân Viên Di Động", wh_data["summary"]["employee_warehouses_qty"] > 0, f"Employee stock: {wh_data['summary']['employee_warehouses_qty']} hộp")

    # Kiểm tra tồn kho tại Kho NVKD Nguyễn Văn Nam
    nam_stock = [r for r in wh_data["employee_warehouses"] if r.warehouse == SALE1_WAREHOUSE]
    record_test("Kho NVKD Nguyễn Văn Nam có cả PLUS và CACAO", len(nam_stock) >= 2)
    # Nguyễn Văn Nam ban đầu nhận 40 hộp PLUS, bán 5 hộp -> còn 35 hộp
    nam_plus_qty = sum(r.actual_qty for r in nam_stock if r.item_code == "TBK-PLUS")
    record_test("Tồn kho NVKD Nguyễn Văn Nam giảm chính xác sau bán lẻ (40 - 5 = 35)", nam_plus_qty == 35.0, f"Actual: {nam_plus_qty}")

    # Kiểm tra cảnh báo Lô cận date (< 60 ngày)
    near_batches = wh_data["batches"]["near_expiry"]
    record_test("Hệ thống phát hiện và cảnh báo Lô cận date", len(near_batches) >= 1 and near_batches[0]["batch_id"] == "LOT-PLUS-NEAR", f"Near expiry: {near_batches[0]['batch_id']} ({near_batches[0]['status']})")

    # Kiểm tra việc Bàn giao kho nhân viên không sinh Doanh thu hay Công nợ
    transfers = frappe.db.get_all("Stock Entry", filters={"purpose": "Material Transfer", "docstatus": 1})
    record_test("Bàn giao kho thực hiện bằng Material Transfer nội bộ", len(transfers) >= 2)

    # ------------------------------------------------------------------
    # 3. KIỂM THỬ BÁN HÀNG ĐA KÊNH & ADAPTER SÀN TMĐT
    # ------------------------------------------------------------------
    print("\n--- 3. Kiểm thử Bán hàng Đa Kênh & Chống trùng đơn sàn ---")
    pnl = get_managerial_pnl_report()
    channels = pnl["by_channel"].keys()
    for ch in ["B2B Sỉ", "B2C Trực tiếp", "TikTok Shop", "Shopee", "Website"]:
        record_test(f"Đã phát sinh doanh số trên kênh {ch}", ch in channels, f"Revenue: {pnl['by_channel'].get(ch, {}).get('revenue', 0):,} đ")

    # Kiểm tra cơ chế chống trùng đơn sàn (Idempotency)
    dedup_test = import_marketplace_order(
        channel="TikTok Shop",
        order_id="TIKTOK-20261010-001",
        customer_name="Khách hàng TikTok Shop - Lê Văn Tuấn",
        items=[{"item_code": "TBK-PLUS", "qty": 10, "rate": 365000}],
        platform_fee=504000,
        shipping_fee=120000,
        order_date="2026-10-10"
    )
    record_test("Adapter tự động nhận diện và chặn đơn trùng (Idempotent)", dedup_test.get("status") == "skipped")

    # ------------------------------------------------------------------
    # 4. KIỂM THỬ ĐỐI SOÁT TIỀN THU HỘ CỦA NHÂN VIÊN (1113)
    # ------------------------------------------------------------------
    print("\n--- 4. Kiểm thử Đối soát Tiền Thu Hộ của NVKD ---")
    # Nguyễn Văn Nam bán lẻ đơn 1.825.000 đ, đã nộp 1.500.000 đ -> còn giữ đúng 325.000 đ
    cash_held = wh_data["summary"]["employee_cash_held"]
    record_test("Số dư tiền NVKD đang thu hộ khớp chính xác số sách (325.000 đ)", cash_held == 325000.0, f"Cash held: {cash_held:,} đ")

    # ------------------------------------------------------------------
    # 5. KIỂM THỬ TÀI CHÍNH & BÁO CÁO LÃI LỖ QUẢN TRỊ (P&L)
    # ------------------------------------------------------------------
    print("\n--- 5. Kiểm thử Tài chính Quản trị & Báo cáo P&L Đa Chiều ---")
    summary = pnl["summary"]
    # Kiểm tra phương trình kế toán quản trị:
    # Gross Profit = Revenue - COGS
    expected_gross_profit = summary["gross_revenue"] - summary["cogs"]
    record_test("Lợi nhuận gộp tính toán chuẩn xác (Doanh thu - Giá vốn)", summary["gross_profit"] == expected_gross_profit, f"Gross Profit: {summary['gross_profit']:,} đ")

    # Net Operating Profit = Gross Profit - Platform Fees - Shipping Fees - Ads - Salaries - Rent - Other
    expected_net = summary["gross_profit"] - summary["platform_fees"] - summary["shipping_fees"] - summary["ads_marketing_expense"] - summary["salary_expense"] - summary["rent_expense"] - summary["other_operating_expense"]
    record_test("Lợi nhuận ròng quản trị khớp phương trình độc lập", summary["net_operating_profit"] == expected_net, f"Net Profit: {summary['net_operating_profit']:,} đ (Tỷ suất {summary['net_profit_margin_pct']}%)")

    # Kiểm tra báo cáo theo Nhãn hàng
    pnl_plus = get_managerial_pnl_report(brand="PLUS")
    record_test("Báo cáo P&L lọc chính xác theo Nhãn hàng PLUS", pnl_plus["summary"]["gross_revenue"] == 90520000.0, f"PLUS Revenue: {pnl_plus['summary']['gross_revenue']:,} đ")

    pnl_cacao = get_managerial_pnl_report(brand="CACAO")
    record_test("Báo cáo P&L lọc chính xác theo Nhãn hàng CACAO", pnl_cacao["summary"]["gross_revenue"] == 45050000.0, f"CACAO Revenue: {pnl_cacao['summary']['gross_revenue']:,} đ")

    pnl_tiboka = get_managerial_pnl_report(brand="TIBOKA")
    record_test("Báo cáo P&L lọc chính xác theo Nhãn hàng TIBOKA", pnl_tiboka["summary"]["gross_revenue"] == 35000000.0, f"TIBOKA Revenue: {pnl_tiboka['summary']['gross_revenue']:,} đ")

    total_brand_rev = pnl_plus["summary"]["gross_revenue"] + pnl_cacao["summary"]["gross_revenue"] + pnl_tiboka["summary"]["gross_revenue"]
    record_test("Tổng doanh thu 3 Nhãn hàng khớp chính xác Tổng doanh thu toàn hệ thống", total_brand_rev == summary["gross_revenue"], f"Sum: {total_brand_rev:,} == Total: {summary['gross_revenue']:,}")

    # ------------------------------------------------------------------
    # 6. KIỂM THỬ NHÂN SỰ, CHẤM CÔNG WIFI & ĐIỂM CHUYÊN CẦN
    # ------------------------------------------------------------------
    print("\n--- 6. Kiểm thử Nhân sự, Chấm công WiFi & My Profile ---")
    active_users = ["chutich@baka.vn", "coo@baka.vn", "sale1@baka.vn", "sale2@baka.vn", "kho@baka.vn"]
    for u in active_users:
        status = get_attendance_status(u)
        record_test(f"Chấm công WiFi hoạt động cho {u}", bool(status.get("employee_id")), f"Emp: {status.get('employee_id')}")

        cc = get_chuyen_can_summary(u)
        record_test(f"Điểm chuyên cần của {u} là số nguyên (không thập phân)", isinstance(cc.get("total_points"), int), f"Points: {cc.get('total_points')}")

        hm = get_chuyen_can_heatmap_data(u)
        max_daily = max(hm.values()) if hm else 0
        record_test(f"Điểm chuyên cần ngày của {u} không vượt quá 8 điểm", max_daily <= 8, f"Max daily: {max_daily} pts")

    # Kiểm tra Đơn xin nghỉ phép
    leaves = frappe.db.get_all("Employee Leave Request", filters={"status": "Đã duyệt"})
    record_test("Có đơn xin nghỉ phép hợp lệ được phê duyệt", len(leaves) >= 1, f"Approved leaves: {len(leaves)}")

    print("\n==================================================================")
    print(f"=== KẾT QUẢ: TẤT CẢ {len(test_results)}/ {len(test_results)} BÀI KIỂM THỬ ĐÃ PASS 100% ===")
    print("==================================================================")
    return {"status": "success", "total_tests": len(test_results), "passed": len(test_results)}
