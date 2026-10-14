# Copyright (c) 2026, BAKA and contributors
# Unified Simulation Script for Beverage Company (Thức Uống Dinh Dưỡng)
# Products: Tinh bột kháng PLUS (365k), Tinh bột kháng CACAO (265k), Tinh bột kháng TIBOKA (250k)
# Department: 1 COO Admin, 2 Sales, 1 Warehouse Manager, plus Chủ tịch

import frappe
from frappe.utils import nowdate, add_days, getdate
from frappe.utils.password import update_password
from erpnext.setup.wifi_attendance import get_employee_for_user
import random

COMPANY = "BAKA"
WAREHOUSE = "Finished Goods - B"

def run():
    print("==================================================================")
    print("=== BẮT ĐẦU MÔ PHỎNG DỮ LIỆU ĐỒNG NHẤT THÁNG 10/2026 CHO BAKA ===")
    print("==================================================================")

    # 1. Lọc bỏ toàn bộ dữ liệu giao dịch cũ, item cũ, khách hàng cũ
    purge_all_old_data()

    # 2. Thiết lập 4 tài khoản phòng ban chuẩn (+ Chủ tịch) và vô hiệu hóa tài khoản thừa
    setup_department_users()

    # 3. Tạo 3 sản phẩm thức uống (Tinh bột kháng) chuẩn giá
    setup_products()

    # 4. Nhập kho ban đầu ngày 01/10/2026 (Quản lý kho thực hiện)
    setup_opening_stock()

    # 5. Tạo khách hàng và mô phỏng luồng bán hàng thống nhất tháng 10
    setup_customers_and_sales_flow()

    # 6. Mô phỏng chấm công Wifi & Điểm chuyên cần tháng 10 (01/10 - 14/10)
    setup_attendance_october()

    # 7. Phân bổ Điểm đánh giá (Energy Points) tháng 10
    setup_energy_points_october()

    # Đảm bảo file Frappe backend user_profile.py luôn trả về Điểm chuyên cần cho Heatmap
    patch_frappe_files()

    frappe.db.commit()
    print("==================================================================")
    print("=== HOÀN TẤT TOÀN BỘ MÔ PHỎNG HỆ THỐNG DOANH NGHIỆP THÁNG 10 ===")
    print("==================================================================")


def purge_all_old_data():
    print("\n[1/7] Lọc bỏ dữ liệu mẫu, giao dịch và cấu hình cũ...")
    tables_to_purge = [
        "tabPayment Entry Reference", "tabPayment Entry Deduction", "tabPayment Entry",
        "tabSales Invoice Item", "tabSales Invoice",
        "tabDelivery Note Item", "tabDelivery Note",
        "tabSales Order Item", "tabSales Order",
        "tabQuotation Item", "tabQuotation",
        "tabStock Entry Detail", "tabStock Entry",
        "tabStock Ledger Entry", "tabGL Entry", "tabBin",
        "tabEnergy Point Log", "tabEmployee Checkin",
        "tabIssue", "tabOpportunity", "tabLead",
        "tabItem Price"
    ]
    for tbl in tables_to_purge:
        try:
            frappe.db.sql(f"DELETE FROM `{tbl}`")
        except Exception as e:
            print(f"! Bỏ qua {tbl}: {e}")

    # Xóa các Item cũ không thuộc công ty
    frappe.db.sql("DELETE FROM `tabItem`")
    frappe.db.sql("DELETE FROM `tabCustomer`")
    frappe.db.sql("DELETE FROM `tabAddress`")
    frappe.db.sql("DELETE FROM `tabContact`")
    frappe.db.sql("DELETE FROM `tabDynamic Link`")
    try:
        frappe.cache.flushall()
    except Exception:
        pass
    print("✓ Đã xóa sạch toàn bộ giao dịch, hóa đơn, tồn kho, khách hàng và sản phẩm cũ.")


