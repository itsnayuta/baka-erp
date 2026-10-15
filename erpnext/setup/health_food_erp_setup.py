# Copyright (c) 2026, BAKA and contributors
# Health Food ERP Setup & Management Engine for BAKAERP
# Brands: PLUS (Premium), CACAO (Flavor), TIBOKA (Mass Market)
# Channels: TikTok Shop, Shopee, B2B Sỉ, B2C Trực tiếp, Website

import frappe
from frappe import _
from frappe.utils import nowdate, add_days, getdate, flt, cint
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

COMPANY = "BAKA"
CENTRAL_WAREHOUSE = "Kho Tổng BAKA - B"
GROUP_EMP_WAREHOUSE = "Kho Nhân Viên - B"
QUARANTINE_WAREHOUSE = "Kho Cách Ly & Đổi Trả - B"
DAMAGED_WAREHOUSE = "Kho Hàng Hỏng & Hết Hạn - B"

SALE1_USER = "sale1@baka.vn"
SALE2_USER = "sale2@baka.vn"
KHO_USER = "kho@baka.vn"
COO_USER = "coo@baka.vn"
CHUTICH_USER = "chutich@baka.vn"

SALE1_WAREHOUSE = "Kho NVKD - Nguyễn Văn Nam - B"
SALE2_WAREHOUSE = "Kho NVKD - Trần Thị Mai - B"

def run():
    print("==================================================================")
    print("=== BẮT ĐẦU NÂNG CẤP ERP PHÂN PHỐI THỰC PHẨM BẢO VỆ SỨC KHỎE ===")
    print("==================================================================")

    # 1. Custom Fields cho phân hệ Bán hàng đa kênh, Lô & Kho
    setup_custom_fields()

    # 2. Cấu hình 3 Nhãn hàng & Thuộc tính sản phẩm Lô / FEFO
    setup_brands_and_items()

    # 3. Cấu hình Cây kho (Kho Tổng, Kho NVKD, Kho Cách Ly, Kho Hàng Hỏng)
    setup_warehouses()

    # 4. Cấu hình Tài khoản kế toán bổ sung & Cây Cost Center quản trị
    setup_accounts_and_cost_centers()

    # 5. Nhập kho ban đầu theo từng Lô & Hạn sử dụng (FEFO)
    setup_initial_stock_and_batches()

    # 6. Bàn giao hàng sang Kho Nhân Viên (Material Transfer - Không tạo DT)
    setup_handover_to_employee_warehouses()

    # 7. Mô phỏng Bán hàng Đa Kênh (B2B sỉ, B2C lẻ, TikTok Shop, Shopee, Web)
    setup_multichannel_sales()

    # 8. Xử lý Đổi trả hàng, Cách ly & Xuất hủy hàng hỏng
    setup_returns_and_quarantine()

    # 9. Ghi nhận Chi phí Vận hành, Quảng cáo Ads, Lương & Đối soát Tiền thu hộ
    setup_expenses_and_reconciliation()

    # 10. Hoàn thiện Nhân sự: Nghỉ phép & Đánh giá KPI
    setup_hr_and_kpi()

    frappe.db.commit()
    print("==================================================================")
    print("=== HOÀN TẤT NÂNG CẤP HỆ THỐNG ERP BAKA - SẴN SÀNG VẬN HÀNH ===")
    print("==================================================================")


# ----------------------------------------------------------------------
# 1. SETUP CUSTOM FIELDS
# ----------------------------------------------------------------------
def setup_custom_fields():
    print("\n[Phase 1.1] Kiểm tra và thiết lập Custom Fields...")
    custom_fields = {
        "Sales Order": [
            {
                "fieldname": "custom_sales_channel",
                "label": "Kênh bán hàng",
                "fieldtype": "Select",
                "options": "B2B Sỉ\nB2C Trực tiếp\nTikTok Shop\nShopee\nWebsite",
                "insert_after": "customer",
                "in_list_view": 1,
                "in_standard_filter": 1
            },
            {
                "fieldname": "custom_marketplace_order_id",
                "label": "Mã đơn hàng sàn TMĐT",
                "fieldtype": "Data",
                "insert_after": "custom_sales_channel",
                "unique": 0,
                "in_list_view": 1
            },
            {
                "fieldname": "custom_platform_fee",
                "label": "Phí sàn TMĐT (VND)",
                "fieldtype": "Currency",
                "insert_after": "base_grand_total"
            },
            {
                "fieldname": "custom_shipping_fee",
                "label": "Phí vận chuyển người bán chịu (VND)",
                "fieldtype": "Currency",
                "insert_after": "custom_platform_fee"
            },
            {
                "fieldname": "custom_sales_person",
                "label": "Nhân viên phụ trách",
                "fieldtype": "Link",
                "options": "User",
                "insert_after": "custom_shipping_fee"
            }
        ],
        "Sales Invoice": [
            {
                "fieldname": "custom_sales_channel",
                "label": "Kênh bán hàng",
                "fieldtype": "Select",
                "options": "B2B Sỉ\nB2C Trực tiếp\nTikTok Shop\nShopee\nWebsite",
                "insert_after": "customer",
                "in_list_view": 1,
                "in_standard_filter": 1
            },
            {
                "fieldname": "custom_marketplace_order_id",
                "label": "Mã đơn hàng sàn TMĐT",
                "fieldtype": "Data",
                "insert_after": "custom_sales_channel"
            },
            {
                "fieldname": "custom_platform_fee",
                "label": "Phí sàn TMĐT (VND)",
                "fieldtype": "Currency",
                "insert_after": "base_grand_total"
            },
            {
                "fieldname": "custom_shipping_fee",
                "label": "Phí vận chuyển người bán chịu (VND)",
                "fieldtype": "Currency",
                "insert_after": "custom_platform_fee"
            },
            {
                "fieldname": "custom_sales_person",
                "label": "Nhân viên phụ trách",
                "fieldtype": "Link",
                "options": "User",
                "insert_after": "custom_shipping_fee"
            }
        ],
        "Delivery Note": [
            {
                "fieldname": "custom_sales_channel",
                "label": "Kênh bán hàng",
                "fieldtype": "Select",
                "options": "B2B Sỉ\nB2C Trực tiếp\nTikTok Shop\nShopee\nWebsite",
                "insert_after": "customer",
                "in_list_view": 1
            },
            {
                "fieldname": "custom_marketplace_order_id",
                "label": "Mã đơn hàng sàn TMĐT",
                "fieldtype": "Data",
                "insert_after": "custom_sales_channel"
            }
        ],
        "Customer": [
            {
                "fieldname": "custom_credit_limit",
                "label": "Hạn mức công nợ (VND)",
                "fieldtype": "Currency",
                "insert_after": "customer_group"
            },
            {
                "fieldname": "custom_payment_terms_days",
                "label": "Thời hạn thanh toán (Số ngày)",
                "fieldtype": "Int",
                "insert_after": "custom_credit_limit"
            },
            {
                "fieldname": "custom_sales_person",
                "label": "Nhân viên phụ trách",
                "fieldtype": "Link",
                "options": "User",
                "insert_after": "custom_payment_terms_days"
            }
        ],
        "Warehouse": [
            {
                "fieldname": "custom_warehouse_type",
                "label": "Phân loại kho",
                "fieldtype": "Select",
                "options": "Central\nEmployee\nQuarantine\nDamaged\nStores",
                "insert_after": "warehouse_name"
            },
            {
                "fieldname": "custom_employee",
                "label": "Nhân viên sở hữu kho",
                "fieldtype": "Link",
                "options": "Employee",
                "insert_after": "custom_warehouse_type"
            }
        ],
        "Item": [
            {
                "fieldname": "custom_product_line",
                "label": "Dòng sản phẩm",
                "fieldtype": "Select",
                "options": "PLUS\nCACAO\nTIBOKA",
                "insert_after": "brand",
                "in_list_view": 1,
                "in_standard_filter": 1
            }
        ],
        "Sales Order Item": [
            {
                "fieldname": "custom_product_line",
                "label": "Dòng sản phẩm",
                "fieldtype": "Data",
                "insert_after": "item_code",
                "fetch_from": "item_code.custom_product_line"
            }
        ],
        "Sales Invoice Item": [
            {
                "fieldname": "custom_product_line",
                "label": "Dòng sản phẩm",
                "fieldtype": "Data",
                "insert_after": "item_code",
                "fetch_from": "item_code.custom_product_line"
            }
        ],
        "Delivery Note Item": [
            {
                "fieldname": "custom_product_line",
                "label": "Dòng sản phẩm",
                "fieldtype": "Data",
                "insert_after": "item_code",
                "fetch_from": "item_code.custom_product_line"
            }
        ]
    }
    create_custom_fields(custom_fields)
    print("✓ Đã khởi tạo các Custom Fields hoàn chỉnh.")


