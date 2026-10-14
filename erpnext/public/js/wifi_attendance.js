// Copyright (c) 2026, BAKA and contributors
// WiFi-based Employee Attendance and Check-in / Check-out Module

frappe.provide("baka.attendance");
frappe.provide("frappe.energy_points");

// Phòng vệ lỗi null.bold() khi hệ thống hiển thị timeline của Energy Point Log
if (frappe.energy_points) {
	const orig_get_form_log = frappe.energy_points.get_form_log_message;
	frappe.energy_points.get_form_log_message = function (log) {
		if (log && log.type === "Auto" && !log.rule) {
			log.rule = __("Hệ thống");
		}
		return orig_get_form_log ? orig_get_form_log.apply(this, arguments) : "";
	};
	const orig_format_history = frappe.energy_points.format_history_log;
	frappe.energy_points.format_history_log = function (log) {
		if (log && log.type === "Auto" && !log.rule) {
			log.rule = __("Hệ thống");
		}
		return orig_format_history ? orig_format_history.apply(this, arguments) : "";
	};
}

baka.attendance = {
	status: null,
	_render_seq: 0,
	_initialized: false,

	init: function () {
		if (this._initialized) return;
		this._initialized = true;

		// 1. Loại bỏ hoàn toàn nút Chấm công trên thanh Navbar (chỉ chấm công trong My Profile)
		$(".baka-nav-checkin-item, .baka-nav-checkin-btn").remove();

		// CSS ẩn triệt để phần Phân phối loại (Type Distribution) và Hoạt động gần đây (Recent Activity)
		frappe.dom.set_style(`
			.percentage-chart-container, .recent-activity {
				display: none !important;
			}
		`);

		// 2. Thiết lập hook tích hợp trực tiếp vào màn hình My Profile
		this.setup_profile_hook();
	},

	setup_profile_hook: function () {
		const hook_controller = () => {
			if (frappe.ui && frappe.ui.UserProfile && !frappe.ui.UserProfile.prototype._baka_attendance_hooked) {
				frappe.ui.UserProfile.prototype._baka_attendance_hooked = true;

				// 1. Hook make_user_profile để chèn widget chấm công và dọn dẹp các khối thừa
				const orig_make = frappe.ui.UserProfile.prototype.make_user_profile;
				frappe.ui.UserProfile.prototype.make_user_profile = function () {
					orig_make.apply(this, arguments);
					baka.attendance.render_profile_widget(this);

					// Loại bỏ hoàn toàn phần Type Distribution và Recent Activity khỏi DOM
					this.main_section.find(".percentage-chart-container, .recent-activity").remove();

					// Đổi tiêu đề: "Điểm năng lượng" -> "Điểm đánh giá", "Tổng quan" -> "Tổng quan chuyên cần"
					this.main_section.find(".line-chart-container .card-title").text(__("Điểm đánh giá"));
					this.main_section.find(".heatmap-container .card-title").text(__("Tổng quan chuyên cần"));
					if (this.heatmap) {
						this.heatmap.countLabel = __("Điểm chuyên cần");
					}
				};

				// Triệt tiêu các hàm xử lý tính toán và gọi API thừa cho Type Distribution & Recent Activity
				frappe.ui.UserProfile.prototype.render_percentage_chart = function () {};
				frappe.ui.UserProfile.prototype.create_percentage_chart_filters = function () {};
				frappe.ui.UserProfile.prototype.setup_user_activity_timeline = function () {};

				// 2. Hook render_heatmap: đảm bảo countLabel lúc khởi tạo chart luôn là "Điểm chuyên cần"
				frappe.ui.UserProfile.prototype.render_heatmap = function () {
					this.heatmap = new frappe.Chart(".performance-heatmap", {
						type: "heatmap",
						start: new Date(moment().subtract(1, "year").toDate()),
						countLabel: __("Điểm chuyên cần"),
						data: {},
						discreteDomains: 1,
						radius: 3,
						height: 140,
					});
					this.update_heatmap_data();
					this.create_heatmap_chart_filters();
				};

				// 3. Hook get_user_points: lấy Điểm đánh giá (Energy Points) và tính Điểm chuyên cần (1h làm việc = 1 điểm)
				frappe.ui.UserProfile.prototype.get_user_points = function () {
					return Promise.all([
						frappe.xcall("frappe.social.doctype.energy_point_log.energy_point_log.get_user_energy_and_review_points", { user: this.user_id }),
						frappe.xcall("erpnext.setup.wifi_attendance.get_chuyen_can_summary", { user: this.user_id })
					]).then(([r, cc]) => {
						if (r && r[this.user_id]) {
							this.energy_points = r[this.user_id].energy_points || 0;
						}
						this.chuyen_can_points = (cc && cc.total_points != null) ? Math.floor(Number(cc.total_points)) : 0;
						this.review_points = this.chuyen_can_points;
					});
				};

				// 4. Hook render_points_and_rank:
				// - Đổi tên cột 1: Điểm đánh giá (thay cho Điểm năng lượng)
				// - Đổi tên cột 2: Điểm chuyên cần (số nguyên hoàn chỉnh)
				frappe.ui.UserProfile.prototype.render_points_and_rank = function () {
					let $profile_details = this.wrapper.find(".user-stats");
					let $profile_details_wrapper = this.wrapper.find(".user-stats-detail");
					$profile_details.empty();

					const _get_stat_dom = (value, label, icon) => {
						let display_val = value;
						if (label === __("Điểm chuyên cần")) {
							display_val = Math.floor(Number(value || 0));
						}
						return `<div class="user-stats-item mt-4">
							${frappe.utils.icon(icon, "lg", "no-stroke")}
							<div>
								<div class="stat-value">${display_val}</div>
								<div class="stat-label">${label}</div>
							</div>
						</div>`;
					};

					this.get_user_rank().then(() => {
						this.get_user_points().then(() => {
							let html = $(`
								${_get_stat_dom(this.energy_points, __("Điểm đánh giá"), "color-energy-points")}
								${_get_stat_dom(this.chuyen_can_points != null ? this.chuyen_can_points : this.review_points, __("Điểm chuyên cần"), "color-review-points")}
								${_get_stat_dom(this.rank, __("Hạng"), "color-rank")}
								${_get_stat_dom(this.month_rank, __("Hạng tháng"), "color-monthly-rank")}
							`);

							$profile_details.html(html);
							$profile_details_wrapper.removeClass("hide");
						});
					});
				};

				// 5. Hook update_heatmap_data: ô xanh trong tổng quan tính theo Điểm chuyên cần (mốc 2, 4, 6, 8 điểm, tính theo năm)
				frappe.ui.UserProfile.prototype.update_heatmap_data = function (date) {
					frappe.xcall("erpnext.setup.wifi_attendance.get_chuyen_can_heatmap_data", {
						user: this.user_id,
						date: date || frappe.datetime.year_start()
					}).then((r) => {
						if (this.heatmap) {
							this.heatmap.countLabel = __("Điểm chuyên cần");
							this.heatmap.update({
								dataPoints: r || {}
							});
						}
					});
				};
			}
		};

		// Tải trước bundle để sẵn sàng hook prototype ngay từ đầu
		if (frappe.require) {
			frappe.require("user_profile_controller.bundle.js", () => {
				hook_controller();
			});
		}

		let debounced_timer = null;
		frappe.router.on("change", () => {
			$(".baka-nav-checkin-item, .baka-nav-checkin-btn").remove();

			let current_route = frappe.get_route();
			if (current_route && current_route[0] === "user-profile") {
				if (frappe.require) {
					frappe.require("user_profile_controller.bundle.js", () => {
						hook_controller();
						let cur_page = frappe.pages && frappe.pages["user-profile"];
						if (cur_page && cur_page.user_profile && cur_page.user_profile.heatmap) {
							cur_page.user_profile.heatmap.countLabel = __("Điểm chuyên cần");
						}
					});
				}
				if (debounced_timer) clearTimeout(debounced_timer);
				debounced_timer = setTimeout(() => {
					if (!$("#baka-profile-attendance-wrapper").length) {
						this.render_profile_widget();
					}
				}, 100);
			} else {
				$(".baka-profile-attendance-card, #baka-profile-attendance-wrapper").remove();
			}
		});

		// Trigger nếu đang ở trang user-profile sẵn
		let route = frappe.get_route();
		if (route && route[0] === "user-profile") {
			if (frappe.require) {
				frappe.require("user_profile_controller.bundle.js", () => {
					hook_controller();
					let cur_page = frappe.pages && frappe.pages["user-profile"];
					if (cur_page && cur_page.user_profile && cur_page.user_profile.heatmap) {
						cur_page.user_profile.heatmap.countLabel = __("Điểm chuyên cần");
					}
				});
			}
			setTimeout(() => {
				if (!$("#baka-profile-attendance-wrapper").length) {
					this.render_profile_widget();
				}
			}, 150);
		}
	},

	fetch_status: function (target_user, callback) {
		if (typeof target_user === "function") {
			callback = target_user;
			target_user = frappe.session.user;
		}
		frappe.call({
			method: "erpnext.setup.wifi_attendance.get_attendance_status",
			args: { user: target_user || frappe.session.user },
			callback: (r) => {
				if (r.message) {
					this.status = r.message;
					if (callback) callback(this.status);
				}
			},
		});
	},

	do_checkin: function (log_type, callback) {
		const $card = $(".baka-profile-attendance-card");
		const $btns = $card.find(".baka-checkin-btn, .baka-checkout-btn");
		
		// Khóa ngay lập tức nút vừa bấm để chống spam/double click
		$btns.prop("disabled", true).css("opacity", "0.6");

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
					this.fetch_status(frappe.session.user, () => {
						if (callback) callback(r.message);
					});
				}
			},
			always: () => {
				$btns.prop("disabled", false).css("opacity", "1");
			}
		});
	},

	render_profile_widget: function (user_profile_inst) {
		// Dọn sạch toàn bộ card hoặc wrapper cũ (bảo đảm 100% không bao giờ bị trùng lặp)
		$(".baka-profile-attendance-card, #baka-profile-attendance-wrapper").remove();

		// Xác định container và user
		let target_container = null;
		let target_user = frappe.session.user;

		if (user_profile_inst && user_profile_inst.main_section) {
			target_container = user_profile_inst.main_section.find(".col-md-12").first();
			target_user = user_profile_inst.user_id || frappe.session.user;
		} else {
			let $profile = $(".user-profile:visible");
			if (!$profile.length) $profile = $(".user-profile");
			target_container = $profile.find(".col-md-12").first();
			let route = frappe.get_route();
			target_user = (route && route[0] === "user-profile" && route[1]) ? route[1] : frappe.session.user;
		}

		if (!target_container || !target_container.length) return;

		// Tạo wrapper duy nhất và chèn trước .performance-graphs
		let $wrapper = $('<div id="baka-profile-attendance-wrapper" style="width: 100%;"></div>');
		let $perf = target_container.find(".performance-graphs");
		if ($perf.length) {
			$perf.before($wrapper);
		} else {
			target_container.prepend($wrapper);
		}

		let req_id = ++this._render_seq;

		this.fetch_status(target_user, (s) => {
			if (req_id !== this._render_seq) return;
			if (!s || !s.employee_id) return;
			if (!$wrapper.closest("body").length) return;

			// Quét dọn lần nữa để bảo đảm không có thẻ card nào rò rỉ bên ngoài
			$(".baka-profile-attendance-card").not($wrapper.find(".baka-profile-attendance-card")).remove();

			let is_own_profile = (target_user === frappe.session.user);

			let wifi_badge = s.is_wifi_ok
				? `<span style="background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px; display: inline-flex; align-items: center; gap: 4px;">
					<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 4C7.31 4 3.07 5.9 0 8.98L12 21 24 8.98C20.93 5.9 16.69 4 12 4zm0 3.5c3.74 0 7.15 1.48 9.68 3.92L12 19.33 2.32 11.42C4.85 8.98 8.26 7.5 12 7.5z"/></svg>
					Đã kết nối WiFi: <b>${frappe.utils.escape_html(s.wifi_ssid)}</b> (IP: ${frappe.utils.escape_html(s.client_ip)})
				   </span>`
				: `<span style="background: #fce8e6; color: #c5221f; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px; display: inline-flex; align-items: center; gap: 4px;">
					<i class="fa fa-exclamation-triangle"></i>
					Chưa vào WiFi công ty (${frappe.utils.escape_html(s.wifi_ssid)}) - IP: ${frappe.utils.escape_html(s.client_ip)}
				   </span>`;

			let action_section_html = "";
			if (is_own_profile) {
				if (s.is_limit_reached || s.today_logs_count >= 10) {
					action_section_html = `
						<div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 14px 18px; width: 100%; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
							<div style="color: #b91c1c; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
								<i class="fa fa-exclamation-triangle" style="font-size: 18px; color: #dc2626;"></i>
								<span>Bạn đã đạt tối đa 10 lần chấm công trong ngày hôm nay. <b>Vui lòng liên hệ với Ban lãnh đạo để được hỗ trợ xử lý!</b></span>
							</div>
							<button class="btn btn-default" disabled style="opacity: 0.65; cursor: not-allowed; font-weight: 600; font-size: 13px; color: #dc2626; border-color: #fca5a5; background: #fff;">
								<i class="fa fa-lock" style="margin-right: 4px;"></i> Đã khóa nút chấm công
							</button>
						</div>
					`;
				} else {
					let checkin_buttons = "";

					if (s.shift_status === "NOT_CHECKED_IN") {
						checkin_buttons = `
							<button class="btn btn-primary baka-checkin-btn" style="min-width: 180px; padding: 10px 24px; font-weight: 600; font-size: 14px; background: #16a34a; border-color: #16a34a; box-shadow: 0 2px 4px rgba(22,163,74,0.2);">
								<i class="fa fa-sign-in" style="margin-right: 6px;"></i> Chấm công VÀO (Check In)
							</button>
						`;
					} else if (s.shift_status === "IN_SHIFT") {
						checkin_buttons = `
							<div style="font-size: 13px; color: #16a34a; font-weight: 600; display: flex; align-items: center; margin-right: 16px;">
								<span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #16a34a; margin-right: 8px;"></span>
								${s.status_label}
							</div>
							<button class="btn btn-info baka-checkout-btn" style="min-width: 180px; padding: 10px 24px; font-weight: 600; font-size: 14px; background: #0284c7; border-color: #0284c7; box-shadow: 0 2px 4px rgba(2,132,199,0.2);">
								<i class="fa fa-sign-out" style="margin-right: 6px;"></i> Chấm công RA (Check Out)
							</button>
						`;
					} else {
						checkin_buttons = `
							<div style="font-size: 13px; color: #0284c7; font-weight: 600; display: flex; align-items: center; margin-right: 16px;">
								<i class="fa fa-check-circle" style="margin-right: 6px; color: #16a34a; font-size: 15px;"></i>
								${s.status_label}
							</div>
							<button class="btn btn-primary baka-checkin-btn" style="min-width: 180px; padding: 10px 24px; font-weight: 600; font-size: 14px; background: #16a34a; border-color: #16a34a; box-shadow: 0 2px 4px rgba(22,163,74,0.2);">
								<i class="fa fa-sign-in" style="margin-right: 6px;"></i> Chấm công VÀO (Ca tiếp theo)
							</button>
						`;
					}

					action_section_html = `
						<div style="display: flex; gap: 12px; justify-content: space-between; align-items: center; flex-wrap: wrap; background: var(--fg-color, #f8fafc); padding: 14px 18px; border-radius: 8px; border: 1px solid var(--border-color, #e2e8f0);">
							<div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap; flex: 1;">
								${checkin_buttons}
							</div>
						</div>
					`;
				}
			} else {
				action_section_html = `
					<div style="display: flex; justify-content: space-between; align-items: center; background: var(--fg-color, #f8fafc); border: 1px dashed var(--border-color, #cbd5e1); border-radius: 8px; padding: 12px 18px; flex-wrap: wrap; gap: 10px;">
						<div style="font-size: 13px; color: var(--text-muted, #64748b);">
							<i class="fa fa-info-circle" style="color: #0284c7; margin-right: 6px;"></i>
							Đang xem dữ liệu chấm công của nhân viên: <b style="color: var(--text-color, #1e293b);">${frappe.utils.escape_html(s.employee_name)}</b> (${s.status_label || ''})
						</div>
					</div>
				`;
			}

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
									<div style="font-size: 12px; color: var(--text-muted, #64748b);">Thời Gian Hôm Nay</div>
									<div style="font-size: 20px; font-weight: 700; color: #3b82f6; margin-top: 4px;">
										${s.work_hours_str || "0 giờ 0 phút"}
									</div>
								</div>
							</div>
							<div class="col-sm-3 col-xs-6" style="margin-bottom: 10px;">
								<div style="background: var(--fg-color, #f8fafc); border: 1px solid var(--border-color, #e2e8f0); border-radius: 8px; padding: 12px; text-align: center;">
									<div style="font-size: 12px; color: var(--text-muted, #64748b);">Tổng Giờ Tháng Này</div>
									<div style="font-size: 20px; font-weight: 700; color: #0f766e; margin-top: 4px;">
										${s.month_hours_str || "0 giờ"}
									</div>
								</div>
							</div>
						</div>

						${action_section_html}
					</div>
				</div>
			`;

			$wrapper.html(card_html);

			$wrapper.find(".baka-checkin-btn").on("click", () => {
				this.do_checkin("IN", () => {
					this.render_profile_widget(user_profile_inst);
				});
			});

			$wrapper.find(".baka-checkout-btn").on("click", () => {
				this.do_checkin("OUT", () => {
					this.render_profile_widget(user_profile_inst);
				});
			});
		});
	}
};

// Khởi chạy khi Frappe App sẵn sàng
$(document).on("app_ready", function () {
	baka.attendance.init();
});

// Fallback nếu app_ready đã kích hoạt trước đó
if (window.frappe && frappe.boot) {
	setTimeout(() => {
		baka.attendance.init();
	}, 300);
}
