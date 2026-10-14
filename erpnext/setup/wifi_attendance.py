import frappe
from frappe import _
from frappe.utils import now_datetime, nowdate, getdate, get_time, time_diff_in_hours
import fnmatch

def get_client_ip():
    try:
        if hasattr(frappe.local, "request_ip") and frappe.local.request_ip:
            return frappe.local.request_ip
        if hasattr(frappe.local, "request") and frappe.local.request:
            if frappe.get_request_header("X-Forwarded-For"):
                return (frappe.get_request_header("X-Forwarded-For").split(",", 1)[0]).strip()
            if hasattr(frappe.local.request, "remote_addr"):
                return frappe.local.request.remote_addr
    except Exception:
        pass
    return "127.0.0.1"

def is_ip_allowed(client_ip, allowed_ips_str):
    if not allowed_ips_str:
        return True
    patterns = []
    for line in allowed_ips_str.replace(",", "\n").splitlines():
        p = line.strip()
        if p:
            patterns.append(p)
    if not patterns or "*" in patterns:
        return True
    
    for pat in patterns:
        if pat == client_ip:
            return True
        if fnmatch.fnmatch(client_ip, pat):
            return True
        # Prefix match like 192.168.1.
        if pat.endswith(".") and client_ip.startswith(pat):
            return True
        # Wildcard prefix
        if "*" in pat and fnmatch.fnmatch(client_ip, pat):
            return True
    return False

def get_employee_for_user(user=None):
    if not user:
        user = frappe.session.user
    emp_name = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not emp_name:
        # Tự động tạo hồ sơ nhân viên nếu chưa có
        u = frappe.get_doc("User", user)
        full_name = f"{u.first_name or ''} {u.last_name or ''}".strip() or user
        emp = frappe.get_doc({
            "doctype": "Employee",
            "first_name": u.first_name or full_name,
            "last_name": u.last_name or "",
            "employee_name": full_name,
            "user_id": user,
            "company": "BAKA",
            "status": "Active",
            "gender": "Male",
            "date_of_birth": "1995-01-01",
            "date_of_joining": "2025-01-01",
            "employment_type": "Full-time"
        })
        emp.flags.ignore_mandatory = True
        emp.insert(ignore_permissions=True)
        emp_name = emp.name
    return frappe.get_doc("Employee", emp_name)