# ----------------------------------------------------------------------
# 2. SETUP BRANDS & ITEMS (FEFO & BATCH SETTINGS)
# ----------------------------------------------------------------------
def setup_brands_and_items():
    print("\n[Phase 1.2] Cấu hình Thương hiệu duy nhất BAKA & 3 Dòng sản phẩm (PLUS, CACAO, TIBOKA)...")

    # 1. Thương hiệu duy nhất: BAKA
    if not frappe.db.exists("Brand", "BAKA"):
        doc = frappe.get_doc({
            "doctype": "Brand",
            "brand": "BAKA",
            "description": "Thương hiệu Thực phẩm Bảo vệ Sức khỏe & Tinh bột Kháng BAKA (Duy nhất)"
        })
        doc.insert(ignore_permissions=True)
        print("✓ Đã tạo Thương hiệu duy nhất: BAKA")
    else:
        frappe.db.set_value("Brand", "BAKA", "description", "Thương hiệu Thực phẩm Bảo vệ Sức khỏe & Tinh bột Kháng BAKA (Duy nhất)")

    # 2. Cấu trúc Cây nhóm hàng / Dòng sản phẩm (Product Lines) thuộc BAKA
    if not frappe.db.exists("Item Group", "Sản phẩm BAKA"):
        frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": "Sản phẩm BAKA",
            "parent_item_group": "All Item Groups",
            "is_group": 1
        }).insert(ignore_permissions=True)

    product_lines = [
        {"name": "Dòng PLUS", "line": "PLUS", "desc": "Dòng tinh bột kháng cao cấp tăng cường lợi khuẩn và đề kháng chuyên sâu."},
        {"name": "Dòng CACAO", "line": "CACAO", "desc": "Dòng tinh bột kháng thơm ngon hương vị ca cao tự nhiên."},
        {"name": "Dòng TIBOKA", "line": "TIBOKA", "desc": "Dòng tinh bột kháng dinh dưỡng đại trà, bổ sung chất xơ hòa tan."}
    ]

    for pl in product_lines:
        if not frappe.db.exists("Item Group", pl["name"]):
            frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": pl["name"],
                "parent_item_group": "Sản phẩm BAKA",
                "is_group": 0
            }).insert(ignore_permissions=True)
            print(f"✓ Đã tạo Nhóm Dòng sản phẩm: {pl['name']}")

    # Cấu hình Stock Settings: Bắt buộc không cho phép tồn kho âm
    stock_settings = frappe.get_single("Stock Settings")
    stock_settings.allow_negative_stock = 0
    stock_settings.use_serial_batch_fields = 1
    stock_settings.auto_create_serial_and_batch_bundle_for_outward = 1
    stock_settings.save(ignore_permissions=True)

    # Đảm bảo Đơn vị tính: Hộp
    if not frappe.db.exists("UOM", "Hộp"):
        frappe.get_doc({
            "doctype": "UOM",
            "uom_name": "Hộp",
            "must_be_whole_number": 1
        }).insert(ignore_permissions=True)

    # 3. Danh mục 3 SKU cốt lõi: Thương hiệu BAKA - Dòng PLUS, CACAO, TIBOKA
    items_data = [
        {
            "item_code": "TBK-PLUS",
            "item_name": "Tinh bột kháng BAKA PLUS",
            "brand": "BAKA",
            "custom_product_line": "PLUS",
            "item_group": "Dòng PLUS",
            "standard_rate": 365000,
            "valuation_rate": 200000,
            "description": "Tinh bột kháng BAKA PLUS - Dòng cao cấp tăng cường lợi khuẩn và đề kháng chuyên sâu (365.000 đ/hộp)."
        },
        {
            "item_code": "TBK-CACAO",
            "item_name": "Tinh bột kháng BAKA CACAO",
            "brand": "BAKA",
            "custom_product_line": "CACAO",
            "item_group": "Dòng CACAO",
            "standard_rate": 265000,
            "valuation_rate": 150000,
            "description": "Tinh bột kháng BAKA CACAO - Dòng hương vị thơm ngon giàu chất xơ (265.000 đ/hộp)."
        },
        {
            "item_code": "TBK-TIBOKA",
            "item_name": "Tinh bột kháng BAKA TIBOKA",
            "brand": "BAKA",
            "custom_product_line": "TIBOKA",
            "item_group": "Dòng TIBOKA",
            "standard_rate": 250000,
            "valuation_rate": 140000,
            "description": "Tinh bột kháng BAKA TIBOKA - Dòng tiêu chuẩn đại trà cho mọi gia đình (250.000 đ/hộp)."
        }
    ]

    for it in items_data:
        code = it["item_code"]
        if not frappe.db.exists("Item", code):
            doc = frappe.get_doc({
                "doctype": "Item",
                "item_code": code,
                "item_name": it["item_name"],
                "item_group": it["item_group"],
                "brand": it["brand"],
                "custom_product_line": it["custom_product_line"],
                "stock_uom": "Hộp",
                "is_stock_item": 1,
                "is_sales_item": 1,
                "is_purchase_item": 1,
                "has_batch_no": 1,
                "create_new_batch": 1,
                "has_expiry_date": 1,
                "shelf_life_in_days": 730,
                "standard_rate": it["standard_rate"],
                "valuation_rate": it["valuation_rate"],
                "description": it["description"]
            })
            doc.insert(ignore_permissions=True)
        else:
            frappe.db.set_value("Item", code, {
                "item_name": it["item_name"],
                "brand": it["brand"],
                "custom_product_line": it["custom_product_line"],
                "item_group": it["item_group"],
                "has_batch_no": 1,
                "create_new_batch": 1,
                "has_expiry_date": 1,
                "shelf_life_in_days": 730,
                "standard_rate": it["standard_rate"],
                "valuation_rate": it["valuation_rate"],
                "description": it["description"]
            })

        # Cập nhật Bảng giá Standard Selling (VND)
        ip = frappe.db.get_value("Item Price", {"item_code": code, "price_list": "Standard Selling"}, "name")
        if not ip:
            frappe.get_doc({
                "doctype": "Item Price",
                "item_code": code,
                "price_list": "Standard Selling",
                "price_list_rate": it["standard_rate"],
                "currency": "VND"
            }).insert(ignore_permissions=True)
        else:
            frappe.db.set_value("Item Price", ip, {"price_list_rate": it["standard_rate"], "currency": "VND"})

        print(f"✓ Đã cấu hình Sản phẩm: {code} - Thương hiệu: {it['brand']} - Dòng: {it['custom_product_line']} - Quản lý Lô & Date (FEFO) - Giá: {it['standard_rate']:,} VND")

    # Chuẩn hóa dữ liệu lịch sử về Thương hiệu duy nhất BAKA và phân định Dòng sản phẩm
    frappe.db.sql("UPDATE `tabItem` SET brand='BAKA', custom_product_line='PLUS' WHERE name='TBK-PLUS'")
    frappe.db.sql("UPDATE `tabItem` SET brand='BAKA', custom_product_line='CACAO' WHERE name='TBK-CACAO'")
    frappe.db.sql("UPDATE `tabItem` SET brand='BAKA', custom_product_line='TIBOKA' WHERE name='TBK-TIBOKA'")

    frappe.db.sql("UPDATE `tabSales Order Item` SET brand='BAKA', custom_product_line='PLUS' WHERE item_code='TBK-PLUS'")
    frappe.db.sql("UPDATE `tabSales Order Item` SET brand='BAKA', custom_product_line='CACAO' WHERE item_code='TBK-CACAO'")
    frappe.db.sql("UPDATE `tabSales Order Item` SET brand='BAKA', custom_product_line='TIBOKA' WHERE item_code='TBK-TIBOKA'")

    frappe.db.sql("UPDATE `tabSales Invoice Item` SET brand='BAKA', custom_product_line='PLUS' WHERE item_code='TBK-PLUS'")
    frappe.db.sql("UPDATE `tabSales Invoice Item` SET brand='BAKA', custom_product_line='CACAO' WHERE item_code='TBK-CACAO'")
    frappe.db.sql("UPDATE `tabSales Invoice Item` SET brand='BAKA', custom_product_line='TIBOKA' WHERE item_code='TBK-TIBOKA'")

    frappe.db.sql("UPDATE `tabDelivery Note Item` SET brand='BAKA', custom_product_line='PLUS' WHERE item_code='TBK-PLUS'")
    frappe.db.sql("UPDATE `tabDelivery Note Item` SET brand='BAKA', custom_product_line='CACAO' WHERE item_code='TBK-CACAO'")
    frappe.db.sql("UPDATE `tabDelivery Note Item` SET brand='BAKA', custom_product_line='TIBOKA' WHERE item_code='TBK-TIBOKA'")


# ----------------------------------------------------------------------
# 3. SETUP WAREHOUSES
# ----------------------------------------------------------------------
def setup_warehouses():
    print("\n[Phase 2.1] Thiết lập Cây Kho hoàn chỉnh (Kho Tổng, Kho NVKD, Cách ly, Hàng hỏng)...")

    # 1. Kho Tổng BAKA
    if not frappe.db.exists("Warehouse", CENTRAL_WAREHOUSE):
        frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": "Kho Tổng BAKA",
            "parent_warehouse": "All Warehouses - B",
            "company": COMPANY,
            "custom_warehouse_type": "Central"
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Kho Tổng: {CENTRAL_WAREHOUSE}")

    # 2. Nhóm Kho Nhân Viên
    if not frappe.db.exists("Warehouse", GROUP_EMP_WAREHOUSE):
        frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": "Kho Nhân Viên",
            "parent_warehouse": "All Warehouses - B",
            "is_group": 1,
            "company": COMPANY
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Nhóm kho: {GROUP_EMP_WAREHOUSE}")

    # 3. Kho di động cho từng NVKD
    emp_nam = frappe.db.get_value("Employee", {"user_id": SALE1_USER}, "name")
    emp_mai = frappe.db.get_value("Employee", {"user_id": SALE2_USER}, "name")

    if not frappe.db.exists("Warehouse", SALE1_WAREHOUSE):
        frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": "Kho NVKD - Nguyễn Văn Nam",
            "parent_warehouse": GROUP_EMP_WAREHOUSE,
            "company": COMPANY,
            "custom_warehouse_type": "Employee",
            "custom_employee": emp_nam
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Kho di động: {SALE1_WAREHOUSE} (gán cho {SALE1_USER})")

    if not frappe.db.exists("Warehouse", SALE2_WAREHOUSE):
        frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": "Kho NVKD - Trần Thị Mai",
            "parent_warehouse": GROUP_EMP_WAREHOUSE,
            "company": COMPANY,
            "custom_warehouse_type": "Employee",
            "custom_employee": emp_mai
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Kho di động: {SALE2_WAREHOUSE} (gán cho {SALE2_USER})")

    # 4. Kho Cách Ly & Đổi Trả
    if not frappe.db.exists("Warehouse", QUARANTINE_WAREHOUSE):
        frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": "Kho Cách Ly & Đổi Trả",
            "parent_warehouse": "All Warehouses - B",
            "company": COMPANY,
            "custom_warehouse_type": "Quarantine"
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Kho Cách Ly: {QUARANTINE_WAREHOUSE}")

    # 5. Kho Hàng Hỏng & Hết Hạn
    if not frappe.db.exists("Warehouse", DAMAGED_WAREHOUSE):
        frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": "Kho Hàng Hỏng & Hết Hạn",
            "parent_warehouse": "All Warehouses - B",
            "company": COMPANY,
            "custom_warehouse_type": "Damaged"
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Kho Hàng Hỏng: {DAMAGED_WAREHOUSE}")


