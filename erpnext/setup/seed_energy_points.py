import frappe
from frappe.utils import nowdate, add_days, getdate
import random

def seed():
    print("=== Bắt đầu khởi tạo dữ liệu Điểm Năng Lượng & Chấm Công cho My Profile ===")

    # 1. Kích hoạt tính năng Energy Point Settings
    frappe.db.set_single_value("Energy Point Settings", "enabled", 1)
    frappe.db.set_single_value("Energy Point Settings", "point_allocation_periodicity", "Monthly")
    print("✓ Đã kích hoạt Energy Point Settings (enabled = 1)")

    # 2. Đảm bảo các Rule chuẩn tồn tại
    custom_rules = [
        {
            "rule_name": "Xử lý Ticket CSKH thành công",
            "reference_doctype": "Issue",
            "for_doc_event": "Custom",
            "points": 15,
            "user_field": "owner"
        },
        {
            "rule_name": "Chăm sóc khách hàng xuất sắc",
            "reference_doctype": "Issue",
            "for_doc_event": "Custom",
            "points": 20,
            "user_field": "owner"
        },
        {
            "rule_name": "Vượt chỉ tiêu doanh số",
            "reference_doctype": "Sales Order",
            "for_doc_event": "Submit",
            "points": 25,
            "user_field": "owner"
        },
        {
            "rule_name": "Phản hồi khách hàng nhanh trong 15 phút",
            "reference_doctype": "Issue",
            "for_doc_event": "Custom",
            "points": 10,
            "user_field": "owner"
        },
    ]

    for r in custom_rules:
        if not frappe.db.exists("Energy Point Rule", r["rule_name"]):
            rule_doc = frappe.get_doc({
                "doctype": "Energy Point Rule",
                "rule_name": r["rule_name"],
                "reference_doctype": r["reference_doctype"],
                "for_doc_event": r["for_doc_event"],
                "points": r["points"],
                "user_field": r["user_field"]
            })
            rule_doc.insert(ignore_permissions=True)
            print(f"✓ Đã tạo Energy Point Rule: {r['rule_name']}")

    # 3. Lấy danh sách chứng từ tham chiếu có thật
    sales_orders = frappe.get_all("Sales Order", pluck="name") or ["SO-2026-00001"]
    issues = frappe.get_all("Issue", pluck="name") or ["ISS-2026-00001"]
    customers = frappe.get_all("Customer", pluck="name") or ["Công ty Cổ phần Công nghệ An Phát"]
    leads = frappe.get_all("Lead", pluck="name") or ["Nguyễn Hoàng Long"]

    # Xóa log cũ để tạo mới đồng bộ
    frappe.db.sql("DELETE FROM `tabEnergy Point Log`")
    try:
        frappe.cache.flushall()
    except Exception:
        pass

    # Dữ liệu kịch bản điểm cho từng nhân sự
    users_config = [
        {
            "user": "sale1@baka.vn",
            "review_points": 80,
            "entries": [
                {"days_ago": 35, "type": "Auto", "points": 10, "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Tạo đơn hàng thành công"},
                {"days_ago": 30, "type": "Auto", "points": 15, "rule": "Trên Customer Tạo", "dt": "Customer", "dn": customers[0], "reason": "Phát triển khách hàng mới"},
                {"days_ago": 26, "type": "Auto", "points": 20, "rule": "On Converting Opportunity", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Chuyển đổi cơ hội thành hợp đồng"},
                {"days_ago": 22, "type": "Appreciation", "points": 40, "rule": None, "dt": "Sales Order", "dn": sales_orders[0], "owner": "coo@baka.vn", "reason": "Khen thưởng: Đàm phán thành công hợp đồng lớn"},
                {"days_ago": 18, "type": "Auto", "points": 25, "rule": "Vượt chỉ tiêu doanh số", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Đạt mốc 150 triệu doanh thu tháng trước"},
                {"days_ago": 14, "type": "Auto", "points": 15, "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Chốt thêm hợp đồng triển khai"},
                {"days_ago": 10, "type": "Appreciation", "points": 50, "rule": None, "dt": "Customer", "dn": customers[0], "owner": "chutich@baka.vn", "reason": "Khen thưởng Ban lãnh đạo: Bứt phá doanh số quý"},
                {"days_ago": 7, "type": "Auto", "points": 10, "rule": "Trên Lead Tạo", "dt": "Lead", "dn": leads[0], "reason": "Tiếp cận khách hàng tiềm năng"},
                {"days_ago": 4, "type": "Auto", "points": 25, "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Ký đơn hàng giải pháp ERP Pro"},
                {"days_ago": 2, "type": "Auto", "points": 20, "rule": "On Converting Opportunity", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Chuyển đổi thành công cơ hội lớn"},
                {"days_ago": 1, "type": "Appreciation", "points": 30, "rule": None, "dt": "Sales Order", "dn": sales_orders[0], "owner": "coo@baka.vn", "reason": "Đóng hợp đồng nhanh trước hạn"},
                {"days_ago": 0, "type": "Auto", "points": 15, "rule": "Trên Customer Tạo", "dt": "Customer", "dn": customers[0], "reason": "Mở rộng thêm tài khoản khách hàng doanh nghiệp"},
            ]
        },
        {
            "user": "cskh@baka.vn",
            "review_points": 70,
            "entries": [
                {"days_ago": 36, "type": "Auto", "points": 15, "rule": "Xử lý Ticket CSKH thành công", "dt": "Issue", "dn": issues[0], "reason": "Giải quyết sự cố phần mềm cho khách hàng trong 30 phút"},
                {"days_ago": 32, "type": "Auto", "points": 10, "rule": "Phản hồi khách hàng nhanh trong 15 phút", "dt": "Issue", "dn": issues[0], "reason": "Tiếp nhận và phản hồi tức thì yêu cầu hỗ trợ"},
                {"days_ago": 28, "type": "Appreciation", "points": 35, "rule": None, "dt": "Issue", "dn": issues[0], "owner": "coo@baka.vn", "reason": "Khách hàng phản hồi khen ngợi phong cách hỗ trợ chuyên nghiệp"},
                {"days_ago": 24, "type": "Auto", "points": 20, "rule": "Chăm sóc khách hàng xuất sắc", "dt": "Issue", "dn": issues[0], "reason": "Hoàn tất hướng dẫn đào tạo người dùng mới"},
                {"days_ago": 20, "type": "Auto", "points": 15, "rule": "Xử lý Ticket CSKH thành công", "dt": "Issue", "dn": issues[min(1, len(issues)-1)], "reason": "Xử lý xong mẫu in báo giá chữ ký số"},
                {"days_ago": 16, "type": "Appreciation", "points": 45, "rule": None, "dt": "Customer", "dn": customers[0], "owner": "chutich@baka.vn", "reason": "Khen thưởng đặc biệt: Duy trì chỉ số hài lòng khách hàng CSAT 100%"},
                {"days_ago": 12, "type": "Auto", "points": 15, "rule": "Xử lý Ticket CSKH thành công", "dt": "Issue", "dn": issues[0], "reason": "Hỗ trợ khách hàng khắc phục lỗi dữ liệu kịp thời"},
                {"days_ago": 9, "type": "Auto", "points": 20, "rule": "Chăm sóc khách hàng xuất sắc", "dt": "Customer", "dn": customers[0], "reason": "Chăm sóc định kỳ và tái ký gói dịch vụ bảo trì 24/7"},
                {"days_ago": 6, "type": "Auto", "points": 10, "rule": "Phản hồi khách hàng nhanh trong 15 phút", "dt": "Issue", "dn": issues[0], "reason": "Phản hồi tin nhắn qua hotline dưới 5 phút"},
                {"days_ago": 3, "type": "Appreciation", "points": 40, "rule": None, "dt": "Issue", "dn": issues[0], "owner": "coo@baka.vn", "reason": "Xử lý tình huống khiếu nại khéo léo, khách hàng đánh giá 5 sao"},
                {"days_ago": 1, "type": "Auto", "points": 20, "rule": "Chăm sóc khách hàng xuất sắc", "dt": "Issue", "dn": issues[0], "reason": "Hoàn thành quy trình onboarding khách hàng mới chu đáo"},
                {"days_ago": 0, "type": "Auto", "points": 15, "rule": "Xử lý Ticket CSKH thành công", "dt": "Issue", "dn": issues[0], "reason": "Giải quyết thắc mắc quy trình xuất hóa đơn"},
            ]
        },
        {
            "user": "sale2@baka.vn",
            "review_points": 50,
            "entries": [
                {"days_ago": 34, "type": "Auto", "points": 10, "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Tạo đơn hàng"},
                {"days_ago": 29, "type": "Auto", "points": 15, "rule": "Trên Customer Tạo", "dt": "Customer", "dn": customers[0], "reason": "Thêm khách hàng miền Nam"},
                {"days_ago": 21, "type": "Appreciation", "points": 35, "rule": None, "dt": "Sales Order", "dn": sales_orders[0], "owner": "coo@baka.vn", "reason": "Khen ngợi nỗ lực phát triển thị trường mới"},
                {"days_ago": 15, "type": "Auto", "points": 20, "rule": "On Converting Opportunity", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Chuyển đổi thành công hợp đồng"},
                {"days_ago": 8, "type": "Auto", "points": 25, "rule": "Vượt chỉ tiêu doanh số", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Đạt chỉ tiêu doanh thu tuần"},
                {"days_ago": 2, "type": "Appreciation", "points": 30, "rule": None, "dt": "Customer", "dn": customers[0], "owner": "chutich@baka.vn", "reason": "Mở rộng hệ thống đại lý phân phối"},
            ]
        },
        {
            "user": "sale3@baka.vn",
            "review_points": 50,
            "entries": [
                {"days_ago": 33, "type": "Auto", "points": 10, "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Ký kết hợp đồng dự án"},
                {"days_ago": 25, "type": "Auto", "points": 20, "rule": "On Converting Opportunity", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Chốt dự án cơ khí Đại Nam"},
                {"days_ago": 17, "type": "Appreciation", "points": 35, "rule": None, "dt": "Sales Order", "dn": sales_orders[0], "owner": "coo@baka.vn", "reason": "Đàm phán xuất sắc gói Enterprise"},
                {"days_ago": 9, "type": "Auto", "points": 15, "rule": "Trên Customer Tạo", "dt": "Customer", "dn": customers[0], "reason": "Tạo đối tác doanh nghiệp lớn"},
                {"days_ago": 3, "type": "Auto", "points": 20, "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Gia hạn hợp đồng dịch vụ bảo trì"},
            ]
        },
        {
            "user": "coo@baka.vn",
            "review_points": 150,
            "entries": [
                {"days_ago": 31, "type": "Auto", "points": 10, "rule": "On Task Completion", "dt": "Task", "dn": None, "reason": "Hoàn tất rà soát quy trình bán hàng"},
                {"days_ago": 23, "type": "Auto", "points": 15, "rule": "On Sales Order Submission", "dt": "Sales Order", "dn": sales_orders[0], "reason": "Phê duyệt đơn hàng lớn"},
                {"days_ago": 14, "type": "Appreciation", "points": 50, "rule": None, "dt": "Sales Order", "dn": sales_orders[0], "owner": "chutich@baka.vn", "reason": "Điều hành vận hành xuất sắc vượt mục tiêu tháng"},
                {"days_ago": 5, "type": "Auto", "points": 20, "rule": "On Task Completion", "dt": "Task", "dn": None, "reason": "Tối ưu hóa thời gian giao hàng & triển khai"},
            ]
        },
        {
            "user": "chutich@baka.vn",
            "review_points": 250,
            "entries": [
                {"days_ago": 30, "type": "Auto", "points": 10, "rule": "On Task Completion", "dt": "Task", "dn": None, "reason": "Thông qua chiến lược mở rộng kinh doanh Q4"},
                {"days_ago": 15, "type": "Auto", "points": 20, "rule": "On Task Completion", "dt": "Task", "dn": None, "reason": "Ký kết thỏa thuận hợp tác chiến lược"},
                {"days_ago": 2, "type": "Auto", "points": 30, "rule": "On Task Completion", "dt": "Task", "dn": None, "reason": "Hoàn thành đánh giá hiệu quả vận hành toàn công ty"},
            ]
        }
    ]

    for u_conf in users_config:
        u = u_conf["user"]
        if not frappe.db.exists("User", u):
            continue

        # Điểm Review (dùng để tặng người khác)
        rev_log = frappe.get_doc({
            "doctype": "Energy Point Log",
            "user": u,
            "points": u_conf["review_points"],
            "type": "Review",
            "reason": "Phân bổ điểm đánh giá & khen thưởng hàng tháng từ Hệ thống Quản trị",
            "owner": "Administrator",
            "creation": add_days(nowdate(), -1)
        })
        rev_log.flags.ignore_permissions = True
        rev_log.insert(ignore_permissions=True)

        # Các điểm Năng Lượng theo thời gian
        for ent in u_conf["entries"]:
            log_date = add_days(nowdate(), -ent["days_ago"]) + " 09:30:00"
            log_doc = frappe.get_doc({
                "doctype": "Energy Point Log",
                "user": u,
                "points": ent["points"],
                "type": ent["type"],
                "rule": ent.get("rule"),
                "reference_doctype": ent.get("dt"),
                "reference_name": ent.get("dn"),
                "reason": ent.get("reason"),
                "owner": ent.get("owner") or "Administrator",
                "creation": log_date,
                "modified": log_date
            })
            log_doc.flags.ignore_permissions = True
            log_doc.insert(ignore_permissions=True)
            # Cập nhật chính xác ngày giờ creation trong DB để Heatmap và biểu đồ hiển thị đúng timeline
            frappe.db.set_value("Energy Point Log", log_doc.name, "creation", log_date, update_modified=False)

        print(f"✓ Đã nạp dữ liệu Điểm Năng Lượng cho: {u}")

    # 4. Khởi tạo dữ liệu Chấm Công thực tế cho tháng này
    # Lấy các ngày làm việc trong tháng hiện tại (từ ngày 01 đến hôm nay)
    today = getdate(nowdate())
    cur_year = today.year
    cur_month = today.month

    # Xóa checkin cũ để tạo bộ dữ liệu sạch
    frappe.db.sql("DELETE FROM `tabEmployee Checkin`")

    sample_employees = [
        {"user": "cskh@baka.vn", "name": "Phạm Thu Hà"},
        {"user": "sale1@baka.vn", "name": "Nguyễn Văn Nam"},
        {"user": "sale2@baka.vn", "name": "Trần Thị Mai"},
        {"user": "sale3@baka.vn", "name": "Lê Hoàng Quân"},
        {"user": "coo@baka.vn", "name": "Trần Vận Hành"},
    ]

    from erpnext.setup.wifi_attendance import get_employee_for_user

    for emp_info in sample_employees:
        if not frappe.db.exists("User", emp_info["user"]):
            continue
        emp = get_employee_for_user(emp_info["user"])

        # Tạo lịch sử chấm công cho các ngày từ ngày 1 đến ngày hôm nay
        for day in range(1, today.day + 1):
            date_str = f"{cur_year:04d}-{cur_month:02d}-{day:02d}"
            d_obj = getdate(date_str)
            # Bỏ qua Chủ nhật (weekday = 6)
            if d_obj.weekday() == 6:
                continue

            # Đi muộn vào một vài ngày ngẫu nhiên để thống kê hiển thị thực tế
            is_late = (day in [3, 8])
            in_minute = random.randint(35, 45) if is_late else random.randint(15, 28)
            in_second = random.randint(10, 55)
            status_in = "Đi muộn" if is_late else "Hợp lệ"
            in_time_str = f"{date_str} 08:{in_minute:02d}:{in_second:02d}"

            # Log VÀO (IN)
            checkin_in = frappe.get_doc({
                "doctype": "Employee Checkin",
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "log_type": "IN",
                "time": in_time_str,
                "date": date_str,
                "ip_address": "127.0.0.1",
                "wifi_ssid": "BAKA-OFFICE-5G",
                "status": status_in,
                "device_info": "Chrome / Windows 11 BAKA-PC"
            })
            checkin_in.insert(ignore_permissions=True)

            # Log RA (OUT) - Nếu là ngày hôm nay thì chỉ check-in vào, hoặc check-out nếu chiều
            if day < today.day:
                out_minute = random.randint(31, 45)
                out_second = random.randint(10, 55)
                out_time_str = f"{date_str} 17:{out_minute:02d}:{out_second:02d}"
                checkin_out = frappe.get_doc({
                    "doctype": "Employee Checkin",
                    "employee": emp.name,
                    "employee_name": emp.employee_name,
                    "log_type": "OUT",
                    "time": out_time_str,
                    "date": date_str,
                    "ip_address": "127.0.0.1",
                    "wifi_ssid": "BAKA-OFFICE-5G",
                    "status": "Hợp lệ",
                    "device_info": "Chrome / Windows 11 BAKA-PC"
                })
                checkin_out.insert(ignore_permissions=True)

        print(f"✓ Đã nạp lịch sử chấm công tháng này cho: {emp.employee_name} ({emp_info['user']})")

    frappe.db.commit()
    print("=== Hoàn tất nạp dữ liệu Điểm Năng Lượng & Chấm Công mẫu ===")