def setup_department_users():
    print("\n[2/7] Cấu hình 4 tài khoản phòng ban (+ Chủ tịch) & phân quyền chuẩn...")

    # Vai trò toàn quyền điều hành cho Admin / Giám đốc Vận hành
    full_manager_roles = [
        "System Manager", "Stock Manager", "Sales Master Manager", "Sales Manager",
        "Accounts Manager", "HR Manager", "Report Manager", "Dashboard Manager",
        "Workspace Manager", "Desk User", "Stock User", "Sales User", "Employee"
    ]

    dept_users = [
        {
            "email": "coo@baka.vn",
            "first_name": "Trần",
            "last_name": "Vận Hành",
            "designation": "Giám đốc Vận hành",
            "roles": full_manager_roles,
            "bio": "Giám đốc Vận hành (COO) - Quản trị viên điều hành toàn quyền hệ thống BAKAERP"
        },
        {
            "email": "sale1@baka.vn",
            "first_name": "Nguyễn Văn",
            "last_name": "Nam",
            "designation": "Chuyên viên Kinh doanh 1",
            "roles": ["Sales User", "Stock User", "Desk User", "Employee"],
            "bio": "Nhân viên Kinh doanh 01 - Phụ trách thị trường Miền Bắc & Nhà phân phối"
        },
        {
            "email": "sale2@baka.vn",
            "first_name": "Trần Thị",
            "last_name": "Mai",
            "designation": "Chuyên viên Kinh doanh 2",
            "roles": ["Sales User", "Stock User", "Desk User", "Employee"],
            "bio": "Nhân viên Kinh doanh 02 - Phụ trách thị trường Miền Nam & Chuỗi bán lẻ"
        },
        {
            "email": "kho@baka.vn",
            "first_name": "Phạm",
            "last_name": "Quản Kho",
            "designation": "Quản lý Kho",
            "roles": ["Stock Manager", "Stock User", "Desk User", "Employee"],
            "bio": "Quản lý Kho - Quản lý xuất nhập tồn kho, kiểm kê hàng hóa thành phẩm"
        },
        {
            "email": "chutich@baka.vn",
            "first_name": "Bùi",
            "last_name": "Chủ Tịch",
            "designation": "Chủ tịch Hội đồng Quản trị",
            "roles": full_manager_roles,
            "bio": "Chủ tịch Hội đồng Quản trị - Giám sát cấp cao toàn diện"
        }
    ]

    # Danh sách các tài khoản cũ cần vô hiệu hóa
    unused_emails = [
        "sale3@baka.vn", "cskh@baka.vn", "giamdoc@baka.vn", "ketoan@baka.vn",
        "banhang@baka.vn", "muahang@baka.vn", "sanxuat@baka.vn", "nhansu@baka.vn"
    ]
    for un_mail in unused_emails:
        if frappe.db.exists("User", un_mail):
            frappe.db.set_value("User", un_mail, "enabled", 0)
        if frappe.db.exists("Employee", {"user_id": un_mail}):
            frappe.db.set_value("Employee", {"user_id": un_mail}, "status", "Left")
    print(f"✓ Đã vô hiệu hóa các tài khoản không thuộc phòng ban: {', '.join(unused_emails)}")

    # Tạo và cập nhật 5 tài khoản hoạt động
    for u in dept_users:
        email = u["email"]
        if not frappe.db.exists("User", email):
            user_doc = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": u["first_name"],
                "last_name": u["last_name"],
                "enabled": 1,
                "send_welcome_email": 0,
                "language": "vi",
                "user_type": "System User",
                "bio": u["bio"]
            })
            user_doc.insert(ignore_permissions=True)
        else:
            user_doc = frappe.get_doc("User", email)
            user_doc.enabled = 1
            user_doc.first_name = u["first_name"]
            user_doc.last_name = u["last_name"]
            user_doc.bio = u["bio"]
            user_doc.save(ignore_permissions=True)

        # Cài đặt mật khẩu chuẩn 123
        update_password(email, "123")
        frappe.db.set_value("User", email, "language", "vi")

        # Gán Roles
        for role in u["roles"]:
            if frappe.db.exists("Role", role) and not frappe.db.exists("Has Role", {"parent": email, "role": role}):
                frappe.get_doc({
                    "doctype": "Has Role",
                    "parent": email,
                    "parenttype": "User",
                    "parentfield": "roles",
                    "role": role
                }).insert(ignore_permissions=True)

        # Hồ sơ Nhân viên (Employee)
        emp_name = frappe.db.get_value("Employee", {"user_id": email}, "name")
        full_name = f"{u['first_name']} {u['last_name']}".strip()
        if not emp_name:
            emp = frappe.get_doc({
                "doctype": "Employee",
                "first_name": u["first_name"],
                "last_name": u["last_name"],
                "employee_name": full_name,
                "user_id": email,
                "company": COMPANY,
                "designation": u["designation"],
                "status": "Active",
                "gender": "Male" if "Mai" not in u["last_name"] else "Female",
                "date_of_birth": "1992-05-15",
                "date_of_joining": "2025-01-01",
                "employment_type": "Full-time"
            })
            emp.flags.ignore_mandatory = True
            emp.insert(ignore_permissions=True)
        else:
            frappe.db.set_value("Employee", emp_name, {
                "employee_name": full_name,
                "designation": u["designation"],
                "status": "Active"
            })

        print(f"✓ Tài khoản: {email} ({full_name}) - {u['designation']} - Mật khẩu: 123")


