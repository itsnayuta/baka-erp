// Copyright (c) 2026, BAKA and contributors
// Managerial Dashboard for Health Food ERP (BAKAERP)

frappe.pages['baka-dashboard'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('BAKAERP - Quản Trị Phân Phối Thực Phẩm Bổ Sung & Tinh Bột Kháng'),
		single_column: true
	});

	new BakaDashboard(page);
};

class BakaDashboard {
	constructor(page) {
		this.page = page;
		this.line_filter = "";
		this.channel_filter = "";
		this.from_date = "2026-10-01";
		this.to_date = "2026-10-31";

		this.make();
	}

	make() {
		this.setup_filters();
		this.setup_actions();
		this.setup_container();
		this.load_data();
	}

	setup_filters() {
		// Bộ lọc Dòng sản phẩm (Thương hiệu BAKA)
		this.line_field = this.page.add_field({
			label: __('Dòng sản phẩm'),
			fieldtype: 'Select',
			fieldname: 'product_line',
			options: '\nTất cả\nPLUS\nCACAO\nTIBOKA',
			default: 'Tất cả',
			change: () => {
				let val = this.line_field.get_value();
				this.line_filter = (val === 'Tất cả' || !val) ? "" : val;
				this.load_data();
			}
		});

		// Bộ lọc Kênh bán hàng
		this.channel_field = this.page.add_field({
			label: __('Kênh bán hàng'),
			fieldtype: 'Select',
			fieldname: 'channel',
			options: '\nTất cả\nB2B Sỉ\nB2C Trực tiếp\nTikTok Shop\nShopee\nWebsite',
			default: 'Tất cả',
			change: () => {
				let val = this.channel_field.get_value();
				this.channel_filter = (val === 'Tất cả' || !val) ? "" : val;
				this.load_data();
			}
		});
	}

	setup_actions() {
		this.page.set_primary_action(__('Làm mới'), () => {
			this.load_data();
		}, 'octicon octicon-sync');

		this.page.add_button(__('Xuất CSV'), () => {
			this.export_csv();
		}, 'octicon octicon-download');

		this.page.add_button(__('Hồ Sơ & Chấm Công'), () => {
			frappe.set_route('user-profile');
		});
	}