@frappe.whitelist()
def get_attendance_status(user=None):
    """Lấy toàn bộ trạng thái WiFi, chấm công hôm nay và tổng quan tháng của nhân viên"""
    if not user:
        user = frappe.session.user
    if user == "Guest":
        return {}

    emp = get_employee_for_user(user)
    client_ip = get_client_ip()

    settings = frappe.get_single("Attendance Settings")
    wifi_ssid = settings.wifi_ssid or "BAKA-OFFICE-5G"
    allowed_ips = settings.allowed_ips or "*"
    enable_wifi_check = int(settings.enable_wifi_check or 0)
    is_wifi_ok = (not enable_wifi_check) or is_ip_allowed(client_ip, allowed_ips)

    today = nowdate()
    today_checkins = frappe.get_all(
        "Employee Checkin",
        filters={"employee": emp.name, "date": today},
        fields=["name", "log_type", "time", "status", "ip_address", "wifi_ssid"],
        order_by="time asc"
    )

    today_in = None
    today_out = None
    for c in today_checkins:
        t_str = c.time.strftime("%H:%M:%S") if hasattr(c.time, "strftime") else str(c.time)[11:19]
        if c.log_type == "IN" and not today_in:
            today_in = t_str
        elif c.log_type == "OUT":
            today_out = t_str

    last_log = today_checkins[-1] if today_checkins else None
    last_log_dict = None
    if last_log:
        last_log_dict = {
            "type": last_log.log_type,
            "time": last_log.time.strftime("%H:%M:%S") if hasattr(last_log.time, "strftime") else str(last_log.time)[11:19],
            "status": last_log.status
        }

    # Thống kê tháng hiện tại
    cur_year = today[:4]
    cur_month = today[5:7]
    month_start = f"{cur_year}-{cur_month}-01"
    
    monthly_logs = frappe.get_all(
        "Employee Checkin",
        filters={"employee": emp.name, "date": [">=", month_start]},
        fields=["name", "date", "log_type", "status"]
    )

    worked_dates = set([str(l.date) for l in monthly_logs if l.log_type == "IN"])
    late_count = len([l for l in monthly_logs if l.log_type == "IN" and l.status == "Đi muộn"])
    early_count = len([l for l in monthly_logs if l.log_type == "OUT" and l.status == "Về sớm"])
    total_days = len(worked_dates)
    on_time_count = max(0, total_days - late_count)

    return {
        "employee_id": emp.name,
        "employee_name": emp.employee_name,
        "designation": emp.designation or "Nhân viên",
        "client_ip": client_ip,
        "wifi_ssid": wifi_ssid,
        "is_wifi_ok": is_wifi_ok,
        "enable_wifi_check": enable_wifi_check,
        "today_date": today,
        "today_in": today_in,
        "today_out": today_out,
        "last_log": last_log_dict,
        "today_logs_count": len(today_checkins),
        "today_logs": [
            {
                "type": c.log_type,
                "time": c.time.strftime("%H:%M:%S") if hasattr(c.time, "strftime") else str(c.time)[11:19],
                "status": c.status
            }
            for c in today_checkins
        ],
        "stats": {
            "total_days": total_days,
            "on_time_count": on_time_count,
            "late_count": late_count,
            "early_count": early_count
        }
    }

@frappe.whitelist()
def checkin(log_type="IN"):
    """Thực hiện Check In / Check Out với xác thực IP mạng WiFi"""
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Vui lòng đăng nhập để chấm công!"))

    log_type = (log_type or "IN").upper()
    if log_type not in ["IN", "OUT"]:
        frappe.throw(_("Loại chấm công không hợp lệ (chỉ chấp nhận IN hoặc OUT)."))

    settings = frappe.get_single("Attendance Settings")
    wifi_ssid = settings.wifi_ssid or "BAKA-OFFICE-5G"
    allowed_ips = settings.allowed_ips or "*"
    enable_wifi_check = int(settings.enable_wifi_check or 0)
    client_ip = get_client_ip()

    if enable_wifi_check and not is_ip_allowed(client_ip, allowed_ips):
        frappe.throw(
            _(f"Chấm công thất bại! Bạn phải kết nối vào mạng WiFi công ty '{wifi_ssid}' để chấm công. Địa chỉ IP hiện tại của bạn là {client_ip}, không thuộc dải WiFi văn phòng.")
        )

    emp = get_employee_for_user(user)
    now = now_datetime()
    today = nowdate()

    # Tính toán trạng thái Đi muộn / Về sớm
    status = "Hợp lệ"
    now_time = now.time()

    if log_type == "IN":
        work_start = get_time(settings.work_start_time or "08:30:00")
        grace = int(settings.late_grace_minutes or 15)
        import datetime
        limit_time = (datetime.datetime.combine(datetime.date.today(), work_start) + datetime.timedelta(minutes=grace)).time()
        if now_time > limit_time:
            status = "Đi muộn"
    elif log_type == "OUT":
        work_end = get_time(settings.work_end_time or "17:30:00")
        if now_time < work_end:
            status = "Về sớm"

    # Lấy thông tin thiết bị (User-Agent)
    user_agent = ""
    try:
        user_agent = frappe.get_request_header("User-Agent") or ""
    except Exception:
        pass
    if len(user_agent) > 140:
        user_agent = user_agent[:140]

    checkin_doc = frappe.get_doc({
        "doctype": "Employee Checkin",
        "employee": emp.name,
        "employee_name": emp.employee_name,
        "log_type": log_type,
        "time": now,
        "date": today,
        "ip_address": client_ip,
        "wifi_ssid": wifi_ssid,
        "status": status,
        "device_info": user_agent
    })
    checkin_doc.insert(ignore_permissions=True)
    frappe.db.commit()

    action_label = "VÀO CA (Check In)" if log_type == "IN" else "HẾT CA (Check Out)"
    time_str = now.strftime("%H:%M:%S")

    return {
        "success": True,
        "name": checkin_doc.name,
        "log_type": log_type,
        "action_label": action_label,
        "time": time_str,
        "status": status,
        "message": f"✓ Đã ghi nhận {action_label} thành công lúc {time_str}! (Trạng thái: {status})"
    }