def setup_products():
    print("\n[3/7] Cấu hình 3 sản phẩm thức uống (Tinh bột kháng)...")

    # Đơn vị tính: Hộp
    if not frappe.db.exists("UOM", "Hộp"):
        frappe.get_doc({
            "doctype": "UOM",
            "uom_name": "Hộp",
            "must_be_whole_number": 1
        }).insert(ignore_permissions=True)

    # Nhóm sản phẩm: Thức uống dinh dưỡng
    if not frappe.db.exists("Item Group", "Thức uống dinh dưỡng"):
        frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": "Thức uống dinh dưỡng",
            "parent_item_group": "Products",
            "is_group": 0
        }).insert(ignore_permissions=True)

    products = [
        {
            "item_code": "TBK-PLUS",
            "item_name": "Tinh bột kháng PLUS",
            "standard_rate": 365000,
            "valuation_rate": 200000,
            "description": "Tinh bột kháng PLUS - Thức uống dinh dưỡng tăng cường hệ vi sinh đường ruột và đề kháng."
        },
        {
            "item_code": "TBK-CACAO",
            "item_name": "Tinh bột kháng CACAO",
            "standard_rate": 265000,
            "valuation_rate": 150000,
            "description": "Tinh bột kháng vị CACAO thơm ngon tự nhiên, giàu chất xơ hòa tan."
        },
        {
            "item_code": "TBK-TIBOKA",
            "item_name": "Tinh bột kháng TIBOKA",
            "standard_rate": 250000,
            "valuation_rate": 140000,
            "description": "Tinh bột kháng TIBOKA - Dòng sản phẩm tiêu chuẩn bổ sung dinh dưỡng hàng ngày cho cả gia đình."
        }
    ]

    # Đảm bảo Price List Standard Selling và Standard Buying là VND
    for pl in ["Standard Selling", "Standard Buying"]:
        if frappe.db.exists("Price List", pl):
            frappe.db.set_value("Price List", pl, "currency", "VND")

    for p in products:
        code = p["item_code"]
        if not frappe.db.exists("Item", code):
            doc = frappe.get_doc({
                "doctype": "Item",
                "item_code": code,
                "item_name": p["item_name"],
                "item_group": "Thức uống dinh dưỡng",
                "stock_uom": "Hộp",
                "is_stock_item": 1,
                "is_sales_item": 1,
                "is_purchase_item": 1,
                "standard_rate": p["standard_rate"],
                "valuation_rate": p["valuation_rate"],
                "description": p["description"]
            })
            doc.insert(ignore_permissions=True)
        else:
            doc = frappe.get_doc("Item", code)
            doc.item_name = p["item_name"]
            doc.standard_rate = p["standard_rate"]
            doc.valuation_rate = p["valuation_rate"]
            doc.save(ignore_permissions=True)

        # Bảng giá Standard Selling
        ip_name = frappe.db.get_value("Item Price", {"item_code": code, "price_list": "Standard Selling"})
        if not ip_name:
            frappe.get_doc({
                "doctype": "Item Price",
                "item_code": code,
                "price_list": "Standard Selling",
                "price_list_rate": p["standard_rate"],
                "currency": "VND"
            }).insert(ignore_permissions=True)
        else:
            frappe.db.set_value("Item Price", ip_name, "price_list_rate", p["standard_rate"])
            frappe.db.set_value("Item Price", ip_name, "currency", "VND")

        print(f"✓ Đã tạo sản phẩm: {code} - {p['item_name']} - Giá bán: {p['standard_rate']:,} VND (UOM: Hộp)")