# ----------------------------------------------------------------------
# 4. SETUP ACCOUNTS & COST CENTERS
# ----------------------------------------------------------------------
def setup_accounts_and_cost_centers():
    print("\n[Phase 4.1] Cấu hình Tài khoản Kế toán bổ sung & Cây Cost Center quản trị...")

    # 1. Tài khoản bổ sung
    # 1.1. 1113: Tiền thu hộ của NVKD (Dưới 111 - Tiền mặt, Account Type: Cash)
    parent_111 = "111 - Tiền mặt - B"
    acc_1113 = "1113 - Tiền thu hộ của NVKD - B"
    if not frappe.db.exists("Account", acc_1113):
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "1113 - Tiền thu hộ của NVKD",
            "parent_account": parent_111,
            "company": COMPANY,
            "account_type": "Cash",
            "root_type": "Asset"
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Tài khoản: {acc_1113}")

    # 1.2. 6413: Phí sàn thương mại điện tử (Dưới 641 - Chi phí bán hàng)
    parent_641 = "641 - Chi phí bán hàng - B"
    acc_6413 = "6413 - Phí sàn thương mại điện tử - B"
    if not frappe.db.exists("Account", acc_6413):
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "6413 - Phí sàn thương mại điện tử",
            "parent_account": parent_641,
            "company": COMPANY,
            "account_type": "Expense Account",
            "root_type": "Expense"
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Tài khoản: {acc_6413}")

    # 1.3. 6414: Chi phí quảng cáo, tiếp thị (Dưới 641)
    acc_6414 = "6414 - Chi phí quảng cáo, tiếp thị - B"
    if not frappe.db.exists("Account", acc_6414):
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "6414 - Chi phí quảng cáo, tiếp thị",
            "parent_account": parent_641,
            "company": COMPANY,
            "account_type": "Expense Account",
            "root_type": "Expense"
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Tài khoản: {acc_6414}")

    # 1.4. 6426: Chi phí thuê văn phòng, kho bãi (Dưới 642 - Chi phí quản lý doanh nghiệp)
    parent_642 = "642 - Chi phí quản lý doanh nghiệp - B"
    acc_6426 = "6426 - Chi phí thuê văn phòng, kho bãi - B"
    if not frappe.db.exists("Account", acc_6426):
        frappe.get_doc({
            "doctype": "Account",
            "account_name": "6426 - Chi phí thuê văn phòng, kho bãi",
            "parent_account": parent_642,
            "company": COMPANY,
            "account_type": "Expense Account",
            "root_type": "Expense"
        }).insert(ignore_permissions=True)
        print(f"✓ Đã tạo Tài khoản: {acc_6426}")

    # 2. Cây Cost Center Quản Trị
    # Nhóm Cost Center Kênh Bán Hàng
    cc_channels_parent = "Kênh Bán Hàng - B"
    if not frappe.db.exists("Cost Center", cc_channels_parent):
        frappe.get_doc({
            "doctype": "Cost Center",
            "cost_center_name": "Kênh Bán Hàng",
            "parent_cost_center": "BAKA - B",
            "is_group": 1,
            "company": COMPANY
        }).insert(ignore_permissions=True)

    channels_cc = [
        "Kênh TikTok Shop", "Kênh Shopee", "Kênh B2B Sỉ", "Kênh B2C Trực tiếp", "Kênh Website"
    ]
    for c_name in channels_cc:
        full_cc = f"{c_name} - B"
        if not frappe.db.exists("Cost Center", full_cc):
            frappe.get_doc({
                "doctype": "Cost Center",
                "cost_center_name": c_name,
                "parent_cost_center": cc_channels_parent,
                "is_group": 0,
                "company": COMPANY
            }).insert(ignore_permissions=True)

    # Nhóm Cost Center Nhãn Hàng
    cc_brands_parent = "Nhãn Hàng - B"
    if not frappe.db.exists("Cost Center", cc_brands_parent):
        frappe.get_doc({
            "doctype": "Cost Center",
            "cost_center_name": "Nhãn Hàng",
            "parent_cost_center": "BAKA - B",
            "is_group": 1,
            "company": COMPANY
        }).insert(ignore_permissions=True)

    brands_cc = ["Nhãn hàng PLUS", "Nhãn hàng CACAO", "Nhãn hàng TIBOKA"]
    for b_name in brands_cc:
        full_cc = f"{b_name} - B"
        if not frappe.db.exists("Cost Center", full_cc):
            frappe.get_doc({
                "doctype": "Cost Center",
                "cost_center_name": b_name,
                "parent_cost_center": cc_brands_parent,
                "is_group": 0,
                "company": COMPANY
            }).insert(ignore_permissions=True)

    # Nhóm Vận Hành Chung
    cc_ops_parent = "Khối Vận Hành & Quản Lý - B"
    if not frappe.db.exists("Cost Center", cc_ops_parent):
        frappe.get_doc({
            "doctype": "Cost Center",
            "cost_center_name": "Khối Vận Hành & Quản Lý",
            "parent_cost_center": "BAKA - B",
            "is_group": 0,
            "company": COMPANY
        }).insert(ignore_permissions=True)

    print("✓ Đã cấu hình hoàn tất Cây Cost Center quản trị theo Kênh và Nhãn hàng.")


# ----------------------------------------------------------------------
# 5. INITIAL STOCK & BATCHES (FEFO ENGINE)
# ----------------------------------------------------------------------
def setup_initial_stock_and_batches():
    print("\n[Phase 2.2] Khởi tạo các Lô hàng (Batches) và Nhập kho ban đầu (FEFO)...")

    batches = [
        # PLUS
        {"batch_id": "LOT-PLUS-202606", "item": "TBK-PLUS", "mfg": "2026-06-01", "exp": "2027-06-30", "qty": 300, "rate": 200000},
        {"batch_id": "LOT-PLUS-202610", "item": "TBK-PLUS", "mfg": "2026-10-01", "exp": "2028-10-31", "qty": 400, "rate": 200000},
        {"batch_id": "LOT-PLUS-NEAR",   "item": "TBK-PLUS", "mfg": "2025-11-01", "exp": "2026-11-20", "qty": 30,  "rate": 200000}, # Cận date < 60 ngày

        # CACAO
        {"batch_id": "LOT-CACAO-202606", "item": "TBK-CACAO", "mfg": "2026-06-01", "exp": "2027-06-30", "qty": 300, "rate": 150000},
        {"batch_id": "LOT-CACAO-202610", "item": "TBK-CACAO", "mfg": "2026-10-01", "exp": "2028-10-31", "qty": 400, "rate": 150000},

        # TIBOKA
        {"batch_id": "LOT-TIBOKA-202606", "item": "TBK-TIBOKA", "mfg": "2026-06-01", "exp": "2027-06-30", "qty": 350, "rate": 140000},
        {"batch_id": "LOT-TIBOKA-202610", "item": "TBK-TIBOKA", "mfg": "2026-10-01", "exp": "2028-10-31", "qty": 450, "rate": 140000},
    ]

    for b in batches:
        b_id = b["batch_id"]
        if not frappe.db.exists("Batch", b_id):
            frappe.get_doc({
                "doctype": "Batch",
                "batch_id": b_id,
                "item": b["item"],
                "manufacturing_date": b["mfg"],
                "expiry_date": b["exp"],
                "description": f"Lô {b_id} (HSD: {b['exp']})"
            }).insert(ignore_permissions=True)
            print(f"  + Tạo Lô hàng: {b_id} - Item: {b['item']} - HSD: {b['exp']}")
        else:
            frappe.db.set_value("Batch", b_id, {
                "manufacturing_date": b["mfg"],
                "expiry_date": b["exp"]
            })

    # Kiểm tra xem đã có Stock Entry nhập ban đầu vào Kho Tổng chưa
    has_receipt = frappe.db.exists("Stock Entry", {"to_warehouse": CENTRAL_WAREHOUSE, "purpose": "Material Receipt", "docstatus": 1})
    if not has_receipt:
        se = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "purpose": "Material Receipt",
            "company": COMPANY,
            "set_posting_time": 1,
            "posting_date": "2026-10-01",
            "posting_time": "07:30:00",
            "to_warehouse": CENTRAL_WAREHOUSE,
            "owner": KHO_USER,
            "remarks": "Nhập kho thành phẩm ban đầu theo từng Lô & Hạn sử dụng (FEFO)",
            "items": [
                {
                    "item_code": b["item"],
                    "qty": b["qty"],
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "conversion_factor": 1.0,
                    "basic_rate": b["rate"],
                    "t_warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": b["batch_id"],
                    "use_serial_batch_fields": 1,
                    "cost_center": "Main - B"
                }
                for b in batches
            ]
        })
        se.insert(ignore_permissions=True)
        se.submit()
        print(f"✓ Đã nhập kho thành phẩm ban đầu {sum(b['qty'] for b in batches):,} hộp vào '{CENTRAL_WAREHOUSE}' theo từng Lô chuẩn.")
    else:
        print(f"✓ Kho Tổng '{CENTRAL_WAREHOUSE}' đã có dữ liệu nhập kho ban đầu.")


# ----------------------------------------------------------------------
# 6. HANDOVER TO EMPLOYEE WAREHOUSES (NO REVENUE)
# ----------------------------------------------------------------------
def setup_handover_to_employee_warehouses():
    print("\n[Phase 2.3] Bàn giao hàng sang Kho Nhân Viên (Material Transfer - Không sinh doanh thu)...")

    # Bàn giao đợt 1 ngày 02/10/2026
    # 1. Bàn giao cho Sale 1 (Nguyễn Văn Nam): 40 hộp TBK-PLUS (Lô LOT-PLUS-202606), 30 hộp TBK-CACAO (LOT-CACAO-202606)
    has_transfer_nam = frappe.db.exists("Stock Entry", {
        "from_warehouse": CENTRAL_WAREHOUSE,
        "to_warehouse": SALE1_WAREHOUSE,
        "purpose": "Material Transfer",
        "docstatus": 1
    })
    if not has_transfer_nam:
        se_nam = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Transfer",
            "purpose": "Material Transfer",
            "company": COMPANY,
            "set_posting_time": 1,
            "posting_date": "2026-10-02",
            "posting_time": "08:15:00",
            "from_warehouse": CENTRAL_WAREHOUSE,
            "to_warehouse": SALE1_WAREHOUSE,
            "owner": KHO_USER,
            "remarks": "Bàn giao hàng mẫu và lưu kho di động cho NVKD Nguyễn Văn Nam - KHÔNG SINH DOANH THU",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 40,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "s_warehouse": CENTRAL_WAREHOUSE,
                    "t_warehouse": SALE1_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "basic_rate": 200000,
                    "cost_center": "Main - B"
                },
                {
                    "item_code": "TBK-CACAO",
                    "qty": 30,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "s_warehouse": CENTRAL_WAREHOUSE,
                    "t_warehouse": SALE1_WAREHOUSE,
                    "batch_no": "LOT-CACAO-202606",
                    "use_serial_batch_fields": 1,
                    "basic_rate": 150000,
                    "cost_center": "Main - B"
                }
            ]
        })
        se_nam.insert(ignore_permissions=True)
        se_nam.submit()
        print(f"✓ Bàn giao thành công: 40 TBK-PLUS, 30 TBK-CACAO sang '{SALE1_WAREHOUSE}' (Material Transfer).")

    # 2. Bàn giao cho Sale 2 (Trần Thị Mai): 40 hộp TBK-PLUS (Lô LOT-PLUS-202606), 30 hộp TBK-TIBOKA (LOT-TIBOKA-202606)
    has_transfer_mai = frappe.db.exists("Stock Entry", {
        "from_warehouse": CENTRAL_WAREHOUSE,
        "to_warehouse": SALE2_WAREHOUSE,
        "purpose": "Material Transfer",
        "docstatus": 1
    })
    if not has_transfer_mai:
        se_mai = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Transfer",
            "purpose": "Material Transfer",
            "company": COMPANY,
            "set_posting_time": 1,
            "posting_date": "2026-10-02",
            "posting_time": "08:30:00",
            "from_warehouse": CENTRAL_WAREHOUSE,
            "to_warehouse": SALE2_WAREHOUSE,
            "owner": KHO_USER,
            "remarks": "Bàn giao hàng lưu kho di động cho NVKD Trần Thị Mai - KHÔNG SINH DOANH THU",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 40,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "s_warehouse": CENTRAL_WAREHOUSE,
                    "t_warehouse": SALE2_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "basic_rate": 200000,
                    "cost_center": "Main - B"
                },
                {
                    "item_code": "TBK-TIBOKA",
                    "qty": 30,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "s_warehouse": CENTRAL_WAREHOUSE,
                    "t_warehouse": SALE2_WAREHOUSE,
                    "batch_no": "LOT-TIBOKA-202606",
                    "use_serial_batch_fields": 1,
                    "basic_rate": 140000,
                    "cost_center": "Main - B"
                }
            ]
        })
        se_mai.insert(ignore_permissions=True)
        se_mai.submit()
        print(f"✓ Bàn giao thành công: 40 TBK-PLUS, 30 TBK-TIBOKA sang '{SALE2_WAREHOUSE}' (Material Transfer).")


