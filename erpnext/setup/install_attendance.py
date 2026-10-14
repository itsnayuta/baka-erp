import frappe

def setup():
    print("=== Cài đặt phân hệ Chấm công WiFi BAKAERP ===")

    # 1. Tạo DocType Attendance Settings (Cấu hình chấm công)
    if not frappe.db.exists("DocType", "Attendance Settings"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Attendance Settings",
            "module": "Setup",
            "custom": 1,
            "issingle": 1,
            "fields": [
                {
                    "fieldname": "sec_wifi",
                    "fieldtype": "Section Break",
                    "label": "Cấu hình Mạng WiFi Công ty"
                },
                {
                    "fieldname": "enable_wifi_check",
                    "fieldtype": "Check",
                    "label": "Bắt buộc kết nối WiFi công ty mới được chấm công",
                    "default": "1"
                },
                {
                    "fieldname": "wifi_ssid",
                    "fieldtype": "Data",
                    "label": "Tên mạng WiFi công ty (SSID)",
                    "default": "BAKA-OFFICE-5G",
                    "reqd": 1
                },
                {
                    "fieldname": "allowed_ips",
                    "fieldtype": "Small Text",
                    "label": "Danh sách IP hoặc Dải IP WiFi được phép (phân cách bằng dấu phẩy hoặc xuống dòng)",
                    "default": "127.0.0.1\n192.168.*\n10.*\n172.*\n*",
                    "description": "Nhập IP hoặc dải IP (hỗ trợ ký tự đại diện *). Nhập * để cho phép mọi mạng khi test."
                },
                {
                    "fieldname": "sec_time",
                    "fieldtype": "Section Break",
                    "label": "Quy định Giờ làm việc"
                },
                {
                    "fieldname": "work_start_time",
                    "fieldtype": "Time",
                    "label": "Giờ bắt đầu làm việc",
                    "default": "08:30:00"
                },
                {
                    "fieldname": "work_end_time",
                    "fieldtype": "Time",
                    "label": "Giờ kết thúc làm việc",
                    "default": "17:30:00"
                },
                {
                    "fieldname": "late_grace_minutes",
                    "fieldtype": "Int",
                    "label": "Thời gian ân hạn đi muộn (phút)",
                    "default": "15"
                }
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1},
                {"role": "All", "read": 1, "write": 0}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("✓ Đã tạo DocType: Attendance Settings")

    # Đặt giá trị mặc định cho Attendance Settings nếu chưa có
    frappe.db.set_single_value("Attendance Settings", "wifi_ssid", "BAKA-OFFICE-5G")
    frappe.db.set_single_value("Attendance Settings", "enable_wifi_check", 1)
    if not frappe.db.get_single_value("Attendance Settings", "allowed_ips"):
        frappe.db.set_single_value("Attendance Settings", "allowed_ips", "127.0.0.1\n192.168.*\n10.*\n172.*\n*")
    frappe.db.set_single_value("Attendance Settings", "work_start_time", "08:30:00")
    frappe.db.set_single_value("Attendance Settings", "work_end_time", "17:30:00")
    frappe.db.set_single_value("Attendance Settings", "late_grace_minutes", 15)

    # 2. Tạo DocType Employee Checkin (Bản ghi chấm công)
    if not frappe.db.exists("DocType", "Employee Checkin"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Employee Checkin",
            "module": "Setup",
            "custom": 1,
            "autoname": "format:CHK-{YYYY}-{MM}-{#####}",
            "fields": [
                {
                    "fieldname": "employee",
                    "fieldtype": "Link",
                    "label": "Nhân viên",
                    "options": "Employee",
                    "reqd": 1,
                    "in_list_view": 1,
                    "in_standard_filter": 1
                },
                {
                    "fieldname": "employee_name",
                    "fieldtype": "Data",
                    "label": "Tên nhân viên",
                    "read_only": 1,
                    "in_list_view": 1
                },
                {
                    "fieldname": "log_type",
                    "fieldtype": "Select",
                    "label": "Loại chấm công",
                    "options": "IN\nOUT",
                    "reqd": 1,
                    "in_list_view": 1,
                    "in_standard_filter": 1
                },
                {
                    "fieldname": "time",
                    "fieldtype": "Datetime",
                    "label": "Thời gian chấm công",
                    "reqd": 1,
                    "in_list_view": 1,
                    "in_standard_filter": 1
                },
                {
                    "fieldname": "date",
                    "fieldtype": "Date",
                    "label": "Ngày",
                    "in_standard_filter": 1
                },
                {
                    "fieldname": "status",
                    "fieldtype": "Select",
                    "label": "Trạng thái",
                    "options": "Hợp lệ\nĐi muộn\nVề sớm\nKhông hợp lệ",
                    "default": "Hợp lệ",
                    "in_list_view": 1,
                    "in_standard_filter": 1
                },
                {
                    "fieldname": "sec_network",
                    "fieldtype": "Section Break",
                    "label": "Thông tin mạng & Thiết bị"
                },
                {
                    "fieldname": "ip_address",
                    "fieldtype": "Data",
                    "label": "Địa chỉ IP",
                    "read_only": 1,
                    "in_list_view": 1
                },
                {
                    "fieldname": "wifi_ssid",
                    "fieldtype": "Data",
                    "label": "WiFi đã kết nối",
                    "read_only": 1
                },
                {
                    "fieldname": "device_info",
                    "fieldtype": "Small Text",
                    "label": "Thông tin thiết bị",
                    "read_only": 1
                }
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Sales Manager", "read": 1, "write": 1, "create": 1},
                {"role": "All", "read": 1, "create": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("✓ Đã tạo DocType: Employee Checkin")

    # 3. Tạo hồ sơ Employee cho tất cả người dùng hiện tại
    users = frappe.get_all("User", filters={"enabled": 1, "user_type": "System User"}, fields=["name", "first_name", "last_name", "email"])
    company = "BAKA"

    for u in users:
        email = u.name
        if email in ["Guest"]:
            continue
        emp_name = frappe.db.get_value("Employee", {"user_id": email}, "name")
        full_name = f"{u.first_name or ''} {u.last_name or ''}".strip() or email
        
        designation = "Nhân viên"
        if "chutich" in email or email == "Administrator":
            designation = "Chủ tịch Hội đồng Quản trị"
        elif "coo" in email or "giamdoc" in email:
            designation = "Giám đốc Vận hành"
        elif "sale" in email or "banhang" in email:
            designation = "Chuyên viên Kinh doanh"
        elif "cskh" in email:
            designation = "Chuyên viên Chăm sóc Khách hàng"
        elif "ketoan" in email:
            designation = "Kế toán viên"

        if designation and not frappe.db.exists("Designation", designation):
            frappe.get_doc({"doctype": "Designation", "designation_name": designation}).insert(ignore_permissions=True)

        if not emp_name:
            gender = "Female" if any(k in full_name for k in ["Mai", "Hà", "Thảo"]) else "Male"
            emp = frappe.get_doc({
                "doctype": "Employee",
                "first_name": u.first_name or full_name,
                "last_name": u.last_name or "",
                "employee_name": full_name,
                "user_id": email,
                "company": company,
                "status": "Active",
                "gender": gender,
                "date_of_birth": "1995-05-15",
                "date_of_joining": "2025-01-01",
                "employment_type": "Full-time",
                "designation": designation
            })
            emp.flags.ignore_mandatory = True
            emp.insert(ignore_permissions=True)
            print(f"✓ Đã tạo Hồ sơ Nhân viên cho: {full_name} ({email}) - {designation}")
        else:
            frappe.db.set_value("Employee", emp_name, "employee_name", full_name)
            frappe.db.set_value("Employee", emp_name, "designation", designation)

    frappe.db.commit()
    print("=== Hoàn tất cài đặt phân hệ Chấm công WiFi ===")