	setup_container() {
		this.container = $('<div class="baka-dashboard-wrapper p-3"></div>').appendTo(this.page.main);
		this.container.html(`
			<!-- BAKA BRAND & PRODUCT LINE BANNER -->
			<div class="mb-3 d-flex align-items-center justify-content-between p-2 px-3 rounded shadow-sm" style="background: linear-gradient(90deg, #ecfdf5 0%, #f0fdf4 100%); border: 1px solid #a7f3d0;">
				<div>
					<span class="badge badge-success mr-2" style="font-size: 13px; background-color: #059669; padding: 5px 10px;">Thương hiệu duy nhất: BAKA</span>
					<span class="text-muted small">| Dòng sản phẩm cốt lõi: <b>PLUS</b> (Cao cấp), <b>CACAO</b> (Hương vị), <b>TIBOKA</b> (Đại trà)</span>
				</div>
				<div class="small font-weight-bold text-success text-uppercase">BAKAERP • HỆ THỐNG QUẢN TRỊ THỰC PHẨM BẢO VỆ SỨC KHỎE</div>
			</div>

			<div class="row kpi-cards-row mb-4">
				<div class="col-md-2 col-sm-6 mb-3">
					<div class="card p-3 shadow-sm border-0 h-100" style="border-left: 4px solid #2563eb !important; background: #fff;">
						<div class="text-muted small font-weight-bold uppercase">DOANH THU THUẦN</div>
						<div class="h4 font-weight-bold text-primary mt-2 kpi-val" id="kpi-revenue">--</div>
						<div class="small text-muted">5 kênh phân phối</div>
					</div>
				</div>
				<div class="col-md-2 col-sm-6 mb-3">
					<div class="card p-3 shadow-sm border-0 h-100" style="border-left: 4px solid #059669 !important; background: #fff;">
						<div class="text-muted small font-weight-bold uppercase">LỢI NHUẬN GỘP</div>
						<div class="h4 font-weight-bold text-success mt-2 kpi-val" id="kpi-gross-profit">--</div>
						<div class="small text-muted" id="kpi-gross-margin">Biên lãi: --%</div>
					</div>
				</div>
				<div class="col-md-2 col-sm-6 mb-3">
					<div class="card p-3 shadow-sm border-0 h-100" style="border-left: 4px solid #10b981 !important; background: #fff;">
						<div class="text-muted small font-weight-bold uppercase">LÃI RÒNG QUẢN TRỊ</div>
						<div class="h4 font-weight-bold text-success mt-2 kpi-val" id="kpi-net-profit">--</div>
						<div class="small text-muted" id="kpi-net-margin">Tỷ suất: --%</div>
					</div>
				</div>
				<div class="col-md-2 col-sm-6 mb-3">
					<div class="card p-3 shadow-sm border-0 h-100" style="border-left: 4px solid #8b5cf6 !important; background: #fff;">
						<div class="text-muted small font-weight-bold uppercase">TỔNG TỒN KHO</div>
						<div class="h4 font-weight-bold text-purple mt-2 kpi-val" id="kpi-stock-qty">--</div>
						<div class="small text-muted" id="kpi-stock-val">Giá trị: -- đ</div>
					</div>
				</div>
				<div class="col-md-2 col-sm-6 mb-3">
					<div class="card p-3 shadow-sm border-0 h-100" style="border-left: 4px solid #f59e0b !important; background: #fff;">
						<div class="text-muted small font-weight-bold uppercase">CẢNH BÁO CẬN DATE</div>
						<div class="h4 font-weight-bold text-warning mt-2 kpi-val" id="kpi-near-expiry">--</div>
						<div class="small text-muted">Lô &lt; 60 ngày hết hạn</div>
					</div>
				</div>
				<div class="col-md-2 col-sm-6 mb-3">
					<div class="card p-3 shadow-sm border-0 h-100" style="border-left: 4px solid #06b6d4 !important; background: #fff;">
						<div class="text-muted small font-weight-bold uppercase">TIỀN THU HỘ (1113)</div>
						<div class="h4 font-weight-bold text-info mt-2 kpi-val" id="kpi-cash-held">--</div>
						<div class="small text-muted">NVKD đang giữ chờ nộp</div>
					</div>
				</div>
			</div>

			<!-- TABS NAVIGATION -->
			<ul class="nav nav-tabs mb-3" id="bakaDashboardTabs" role="tablist">
				<li class="nav-item">
					<a class="nav-link active font-weight-bold" id="tab-pnl-link" data-toggle="tab" href="#tab-pnl" role="tab">Báo cáo Lãi Lỗ Quản Trị (P&amp;L)</a>
				</li>
				<li class="nav-item">
					<a class="nav-link font-weight-bold" id="tab-stock-link" data-toggle="tab" href="#tab-stock" role="tab">Kho Vận &amp; Lô Hàng (FEFO)</a>
				</li>
				<li class="nav-item">
					<a class="nav-link font-weight-bold" id="tab-emp-stock-link" data-toggle="tab" href="#tab-emp-stock" role="tab">Kho Nhân Viên &amp; Đối Soát Tiền</a>
				</li>
			</ul>

			<!-- TABS CONTENT -->
			<div class="tab-content" id="bakaDashboardTabContent">
				<!-- TAB 1: P&L QUẢN TRỊ -->
				<div class="tab-pane fade show active" id="tab-pnl" role="tabpanel">
					<div class="row">
						<div class="col-md-6 mb-3">
							<div class="card shadow-sm p-3 border-0 h-100">
								<h6 class="font-weight-bold mb-3 text-dark">1. Doanh Thu &amp; Lợi Nhuận Theo Kênh Bán Hàng</h6>
								<div class="table-responsive">
									<table class="table table-hover table-sm text-center mb-0" id="tbl-by-channel">
										<thead class="thead-light">
											<tr>
												<th class="text-left">Kênh Bán</th>
												<th>Số lượng</th>
												<th>Doanh thu</th>
												<th>Giá vốn</th>
												<th>Lợi nhuận gộp</th>
												<th>Biên lãi</th>
											</tr>
										</thead>
										<tbody></tbody>
									</table>
								</div>
							</div>
						</div>
						<div class="col-md-6 mb-3">
							<div class="card shadow-sm p-3 border-0 h-100">
								<h6 class="font-weight-bold mb-3 text-dark">2. Doanh Thu &amp; Hiệu Quả Theo Dòng Sản Phẩm (Thương hiệu BAKA)</h6>
								<div class="table-responsive">
									<table class="table table-hover table-sm text-center mb-0" id="tbl-by-brand">
										<thead class="thead-light">
											<tr>
												<th class="text-left">Dòng Sản Phẩm</th>
												<th>Số lượng</th>
												<th>Doanh thu</th>
												<th>Giá vốn</th>
												<th>Lợi nhuận gộp</th>
												<th>Biên lãi</th>
											</tr>
										</thead>
										<tbody></tbody>
									</table>
								</div>
							</div>
						</div>
					</div>

					<!-- CHI PHÍ VẬN HÀNH & LỢI NHUẬN RÒNG -->
					<div class="card shadow-sm p-3 border-0 mt-2">
						<h6 class="font-weight-bold mb-3 text-dark">3. Bảng Tổng Hợp Chi Phí &amp; Lợi Nhuận Ròng Quản Trị</h6>
						<div class="table-responsive">
							<table class="table table-bordered table-sm mb-0" id="tbl-pnl-summary">
								<tbody></tbody>
							</table>
						</div>
					</div>
				</div>

				<!-- TAB 2: KHO VẬN & LÔ HÀNG FEFO -->
				<div class="tab-pane fade" id="tab-stock" role="tabpanel">
					<div class="row">
						<div class="col-md-7 mb-3">
							<div class="card shadow-sm p-3 border-0 h-100">
								<h6 class="font-weight-bold mb-3 text-dark">Theo Dõi Tồn Kho Theo Lô &amp; Hạn Sử Dụng (FEFO)</h6>
								<div class="table-responsive">
									<table class="table table-hover table-sm text-center mb-0" id="tbl-batches">
										<thead class="thead-light">
											<tr class="small font-weight-bold">
												<th class="text-left">Mã Lô</th>
												<th class="text-left">Sản phẩm</th>
												<th>Dòng sản phẩm</th>
												<th>Ngày SX</th>
												<th>Hạn Dùng</th>
												<th>Thời hạn còn lại</th>
												<th>Trạng thái</th>
											</tr>
										</thead>
										<tbody></tbody>
									</table>
								</div>
							</div>
						</div>
						<div class="col-md-5 mb-3">
							<div class="card shadow-sm p-3 border-0 h-100">
								<h6 class="font-weight-bold mb-3 text-dark">Cơ Cấu Tồn Kho Theo Phân Loại</h6>
								<ul class="list-group list-group-flush mb-3" id="list-warehouse-types"></ul>
								<div class="alert alert-info small mb-0">
									<b>Nguyên tắc FEFO:</b> Hệ thống tự động ưu tiên xuất các lô hàng có hạn sử dụng gần nhất. Lô hàng cận date (&lt; 60 ngày) được cảnh báo màu vàng để ưu tiên luân chuyển.
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- TAB 3: KHO NHÂN VIÊN & ĐỐI SOÁT TIỀN THU HỘ -->
				<div class="tab-pane fade" id="tab-emp-stock" role="tabpanel">
					<div class="row">
						<div class="col-md-7 mb-3">
							<div class="card shadow-sm p-3 border-0 h-100">
								<h6 class="font-weight-bold mb-3 text-dark">Hàng Tồn Nằm Tại Kho Nhân Viên Di Động (Mobile Stock)</h6>
								<div class="table-responsive">
									<table class="table table-hover table-sm text-center mb-0" id="tbl-emp-stock">
										<thead class="thead-light">
											<tr>
												<th class="text-left">Kho Nhân Viên</th>
												<th class="text-left">Sản phẩm</th>
												<th>Dòng sản phẩm</th>
												<th>Tồn thực tế</th>
												<th>Giá trị (VND)</th>
											</tr>
										</thead>
										<tbody></tbody>
									</table>
								</div>
							</div>
						</div>
						<div class="col-md-5 mb-3">
							<div class="card shadow-sm p-3 border-0 h-100">
								<h6 class="font-weight-bold mb-3 text-dark">Đối Soát Tiền Thu Hộ Bán Lẻ (Tài khoản 1113)</h6>
								<div class="p-3 mb-3 bg-light rounded">
									<div class="d-flex justify-content-between mb-2">
										<span>Tổng tiền thu hộ từ khách:</span>
										<b class="text-dark">1.825.000 đ</b>
									</div>
									<div class="d-flex justify-content-between mb-2">
										<span>Đã nộp về công ty (UNC):</span>
										<b class="text-success">1.500.000 đ</b>
									</div>
									<hr class="my-2">
									<div class="d-flex justify-content-between">
										<span class="font-weight-bold text-danger">Số dư NVKD còn phải nộp:</span>
										<b class="text-danger font-weight-bold h5 mb-0" id="val-reconciliation-held">325.000 đ</b>
									</div>
								</div>
								<div class="small text-muted">
									NVKD thu tiền mặt/chuyển khoản từ khách hàng được ghi nhận vào TK 1113. Khi nộp tiền về ngân hàng công ty (TK 1121), thủ quỹ lập phiếu chuyển khoản nội bộ đối soát.
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		`);
	}