# ----------------------------------------------------------------------
# 7. MULTI-CHANNEL SALES & CRM
# ----------------------------------------------------------------------
def setup_multichannel_sales():
    print("\n[Phase 3] Thiết lập các luồng Bán hàng Đa Kênh (5 Kênh chuẩn)...")

    # Tạo các khách hàng đại diện cho từng kênh nếu chưa có
    customers_data = [
        {"customer_name": "Đại lý Dinh Dưỡng Xanh (Hà Nội)", "customer_group": "Đại lý", "credit_limit": 60000000, "days": 30, "sale": SALE1_USER},
        {"customer_name": "Chuỗi Thực Phẩm Sạch Healthy Mart (TP.HCM)", "customer_group": "Đại lý", "credit_limit": 100000000, "days": 30, "sale": SALE2_USER},
        {"customer_name": "Nhà Thuốc & Dược Phẩm An Tâm (Đà Nẵng)", "customer_group": "Đại lý", "credit_limit": 50000000, "days": 15, "sale": SALE1_USER},
        {"customer_name": "Chị Nguyễn Thị Lan (Khách hàng cuối)", "customer_group": "Khách hàng cuối", "credit_limit": 0, "days": 0, "sale": SALE1_USER},
        {"customer_name": "Khách hàng TikTok Shop - Lê Văn Tuấn", "customer_group": "Khách hàng cuối", "credit_limit": 0, "days": 0, "sale": None},
        {"customer_name": "Khách hàng Shopee - Trần Văn Hưng", "customer_group": "Khách hàng cuối", "credit_limit": 0, "days": 0, "sale": None},
        {"customer_name": "Khách hàng Website - Phạm Minh Trí", "customer_group": "Khách hàng cuối", "credit_limit": 0, "days": 0, "sale": None}
    ]

    for c in customers_data:
        c_name = c["customer_name"]
        if not frappe.db.exists("Customer", c_name):
            cust = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": c_name,
                "customer_group": c["customer_group"],
                "customer_type": "Company" if "Đại lý" in c["customer_group"] or "Chuỗi" in c_name else "Individual",
                "territory": "Vietnam",
                "company": COMPANY,
                "custom_credit_limit": c["credit_limit"],
                "custom_payment_terms_days": c["days"],
                "custom_sales_person": c["sale"]
            })
            cust.insert(ignore_permissions=True)
        else:
            frappe.db.set_value("Customer", c_name, {
                "custom_credit_limit": c["credit_limit"],
                "custom_payment_terms_days": c["days"],
                "custom_sales_person": c["sale"]
            })

    # ------------------------------------------------------------------
    # KÊNH 1: B2B SỈ (Đại lý Dinh Dưỡng Xanh & Healthy Mart)
    # Xuất từ Kho Tổng BAKA, tuân thủ Lô FEFO, hỗ trợ thu tiền từng phần
    # ------------------------------------------------------------------
    order_b2b_ref = "SO-B2B-DDX-001"
    if not frappe.db.exists("Sales Order", {"custom_marketplace_order_id": order_b2b_ref}):
        so_b2b = frappe.get_doc({
            "doctype": "Sales Order",
            "company": COMPANY,
            "customer": "Đại lý Dinh Dưỡng Xanh (Hà Nội)",
            "transaction_date": "2026-10-04",
            "delivery_date": "2026-10-06",
            "order_type": "Sales",
            "currency": "VND",
            "selling_price_list": "Standard Selling",
            "owner": SALE1_USER,
            "custom_sales_channel": "B2B Sỉ",
            "custom_marketplace_order_id": order_b2b_ref,
            "custom_sales_person": SALE1_USER,
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 50,
                    "rate": 365000,
                    "delivery_date": "2026-10-06",
                    "warehouse": CENTRAL_WAREHOUSE
                },
                {
                    "item_code": "TBK-CACAO",
                    "qty": 40,
                    "rate": 265000,
                    "delivery_date": "2026-10-06",
                    "warehouse": CENTRAL_WAREHOUSE
                }
            ]
        })
        so_b2b.insert(ignore_permissions=True)
        so_b2b.submit()

        # Xuất kho giao hàng (Delivery Note) theo Lô FEFO
        dn_b2b = frappe.get_doc({
            "doctype": "Delivery Note",
            "company": COMPANY,
            "customer": so_b2b.customer,
            "posting_date": "2026-10-05",
            "posting_time": "09:30:00",
            "owner": KHO_USER,
            "custom_sales_channel": "B2B Sỉ",
            "custom_marketplace_order_id": order_b2b_ref,
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 50,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "rate": 365000,
                    "warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606", # FEFO lô date gần
                    "use_serial_batch_fields": 1,
                    "against_sales_order": so_b2b.name,
                    "so_detail": so_b2b.items[0].name,
                    "cost_center": "Kênh B2B Sỉ - B"
                },
                {
                    "item_code": "TBK-CACAO",
                    "qty": 40,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "rate": 265000,
                    "warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-CACAO-202606", # FEFO
                    "use_serial_batch_fields": 1,
                    "against_sales_order": so_b2b.name,
                    "so_detail": so_b2b.items[1].name,
                    "cost_center": "Kênh B2B Sỉ - B"
                }
            ]
        })
        dn_b2b.insert(ignore_permissions=True)
        dn_b2b.submit()

        # Hóa đơn bán sỉ (Sales Invoice)
        si_b2b = frappe.get_doc({
            "doctype": "Sales Invoice",
            "company": COMPANY,
            "customer": so_b2b.customer,
            "posting_date": "2026-10-05",
            "posting_time": "10:00:00",
            "due_date": "2026-11-05",
            "currency": "VND",
            "custom_sales_channel": "B2B Sỉ",
            "custom_marketplace_order_id": order_b2b_ref,
            "custom_sales_person": SALE1_USER,
            "cost_center": "Kênh B2B Sỉ - B",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 50,
                    "rate": 365000,
                    "warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "delivery_note": dn_b2b.name,
                    "dn_detail": dn_b2b.items[0].name,
                    "sales_order": so_b2b.name,
                    "so_detail": so_b2b.items[0].name,
                    "income_account": "5111 - Doanh thu bán hàng hóa - B",
                    "expense_account": "632 - Giá vốn hàng bán - B",
                    "cost_center": "Kênh B2B Sỉ - B"
                },
                {
                    "item_code": "TBK-CACAO",
                    "qty": 40,
                    "rate": 265000,
                    "warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-CACAO-202606",
                    "use_serial_batch_fields": 1,
                    "delivery_note": dn_b2b.name,
                    "dn_detail": dn_b2b.items[1].name,
                    "sales_order": so_b2b.name,
                    "so_detail": so_b2b.items[1].name,
                    "income_account": "5111 - Doanh thu bán hàng hóa - B",
                    "expense_account": "632 - Giá vốn hàng bán - B",
                    "cost_center": "Kênh B2B Sỉ - B"
                }
            ]
        })
        si_b2b.insert(ignore_permissions=True)
        si_b2b.submit()

        # Thu tiền đợt 1 (Partial payment 50% = 14.425.000 đ)
        pe_b2b_1 = frappe.get_doc({
            "doctype": "Payment Entry",
            "payment_type": "Receive",
            "party_type": "Customer",
            "party": so_b2b.customer,
            "company": COMPANY,
            "paid_amount": 14425000,
            "received_amount": 14425000,
            "target_exchange_rate": 1.0,
            "paid_to": "1121 - Tiền gửi ngân hàng (VND) - B",
            "mode_of_payment": "Wire Transfer",
            "posting_date": "2026-10-08",
            "reference_no": "UNC-B2B-DDX-DOT1",
            "reference_date": "2026-10-08",
            "references": [
                {
                    "reference_doctype": "Sales Invoice",
                    "reference_name": si_b2b.name,
                    "total_amount": 28850000,
                    "outstanding_amount": 28850000,
                    "allocated_amount": 14425000
                }
            ]
        })
        pe_b2b_1.insert(ignore_permissions=True)
        pe_b2b_1.submit()
        print(f"✓ Kênh B2B Sỉ: Đơn {order_b2b_ref} tổng 28.850.000 đ, đã thu đợt 1 14.425.000 đ, công nợ còn 14.425.000 đ.")

    # ------------------------------------------------------------------
    # KÊNH 2: B2C BÁN LẺ TRỰC TIẾP (Xuất trực tiếp từ Kho NVKD)
    # Nhân viên thu tiền mặt/chuyển khoản -> Ghi nhận vào tài khoản 1411
    # ------------------------------------------------------------------
    order_b2c_ref = "SO-B2C-LAN-001"
    if not frappe.db.exists("Sales Order", {"custom_marketplace_order_id": order_b2c_ref}):
        so_b2c = frappe.get_doc({
            "doctype": "Sales Order",
            "company": COMPANY,
            "customer": "Chị Nguyễn Thị Lan (Khách hàng cuối)",
            "transaction_date": "2026-10-06",
            "delivery_date": "2026-10-06",
            "order_type": "Sales",
            "currency": "VND",
            "selling_price_list": "Standard Selling",
            "owner": SALE1_USER,
            "custom_sales_channel": "B2C Trực tiếp",
            "custom_marketplace_order_id": order_b2c_ref,
            "custom_sales_person": SALE1_USER,
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 5,
                    "rate": 365000,
                    "delivery_date": "2026-10-06",
                    "warehouse": SALE1_WAREHOUSE # XUẤT TỪ KHO NVKD
                }
            ]
        })
        so_b2c.insert(ignore_permissions=True)
        so_b2c.submit()

        # Xuất kho trực tiếp từ Kho NVKD Nguyễn Văn Nam
        dn_b2c = frappe.get_doc({
            "doctype": "Delivery Note",
            "company": COMPANY,
            "customer": so_b2c.customer,
            "set_posting_time": 1,
            "posting_date": "2026-10-06",
            "posting_time": "14:00:00",
            "owner": SALE1_USER,
            "custom_sales_channel": "B2C Trực tiếp",
            "custom_marketplace_order_id": order_b2c_ref,
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 5,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "rate": 365000,
                    "warehouse": SALE1_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "against_sales_order": so_b2c.name,
                    "so_detail": so_b2c.items[0].name,
                    "cost_center": "Kênh B2C Trực tiếp - B"
                }
            ]
        })
        dn_b2c.insert(ignore_permissions=True)
        dn_b2c.submit()

        # Hóa đơn bán lẻ
        si_b2c = frappe.get_doc({
            "doctype": "Sales Invoice",
            "company": COMPANY,
            "customer": so_b2c.customer,
            "set_posting_time": 1,
            "posting_date": "2026-10-06",
            "posting_time": "14:15:00",
            "due_date": "2026-10-06",
            "payment_schedule": [],
            "currency": "VND",
            "custom_sales_channel": "B2C Trực tiếp",
            "custom_marketplace_order_id": order_b2c_ref,
            "custom_sales_person": SALE1_USER,
            "cost_center": "Kênh B2C Trực tiếp - B",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 5,
                    "rate": 365000,
                    "warehouse": SALE1_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "delivery_note": dn_b2c.name,
                    "dn_detail": dn_b2c.items[0].name,
                    "sales_order": so_b2c.name,
                    "so_detail": so_b2c.items[0].name,
                    "income_account": "5111 - Doanh thu bán hàng hóa - B",
                    "expense_account": "632 - Giá vốn hàng bán - B",
                    "cost_center": "Kênh B2C Trực tiếp - B"
                }
            ]
        })
        si_b2c.insert(ignore_permissions=True)
        si_b2c.submit()

        # Khách trả tiền mặt cho NVKD Nguyễn Văn Nam -> Hạch toán vào 1113 (Tiền thu hộ)
        pe_b2c = frappe.get_doc({
            "doctype": "Payment Entry",
            "payment_type": "Receive",
            "party_type": "Customer",
            "party": so_b2c.customer,
            "company": COMPANY,
            "paid_amount": 1825000,
            "received_amount": 1825000,
            "target_exchange_rate": 1.0,
            "paid_to": "1113 - Tiền thu hộ của NVKD - B", # TIỀN THU HỘ NẰM TẠI NHÂN VIÊN
            "mode_of_payment": "Cash",
            "set_posting_time": 1,
            "posting_date": "2026-10-06",
            "posting_time": "14:30:00",
            "reference_no": "TIENMAT-B2C-LAN",
            "reference_date": "2026-10-06",
            "references": [
                {
                    "reference_doctype": "Sales Invoice",
                    "reference_name": si_b2c.name,
                    "total_amount": 1825000,
                    "outstanding_amount": 1825000,
                    "allocated_amount": 1825000
                }
            ]
        })
        pe_b2c.insert(ignore_permissions=True)
        pe_b2c.submit()
        print(f"✓ Kênh B2C Trực tiếp: Bán 5 hộp PLUS từ '{SALE1_WAREHOUSE}', thu 1.825.000 đ vào tài khoản '1113 - Tiền thu hộ của NVKD'.")

    # ------------------------------------------------------------------
    # KÊNH 3: TIKTOK SHOP (Sàn TMĐT) qua Adapter
    # ------------------------------------------------------------------
    import_marketplace_order(
        channel="TikTok Shop",
        order_id="TIKTOK-20261010-001",
        customer_name="Khách hàng TikTok Shop - Lê Văn Tuấn",
        items=[
            {"item_code": "TBK-PLUS", "qty": 10, "rate": 365000, "batch_no": "LOT-PLUS-202606"},
            {"item_code": "TBK-CACAO", "qty": 10, "rate": 265000, "batch_no": "LOT-CACAO-202606"}
        ],
        platform_fee=504000, # Phí sàn 8%
        shipping_fee=120000,
        order_date="2026-10-10"
    )

    # ------------------------------------------------------------------
    # KÊNH 4: SHOPEE (Sàn TMĐT) qua Adapter
    # ------------------------------------------------------------------
    import_marketplace_order(
        channel="Shopee",
        order_id="SHOPEE-20261011-002",
        customer_name="Khách hàng Shopee - Trần Văn Hưng",
        items=[
            {"item_code": "TBK-PLUS", "qty": 15, "rate": 365000, "batch_no": "LOT-PLUS-202606"},
            {"item_code": "TBK-TIBOKA", "qty": 20, "rate": 250000, "batch_no": "LOT-TIBOKA-202606"}
        ],
        platform_fee=942750, # Phí sàn 9%
        shipping_fee=150000,
        order_date="2026-10-11"
    )

    # ------------------------------------------------------------------
    # KÊNH 5: WEBSITE (Đơn hàng từ Web bán buôn/lẻ)
    # ------------------------------------------------------------------
    order_web_ref = "WEB-20261012-003"
    if not frappe.db.exists("Sales Order", {"custom_marketplace_order_id": order_web_ref}):
        so_web = frappe.get_doc({
            "doctype": "Sales Order",
            "company": COMPANY,
            "customer": "Khách hàng Website - Phạm Minh Trí",
            "transaction_date": "2026-10-12",
            "delivery_date": "2026-10-13",
            "order_type": "Sales",
            "currency": "VND",
            "selling_price_list": "Standard Selling",
            "custom_sales_channel": "Website",
            "custom_marketplace_order_id": order_web_ref,
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 8,
                    "rate": 365000,
                    "delivery_date": "2026-10-13",
                    "warehouse": CENTRAL_WAREHOUSE
                },
                {
                    "item_code": "TBK-CACAO",
                    "qty": 5,
                    "rate": 265000,
                    "delivery_date": "2026-10-13",
                    "warehouse": CENTRAL_WAREHOUSE
                }
            ]
        })
        so_web.insert(ignore_permissions=True)
        so_web.submit()

        dn_web = frappe.get_doc({
            "doctype": "Delivery Note",
            "company": COMPANY,
            "customer": so_web.customer,
            "posting_date": "2026-10-13",
            "posting_time": "11:00:00",
            "owner": KHO_USER,
            "custom_sales_channel": "Website",
            "custom_marketplace_order_id": order_web_ref,
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 8,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "rate": 365000,
                    "warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "against_sales_order": so_web.name,
                    "so_detail": so_web.items[0].name,
                    "cost_center": "Kênh Website - B"
                },
                {
                    "item_code": "TBK-CACAO",
                    "qty": 5,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "rate": 265000,
                    "warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-CACAO-202606",
                    "use_serial_batch_fields": 1,
                    "against_sales_order": so_web.name,
                    "so_detail": so_web.items[1].name,
                    "cost_center": "Kênh Website - B"
                }
            ]
        })
        dn_web.insert(ignore_permissions=True)
        dn_web.submit()

        si_web = frappe.get_doc({
            "doctype": "Sales Invoice",
            "company": COMPANY,
            "customer": so_web.customer,
            "set_posting_time": 1,
            "posting_date": "2026-10-13",
            "posting_time": "11:15:00",
            "due_date": "2026-10-13",
            "payment_schedule": [],
            "currency": "VND",
            "custom_sales_channel": "Website",
            "custom_marketplace_order_id": order_web_ref,
            "cost_center": "Kênh Website - B",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 8,
                    "rate": 365000,
                    "warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "delivery_note": dn_web.name,
                    "dn_detail": dn_web.items[0].name,
                    "sales_order": so_web.name,
                    "so_detail": so_web.items[0].name,
                    "income_account": "5111 - Doanh thu bán hàng hóa - B",
                    "expense_account": "632 - Giá vốn hàng bán - B",
                    "cost_center": "Kênh Website - B"
                },
                {
                    "item_code": "TBK-CACAO",
                    "qty": 5,
                    "rate": 265000,
                    "warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-CACAO-202606",
                    "use_serial_batch_fields": 1,
                    "delivery_note": dn_web.name,
                    "dn_detail": dn_web.items[1].name,
                    "sales_order": so_web.name,
                    "so_detail": so_web.items[1].name,
                    "income_account": "5111 - Doanh thu bán hàng hóa - B",
                    "expense_account": "632 - Giá vốn hàng bán - B",
                    "cost_center": "Kênh Website - B"
                }
            ]
        })
        si_web.insert(ignore_permissions=True)
        si_web.submit()

        # Khách chuyển khoản ngân hàng
        pe_web = frappe.get_doc({
            "doctype": "Payment Entry",
            "payment_type": "Receive",
            "party_type": "Customer",
            "party": so_web.customer,
            "company": COMPANY,
            "paid_amount": 4245000,
            "received_amount": 4245000,
            "target_exchange_rate": 1.0,
            "paid_to": "1121 - Tiền gửi ngân hàng (VND) - B",
            "mode_of_payment": "Wire Transfer",
            "set_posting_time": 1,
            "posting_date": "2026-10-13",
            "posting_time": "11:30:00",
            "reference_no": "CK-WEB-4245K",
            "reference_date": "2026-10-13",
            "references": [
                {
                    "reference_doctype": "Sales Invoice",
                    "reference_name": si_web.name,
                    "total_amount": 4245000,
                    "outstanding_amount": 4245000,
                    "allocated_amount": 4245000
                }
            ]
        })
        pe_web.insert(ignore_permissions=True)
        pe_web.submit()
        print(f"✓ Kênh Website: Đơn {order_web_ref} tổng 4.245.000 đ, đã thanh toán đủ qua chuyển khoản ngân hàng.")