def setup_opening_stock():
    print("\n[4/7] Khởi tạo tồn kho ban đầu ngày 01/10/2026 (Quản lý kho: kho@baka.vn)...")

    se = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Material Receipt",
        "purpose": "Material Receipt",
        "company": COMPANY,
        "set_posting_time": 1,
        "posting_date": "2026-10-01",
        "posting_time": "08:00:00",
        "to_warehouse": WAREHOUSE,
        "owner": "kho@baka.vn",
        "remarks": "Nhập kho thành phẩm ban đầu đầu tháng 10/2026 - Quản lý kho: Phạm Quản Kho",
        "items": [
            {
                "item_code": "TBK-PLUS",
                "qty": 500,
                "uom": "Hộp",
                "stock_uom": "Hộp",
                "conversion_factor": 1.0,
                "basic_rate": 200000,
                "t_warehouse": WAREHOUSE,
                "cost_center": "Main - B"
            },
            {
                "item_code": "TBK-CACAO",
                "qty": 500,
                "uom": "Hộp",
                "stock_uom": "Hộp",
                "conversion_factor": 1.0,
                "basic_rate": 150000,
                "t_warehouse": WAREHOUSE,
                "cost_center": "Main - B"
            },
            {
                "item_code": "TBK-TIBOKA",
                "qty": 600,
                "uom": "Hộp",
                "stock_uom": "Hộp",
                "conversion_factor": 1.0,
                "basic_rate": 140000,
                "t_warehouse": WAREHOUSE,
                "cost_center": "Main - B"
            }
        ]
    })
    se.insert(ignore_permissions=True)
    se.submit()
    print("✓ Đã nhập kho thành phẩm ban đầu: 500 PLUS, 500 CACAO, 600 TIBOKA vào 'Finished Goods - B' (Tổng 1.600 hộp, 259.000.000 đ).")