	load_data() {
		frappe.ui.form.trigger_render = true;

		// 1. Load P&L Report Data
		frappe.call({
			method: 'erpnext.setup.health_food_erp_setup.get_managerial_pnl_report',
			args: {
				from_date: this.from_date,
				to_date: this.to_date,
				brand: this.line_filter,
				product_line: this.line_filter,
				channel: this.channel_filter
			},
			callback: (r) => {
				if (r.message) {
					this.render_pnl(r.message);
				}
			}
		});

		// 2. Load Warehouse Dashboard Data
		frappe.call({
			method: 'erpnext.setup.health_food_erp_setup.get_warehouse_dashboard_data',
			callback: (r) => {
				if (r.message) {
					this.render_warehouse(r.message);
				}
			}
		});
	}

	render_pnl(data) {
		let s = data.summary;
		$('#kpi-revenue').text(format_currency(s.gross_revenue, 'VND', 0));
		$('#kpi-gross-profit').text(format_currency(s.gross_profit, 'VND', 0));
		$('#kpi-gross-margin').text(`Biên lãi: ${s.gross_margin_pct}%`);
		$('#kpi-net-profit').text(format_currency(s.net_operating_profit, 'VND', 0));
		$('#kpi-net-margin').text(`Tỷ suất: ${s.net_profit_margin_pct}%`);

		// Render Table By Channel
		let $tbody_channel = $('#tbl-by-channel tbody').empty();
		for (let [ch, d] of Object.entries(data.by_channel)) {
			$tbody_channel.append(`
				<tr>
					<td class="text-left font-weight-bold">${ch}</td>
					<td>${d.qty.toLocaleString()} hộp</td>
					<td class="font-weight-bold text-primary">${format_currency(d.revenue, 'VND', 0)}</td>
					<td>${format_currency(d.cogs, 'VND', 0)}</td>
					<td class="text-success font-weight-bold">${format_currency(d.gross_profit, 'VND', 0)}</td>
					<td><span class="badge badge-success">${d.margin_pct}%</span></td>
				</tr>
			`);
		}

		// Render Table By Product Line (Thương hiệu BAKA)
		let $tbody_brand = $('#tbl-by-brand tbody').empty();
		let line_data = data.by_product_line || data.by_brand;
		for (let [br, d] of Object.entries(line_data)) {
			let badge_class = br === 'PLUS' ? 'badge-primary' : (br === 'CACAO' ? 'badge-warning text-dark' : 'badge-info');
			$tbody_brand.append(`
				<tr>
					<td class="text-left"><span class="badge ${badge_class}">Dòng ${br}</span></td>
					<td>${d.qty.toLocaleString()} hộp</td>
					<td class="font-weight-bold text-primary">${format_currency(d.revenue, 'VND', 0)}</td>
					<td>${format_currency(d.cogs, 'VND', 0)}</td>
					<td class="text-success font-weight-bold">${format_currency(d.gross_profit, 'VND', 0)}</td>
					<td><span class="badge badge-success">${d.margin_pct}%</span></td>
				</tr>
			`);
		}

		// Render P&L Summary Table
		let $tbl_pnl = $('#tbl-pnl-summary tbody').empty();
		$tbl_pnl.append(`
			<tr class="table-primary font-weight-bold">
				<td>1. DOANH THU THUẦN</td>
				<td class="text-right">${format_currency(s.gross_revenue, 'VND', 0)}</td>
				<td class="text-right">100.0%</td>
			</tr>
			<tr>
				<td>2. Giá vốn hàng bán (COGS - TK 632)</td>
				<td class="text-right text-danger">- ${format_currency(s.cogs, 'VND', 0)}</td>
				<td class="text-right">${((s.cogs / (s.gross_revenue || 1)) * 100).toFixed(1)}%</td>
			</tr>
			<tr class="table-success font-weight-bold">
				<td>3. LỢI NHUẬN GỘP (GROSS PROFIT = 1 - 2)</td>
				<td class="text-right text-success">${format_currency(s.gross_profit, 'VND', 0)}</td>
				<td class="text-right text-success">${s.gross_margin_pct}%</td>
			</tr>
			<tr>
				<td>4. Phí sàn TMĐT (Shopee &amp; TikTok Shop - TK 6413)</td>
				<td class="text-right text-danger">- ${format_currency(s.platform_fees, 'VND', 0)}</td>
				<td class="text-right">${((s.platform_fees / (s.gross_revenue || 1)) * 100).toFixed(2)}%</td>
			</tr>
			<tr>
				<td>5. Phí vận chuyển người bán chịu (TK 6412)</td>
				<td class="text-right text-danger">- ${format_currency(s.shipping_fees, 'VND', 0)}</td>
				<td class="text-right">${((s.shipping_fees / (s.gross_revenue || 1)) * 100).toFixed(2)}%</td>
			</tr>
			<tr class="font-weight-bold">
				<td>6. Lợi nhuận trực tiếp sau phí bán hàng (= 3 - 4 - 5)</td>
				<td class="text-right">${format_currency(s.direct_operating_profit, 'VND', 0)}</td>
				<td class="text-right">${((s.direct_operating_profit / (s.gross_revenue || 1)) * 100).toFixed(1)}%</td>
			</tr>
			<tr>
				<td>7. Chi phí Quảng cáo Ads Marketing (TK 6414)</td>
				<td class="text-right text-danger">- ${format_currency(s.ads_marketing_expense, 'VND', 0)}</td>
				<td class="text-right">${((s.ads_marketing_expense / (s.gross_revenue || 1)) * 100).toFixed(1)}%</td>
			</tr>
			<tr>
				<td>8. Chi phí Lương nhân sự (Kinh doanh &amp; Quản lý - TK 6411 &amp; 6421)</td>
				<td class="text-right text-danger">- ${format_currency(s.salary_expense, 'VND', 0)}</td>
				<td class="text-right">${((s.salary_expense / (s.gross_revenue || 1)) * 100).toFixed(1)}%</td>
			</tr>
			<tr>
				<td>9. Chi phí Thuê mặt bằng, văn phòng &amp; kho bãi (TK 6426)</td>
				<td class="text-right text-danger">- ${format_currency(s.rent_expense, 'VND', 0)}</td>
				<td class="text-right">${((s.rent_expense / (s.gross_revenue || 1)) * 100).toFixed(1)}%</td>
			</tr>
			<tr class="table-info font-weight-bold h5">
				<td>10. LỢI NHUẬN RÒNG QUẢN TRỊ (NET OPERATING PROFIT)</td>
				<td class="text-right text-success">${format_currency(s.net_operating_profit, 'VND', 0)}</td>
				<td class="text-right text-success">${s.net_profit_margin_pct}%</td>
			</tr>
		`);
	}

