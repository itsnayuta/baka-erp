// Copyright (c) 2026, BAKA and contributors
// WiFi-based Employee Attendance and Check-in / Check-out Module

frappe.provide("baka.attendance");

baka.attendance = {
	status: null,

	init: function () {
		this.setup_navbar_button();
		this.setup_router_listener();
	},

	setup_navbar_button: function () {
		if ($(".baka-nav-checkin-btn").length) return;

		// Thêm nút Chấm công nhanh trên thanh Navbar góc trên bên phải
		let nav_target = $(".navbar .navbar-nav:last, header .navbar-right").first();
		if (!nav_target.length) {
			nav_target = $(".navbar").first();
		}

		if (nav_target.length && frappe.session.user !== "Guest") {
			let btn = $(`
				<li class="nav-item baka-nav-checkin-item" style="display: flex; align-items: center; margin-right: 8px;">
					<button class="btn btn-sm btn-default baka-nav-checkin-btn" style="border-radius: 16px; font-weight: 600; padding: 4px 12px; background: var(--bg-color, #fff); border: 1px solid var(--border-color, #d1d8dd); box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; align-items: center; gap: 6px; cursor: pointer;">
						<span class="indicator-pill green" style="width: 8px; height: 8px; border-radius: 50%; background: #28a745; display: inline-block;"></span>
						<span>Chấm công WiFi</span>
					</button>
				</li>
			`);
			btn.find("button").on("click", () => {
				this.open_checkin_dialog();
			});
			nav_target.prepend(btn);
		}
	},

	setup_router_listener: function () {
		frappe.router.on("change", () => {
			let current_route = frappe.get_route();
			if (current_route && current_route[0] === "user-profile") {
				setTimeout(() => {
					this.render_profile_widget();
				}, 300);
			}
		});

		// Trigger if already on user-profile
		let route = frappe.get_route();
		if (route && route[0] === "user-profile") {
			setTimeout(() => {
				this.render_profile_widget();
			}, 300);
		}
	},

	fetch_status: function (callback) {
		frappe.call({
			method: "erpnext.setup.wifi_attendance.get_attendance_status",
			callback: (r) => {
				if (r.message) {
					this.status = r.message;
					if (callback) callback(this.status);
				}
			},
		});
	},

	do_checkin: function (log_type, callback) {
		frappe.call({
			method: "erpnext.setup.wifi_attendance.checkin",
			args: { log_type: log_type },
			freeze: true,
			freeze_message: __("Đang xác thực kết nối WiFi và ghi nhận thời gian..."),
			callback: (r) => {
				if (r.message && r.message.success) {
					frappe.show_alert({
						message: r.message.message,
						indicator: "green",
					});
					this.fetch_status(() => {
						if (callback) callback(r.message);
					});
				}
			},
		});
	},

	render_profile_widget: function () {
		if ($(".baka-profile-attendance-card").length) {
			$(".baka-profile-attendance-card").remove();
		}

		let container = $(".user-profile .col-md-12").first();
		if (!container.length) return;

		this.fetch_status((s) => {
			let wifi_badge = s.is_wifi_ok
				? `<span style="background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px; display: inline-flex; align-items: center; gap: 4px;">
					<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4C7.31 4 3.07 5.9 0 8.98L12 21 24 8.98C20.93 5.9 16.69 4 12 4zm0 3.5c3.74 0 7.15 1.48 9.68 3.92L12 19.33 2.32 11.42C4.85 8.98 8.26 7.5 12 7.5z"/></svg>
					Đã kết nối WiFi: <b>${frappe.utils.escape_html(s.wifi_ssid)}</b> (IP: ${frappe.utils.escape_html(s.client_ip)})
				   </span>`
				: `<span style="background: #fce8e6; color: #c5221f; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px; display: inline-flex; align-items: center; gap: 4px;">
					<i class="fa fa-exclamation-triangle"></i>
					Chưa vào WiFi công ty (${frappe.utils.escape_html(s.wifi_ssid)}) - IP: ${frappe.utils.escape_html(s.client_ip)}
				   </span>`;

			let card_html = `
				<div class="frappe-card baka-profile-attendance-card" style="margin-bottom: 20px; border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; background: var(--card-bg, #fff); box-shadow: 0 2px 6px rgba(0,0,0,0.04); overflow: hidden;">
					<div style="padding: 16px 20px; border-bottom: 1px solid var(--border-color, #f1f5f9); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
						<div>
							<h4 style="margin: 0; font-size: 16px; font-weight: 700; color: var(--text-color, #1e293b); display: flex; align-items: center; gap: 8px;">
								<span style="font-size: 18px;">🕒</span> Chấm Công WiFi Văn Phòng
							</h4>
							<div style="font-size: 13px; color: var(--text-muted, #64748b); margin-top: 4px;">
								Hồ sơ nhân viên: <b>${frappe.utils.escape_html(s.employee_name)}</b> (${frappe.utils.escape_html(s.designation)})
							</div>
						</div>
						<div>${wifi_badge}</div>
					</div>

					<div style="padding: 20px;">
						<div class="row" style="margin-bottom: 20px;">
							<div class="col-sm-3 col-xs-6" style="margin-bottom: 10px;">
								<div style="background: var(--fg-color, #f8fafc); border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; padding: 12px; text-align: center;">
									<div style="font-size: 12px; color: var(--text-muted, #64748b);">Giờ Vào Hôm Nay</div>
									<div style="font-size: 20px; font-weight: 700; color: ${s.today_in ? "#16a34a" : "#94a3b8"}; margin-top: 4px;">
										${s.today_in || "--:--"}
									</div>
								</div>
							</div>
							<div class="col-sm-3 col-xs-6" style="margin-bottom: 10px;">
								<div style="background: var(--fg-color, #f8fafc); border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; padding: 12px; text-align: center;">
									<div style="font-size: 12px; color: var(--text-muted, #64748b);">Giờ Ra Hôm Nay</div>
									<div style="font-size: 20px; font-weight: 700; color: ${s.today_out ? "#0284c7" : "#94a3b8"}; margin-top: 4px;">
										${s.today_out || "--:--"}
									</div>
								</div>
							</div>
							<div class="col-sm-3 col-xs-6" style="margin-bottom: 10px;">
								<div style="background: var(--fg-color, #f8fafc); border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; padding: 12px; text-align: center;">
									<div style="font-size: 12px; color: var(--text-muted, #64748b);">Ngày Công Tháng Này</div>
									<div style="font-size: 20px; font-weight: 700; color: #3b82f6; margin-top: 4px;">
										${s.stats.total_days} ngày
									</div>
								</div>
							</div>
							<div class="col-sm-3 col-xs-6" style="margin-bottom: 10px;">
								<div style="background: var(--fg-color, #f8fafc); border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; padding: 12px; text-align: center;">
									<div style="font-size: 12px; color: var(--text-muted, #64748b);">Đúng Giờ / Đi Muộn</div>
									<div style="font-size: 20px; font-weight: 700; margin-top: 4px;">
										<span style="color: #16a34a;">${s.stats.on_time_count}</span> / <span style="color: #dc2626;">${s.stats.late_count}</span>
									</div>
								</div>
							</div>
						</div>

						<div style="display: flex; gap: 12px; flex-wrap: wrap;">
							<button class="btn btn-primary baka-checkin-btn" style="flex: 1; min-width: 140px; padding: 10px 20px; font-weight: 600; font-size: 14px; background: #16a34a; border-color: #16a34a;">
								<i class="fa fa-sign-in"></i> Chấm công VÀO (Check In)
							</button>
							<button class="btn btn-info baka-checkout-btn" style="flex: 1; min-width: 140px; padding: 10px 20px; font-weight: 600; font-size: 14px; background: #0284c7; border-color: #0284c7;">
								<i class="fa fa-sign-out"></i> Chấm công RA (Check Out)
							</button>
							<button class="btn btn-default baka-view-history-btn" style="padding: 10px 16px; font-weight: 500;">
								<i class="fa fa-list"></i> Xem lịch sử chi tiết
							</button>
						</div>
					</div>
				</div>
			`;

			container.prepend(card_html);

			$(".baka-checkin-btn").on("click", () => {
				this.do_checkin("IN", () => {
					this.render_profile_widget();
				});
			});

			$(".baka-checkout-btn").on("click", () => {
				this.do_checkin("OUT", () => {
					this.render_profile_widget();
				});
			});

			$(".baka-view-history-btn").on("click", () => {
				frappe.set_route("List", "Employee Checkin", {
					employee: s.employee_id,
				});
			});
		});
	},

	open_checkin_dialog: function () {
		this.fetch_status((s) => {
			let wifi_status_text = s.is_wifi_ok
				? `<div style="background: #e6f4ea; border: 1px solid #ceead6; color: #137333; padding: 10px; border-radius: 6px; font-size: 13px;">
					<i class="fa fa-check-circle"></i> Đang kết nối đúng mạng WiFi văn phòng: <b>${frappe.utils.escape_html(s.wifi_ssid)}</b> (IP: ${frappe.utils.escape_html(s.client_ip)})
				   </div>`
				: `<div style="background: #fce8e6; border: 1px solid #fad2cf; color: #c5221f; padding: 10px; border-radius: 6px; font-size: 13px;">
					<i class="fa fa-exclamation-triangle"></i> Bạn chưa kết nối vào WiFi văn phòng (Yêu cầu mạng: <b>${frappe.utils.escape_html(s.wifi_ssid)}</b>). IP hiện tại: ${frappe.utils.escape_html(s.client_ip)}.
				   </div>`;

			let d = new frappe.ui.Dialog({
				title: __("Chấm Công WiFi Văn Phòng"),
				fields: [
					{
						fieldtype: "HTML",
						fieldname: "attendance_html",
						options: `
							<div style="margin-bottom: 15px;">${wifi_status_text}</div>
							<div style="background: var(--fg-color, #f8fafc); border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; padding: 15px; margin-bottom: 15px;">
								<div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
									<span style="color: var(--text-muted, #64748b);">Nhân viên:</span>
									<span style="font-weight: 600;">${frappe.utils.escape_html(s.employee_name)}</span>
								</div>
								<div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
									<span style="color: var(--text-muted, #64748b);">Giờ vào hôm nay:</span>
									<span style="font-weight: 700; color: ${s.today_in ? "#16a34a" : "#64748b"};">${s.today_in || "Chưa ghi nhận"}</span>
								</div>
								<div style="display: flex; justify-content: space-between;">
									<span style="color: var(--text-muted, #64748b);">Giờ ra hôm nay:</span>
									<span style="font-weight: 700; color: ${s.today_out ? "#0284c7" : "#64748b"};">${s.today_out || "Chưa ghi nhận"}</span>
								</div>
							</div>
							<div style="display: flex; gap: 10px;">
								<button class="btn btn-primary baka-dlg-checkin" style="flex: 1; padding: 12px; font-weight: 600; background: #16a34a; border-color: #16a34a;">
									<i class="fa fa-sign-in"></i> Chấm công VÀO (IN)
								</button>
								<button class="btn btn-info baka-dlg-checkout" style="flex: 1; padding: 12px; font-weight: 600; background: #0284c7; border-color: #0284c7;">
									<i class="fa fa-sign-out"></i> Chấm công RA (OUT)
								</button>
							</div>
						`,
					},
				],
			});

			d.show();

			d.$wrapper.find(".baka-dlg-checkin").on("click", () => {
				this.do_checkin("IN", () => {
					d.hide();
					this.render_profile_widget();
				});
			});

			d.$wrapper.find(".baka-dlg-checkout").on("click", () => {
				this.do_checkin("OUT", () => {
					d.hide();
					this.render_profile_widget();
				});
			});
		});
	},
};

// Khởi chạy khi Frappe App sẵn sàng
$(document).on("app_ready", function () {
	baka.attendance.init();
});

// Fallback nếu app_ready đã kích hoạt trước đó
if (window.frappe && frappe.boot) {
	setTimeout(() => {
		baka.attendance.init();
	}, 500);
}