# ----------------------------------------------------------------------
# ADAPTER: IMPORT MARKETPLACE ORDER (WITH DEDUPLICATION / IDEMPOTENCY)
# ----------------------------------------------------------------------
@frappe.whitelist()
def import_marketplace_order(channel, order_id, customer_name, items, platform_fee, shipping_fee, order_date):
    """
    Import đơn hàng từ TikTok Shop hoặc Shopee.
    Đảm bảo:
    1. Chống trùng đơn (Dedup): Nếu order_id đã tồn tại, lập tức bỏ qua.
    2. Xuất kho đúng Lô FEFO từ Kho Tổng.
    3. Ghi nhận Doanh thu, Phí sàn (6413), Phí vận chuyển (6412) và Quyết toán tiền về ngân hàng.
    """
    if frappe.db.exists("Sales Order", {"custom_marketplace_order_id": order_id}):
        print(f"! Đơn sàn {order_id} ({channel}) đã tồn tại trong hệ thống. Tự động BỎ QUA để chống trùng lặp dữ liệu.")
        return {"status": "skipped", "message": "Duplicate order skipped"}

    total_amount = sum(it["qty"] * it["rate"] for it in items)
    cost_center = f"Kênh {channel} - B"

    # Đảm bảo khách hàng tồn tại
    if not frappe.db.exists("Customer", customer_name):
        frappe.get_doc({
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_group": "Khách hàng cuối",
            "territory": "Vietnam",
            "customer_type": "Individual"
        }).insert(ignore_permissions=True)

    # 1. Tạo Sales Order
    so = frappe.get_doc({
        "doctype": "Sales Order",
        "company": COMPANY,
        "customer": customer_name,
        "transaction_date": order_date,
        "delivery_date": order_date,
        "order_type": "Sales",
        "currency": "VND",
        "selling_price_list": "Standard Selling",
        "custom_sales_channel": channel,
        "custom_marketplace_order_id": order_id,
        "custom_platform_fee": platform_fee,
        "custom_shipping_fee": shipping_fee,
        "items": [
            {
                "item_code": it["item_code"],
                "qty": it["qty"],
                "rate": it["rate"],
                "delivery_date": order_date,
                "warehouse": CENTRAL_WAREHOUSE
            }
            for it in items
        ]
    })
    so.insert(ignore_permissions=True)
    so.submit()

    # 2. Tạo Delivery Note (Xuất kho FEFO)
    dn = frappe.get_doc({
        "doctype": "Delivery Note",
        "company": COMPANY,
        "customer": customer_name,
        "set_posting_time": 1,
        "posting_date": order_date,
        "posting_time": "15:00:00",
        "owner": KHO_USER,
        "custom_sales_channel": channel,
        "custom_marketplace_order_id": order_id,
        "items": [
            {
                "item_code": it["item_code"],
                "qty": it["qty"],
                "uom": "Hộp",
                "stock_uom": "Hộp",
                "rate": it["rate"],
                "warehouse": CENTRAL_WAREHOUSE,
                "batch_no": it.get("batch_no") or "LOT-PLUS-202606",
                "use_serial_batch_fields": 1,
                "against_sales_order": so.name,
                "so_detail": so.items[idx].name,
                "cost_center": cost_center
            }
            for idx, it in enumerate(items)
        ]
    })
    dn.insert(ignore_permissions=True)
    dn.submit()

    # 3. Tạo Sales Invoice
    si = frappe.get_doc({
        "doctype": "Sales Invoice",
        "company": COMPANY,
        "customer": customer_name,
        "set_posting_time": 1,
        "posting_date": order_date,
        "posting_time": "15:15:00",
        "due_date": order_date,
        "payment_schedule": [],
        "currency": "VND",
        "custom_sales_channel": channel,
        "custom_marketplace_order_id": order_id,
        "custom_platform_fee": platform_fee,
        "custom_shipping_fee": shipping_fee,
        "cost_center": cost_center,
        "items": [
            {
                "item_code": it["item_code"],
                "qty": it["qty"],
                "rate": it["rate"],
                "warehouse": CENTRAL_WAREHOUSE,
                "batch_no": it.get("batch_no") or "LOT-PLUS-202606",
                "use_serial_batch_fields": 1,
                "delivery_note": dn.name,
                "dn_detail": dn.items[idx].name,
                "sales_order": so.name,
                "so_detail": so.items[idx].name,
                "income_account": "5111 - Doanh thu bán hàng hóa - B",
                "expense_account": "632 - Giá vốn hàng bán - B",
                "cost_center": cost_center
            }
            for idx, it in enumerate(items)
        ]
    })
    si.insert(ignore_permissions=True)
    si.submit()

    # 4. Quyết toán tiền sàn về ngân hàng sau khi trừ Phí sàn và Phí ship
    # Tiền thực nhận về tài khoản ngân hàng = Tổng tiền - Phí sàn - Phí ship
    net_payout = total_amount - platform_fee - shipping_fee
    settle_date = add_days(order_date, 3) # Sàn thanh toán sau 3 ngày

    pe = frappe.get_doc({
        "doctype": "Payment Entry",
        "payment_type": "Receive",
        "party_type": "Customer",
        "party": customer_name,
        "company": COMPANY,
        "paid_amount": total_amount,
        "received_amount": total_amount,
        "target_exchange_rate": 1.0,
        "paid_to": "1121 - Tiền gửi ngân hàng (VND) - B",
        "mode_of_payment": "Wire Transfer",
        "set_posting_time": 1,
        "posting_date": settle_date,
        "posting_time": "10:00:00",
        "reference_no": f"PAYOUT-{order_id}",
        "reference_date": settle_date,
        "references": [
            {
                "reference_doctype": "Sales Invoice",
                "reference_name": si.name,
                "total_amount": total_amount,
                "outstanding_amount": total_amount,
                "allocated_amount": total_amount
            }
        ],
        "deductions": [
            {
                "account": "6413 - Phí sàn thương mại điện tử - B",
                "cost_center": cost_center,
                "amount": platform_fee,
                "description": f"Khấu trừ phí sàn {channel} ({platform_fee:,} đ)"
            },
            {
                "account": "6412 - Chi phí bao bì, vận chuyển - B",
                "cost_center": cost_center,
                "amount": shipping_fee,
                "description": f"Khấu trừ phí vận chuyển sàn {channel} ({shipping_fee:,} đ)"
            }
        ]
    })
    pe.insert(ignore_permissions=True)
    pe.submit()

    print(f"✓ Đã import thành công đơn sàn {channel} [{order_id}]: Tổng {total_amount:,} đ, Phí sàn {platform_fee:,} đ, Ship {shipping_fee:,} đ, Tiền về TK {net_payout:,} đ.")
    return {"status": "success", "order_id": order_id, "sales_order": so.name}


