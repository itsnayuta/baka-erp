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

    # 1. Giờ vào đầu tiên và Giờ ra gần nhất hôm nay
    today_ins = [c for c in today_checkins if c.log_type == "IN"]
    today_outs = [c for c in today_checkins if c.log_type == "OUT"]

    today_in = today_ins[0].time.strftime("%H:%M:%S") if today_ins else None
    today_out = today_outs[-1].time.strftime("%H:%M:%S") if today_outs else None

    # 2. Tính tổng thời gian làm việc hôm nay theo từng cặp ca
    cur_in = None
    today_seconds = 0
    pair_count = 0
    for l in today_checkins:
        if l.log_type == "IN":
            if cur_in is None:
                cur_in = l.time
        elif l.log_type == "OUT":
            if cur_in is not None:
                today_seconds += max(0, (l.time - cur_in).total_seconds())
                cur_in = None
                pair_count += 1
    if cur_in is not None:
        today_seconds += max(0, (now_datetime() - cur_in).total_seconds())

    if pair_count == 1 and cur_in is None and today_seconds >= 5 * 3600:
        today_seconds -= 3600

    t_h = int(today_seconds // 3600)
    t_m = int((today_seconds % 3600) // 60)
    work_hours_str = f"{t_h} giờ {t_m} phút"

    # 3. Trạng thái ca làm việc hiện tại (Hỗ trợ 2 ca / nhiều ca đan xen & giới hạn 10 lần/ngày)
    is_limit_reached = len(today_checkins) >= 10
    if is_limit_reached:
        shift_status = "LIMIT_REACHED"
        status_label = "Đã đạt giới hạn 10 lần/ngày"
        status_color = "#dc2626"
    elif not last_log:
        shift_status = "NOT_CHECKED_IN"
        status_label = "Chưa vào ca"
        status_color = "#eab308"
    elif last_log.log_type == "IN":
        shift_status = "IN_SHIFT"
        cur_shift = len(today_ins)
        status_label = f"Đang trong Ca {cur_shift}" if cur_shift > 1 else "Đang trong ca làm việc"
        status_color = "#16a34a"
    else:
        shift_status = "OUT_OF_SHIFT"
        cur_shift = len(today_outs)
        status_label = f"Đã hoàn thành Ca {cur_shift}" if cur_shift > 1 else "Đã hoàn thành ca làm việc"
        status_color = "#0284c7"

    # 4. Thống kê tổng số giờ làm việc trong tháng hiện tại
    daily_data = get_daily_work_hours_and_points(emp.name)
    month_prefix = f"{cur_year}-{cur_month}"
    month_hours_total = sum(
        d["hours"] for d_str, d in daily_data.items() if d_str.startswith(month_prefix)
    )
    month_hours_str = f"{round(month_hours_total, 1)} giờ"

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
        "shift_status": shift_status,
        "status_label": status_label,
        "status_color": status_color,
        "work_hours_str": work_hours_str,
        "month_hours_total": round(month_hours_total, 1),
        "month_hours_str": month_hours_str,
        "cur_month": cur_month,
        "is_limit_reached": is_limit_reached,
        "max_daily_logs": 10,
        "remaining_logs": max(0, 10 - len(today_checkins)),
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
    """Thực hiện Check In / Check Out với xác thực IP mạng WiFi và chống spam triệt để"""
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

    # 1. Kiểm tra giới hạn tối đa 10 lần chấm công trong ngày
    today_checkins = frappe.get_all(
        "Employee Checkin",
        filters={"employee": emp.name, "date": today},
        fields=["name", "log_type", "time", "status"],
        order_by="time asc"
    )

    if len(today_checkins) >= 10:
        frappe.throw(_("Bạn đã đạt giới hạn tối đa 10 lần chấm công trong ngày hôm nay. Vui lòng liên hệ với Ban lãnh đạo để được hỗ trợ xử lý!"))

    last_log = today_checkins[-1] if today_checkins else None

    # 2. Quản lý logic ca làm việc chuẩn (Đan xen IN -> OUT -> IN -> OUT hỗ trợ 2 ca / nhiều ca)
    if log_type == "IN":
        if last_log and last_log.log_type == "IN":
            in_time_str = last_log.time.strftime("%H:%M:%S") if hasattr(last_log.time, "strftime") else str(last_log.time)[11:19]
            frappe.throw(_(f"Bạn đang trong ca làm việc (đã chấm công VÀO lúc {in_time_str})! Vui lòng bấm 'Chấm công RA' khi kết thúc ca."))
    elif log_type == "OUT":
        if not last_log or last_log.log_type != "IN":
            frappe.throw(_("Bạn chưa chấm công VÀO ca! Vui lòng bấm 'Chấm công VÀO' trước khi bấm ra ca."))

    # 4. Tính toán trạng thái Đi muộn / Về sớm
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

    time_str = now.strftime("%H:%M:%S")

    # Tạo bản ghi mới cho lượt chấm công
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

    shift_num = len([c for c in today_checkins if c.log_type == "IN"]) + (1 if log_type == "IN" else 0)
    shift_label = f"Ca {shift_num}" if shift_num > 1 else "Ca làm việc"
    action_label = f"VÀO {shift_label}" if log_type == "IN" else f"HẾT {shift_label}"
    msg_action = "VÀO" if log_type == "IN" else "RA"

    return {
        "success": True,
        "name": checkin_doc.name,
        "log_type": log_type,
        "action_label": action_label,
        "time": time_str,
        "status": status,
        "message": f"✓ Đã chấm công {msg_action} {shift_label} lúc {time_str} thành công! (Trạng thái: {status})"
    }

def get_daily_work_hours_and_points(employee_id, year=None):
    """
    Tính số giờ làm việc thực tế và điểm chuyên cần theo từng ngày:
    - Tính theo năm (mỗi năm reset 1 lần).
    - Cứ làm đủ 8 tiếng 1 ngày = 1 điểm (số nguyên, không có phần thập phân).
    - Dưới 8 tiếng = 0 điểm.
    """
    filters = {"employee": employee_id}
    if year:
        y_str = str(year)
        filters["date"] = ["between", [f"{y_str}-01-01", f"{y_str}-12-31"]]

    checkins = frappe.get_all(
        "Employee Checkin",
        filters=filters,
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
        cur_in = None
        day_seconds = 0
        pair_count = 0
        for l in logs:
            if l.log_type == "IN":
                if cur_in is None:
                    cur_in = l.time
            elif l.log_type == "OUT":
                if cur_in is not None:
                    day_seconds += max(0, (l.time - cur_in).total_seconds())
                    cur_in = None
                    pair_count += 1

        if cur_in is not None:
            if d_str == today_str:
                day_seconds += max(0, (now - cur_in).total_seconds())
            else:
                day_seconds += 4 * 3600

        # Nếu chỉ có 1 ca duy nhất dài >= 5 tiếng (làm xuyên trưa không bấm ra), trừ 1h nghỉ trưa
        if pair_count == 1 and cur_in is None and day_seconds >= 5 * 3600:
            day_seconds -= 3600

        raw_hours = max(0.0, day_seconds / 3600.0)
        # Cứ làm đủ 8 tiếng 1 ngày = 1 điểm (số nguyên, không có phần thập phân)
        points = 1 if raw_hours >= 8.0 else 0

        result[d_str] = {
            "hours": round(raw_hours, 1),
            "points": points
        }

    return result

@frappe.whitelist()
def get_chuyen_can_summary(user=None, year=None):
    """
    Lấy tổng điểm chuyên cần tích lũy trong năm của nhân viên:
    - Tính theo năm (hết 1 năm thì reset 1 lần).
    - Cứ làm đủ 8 tiếng 1 ngày = 1 điểm (số nguyên, không có phần thập phân).
    """
    if not user:
        user = frappe.session.user
    if user == "Guest":
        return {"total_points": 0, "today_points": 0}

    cur_year = str(year) if year else nowdate()[:4]
    emp = get_employee_for_user(user)
    daily_data = get_daily_work_hours_and_points(emp.name, year=cur_year)
    total_points = sum(d["points"] for d in daily_data.values())
    today_str = nowdate()
    today_points = daily_data.get(today_str, {}).get("points", 0)

    return {
        "year": cur_year,
        "total_points": int(total_points),
        "total_points_int": int(total_points),
        "today_points": int(today_points),
        "days_worked": len(daily_data),
        "qualified_days": int(total_points)
    }

@frappe.whitelist()
def get_chuyen_can_heatmap_data(user=None, date=None):
    """
    Trả về dữ liệu heatmap điểm chuyên cần theo năm:
    - Cứ đủ 8 tiếng = 1 điểm, dưới 8 tiếng = 0 điểm.
    - Reset theo từng năm.
    """
    if not user:
        user = frappe.session.user
    if user == "Guest":
        return {}

    target_year = str(date)[:4] if date else nowdate()[:4]
    emp = get_employee_for_user(user)
    daily_data = get_daily_work_hours_and_points(emp.name, year=target_year)

    import time
    heatmap_dict = {}
    for d_str, info in daily_data.items():
        try:
            d_obj = getdate(d_str)
            ts = int(time.mktime(d_obj.timetuple()))
            # Chỉ ghi nhận điểm khi >= 1 (đủ 8 tiếng) để hiển thị ô xanh trên Heatmap
            if info["points"] >= 1:
                heatmap_dict[str(ts)] = int(info["points"])
        except Exception:
            pass

    return heatmap_dict