def setup_customers_and_sales_flow():
    print("\n[5/7] Tạo khách hàng & mô phỏng luồng bán hàng thống nhất tháng 10...")

    customers = [
        {"customer_name": "Đại lý Dinh Dưỡng Xanh (Hà Nội)", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam"},
        {"customer_name": "Chuỗi Thực Phẩm Sạch Healthy Mart (TP.HCM)", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam"},
        {"customer_name": "Nhà Thuốc & Dược Phẩm An Tâm (Đà Nẵng)", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam"},
        {"customer_name": "Cửa Hàng Thực Dưỡng Tâm An (Hà Nội)", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam"},
        {"customer_name": "Chị Nguyễn Thị Lan (Khách sỉ)", "customer_group": "Individual", "customer_type": "Individual", "territory": "Vietnam"}
    ]

    for c in customers:
        c_name = c["customer_name"]
        if not frappe.db.exists("Customer", c_name):
            cust = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": c_name,
                "customer_group": c["customer_group"],
                "customer_type": c["customer_type"],
                "territory": c["territory"],
                "company": COMPANY
            })
            cust.insert(ignore_permissions=True)
    print("✓ Đã tạo danh sách khách hàng & đại lý phân phối thức uống.")

    from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note, make_sales_invoice
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

    # Kịch bản 7 đơn hàng thực tế trải dài từ 02/10 đến 14/10/2026:
    orders_scenario = [
        {
            "so_date": "2026-10-02",
            "customer": "Đại lý Dinh Dưỡng Xanh (Hà Nội)",
            "sales_user": "sale1@baka.vn",
            "items": [
                {"item_code": "TBK-PLUS", "qty": 50, "rate": 365000},
                {"item_code": "TBK-CACAO", "qty": 40, "rate": 265000}
            ],
            "dn_date": "2026-10-03",
            "si_date": "2026-10-03",
            "pe_date": "2026-10-04",
            "is_paid": True,
            "desc": "Đơn số 1: Đại lý Dinh Dưỡng Xanh (Sale 1) - Hoàn tất giao hàng & thanh toán"
        },
        {
            "so_date": "2026-10-04",
            "customer": "Chuỗi Thực Phẩm Sạch Healthy Mart (TP.HCM)",
            "sales_user": "sale2@baka.vn",
            "items": [
                {"item_code": "TBK-PLUS", "qty": 60, "rate": 365000},
                {"item_code": "TBK-TIBOKA", "qty": 50, "rate": 250000}
            ],
            "dn_date": "2026-10-05",
            "si_date": "2026-10-05",
            "pe_date": "2026-10-06",
            "is_paid": True,
            "desc": "Đơn số 2: Chuỗi Healthy Mart (Sale 2) - Hoàn tất giao hàng & thanh toán"
        },
        {
            "so_date": "2026-10-06",
            "customer": "Nhà Thuốc & Dược Phẩm An Tâm (Đà Nẵng)",
            "sales_user": "sale1@baka.vn",
            "items": [
                {"item_code": "TBK-PLUS", "qty": 40, "rate": 365000},
                {"item_code": "TBK-CACAO", "qty": 40, "rate": 265000},
                {"item_code": "TBK-TIBOKA", "qty": 40, "rate": 250000}
            ],
            "dn_date": "2026-10-07",
            "si_date": "2026-10-07",
            "pe_date": "2026-10-08",
            "is_paid": True,
            "desc": "Đơn số 3: Nhà Thuốc An Tâm (Sale 1) - Hoàn tất giao hàng & thanh toán"
        },
        {
            "so_date": "2026-10-09",
            "customer": "Cửa Hàng Thực Dưỡng Tâm An (Hà Nội)",
            "sales_user": "sale2@baka.vn",
            "items": [
                {"item_code": "TBK-CACAO", "qty": 30, "rate": 265000},
                {"item_code": "TBK-TIBOKA", "qty": 30, "rate": 250000}
            ],
            "dn_date": "2026-10-10",
            "si_date": "2026-10-10",
            "pe_date": "2026-10-11",
            "is_paid": True,
            "desc": "Đơn số 4: Thực Dưỡng Tâm An (Sale 2) - Hoàn tất giao hàng & thanh toán"
        },
        {
            "so_date": "2026-10-12",
            "customer": "Chị Nguyễn Thị Lan (Khách sỉ)",
            "sales_user": "sale1@baka.vn",
            "items": [
                {"item_code": "TBK-PLUS", "qty": 10, "rate": 365000},
                {"item_code": "TBK-CACAO", "qty": 5, "rate": 265000}
            ],
            "dn_date": "2026-10-12",
            "si_date": "2026-10-12",
            "pe_date": "2026-10-13",
            "is_paid": True,
            "desc": "Đơn số 5: Chị Nguyễn Thị Lan (Sale 1) - Hoàn tất giao hàng & thanh toán"
        },
        {
            "so_date": "2026-10-13",
            "customer": "Chuỗi Thực Phẩm Sạch Healthy Mart (TP.HCM)",
            "sales_user": "sale2@baka.vn",
            "items": [
                {"item_code": "TBK-PLUS", "qty": 80, "rate": 365000},
                {"item_code": "TBK-CACAO", "qty": 60, "rate": 265000}
            ],
            "dn_date": None,
            "si_date": None,
            "pe_date": None,
            "is_paid": False,
            "desc": "Đơn số 6: Healthy Mart (Sale 2) - Đơn hàng lớn 45,1 triệu đã duyệt, đang chờ Quản lý kho xuất hàng"
        },
        {
            "so_date": "2026-10-14",
            "customer": "Đại lý Dinh Dưỡng Xanh (Hà Nội)",
            "sales_user": "sale1@baka.vn",
            "items": [
                {"item_code": "TBK-TIBOKA", "qty": 50, "rate": 250000}
            ],
            "dn_date": None,
            "si_date": None,
            "pe_date": None,
            "is_paid": False,
            "desc": "Đơn số 7: Đại lý Dinh Dưỡng Xanh (Sale 1) - Đơn hàng mới tạo sáng nay 14/10/2026"
        }
    ]

    for ord_info in orders_scenario:
        # 1. Tạo Sales Order
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "company": COMPANY,
            "customer": ord_info["customer"],
            "transaction_date": ord_info["so_date"],
            "delivery_date": add_days(ord_info["so_date"], 2),
            "order_type": "Sales",
            "currency": "VND",
            "price_list_currency": "VND",
            "plc_conversion_rate": 1.0,
            "conversion_rate": 1.0,
            "selling_price_list": "Standard Selling",
            "owner": ord_info["sales_user"],
            "items": [
                {
                    "item_code": it["item_code"],
                    "qty": it["qty"],
                    "rate": it["rate"],
                    "delivery_date": add_days(ord_info["so_date"], 2),
                    "warehouse": WAREHOUSE
                }
                for it in ord_info["items"]
            ]
        })
        so.insert(ignore_permissions=True)
        so.submit()

        # 2. Tạo Delivery Note (Quản lý kho xuất hàng) nếu đơn hàng đã giao
        if ord_info["dn_date"]:
            dn = make_delivery_note(so.name)
            dn.set_posting_time = 1
            dn.posting_date = ord_info["dn_date"]
            dn.posting_time = "10:30:00"
            dn.owner = "kho@baka.vn"
            dn.insert(ignore_permissions=True)
            dn.submit()

            # 3. Tạo Sales Invoice
            si = make_sales_invoice(so.name)
            si.set_posting_time = 1
            si.posting_date = ord_info["si_date"]
            si.due_date = add_days(ord_info["si_date"], 7)
            si.payment_schedule = []
            si.insert(ignore_permissions=True)
            si.submit()

            # 4. Tạo Payment Entry (Khách hàng thanh toán)
            if ord_info["is_paid"]:
                pe = get_payment_entry("Sales Invoice", si.name)
                pe.set_posting_time = 1
                pe.posting_date = ord_info["pe_date"]
                pe.mode_of_payment = "Wire Transfer"
                pe.paid_to = "1121 - Tiền gửi ngân hàng (VND) - B"
                pe.reference_no = f"UNC-202610-{so.name[-4:]}"
                pe.reference_date = ord_info["pe_date"]
                pe.insert(ignore_permissions=True)
                pe.submit()

        print(f"✓ {ord_info['desc']}")