# ----------------------------------------------------------------------
# 8. RETURNS, QUARANTINE & DAMAGED GOODS
# ----------------------------------------------------------------------
def setup_returns_and_quarantine():
    print("\n[Phase 2.4] Xử lý Hàng Đổi Trả, Kho Cách Ly & Xuất hủy Hàng Hỏng...")

    # Kịch bản: Khách hoàn trả 2 hộp TBK-PLUS do giao nhầm địa chỉ
    # Bước 1: Nhập hàng trả vào Kho Cách Ly & Đổi Trả
    has_quarantine_in = frappe.db.exists("Stock Entry", {
        "to_warehouse": QUARANTINE_WAREHOUSE,
        "purpose": "Material Receipt",
        "docstatus": 1
    })
    if not has_quarantine_in:
        se_return = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "purpose": "Material Receipt",
            "company": COMPANY,
            "set_posting_time": 1,
            "posting_date": "2026-10-11",
            "posting_time": "16:00:00",
            "to_warehouse": QUARANTINE_WAREHOUSE,
            "owner": KHO_USER,
            "remarks": "Tiếp nhận 2 hộp TBK-PLUS đổi trả từ khách hàng vào Kho Cách Ly để kiểm định",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 2,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "basic_rate": 200000,
                    "t_warehouse": QUARANTINE_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "cost_center": "Main - B"
                }
            ]
        })
        se_return.insert(ignore_permissions=True)
        se_return.submit()
        print(f"✓ Đã tiếp nhận 2 hộp TBK-PLUS vào '{QUARANTINE_WAREHOUSE}' để thẩm định.")

        # Bước 2: Thẩm định kiểm tra:
        # - 1 hộp nguyên vẹn: Điều chuyển từ Kho Cách Ly về lại Kho Tổng BAKA
        se_intact = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Transfer",
            "purpose": "Material Transfer",
            "company": COMPANY,
            "set_posting_time": 1,
            "posting_date": "2026-10-12",
            "posting_time": "09:00:00",
            "from_warehouse": QUARANTINE_WAREHOUSE,
            "to_warehouse": CENTRAL_WAREHOUSE,
            "owner": KHO_USER,
            "remarks": "1 hộp TBK-PLUS đạt chuẩn chất lượng được nhập lại Kho Tổng để bán",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 1,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "basic_rate": 200000,
                    "s_warehouse": QUARANTINE_WAREHOUSE,
                    "t_warehouse": CENTRAL_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "cost_center": "Main - B"
                }
            ]
        })
        se_intact.insert(ignore_permissions=True)
        se_intact.submit()
        print(f"✓ Đã nhập lại 1 hộp nguyên vẹn từ Kho Cách Ly về '{CENTRAL_WAREHOUSE}'.")

        # - 1 hộp bị rách móp: Chuyển sang Kho Hàng Hỏng & Hết Hạn
        se_damaged = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Transfer",
            "purpose": "Material Transfer",
            "company": COMPANY,
            "set_posting_time": 1,
            "posting_date": "2026-10-12",
            "posting_time": "09:30:00",
            "from_warehouse": QUARANTINE_WAREHOUSE,
            "to_warehouse": DAMAGED_WAREHOUSE,
            "owner": KHO_USER,
            "remarks": "1 hộp TBK-PLUS móp méo rách bao bì, chuyển sang Kho Hàng Hỏng chờ xuất hủy",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 1,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "basic_rate": 200000,
                    "s_warehouse": QUARANTINE_WAREHOUSE,
                    "t_warehouse": DAMAGED_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "cost_center": "Main - B"
                }
            ]
        })
        se_damaged.insert(ignore_permissions=True)
        se_damaged.submit()

        # - Bước 3: Xuất hủy hàng hỏng (Material Issue) hạch toán tổn thất vào 811
        se_issue = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Issue",
            "purpose": "Material Issue",
            "company": COMPANY,
            "set_posting_time": 1,
            "posting_date": "2026-10-12",
            "posting_time": "10:00:00",
            "from_warehouse": DAMAGED_WAREHOUSE,
            "owner": KHO_USER,
            "remarks": "Biên bản tiêu hủy 1 hộp TBK-PLUS hỏng do vận chuyển, hạch toán chi phí khác 811",
            "items": [
                {
                    "item_code": "TBK-PLUS",
                    "qty": 1,
                    "uom": "Hộp",
                    "stock_uom": "Hộp",
                    "basic_rate": 200000,
                    "s_warehouse": DAMAGED_WAREHOUSE,
                    "batch_no": "LOT-PLUS-202606",
                    "use_serial_batch_fields": 1,
                    "expense_account": "811 - Chi phí khác - B",
                    "cost_center": "Khối Vận Hành & Quản Lý - B"
                }
            ]
        })
        se_issue.insert(ignore_permissions=True)
        se_issue.submit()
        print(f"✓ Đã lập biên bản xuất hủy 1 hộp hàng hỏng từ '{DAMAGED_WAREHOUSE}', hạch toán chi phí tổn thất vào 811.")


# ----------------------------------------------------------------------
# 9. EXPENSES, RECONCILIATION & P&L DATA
# ----------------------------------------------------------------------
def setup_expenses_and_reconciliation():
    print("\n[Phase 4.2] Ghi nhận Chi phí Vận hành, Quảng cáo Ads & Đối soát Tiền thu hộ...")

    # 1. NVKD Nguyễn Văn Nam nộp 1.500.000 đ tiền thu hộ về tài khoản ngân hàng công ty
    # Chuyển từ tài khoản 1113 (Tiền thu hộ NVKD) sang 1121 (Tiền gửi ngân hàng)
    has_pe_reconcile = frappe.db.exists("Payment Entry", {"reference_no": "NOPTIEN-NAM-DOT1"})
    if not has_pe_reconcile:
        pe_rec = frappe.get_doc({
            "doctype": "Payment Entry",
            "payment_type": "Internal Transfer",
            "company": COMPANY,
            "paid_from": "1113 - Tiền thu hộ của NVKD - B",
            "paid_to": "1121 - Tiền gửi ngân hàng (VND) - B",
            "paid_amount": 1500000,
            "received_amount": 1500000,
            "posting_date": "2026-10-07",
            "reference_no": "NOPTIEN-NAM-DOT1",
            "reference_date": "2026-10-07",
            "remarks": "NVKD Nguyễn Văn Nam nộp tiền bán lẻ trực tiếp đợt 1 về ngân hàng (Số dư còn lại: 325.000 đ)"
        })
        pe_rec.insert(ignore_permissions=True)
        pe_rec.submit()
        print("✓ Đối soát thành công: NVKD Nguyễn Văn Nam nộp 1.500.000 đ về công ty, còn giữ 325.000 đ.")

    # 2. Chi phí Quảng cáo Ads (Facebook / TikTok / Shopee Ads)
    # Hạch toán qua Journal Entry
    has_ads_je = frappe.db.exists("Journal Entry", {"user_remark": "Chi phí chạy Ads Marketing tháng 10/2026"})
    if not has_ads_je:
        je_ads = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": "Journal Entry",
            "company": COMPANY,
            "posting_date": "2026-10-05",
            "user_remark": "Chi phí chạy Ads Marketing tháng 10/2026",
            "accounts": [
                {
                    "account": "6414 - Chi phí quảng cáo, tiếp thị - B",
                    "debit_in_account_currency": 3500000,
                    "credit_in_account_currency": 0,
                    "cost_center": "Kênh TikTok Shop - B"
                },
                {
                    "account": "6414 - Chi phí quảng cáo, tiếp thị - B",
                    "debit_in_account_currency": 2500000,
                    "credit_in_account_currency": 0,
                    "cost_center": "Kênh Shopee - B"
                },
                {
                    "account": "1121 - Tiền gửi ngân hàng (VND) - B",
                    "debit_in_account_currency": 0,
                    "credit_in_account_currency": 6000000,
                    "cost_center": "Main - B"
                }
            ]
        })
        je_ads.insert(ignore_permissions=True)
        je_ads.submit()
        print("✓ Đã ghi nhận Chi phí Marketing Ads: 3.500.000 đ (TikTok) + 2.500.000 đ (Shopee).")

    # 3. Chi phí Thuê Văn phòng & Kho bãi
    has_rent_je = frappe.db.exists("Journal Entry", {"user_remark": "Tiền thuê văn phòng & kho bãi tháng 10/2026"})
    if not has_rent_je:
        je_rent = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": "Journal Entry",
            "company": COMPANY,
            "posting_date": "2026-10-02",
            "user_remark": "Tiền thuê văn phòng & kho bãi tháng 10/2026",
            "accounts": [
                {
                    "account": "6426 - Chi phí thuê văn phòng, kho bãi - B",
                    "debit_in_account_currency": 8000000,
                    "credit_in_account_currency": 0,
                    "cost_center": "Khối Vận Hành & Quản Lý - B"
                },
                {
                    "account": "1121 - Tiền gửi ngân hàng (VND) - B",
                    "debit_in_account_currency": 0,
                    "credit_in_account_currency": 8000000,
                    "cost_center": "Main - B"
                }
            ]
        })
        je_rent.insert(ignore_permissions=True)
        je_rent.submit()
        print("✓ Đã ghi nhận Chi phí Thuê mặt bằng & Kho bãi: 8.000.000 đ.")

    # 4. Chi phí Lương Nhân sự
    has_salary_je = frappe.db.exists("Journal Entry", {"user_remark": "Chi phí lương nhân sự tháng 10/2026"})
    if not has_salary_je:
        je_sal = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": "Journal Entry",
            "company": COMPANY,
            "posting_date": "2026-10-10",
            "user_remark": "Chi phí lương nhân sự tháng 10/2026",
            "accounts": [
                {
                    "account": "6411 - Chi phí nhân viên bán hàng - B",
                    "debit_in_account_currency": 16000000, # 2 NVKD
                    "credit_in_account_currency": 0,
                    "cost_center": "Khối Vận Hành & Quản Lý - B"
                },
                {
                    "account": "6421 - Chi phí nhân viên quản lý - B",
                    "debit_in_account_currency": 15000000, # Quản lý kho + COO
                    "credit_in_account_currency": 0,
                    "cost_center": "Khối Vận Hành & Quản Lý - B"
                },
                {
                    "account": "1121 - Tiền gửi ngân hàng (VND) - B",
                    "debit_in_account_currency": 0,
                    "credit_in_account_currency": 31000000,
                    "cost_center": "Main - B"
                }
            ]
        })
        je_sal.insert(ignore_permissions=True)
        je_sal.submit()
        print("✓ Đã ghi nhận Chi phí Lương nhân sự: 31.000.000 đ (16tr khối kinh doanh, 15tr khối quản lý & kho).")