	render_warehouse(data) {
		let s = data.summary;
		$('#kpi-stock-qty').text(`${s.total_items_in_stock.toLocaleString()} hộp`);
		$('#kpi-stock-val').text(`Giá trị: ${format_currency(s.total_stock_value, 'VND', 0)}`);
		$('#kpi-near-expiry').text(`${s.near_expiry_count} lô`);
		$('#kpi-cash-held').text(format_currency(s.employee_cash_held, 'VND', 0));
		$('#val-reconciliation-held').text(format_currency(s.employee_cash_held, 'VND', 0));

		// Render Batches Table
		let $tbody_batches = $('#tbl-batches tbody').empty();
		let all_batches = [
			...(data.batches.expired || []),
			...(data.batches.near_expiry || []),
			...(data.batches.safe || [])
		];
		for (let b of all_batches) {
			let badge = b.alert_level === 'warning' ? 'badge-warning text-dark' : (b.alert_level === 'danger' ? 'badge-danger' : 'badge-success');
			let line_text = b.product_line ? ('Dòng ' + b.product_line) : (b.brand || '--');
			$tbody_batches.append(`
				<tr>
					<td class="text-left font-weight-bold">${b.batch_id}</td>
					<td class="text-left">${b.item_name}</td>
					<td><span class="badge badge-light font-weight-bold text-success">${line_text}</span></td>
					<td>${b.manufacturing_date || '--'}</td>
					<td class="font-weight-bold">${b.expiry_date || '--'}</td>
					<td>${b.days_to_expire != null ? b.days_to_expire + ' ngày' : '--'}</td>
					<td><span class="badge ${badge}">${b.status}</span></td>
				</tr>
			`);
		}

		// Warehouse types breakdown
		$('#list-warehouse-types').empty().append(`
			<li class="list-group-item d-flex justify-content-between align-items-center">
				Kho Tổng Công Ty BAKA
				<span class="badge badge-primary badge-pill">${s.central_warehouse_qty.toLocaleString()} hộp</span>
			</li>
			<li class="list-group-item d-flex justify-content-between align-items-center">
				Kho Nhân Viên Di Động
				<span class="badge badge-purple badge-pill">${s.employee_warehouses_qty.toLocaleString()} hộp</span>
			</li>
			<li class="list-group-item d-flex justify-content-between align-items-center">
				Kho Cách Ly &amp; Đổi Trả
				<span class="badge badge-warning badge-pill">${s.quarantine_qty.toLocaleString()} hộp</span>
			</li>
			<li class="list-group-item d-flex justify-content-between align-items-center">
				Kho Hàng Hỏng &amp; Hết Hạn
				<span class="badge badge-danger badge-pill">${s.damaged_qty.toLocaleString()} hộp</span>
			</li>
		`);

		// Render Employee Mobile Warehouses
		let $tbody_emp = $('#tbl-emp-stock tbody').empty();
		for (let row of data.employee_warehouses) {
			let line_text = row.product_line ? ('Dòng ' + row.product_line) : (row.brand || '--');
			$tbody_emp.append(`
				<tr>
					<td class="text-left font-weight-bold text-dark">${row.warehouse_name}</td>
					<td class="text-left">${row.item_name}</td>
					<td><span class="badge badge-light font-weight-bold text-success">${line_text}</span></td>
					<td class="font-weight-bold text-primary">${row.actual_qty.toLocaleString()} hộp</td>
					<td>${format_currency(row.stock_value, 'VND', 0)}</td>
				</tr>
			`);
		}
	}