def setup_attendance_october():
    print("\n[6/7] Khởi tạo dữ liệu Chấm Công Wifi & Điểm chuyên cần tháng 10 (01/10 - 14/10)...")
    frappe.db.sql("DELETE FROM `tabEmployee Checkin`")

    active_users = [
        "coo@baka.vn", "sale1@baka.vn", "sale2@baka.vn", "kho@baka.vn", "chutich@baka.vn"
    ]

    for u in active_users:
        emp = get_employee_for_user(u)

        # Lịch sử chấm công từ ngày 01/10/2026 đến ngày 14/10/2026
        for day in range(1, 15):
            date_str = f"2026-10-{day:02d}"
            d_obj = getdate(date_str)

            # Bỏ qua Chủ nhật (weekday = 6)
            if d_obj.weekday() == 6:
                continue

            # Thứ 7 (weekday = 5): Làm nửa ngày 4 tiếng (08:30 -> 12:30 -> 4 điểm)
            if d_obj.weekday() == 5:
                in_time = f"{date_str} 08:30:15"
                out_time = f"{date_str} 12:30:45"
            else:
                # Ngày thường: Đủ ca chuẩn ~8.3 tiếng (trừ 1h trưa -> 8.0 Điểm chuyên cần)
                in_m = random.randint(15, 25)
                in_s = random.randint(10, 50)
                in_time = f"{date_str} 08:{in_m:02d}:{in_s:02d}"

                out_m = random.randint(35, 48)
                out_s = random.randint(10, 50)
                out_time = f"{date_str} 17:{out_m:02d}:{out_s:02d}"

            # Checkin IN
            cin = frappe.get_doc({
                "doctype": "Employee Checkin",
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "log_type": "IN",
                "time": in_time,
                "date": date_str,
                "ip_address": "127.0.0.1",
                "wifi_ssid": "BAKA-OFFICE-5G",
                "status": "Hợp lệ",
                "device_info": "Chrome / Windows 11 BAKA-PC"
            })
            cin.insert(ignore_permissions=True)

            # Checkin OUT: Ngày hôm nay (14/10) chỉ chấm vào buổi sáng để user có thể bấm test nút Chấm công RA
            if day < 14:
                cout = frappe.get_doc({
                    "doctype": "Employee Checkin",
                    "employee": emp.name,
                    "employee_name": emp.employee_name,
                    "log_type": "OUT",
                    "time": out_time,
                    "date": date_str,
                    "ip_address": "127.0.0.1",
                    "wifi_ssid": "BAKA-OFFICE-5G",
                    "status": "Hợp lệ",
                    "device_info": "Chrome / Windows 11 BAKA-PC"
                })
                cout.insert(ignore_permissions=True)

        print(f"✓ Đã nạp chấm công Wifi tháng 10 cho: {emp.employee_name} ({u})")