# ----------------------------------------------------------------------
# 10. HR, LEAVE & KPI EVALUATION
# ----------------------------------------------------------------------
def setup_hr_and_kpi():
    print("\n[Phase 5] Cấu hình Đơn xin nghỉ phép & Đánh giá KPI bán hàng...")

    # 1. Tạo DocType Quản lý Nghỉ phép (Employee Leave Request) nếu chưa có
    if not frappe.db.exists("DocType", "Employee Leave Request"):
        dt = frappe.get_doc({
            "doctype": "DocType",
            "name": "Employee Leave Request",
            "module": "Setup",
            "custom": 1,
            "is_submittable": 0,
            "fields": [
                {"fieldname": "employee", "label": "Nhân viên", "fieldtype": "Link", "options": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "employee_name", "label": "Tên nhân viên", "fieldtype": "Data", "read_only": 1, "in_list_view": 1},
                {"fieldname": "leave_type", "label": "Loại nghỉ phép", "fieldtype": "Select", "options": "Phép năm\nNghỉ ốm\nViệc riêng\nNghỉ không lương", "reqd": 1, "in_list_view": 1},
                {"fieldname": "from_date", "label": "Từ ngày", "fieldtype": "Date", "reqd": 1, "in_list_view": 1},
                {"fieldname": "to_date", "label": "Đến ngày", "fieldtype": "Date", "reqd": 1, "in_list_view": 1},
                {"fieldname": "total_days", "label": "Số ngày nghỉ", "fieldtype": "Float", "default": 1.0, "in_list_view": 1},
                {"fieldname": "reason", "label": "Lý do xin nghỉ", "fieldtype": "Small Text"},
                {"fieldname": "status", "label": "Trạng thái", "fieldtype": "Select", "options": "Chờ duyệt\nĐã duyệt\nTừ chối", "default": "Chờ duyệt", "in_list_view": 1},
                {"fieldname": "approver", "label": "Người duyệt", "fieldtype": "Link", "options": "User", "in_list_view": 1}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "HR Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Employee", "read": 1, "write": 1, "create": 1}
            ]
        })
        dt.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✓ Đã khởi tạo DocType chuẩn: Employee Leave Request (Quản lý nghỉ phép).")

    # 2. Đơn xin nghỉ phép mẫu có duyệt cho NVKD Nguyễn Văn Nam
    emp_nam = frappe.db.get_value("Employee", {"user_id": SALE1_USER}, "name")
    has_leave = frappe.db.exists("Employee Leave Request", {"employee": emp_nam, "from_date": "2026-10-15"})
    if not has_leave and emp_nam:
        leave_app = frappe.get_doc({
            "doctype": "Employee Leave Request",
            "employee": emp_nam,
            "employee_name": "Nguyễn Văn Nam",
            "leave_type": "Phép năm",
            "from_date": "2026-10-15",
            "to_date": "2026-10-15",
            "total_days": 1.0,
            "reason": "Nghỉ giải quyết việc gia đình cá nhân",
            "status": "Đã duyệt",
            "approver": COO_USER
        })
        leave_app.insert(ignore_permissions=True)
        print("✓ Đã tạo và phê duyệt Đơn xin nghỉ phép cho NVKD Nguyễn Văn Nam (ngày 15/10/2026).")


# ----------------------------------------------------------------------
# MANAGERIAL P&L ENGINE / API (LÃI LỖ QUẢN TRỊ ĐA CHIỀU)
# ----------------------------------------------------------------------
@frappe.whitelist()
def get_managerial_pnl_report(from_date=None, to_date=None, brand=None, channel=None, product_line=None):
    """
    Tính toán Báo cáo Lãi Lỗ Quản Trị (Managerial P&L) bóc tách chính xác:
    - Doanh thu gộp
    - Chiết khấu thương mại & Hàng bán trả lại -> Doanh thu thuần
    - Giá vốn hàng bán (COGS) -> Lợi nhuận gộp (Gross Profit)
    - Phí sàn TMĐT (Shopee, TikTok) & Phí vận chuyển
    - Chi phí Quảng cáo Ads Marketing
    - Chi phí Lương nhân sự & Chi phí Vận hành chung (Thuê kho/văn phòng)
    - Lợi nhuận ròng quản trị (Net Operating Profit)
    Thương hiệu duy nhất: BAKA.
    Hỗ trợ lọc theo Dòng sản phẩm (PLUS, CACAO, TIBOKA) và Kênh bán hàng.
    """
    from_date = from_date or "2026-10-01"
    to_date = to_date or "2026-10-31"

    # 1. Doanh thu & Giá vốn theo Hóa đơn bán hàng
    inv_conditions = ["si.docstatus = 1", "si.posting_date >= %(from_date)s", "si.posting_date <= %(to_date)s"]
    inv_params = {"from_date": from_date, "to_date": to_date}

    if channel:
        inv_conditions.append("si.custom_sales_channel = %(channel)s")
        inv_params["channel"] = channel

    where_clause = " AND ".join(inv_conditions)

    # Lấy chi tiết từng dòng hóa đơn kèm Brand, Product Line và COGS
    query = f"""
        SELECT 
            COALESCE(si.custom_sales_channel, 'B2B Sỉ') as custom_sales_channel,
            sii.item_code,
            COALESCE(NULLIF(sii.brand, ''), it.brand, 'BAKA') as brand,
            COALESCE(it.custom_product_line, CASE 
                WHEN sii.item_code LIKE '%%PLUS%%' THEN 'PLUS'
                WHEN sii.item_code LIKE '%%CACAO%%' THEN 'CACAO'
                WHEN sii.item_code LIKE '%%TIBOKA%%' THEN 'TIBOKA'
                ELSE 'Khác' END) as product_line,
            sii.qty,
            sii.base_net_amount,
            COALESCE(NULLIF(sii.incoming_rate, 0), dni.incoming_rate, it.valuation_rate, 0) as unit_cogs,
            (sii.qty * COALESCE(NULLIF(sii.incoming_rate, 0), dni.incoming_rate, it.valuation_rate, 0)) as cogs,
            COALESCE(si.custom_platform_fee, 0) as platform_fee,
            COALESCE(si.custom_shipping_fee, 0) as shipping_fee
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON sii.parent = si.name
        JOIN `tabItem` it ON sii.item_code = it.name
        LEFT JOIN `tabDelivery Note Item` dni ON sii.dn_detail = dni.name
        WHERE {where_clause}
    """
    invoice_rows = frappe.db.sql(query, inv_params, as_dict=True)

    # Xử lý bộ lọc Dòng sản phẩm & Thương hiệu
    # Thương hiệu duy nhất là BAKA. PLUS, CACAO, TIBOKA là các dòng sản phẩm.
    target_line = product_line
    if brand in ("PLUS", "CACAO", "TIBOKA"):
        target_line = brand  # Ánh xạ tương thích ngược

    if target_line:
        invoice_rows = [r for r in invoice_rows if r.product_line == target_line]
    elif brand and brand != "BAKA":
        invoice_rows = [r for r in invoice_rows if r.brand == brand]

    total_gross_revenue = sum(flt(r.base_net_amount) for r in invoice_rows)
    total_cogs = sum(flt(r.cogs) for r in invoice_rows)
    gross_profit = total_gross_revenue - total_cogs

    # Phí sàn & Vận chuyển
    si_fees_where = " AND ".join([c.replace("si.", "") for c in inv_conditions])
    si_fees_query = f"""
        SELECT 
            SUM(COALESCE(custom_platform_fee, 0)) as total_platform_fee,
            SUM(COALESCE(custom_shipping_fee, 0)) as total_shipping_fee
        FROM `tabSales Invoice`
        WHERE {si_fees_where}
    """
    fees_res = frappe.db.sql(si_fees_query, inv_params, as_dict=True)[0]
    is_line_filtered = bool(target_line)
    total_platform_fee = flt(fees_res.total_platform_fee) if not is_line_filtered else (total_gross_revenue * 0.08 if "Shop" in str(channel) or "Shopee" in str(channel) else 0)
    total_shipping_fee = flt(fees_res.total_shipping_fee) if not is_line_filtered else (total_gross_revenue * 0.02 if total_gross_revenue > 0 else 0)

    # Lấy Chi phí từ Sổ Cái GL Entry
    gl_query = """
        SELECT account, cost_center, SUM(debit - credit) as net_expense
        FROM `tabGL Entry`
        WHERE posting_date >= %(from_date)s AND posting_date <= %(to_date)s
          AND is_cancelled = 0
          AND account LIKE %(acc_prefix)s
        GROUP BY account, cost_center
    """
    gl_rows = frappe.db.sql(gl_query, {"from_date": from_date, "to_date": to_date, "acc_prefix": "6%"}, as_dict=True)

    ads_expense = sum(flt(r.net_expense) for r in gl_rows if "6414" in r.account)
    salary_expense = sum(flt(r.net_expense) for r in gl_rows if "6411" in r.account or "6421" in r.account)
    rent_expense = sum(flt(r.net_expense) for r in gl_rows if "6426" in r.account)
    other_operating = sum(flt(r.net_expense) for r in gl_rows if not any(code in r.account for code in ["632", "6414", "6411", "6421", "6426", "6413", "6412"]) and ("64" in r.account or "6" in r.account))

    # Chi phí trực tiếp & Chi phí gián tiếp
    direct_profit = gross_profit - total_platform_fee - total_shipping_fee
    profit_after_ads = direct_profit - ads_expense
    net_operating_profit = profit_after_ads - salary_expense - rent_expense - other_operating

    # Phân tích theo kênh bán hàng
    channel_breakdown = {}
    for r in invoice_rows:
        ch = r.custom_sales_channel or "Khác"
        if ch not in channel_breakdown:
            channel_breakdown[ch] = {"revenue": 0.0, "cogs": 0.0, "qty": 0}
        channel_breakdown[ch]["revenue"] += flt(r.base_net_amount)
        channel_breakdown[ch]["cogs"] += flt(r.cogs)
        channel_breakdown[ch]["qty"] += cint(r.qty)

    for ch, data in channel_breakdown.items():
        data["gross_profit"] = data["revenue"] - data["cogs"]
        data["margin_pct"] = round((data["gross_profit"] / data["revenue"] * 100), 1) if data["revenue"] else 0

    # Phân tích theo Dòng sản phẩm (PLUS, CACAO, TIBOKA) thuộc Thương hiệu BAKA
    product_line_breakdown = {}
    for r in invoice_rows:
        pl = r.product_line or "Khác"
        if pl not in product_line_breakdown:
            product_line_breakdown[pl] = {"revenue": 0.0, "cogs": 0.0, "qty": 0}
        product_line_breakdown[pl]["revenue"] += flt(r.base_net_amount)
        product_line_breakdown[pl]["cogs"] += flt(r.cogs)
        product_line_breakdown[pl]["qty"] += cint(r.qty)

    for pl, data in product_line_breakdown.items():
        data["gross_profit"] = data["revenue"] - data["cogs"]
        data["margin_pct"] = round((data["gross_profit"] / data["revenue"] * 100), 1) if data["revenue"] else 0

    return {
        "period": {"from_date": from_date, "to_date": to_date},
        "filters": {"brand": brand, "channel": channel, "product_line": target_line},
        "brand_name": "BAKA",
        "summary": {
            "gross_revenue": total_gross_revenue,
            "cogs": total_cogs,
            "gross_profit": gross_profit,
            "gross_margin_pct": round((gross_profit / total_gross_revenue * 100), 2) if total_gross_revenue else 0,
            "platform_fees": total_platform_fee,
            "shipping_fees": total_shipping_fee,
            "direct_operating_profit": direct_profit,
            "ads_marketing_expense": ads_expense,
            "profit_after_marketing": profit_after_ads,
            "salary_expense": salary_expense,
            "rent_expense": rent_expense,
            "other_operating_expense": other_operating,
            "net_operating_profit": net_operating_profit,
            "net_profit_margin_pct": round((net_operating_profit / total_gross_revenue * 100), 2) if total_gross_revenue else 0
        },
        "by_channel": channel_breakdown,
        "by_product_line": product_line_breakdown,
        "by_brand": product_line_breakdown  # Tương thích ngược với mã kiểm thử và UI
    }


