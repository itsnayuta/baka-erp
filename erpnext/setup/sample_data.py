import frappe
from frappe.utils import nowdate, add_days, add_months
from frappe.utils.password import update_password

def run():
    print("=== Đang thiết lập dữ liệu mẫu và mô phỏng hệ thống BAKAERP ===")
    company = "BAKA"
    frappe.db.set_value("Company", company, "round_off_cost_center", "Main - B")

    # 1. Tạo các tài khoản người dùng chuẩn theo cơ cấu doanh nghiệp
    full_executive_roles = [
        r for r in frappe.get_all("Role", filters={"disabled": 0}, pluck="name")
        if r not in ["Customer", "Supplier", "Guest", "Administrator"]
    ]

    users = [
        {
            "email": "chutich@baka.vn",
            "first_name": "Bùi",
            "last_name": "Chủ Tịch",
            "roles": full_executive_roles,
            "bio": "Chủ tịch Hội đồng Quản trị - Quyền quản trị tối cao, kiểm soát toàn bộ hệ thống"
        },
        {
            "email": "coo@baka.vn",
            "first_name": "Trần",
            "last_name": "Vận Hành",
            "roles": full_executive_roles,
            "bio": "Giám đốc Vận hành (COO) - Điều phối bán hàng, duyệt đơn, giám sát tiến độ"
        },
        {
            "email": "sale1@baka.vn",
            "first_name": "Nguyễn Văn",
            "last_name": "Nam",
            "roles": ["Sales User", "Desk User"],
            "bio": "Kinh doanh 01 - Phụ trách thị trường Miền Bắc"
        },
        {
            "email": "sale2@baka.vn",
            "first_name": "Trần Thị",
            "last_name": "Mai",
            "roles": ["Sales User", "Desk User"],
            "bio": "Kinh doanh 02 - Phụ trách thị trường Miền Nam"
        },
        {
            "email": "sale3@baka.vn",
            "first_name": "Lê Hoàng",
            "last_name": "Quân",
            "roles": ["Sales User", "Desk User"],
            "bio": "Kinh doanh 03 - Phụ trách Khách hàng Doanh nghiệp lớn & Dự án"
        },
        {
            "email": "cskh@baka.vn",
            "first_name": "Phạm Thu",
            "last_name": "Hà",
            "roles": ["Support User", "Sales User", "Desk User"],
            "bio": "Chăm sóc khách hàng - Tiếp nhận hỗ trợ, ticket, hậu mãi"
        },
    ]

    for u in users:
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
            print(f"✓ Đã tạo tài khoản: {email}")
        else:
            user_doc = frappe.get_doc("User", email)
            user_doc.enabled = 1
            user_doc.first_name = u["first_name"]
            user_doc.last_name = u["last_name"]
            user_doc.save(ignore_permissions=True)

        # Cập nhật Roles
        for role in u["roles"]:
            if frappe.db.exists("Role", role) and not frappe.db.exists("Has Role", {"parent": email, "role": role}):
                frappe.get_doc({
                    "doctype": "Has Role",
                    "parent": email,
                    "parenttype": "User",
                    "parentfield": "roles",
                    "role": role
                }).insert(ignore_permissions=True)

        # Cài đặt mật khẩu đồng bộ 123
        update_password(email, "123")
        frappe.db.set_value("User", email, "language", "vi")

    # 2. Tạo Danh mục sản phẩm / Dịch vụ (Item)
    items_data = [
        {
            "item_code": "BAKA-PRO",
            "item_name": "Phần mềm BAKAERP Pro (Bản quyền 12 tháng)",
            "item_group": "Services",
            "standard_rate": 36000000,
            "description": "Gói phần mềm BAKAERP bản quyền 12 tháng cho doanh nghiệp vừa và nhỏ."
        },
        {
            "item_code": "BAKA-ENT",
            "item_name": "Phần mềm BAKAERP Enterprise (Bản quyền 12 tháng)",
            "item_group": "Services",
            "standard_rate": 85000000,
            "description": "Gói phần mềm BAKAERP Enterprise đầy đủ tính năng mở rộng."
        },
        {
            "item_code": "DV-TRIENKHAI",
            "item_name": "Dịch vụ Triển khai, Cấu hình & Đào tạo tận nơi",
            "item_group": "Services",
            "standard_rate": 25000000,
            "description": "Chuyên gia BAKA đến tận doanh nghiệp khảo sát, đào tạo và chuyển giao vận hành."
        },
        {
            "item_code": "DV-TUHOA",
            "item_name": "Tư vấn Tối ưu Quy trình & Tự động hóa Doanh nghiệp",
            "item_group": "Services",
            "standard_rate": 50000000,
            "description": "Tư vấn tinh gọn quy trình bán hàng, vận hành và quản trị nhân sự."
        },
        {
            "item_code": "DV-BAOTRI",
            "item_name": "Gói Hỗ trợ Kỹ thuật & Bảo trì 24/7 (Gói 1 năm)",
            "item_group": "Services",
            "standard_rate": 18000000,
            "description": "Cam kết SLA phản hồi dưới 30 phút, backup dữ liệu hàng ngày."
        }
    ]

    for item in items_data:
        code = item["item_code"]
        if not frappe.db.exists("Item", code):
            doc = frappe.get_doc({
                "doctype": "Item",
                "item_code": code,
                "item_name": item["item_name"],
                "item_group": item["item_group"],
                "stock_uom": "Unit",
                "is_stock_item": 0,
                "is_sales_item": 1,
                "is_purchase_item": 0,
                "standard_rate": item["standard_rate"],
                "description": item["description"]
            })
            doc.insert(ignore_permissions=True)
            print(f"✓ Đã tạo sản phẩm/dịch vụ: {code} - {item['item_name']}")

    # 3. Tạo Khách hàng tiềm năng (Leads)
    leads_data = [
        {"lead_name": "Nguyễn Hoàng Long", "company_name": "Công ty TNHH Vận tải Long Vũ", "email_id": "longvu@gmail.com", "phone": "0912345678", "lead_owner": "sale3@baka.vn", "status": "Lead"},
        {"lead_name": "Đỗ Minh Trí", "company_name": "Công ty CP Truyền thông Sen Vàng", "email_id": "tri.do@senvang.vn", "phone": "0987654321", "lead_owner": "sale1@baka.vn", "status": "Open"},
        {"lead_name": "Hoàng Thu Thảo", "company_name": "Chuỗi Thời trang Thảo My", "email_id": "thaomy@thaomyfashion.com", "phone": "0905123456", "lead_owner": "sale2@baka.vn", "status": "Interested"},
    ]

    for ld in leads_data:
        if not frappe.db.exists("Lead", {"email_id": ld["email_id"]}):
            doc = frappe.get_doc({
                "doctype": "Lead",
                "lead_name": ld["lead_name"],
                "company_name": ld["company_name"],
                "email_id": ld["email_id"],
                "mobile_no": ld["phone"],
                "lead_owner": ld["lead_owner"],
                "status": ld["status"],
                "country": "Vietnam"
            })
            doc.insert(ignore_permissions=True)
    # 3.1 Đảm bảo Territory Vietnam tồn tại
    if not frappe.db.exists("Territory", "Vietnam"):
        frappe.get_doc({
            "doctype": "Territory",
            "territory_name": "Vietnam",
            "parent_territory": "All Territories",
            "is_group": 0
        }).insert(ignore_permissions=True)
        print("✓ Đã tạo Territory: Vietnam")

    # 4. Tạo Khách hàng chính thức (Customers)
    customers_data = [
        {"customer_name": "Công ty Cổ phần Công nghệ An Phát", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam", "owner": "sale1@baka.vn"},
        {"customer_name": "Tập đoàn Bất động sản Thịnh Phát", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam", "owner": "sale2@baka.vn"},
        {"customer_name": "Công ty TNHH Sản xuất Cơ khí Đại Nam", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam", "owner": "sale3@baka.vn"},
        {"customer_name": "Chuỗi Cửa hàng Bán lẻ Minh Tâm", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam", "owner": "sale1@baka.vn"},
        {"customer_name": "Công ty CP Vận tải Giao Hàng Xanh", "customer_group": "Commercial", "customer_type": "Company", "territory": "Vietnam", "owner": "sale2@baka.vn"},
    ]

    for cust in customers_data:
        name = cust["customer_name"]
        if not frappe.db.exists("Customer", name):
            doc = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": name,
                "customer_group": cust["customer_group"],
                "customer_type": cust["customer_type"],
                "territory": cust["territory"],
                "owner": cust["owner"]
            })
            doc.insert(ignore_permissions=True)
            print(f"✓ Đã tạo Khách hàng: {name}")

    # 5. Tạo Báo giá mở (Quotations - đang đàm phán)
    quotes_data = [
        {
            "customer": "Chuỗi Cửa hàng Bán lẻ Minh Tâm",
            "owner": "sale1@baka.vn",
            "items": [{"item_code": "BAKA-PRO", "qty": 1, "rate": 36000000}, {"item_code": "DV-TRIENKHAI", "qty": 1, "rate": 20000000}]
        },
        {
            "customer": "Công ty CP Vận tải Giao Hàng Xanh",
            "owner": "sale2@baka.vn",
            "items": [{"item_code": "BAKA-ENT", "qty": 1, "rate": 80000000}, {"item_code": "DV-TUHOA", "qty": 1, "rate": 45000000}]
        }
    ]

    for q in quotes_data:
        if not frappe.db.exists("Quotation", {"party_name": q["customer"]}):
            q_doc = frappe.get_doc({
                "doctype": "Quotation",
                "party_name": q["customer"],
                "quotation_to": "Customer",
                "transaction_date": nowdate(),
                "order_type": "Sales",
                "company": company,
                "owner": q["owner"],
                "items": q["items"]
            })
            q_doc.insert(ignore_permissions=True)
            print(f"✓ Đã tạo Báo giá cho: {q['customer']}")

    # 6. Tạo Đơn hàng bán (Sales Orders - Đã chốt hợp đồng) trải dài các tháng
    orders_data = [
        {
            "customer": "Công ty Cổ phần Công nghệ An Phát",
            "date": add_months(nowdate(), -2),
            "owner": "sale1@baka.vn",
            "items": [{"item_code": "BAKA-PRO", "qty": 1, "rate": 36000000}, {"item_code": "DV-TRIENKHAI", "qty": 1, "rate": 25000000}]
        },
        {
            "customer": "Tập đoàn Bất động sản Thịnh Phát",
            "date": add_months(nowdate(), -1),
            "owner": "sale2@baka.vn",
            "items": [{"item_code": "BAKA-ENT", "qty": 2, "rate": 85000000}, {"item_code": "DV-TUHOA", "qty": 1, "rate": 50000000}]
        },
        {
            "customer": "Công ty TNHH Sản xuất Cơ khí Đại Nam",
            "date": nowdate(),
            "owner": "sale3@baka.vn",
            "items": [{"item_code": "BAKA-ENT", "qty": 1, "rate": 85000000}, {"item_code": "DV-TRIENKHAI", "qty": 1, "rate": 25000000}, {"item_code": "DV-BAOTRI", "qty": 1, "rate": 18000000}]
        }
    ]

    for ord_info in orders_data:
        if not frappe.db.exists("Sales Order", {"customer": ord_info["customer"]}):
            so = frappe.get_doc({
                "doctype": "Sales Order",
                "customer": ord_info["customer"],
                "transaction_date": ord_info["date"],
                "delivery_date": add_days(ord_info["date"], 15),
                "company": company,
                "owner": ord_info["owner"],
                "items": ord_info["items"]
            })
            so.insert(ignore_permissions=True)
            so.submit()
            print(f"✓ Đã tạo & Duyệt Đơn hàng bán ({so.name}) cho {ord_info['customer']} (Tổng: {so.grand_total:,.0f} VND)")

            # Tạo Hóa đơn bán hàng từ Sales Order
            from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
            sinv = make_sales_invoice(so.name)
            sinv.set_posting_time = 1
            sinv.posting_date = ord_info["date"]
            sinv.due_date = add_days(ord_info["date"], 30)
            sinv.insert(ignore_permissions=True)
            sinv.submit()
            print(f"  -> Đã lập Hóa đơn bán hàng: {sinv.name} ({sinv.grand_total:,.0f} VND)")

            # Thu tiền 2 khách hàng đầu để có doanh thu tiền vào tài khoản
            if ord_info["customer"] in ["Công ty Cổ phần Công nghệ An Phát", "Tập đoàn Bất động sản Thịnh Phát"]:
                from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
                pe = get_payment_entry("Sales Invoice", sinv.name)
                pe.posting_date = ord_info["date"]
                pe.paid_to = "1121 - Tiền gửi ngân hàng (VND) - B"
                pe.reference_no = f"UNC-{sinv.name}"
                pe.reference_date = ord_info["date"]
                pe.insert(ignore_permissions=True)
                pe.submit()
                print(f"  -> Đã ghi nhận thu tiền qua Ngân hàng ({pe.name}): {pe.paid_amount:,.0f} VND")

    # 7. Tạo Sự vụ CSKH (Support Issues / Tickets)
    issues_data = [
        {
            "subject": "Yêu cầu hỗ trợ hướng dẫn thiết kế mẫu in Báo giá có chữ ký số",
            "customer": "Công ty Cổ phần Công nghệ An Phát",
            "raised_by": "anphat@tech.vn",
            "status": "Closed",
            "priority": "Medium",
            "description": "Khách hàng muốn tùy biến mẫu in Báo giá hiển thị con dấu đỏ và chữ ký số giám đốc."
        },
        {
            "subject": "Khách hàng đề nghị đào tạo thêm cho 3 nhân viên kinh doanh mới",
            "customer": "Tập đoàn Bất động sản Thịnh Phát",
            "raised_by": "hr@thinhphatland.com",
            "status": "Replied",
            "priority": "High",
            "description": "Thịnh Phát mới tuyển thêm 3 bạn sale, nhờ BAKA xếp lịch training online vào chiều thứ 6."
        },
        {
            "subject": "Khách hàng quan tâm và đề xuất nâng cấp lên gói Enterprise",
            "customer": "Công ty TNHH Sản xuất Cơ khí Đại Nam",
            "raised_by": "ceo@dainam.vn",
            "status": "Open",
            "priority": "High",
            "description": "Đại Nam muốn tích hợp thêm cổng thanh toán và quản lý đa chi nhánh, cần Sale tư vấn gói Enterprise."
        }
    ]

    for iss in issues_data:
        if not frappe.db.exists("Issue", {"subject": iss["subject"]}):
            i_doc = frappe.get_doc({
                "doctype": "Issue",
                "subject": iss["subject"],
                "customer": iss["customer"],
                "raised_by": iss["raised_by"],
                "status": iss["status"],
                "priority": iss["priority"],
                "owner": "cskh@baka.vn",
                "description": iss["description"]
            })
            i_doc.insert(ignore_permissions=True)
            print(f"✓ Đã tạo Ticket CSKH: {iss['subject']} [{iss['status']}]")

    frappe.db.commit()
    print("=== Hoàn tất tạo dữ liệu mẫu và mô phỏng hệ thống ===")