def get_daily_work_hours_and_points(employee_id):
    """
    Tính số giờ làm việc thực tế và điểm chuyên cần theo từng ngày:
    - Cứ tích lũy 1 tiếng làm trong ngày là 1 điểm.
    - Càng nhiều điểm ô trên Heatmap sẽ càng xanh.
    - Tối đa 8 điểm 1 ngày.
    """
    checkins = frappe.get_all(
        "Employee Checkin",
        filters={"employee": employee_id},
        fields=["name", "date", "time", "log_type"],
        order_by="time asc"
    )

    by_date = {}
    for c in checkins:
        d_str = str(c.date)
        if d_str not in by_date:
            by_date[d_str] = []
        by_date[d_str].append(c)

    result = {}
    now = now_datetime()
    today_str = nowdate()

    for d_str, logs in by_date.items():
        ins = [l.time for l in logs if l.log_type == "IN"]
        outs = [l.time for l in logs if l.log_type == "OUT"]

        if not ins:
            continue

        first_in = min(ins)
        last_out = max(outs) if outs else None

        if last_out:
            work_seconds = (last_out - first_in).total_seconds()
        elif d_str == today_str:
            work_seconds = (now - first_in).total_seconds()
        else:
            work_seconds = 8 * 3600

        raw_hours = max(0.0, work_seconds / 3600.0)
        # Giảm trừ 1h nghỉ trưa nếu ca làm việc >= 5h
        effective_hours = raw_hours - 1.0 if raw_hours >= 5.0 else raw_hours
        # 1 tiếng = 1 điểm, tối đa 8 điểm/ngày
        points = round(min(8.0, max(0.0, effective_hours)), 1)

        result[d_str] = {
            "hours": round(effective_hours, 2),
            "points": points
        }

    return result

@frappe.whitelist()
def get_chuyen_can_summary(user=None):
    """Lấy tổng điểm chuyên cần tích lũy của nhân viên"""
    if not user:
        user = frappe.session.user
    if user == "Guest":
        return {"total_points": 0, "today_points": 0}

    emp = get_employee_for_user(user)
    daily_data = get_daily_work_hours_and_points(emp.name)
    total_points = sum(d["points"] for d in daily_data.values())
    today_str = nowdate()
    today_points = daily_data.get(today_str, {}).get("points", 0.0)

    return {
        "total_points": round(total_points, 1),
        "total_points_int": int(round(total_points)),
        "today_points": round(today_points, 1),
        "days_worked": len(daily_data)
    }

@frappe.whitelist()
def get_chuyen_can_heatmap_data(user=None, date=None):
    """Trả về dữ liệu heatmap điểm chuyên cần (1 tiếng làm = 1 điểm, tối đa 8 điểm/ngày)"""
    if not user:
        user = frappe.session.user
    if user == "Guest":
        return {}

    emp = get_employee_for_user(user)
    daily_data = get_daily_work_hours_and_points(emp.name)

    import time
    heatmap_dict = {}
    for d_str, info in daily_data.items():
        try:
            d_obj = getdate(d_str)
            ts = int(time.mktime(d_obj.timetuple()))
            heatmap_dict[str(ts)] = info["points"]
        except Exception:
            pass

    return heatmap_dict