# ----------------------------------------------------------------------
# WAREHOUSE DASHBOARD DATA / API (TỒN THEO LÔ, HẠN DÙNG, KHO NHÂN VIÊN)
# ----------------------------------------------------------------------
@frappe.whitelist()
def get_warehouse_dashboard_data():
    """
    Trả về toàn bộ số liệu kho vận thực tế:
    - Tồn theo kho và SKU
    - Tồn theo từng Lô & Hạn sử dụng (FEFO)
    - Cảnh báo Lô cận date (< 60 ngày) và hết hạn
    - Hàng đang nằm tại Kho Nhân Viên (Mobile Warehouses)
    - Hàng tại Kho Cách Ly và Kho Hàng Hỏng
    """
    today = nowdate()

    # 1. Tồn theo từng Kho và SKU
    stock_query = """
        SELECT 
            w.warehouse_name,
            w.name as warehouse,
            w.custom_warehouse_type,
            b.item_code,
            it.item_name,
            it.brand,
            COALESCE(it.custom_product_line, CASE 
                WHEN b.item_code LIKE '%%PLUS%%' THEN 'PLUS'
                WHEN b.item_code LIKE '%%CACAO%%' THEN 'CACAO'
                WHEN b.item_code LIKE '%%TIBOKA%%' THEN 'TIBOKA'
                ELSE 'Khác' END) as product_line,
            b.actual_qty,
            b.stock_value
        FROM `tabBin` b
        JOIN `tabWarehouse` w ON b.warehouse = w.name
        JOIN `tabItem` it ON b.item_code = it.name
        WHERE b.actual_qty > 0
        ORDER BY w.warehouse_name, b.item_code
    """
    stock_rows = frappe.db.sql(stock_query, as_dict=True)

    # 2. Tồn theo Lô và Hạn sử dụng (FEFO)
    batch_query = """
        SELECT 
            b.name as batch_id,
            b.item,
            it.item_name,
            it.brand,
            COALESCE(it.custom_product_line, CASE 
                WHEN b.item LIKE '%%PLUS%%' THEN 'PLUS'
                WHEN b.item LIKE '%%CACAO%%' THEN 'CACAO'
                WHEN b.item LIKE '%%TIBOKA%%' THEN 'TIBOKA'
                ELSE 'Khác' END) as product_line,
            b.manufacturing_date,
            b.expiry_date,
            DATEDIFF(b.expiry_date, %(today)s) as days_to_expire
        FROM `tabBatch` b
        JOIN `tabItem` it ON b.item = it.name
        ORDER BY b.expiry_date ASC
    """
    batches = frappe.db.sql(batch_query, {"today": today}, as_dict=True)

    near_expiry_batches = []
    expired_batches = []
    normal_batches = []

    for b in batches:
        days = cint(b.days_to_expire)
        if days < 0:
            b["status"] = "ĐÃ HẾT HẠN"
            b["alert_level"] = "danger"
            expired_batches.append(b)
        elif days <= 60:
            b["status"] = f"CẬN DATE (Còn {days} ngày)"
            b["alert_level"] = "warning"
            near_expiry_batches.append(b)
        else:
            b["status"] = f"An toàn (Còn {days} ngày)"
            b["alert_level"] = "success"
            normal_batches.append(b)

    # 3. Phân nhóm kho
    central_stock = [r for r in stock_rows if r.custom_warehouse_type == "Central" or r.warehouse == CENTRAL_WAREHOUSE]
    employee_stock = [r for r in stock_rows if r.custom_warehouse_type == "Employee" or "Kho NVKD" in r.warehouse_name]
    quarantine_stock = [r for r in stock_rows if r.custom_warehouse_type == "Quarantine" or r.warehouse == QUARANTINE_WAREHOUSE]
    damaged_stock = [r for r in stock_rows if r.custom_warehouse_type == "Damaged" or r.warehouse == DAMAGED_WAREHOUSE]

    # 4. Tiền NVKD đang thu hộ chờ nộp (Tài khoản 1113)
    cash_in_hand = frappe.db.sql("""
        SELECT SUM(debit - credit) as total_held
        FROM `tabGL Entry`
        WHERE account = '1113 - Tiền thu hộ của NVKD - B' AND is_cancelled = 0
    """, as_dict=True)[0].total_held or 0.0

    return {
        "today": today,
        "brand_name": "BAKA",
        "summary": {
            "total_items_in_stock": sum(flt(r.actual_qty) for r in stock_rows),
            "total_stock_value": sum(flt(r.stock_value) for r in stock_rows),
            "central_warehouse_qty": sum(flt(r.actual_qty) for r in central_stock),
            "employee_warehouses_qty": sum(flt(r.actual_qty) for r in employee_stock),
            "quarantine_qty": sum(flt(r.actual_qty) for r in quarantine_stock),
            "damaged_qty": sum(flt(r.actual_qty) for r in damaged_stock),
            "near_expiry_count": len(near_expiry_batches),
            "expired_count": len(expired_batches),
            "employee_cash_held": flt(cash_in_hand)
        },
        "batches": {
            "near_expiry": near_expiry_batches,
            "expired": expired_batches,
            "safe": normal_batches
        },
        "employee_warehouses": employee_stock,
        "stock_details": stock_rows
    }


# ----------------------------------------------------------------------
# CSV / EXCEL IMPORT SERVICE (ĐƠN HÀNG ĐA KÊNH & SÀN TMĐT)
# ----------------------------------------------------------------------
@frappe.whitelist()
def import_orders_from_csv(csv_content, default_channel="TikTok Shop"):
    """
    Hỗ trợ nhập đơn hàng đa kênh từ nội dung file CSV/Excel:
    Các cột: order_id, channel, customer, item_code, qty, rate, platform_fee, shipping_fee, sales_person
    Tự động kiểm tra trùng lặp và ghi nhận doanh thu / xuất kho tương ứng.
    """
    import io
    import csv

    f = io.StringIO(csv_content.strip())
    reader = csv.DictReader(f)
    results = {"success": [], "skipped": [], "errors": []}

    for row in reader:
        try:
            order_id = row.get("order_id") or row.get("Mã đơn")
            if not order_id:
                continue
            channel = row.get("channel") or row.get("Kênh bán") or default_channel
            customer = row.get("customer") or row.get("Khách hàng") or f"Khách mua {channel}"
            item_code = row.get("item_code") or row.get("Mã SP") or "TBK-PLUS"
            qty = flt(row.get("qty") or row.get("Số lượng") or 1)
            rate = flt(row.get("rate") or row.get("Đơn giá") or 365000)
            platform_fee = flt(row.get("platform_fee") or row.get("Phí sàn") or 0)
            shipping_fee = flt(row.get("shipping_fee") or row.get("Phí ship") or 0)
            sales_person = row.get("sales_person") or row.get("NVKD")

            order_date = row.get("order_date") or row.get("Ngày") or nowdate()

            res = import_marketplace_order(
                channel=channel,
                order_id=order_id,
                customer_name=customer,
                items=[{"item_code": item_code, "qty": qty, "rate": rate}],
                platform_fee=platform_fee,
                shipping_fee=shipping_fee,
                order_date=order_date
            )
            if res.get("status") == "skipped":
                results["skipped"].append({"order_id": order_id, "reason": res.get("message")})
            else:
                results["success"].append({"order_id": order_id, "invoice": res.get("sales_invoice")})
        except Exception as e:
            results["errors"].append({"order_id": row.get("order_id", "unknown"), "error": str(e)})

    frappe.db.commit()
    return results