def setup_energy_points_october():
    print("\n[7/7] Khởi tạo Điểm đánh giá (Energy Points) tháng 10...")
    frappe.db.sql("DELETE FROM `tabEnergy Point Log`")

    # Kích hoạt Energy Point Settings
    frappe.db.set_single_value("Energy Point Settings", "enabled", 1)
    frappe.db.set_single_value("Energy Point Settings", "point_allocation_periodicity", "Monthly")

    # Lấy Sales Orders thực tế vừa tạo để liên kết chứng từ
    sales_orders = frappe.get_all("Sales Order", pluck="name") or ["SO-2026-00001"]

    energy_scenarios = [
        {
            "user": "sale1@baka.vn",
            "review_points": 50,
            "entries": [
                {"date": "2026-10-02 11:30:00", "points": 25, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Chốt đơn hàng thành công Đại lý Dinh Dưỡng Xanh"},
                {"date": "2026-10-06 14:20:00", "points": 25, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[min(2, len(sales_orders)-1)], "reason": "Ký đơn hàng phân phối Nhà Thuốc An Tâm"},
                {"date": "2026-10-12 16:00:00", "points": 15, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[min(4, len(sales_orders)-1)], "reason": "Chăm sóc và chốt đơn sỉ Chị Nguyễn Thị Lan"},
                {"date": "2026-10-14 09:15:00", "points": 20, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[-1], "reason": "Tạo đơn hàng mới đầu tuần TIBOKA"},
            ]
        },
        {
            "user": "sale2@baka.vn",
            "review_points": 50,
            "entries": [
                {"date": "2026-10-04 10:45:00", "points": 25, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[min(1, len(sales_orders)-1)], "reason": "Chốt đơn chuỗi thực phẩm sạch Healthy Mart"},
                {"date": "2026-10-09 15:30:00", "points": 20, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[min(3, len(sales_orders)-1)], "reason": "Ký đơn hàng Thực Dưỡng Tâm An"},
                {"date": "2026-10-13 16:45:00", "points": 35, "type": "Appreciation", "rule": None, "dt": "Sales Order", "dn": sales_orders[min(5, len(sales_orders)-1)], "owner": "coo@baka.vn", "reason": "Khen thưởng: Đàm phán xuất sắc đơn hàng lớn 45 triệu Healthy Mart"},
            ]
        },
        {
            "user": "kho@baka.vn",
            "review_points": 30,
            "entries": [
                {"date": "2026-10-01 09:30:00", "points": 20, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Tiếp nhận và nhập kho hoàn tất 1.600 hộp thành phẩm chính xác"},
                {"date": "2026-10-05 11:00:00", "points": 15, "type": "Appreciation", "rule": None, "dt": "Sales Order", "dn": sales_orders[1], "owner": "coo@baka.vn", "reason": "Đóng gói và xuất hàng siêu tốc cho đơn Healthy Mart"},
                {"date": "2026-10-10 14:00:00", "points": 15, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[3], "reason": "Xuất kho giao hàng đúng hẹn không sai lệch"},
            ]
        },
        {
            "user": "coo@baka.vn",
            "review_points": 100,
            "entries": [
                {"date": "2026-10-01 10:00:00", "points": 50, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Phê duyệt kế hoạch bán hàng & tồn kho tháng 10"},
                {"date": "2026-10-08 17:00:00", "points": 50, "type": "Appreciation", "rule": None, "dt": "Sales Order", "dn": sales_orders[2], "owner": "chutich@baka.vn", "reason": "Lãnh đạo xuất sắc: Vận hành trơn tru chuỗi cung ứng thức uống"},
            ]
        },
        {
            "user": "chutich@baka.vn",
            "review_points": 200,
            "entries": [
                {"date": "2026-10-01 09:00:00", "points": 100, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Thông qua chiến lược phát triển 3 dòng sản phẩm Tinh bột kháng"},
                {"date": "2026-10-10 17:00:00", "points": 100, "type": "Auto", "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[3], "reason": "Khen thưởng và đánh giá hiệu quả tháng 10 toàn bộ phận"},
            ]
        }
    ]

    for u_conf in energy_scenarios:
        u = u_conf["user"]
        if not frappe.db.exists("User", u):
            continue

        # Điểm Review cấp phát
        rev_log = frappe.get_doc({
            "doctype": "Energy Point Log",
            "user": u,
            "points": u_conf["review_points"],
            "type": "Review",
            "reason": "Phân bổ điểm đánh giá & khen thưởng tháng 10/2026",
            "owner": "Administrator",
            "creation": "2026-10-01 08:00:00"
        })
        rev_log.flags.ignore_permissions = True
        rev_log.flags.ignore_notification = True
        rev_log.insert(ignore_permissions=True)

        for ent in u_conf["entries"]:
            log_doc = frappe.get_doc({
                "doctype": "Energy Point Log",
                "user": u,
                "points": ent["points"],
                "type": ent["type"],
                "rule": ent.get("rule"),
                "reference_doctype": ent.get("dt") or "Sales Order",
                "reference_name": ent.get("dn") or sales_orders[0],
                "reason": ent.get("reason"),
                "owner": ent.get("owner") or "Administrator",
                "creation": ent["date"],
                "modified": ent["date"]
            })
            log_doc.flags.ignore_permissions = True
            log_doc.flags.ignore_notification = True
            log_doc.insert(ignore_permissions=True)
            frappe.db.set_value("Energy Point Log", log_doc.name, "creation", ent["date"], update_modified=False)

        print(f"✓ Đã cấp Điểm đánh giá tháng 10 cho: {u}")


def patch_frappe_files():
    # 1. Patch user_profile_controller.js
    js_path = "/home/frappe/frappe-bench/apps/frappe/frappe/desk/page/user_profile/user_profile_controller.js"
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            js_code = f.read()
        target_js = 'countLabel: __("Energy Points"),'
        replacement_js = 'countLabel: __("Điểm chuyên cần"),'
        if target_js in js_code:
            js_code = js_code.replace(target_js, replacement_js)
            with open(js_path, "w", encoding="utf-8") as f:
                f.write(js_code)
            print("✓ Đã cập nhật countLabel thành 'Điểm chuyên cần' trong user_profile_controller.js")
    except Exception as e:
        print("! Bỏ qua patch js:", e)

    # 2. Patch user_profile.py
    py_path = "/home/frappe/frappe-bench/apps/frappe/frappe/desk/page/user_profile/user_profile.py"
    try:
        with open(py_path, "r", encoding="utf-8") as f:
            py_code = f.read()

        import re
        new_func = '''@frappe.whitelist()
def get_energy_points_heatmap_data(user: str, date: str | None = None):
	try:
		from erpnext.setup.wifi_attendance import get_chuyen_can_heatmap_data
		return get_chuyen_can_heatmap_data(user, date)
	except Exception:
		return {}'''

        py_code = re.sub(
            r'@frappe\.whitelist\(\)\s*def get_energy_points_heatmap_data\([^)]*\):.*?(?=@frappe\.whitelist\(\)|$)',
            new_func + '\n\n\n',
            py_code,
            flags=re.DOTALL
        )
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(py_code)
        print("✓ Đã cập nhật get_energy_points_heatmap_data trong user_profile.py")
    except Exception as e:
        print("! Bỏ qua patch py:", e)