	export_csv() {
		frappe.call({
			method: 'erpnext.setup.health_food_erp_setup.get_managerial_pnl_report',
			args: {
				from_date: this.from_date,
				to_date: this.to_date,
				brand: this.line_filter,
				product_line: this.line_filter,
				channel: this.channel_filter
			},
			callback: (r) => {
				if (!r.message) return;
				let pnl = r.message;
				let csv = 'BAKAERP - BÁO CÁO KẾT QUẢ KINH DOANH QUẢN TRỊ\n';
				csv += 'THƯƠNG HIỆU: BAKA (DUY NHẤT)\n';
				csv += `Kỳ báo cáo: ${pnl.period.from_date} đến ${pnl.period.to_date}\n\n`;
				csv += 'KÊNH BÁN HÀNG,SỐ LƯỢNG (HỘP),DOANH THU (VND),GIÁ VỐN (VND),LỢI NHUẬN GỘP (VND),BIÊN LÃI GỘP (%)\n';
				for (let [ch, d] of Object.entries(pnl.by_channel)) {
					csv += `"${ch}",${d.qty},${d.revenue},${d.cogs},${d.gross_profit},${d.margin_pct}%\n`;
				}
				csv += '\nDÒNG SẢN PHẨM (THƯƠNG HIỆU BAKA),SỐ LƯỢNG (HỘP),DOANH THU (VND),GIÁ VỐN (VND),LỢI NHUẬN GỘP (VND),BIÊN LÃI GỘP (%)\n';
				let line_data = pnl.by_product_line || pnl.by_brand;
				for (let [br, d] of Object.entries(line_data)) {
					csv += `"Dòng ${br}",${d.qty},${d.revenue},${d.cogs},${d.gross_profit},${d.margin_pct}%\n`;
				}
				csv += '\nCHỈ TIÊU TÀI CHÍNH QUẢN TRỊ,SỐ TIỀN (VND)\n';
				csv += `Doanh thu thuần,${pnl.summary.gross_revenue}\n`;
				csv += `Giá vốn hàng bán (COGS),${pnl.summary.cogs}\n`;
				csv += `Lợi nhuận gộp,${pnl.summary.gross_profit}\n`;
				csv += `Phí sàn TMĐT,${pnl.summary.platform_fees}\n`;
				csv += `Phí vận chuyển người bán chịu,${pnl.summary.shipping_fees}\n`;
				csv += `Chi phí Quảng cáo Ads Marketing,${pnl.summary.ads_marketing_expense}\n`;
				csv += `Chi phí Lương nhân sự,${pnl.summary.salary_expense}\n`;
				csv += `Chi phí Thuê văn phòng & kho bãi,${pnl.summary.rent_expense}\n`;
				csv += `Lợi nhuận ròng quản trị,${pnl.summary.net_operating_profit}\n`;

				let blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
				let link = document.createElement("a");
				let url = URL.createObjectURL(blob);
				link.setAttribute("href", url);
				link.setAttribute("download", `BAKAERP_Bao_Cao_Quan_Tri_${nowdate()}.csv`);
				document.body.appendChild(link);
				link.click();
				document.body.removeChild(link);
			}
		});
	}
}

