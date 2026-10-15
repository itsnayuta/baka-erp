import frappe
from frappe import _

def test_profile_logic():
    from erpnext.setup.wifi_attendance import (
        get_attendance_status, get_chuyen_can_summary, get_chuyen_can_heatmap_data
    )
    from frappe.social.doctype.energy_point_log.energy_point_log import get_user_energy_and_review_points

    users = ["chutich@baka.vn", "coo@baka.vn", "sale1@baka.vn", "sale2@baka.vn", "kho@baka.vn"]
    print("=== TESTING MY PROFILE LOGIC FOR ALL USERS ===")
    
    for u in users:
        print(f"\n--- User: {u} ---")
        # 1. Attendance Status
        status = get_attendance_status(u)
        print(f"  Attendance: Employee={status.get('employee_id')} ({status.get('employee_name')}), In={status.get('today_in')}, Out={status.get('today_out')}, Total Days Worked={status.get('stats', {}).get('total_days')}, On-time={status.get('stats', {}).get('on_time_count')}")
        
        # 2. Điểm chuyên cần theo năm (Cứ tròn 1 tiếng = 1 điểm, max 8đ/ngày, số nguyên)
        cc = get_chuyen_can_summary(u)
        print(f"  Chuyên cần (Năm {cc.get('year')}): Total Points={cc.get('total_points')}, Today Points={cc.get('today_points')}, Days Worked={cc.get('days_worked')}")
        assert isinstance(cc.get("total_points"), int), "Error: Chuyên cần points must be an integer"
        assert isinstance(cc.get("today_points"), int), "Error: Today points must be an integer"

        # 3. Heatmap Data (Mốc 2, 4, 6, 8 điểm, max 8đ/ngày, số nguyên)
        hm = get_chuyen_can_heatmap_data(u)
        max_pt = max(hm.values()) if hm else 0
        min_pt = min(hm.values()) if hm else 0
        print(f"  Heatmap: {len(hm)} data points, Min Daily Point={min_pt}, Max Daily Point={max_pt} (Expected <= 8)")
        assert max_pt <= 8, f"Error: Daily point exceeds 8: {max_pt}"
        assert all(isinstance(v, int) for v in hm.values()), "Error: Heatmap points must be integer"
        
        # 4. Điểm đánh giá (Energy Points)
        ep = get_user_energy_and_review_points(u)
        user_ep = ep.get(u, {}).get("energy_points", 0) if ep else 0
        print(f"  Điểm đánh giá (Energy Points): {user_ep}")

    print("\n✓ ALL MY PROFILE LOGIC TESTS PASSED SUCCESSFULLY!")

def run():
    print("=== Configuring ERP for Vietnam (BAKAERP) ===")
    
    # 0. Check Country doctype
    viet_countries = frappe.db.sql("SELECT name, code FROM `tabCountry` WHERE name LIKE '%Viet%'", as_dict=True)
    country_name = viet_countries[0].name if viet_countries else "Vietnam"
    print(f"Using country name: {country_name}")

    # 1. System Settings & BAKAERP Branding
    sys_doc = frappe.get_doc("System Settings")
    sys_doc.app_name = "BAKAERP"
    sys_doc.country = country_name
    sys_doc.currency = "VND"
    sys_doc.time_zone = "Asia/Ho_Chi_Minh"
    sys_doc.date_format = "dd-mm-yyyy"
    sys_doc.number_format = "#.###,##"
    sys_doc.language = "vi"
    sys_doc.enable_onboarding = 0
    sys_doc.flags.ignore_mandatory = True
    sys_doc.save(ignore_permissions=True)
    frappe.db.set_single_value("System Settings", "app_name", "BAKAERP")
    print(f"✓ Configured System Settings (App Name: BAKAERP, Country: {country_name}, Currency: VND, Timezone: Asia/Ho_Chi_Minh, Language: vi)")

    frappe.db.set_default("app_name", "BAKAERP")
    frappe.db.set_default("country", country_name)
    frappe.db.set_default("currency", "VND")
    frappe.db.set_default("time_zone", "Asia/Ho_Chi_Minh")
    frappe.db.set_default("date_format", "dd-mm-yyyy")
    frappe.db.set_default("number_format", "#.###,##")
    frappe.db.set_default("language", "vi")

    # 1.1 Navbar Settings (Hide foreign/external Frappe/ERPNext help links, set BAKA logo)
    try:
        navbar_settings = frappe.get_single("Navbar Settings")
        navbar_settings.app_logo = "/assets/erpnext/images/baka-logo.svg"
        for item in navbar_settings.help_dropdown:
            item.hidden = 1
        for item in navbar_settings.settings_dropdown:
            if any(term in (item.route or "").lower() for term in ["docs", "frappe", "erpnext", "discuss", "school", "issue"]):
                item.hidden = 1
        navbar_settings.save(ignore_permissions=True)
        print("✓ Configured Navbar Settings (App Logo: baka-logo.svg, hid foreign links)")
    except Exception as e:
        print(f"! Navbar Settings notice: {e}")

    # 1.2 Website Settings (Full BAKAERP branding: Logo, Favicon, Banner, Title, Head styling)
    try:
        if frappe.db.exists("DocType", "Website Settings"):
            web_settings = frappe.get_single("Website Settings")
            web_settings.app_name = "BAKAERP"
            web_settings.app_logo = "/assets/erpnext/images/baka-logo.svg"
            web_settings.favicon = "/assets/erpnext/images/baka-favicon.svg"
            web_settings.title_prefix = "BAKAERP"
            web_settings.brand_html = '<span style="font-weight: 800; font-size: 18px; color: #047857; letter-spacing: 0.5px;">BAKA</span><span style="font-weight: 600; font-size: 18px; color: #0f172a; margin-left: 2px;">ERP</span>'
            web_settings.banner_html = '<div style="font-size: 12.5px; color: #047857; font-weight: 600; text-align: center; padding: 4px 0;">HỆ THỐNG QUẢN TRỊ DOANH NGHIỆP THỰC PHẨM BỔ SUNG &amp; TINH BỘT KHÁNG BAKA</div>'
            web_settings.copyright = "BAKAERP © 2026. Phân phối Thực phẩm Bổ sung & Tinh bột Kháng"
            web_settings.footer_powered = ""
            web_settings.hide_footer_signup = 1
            web_settings.head_html = """
<style>
  .navbar-brand { font-weight: 800; color: #059669 !important; font-size: 18px; }
  .page-card-head h4 { font-weight: 800; color: #065f46; letter-spacing: -0.2px; }
  .page-card-head::after {
    content: "Hệ thống Quản trị Doanh nghiệp Thực phẩm Bổ sung & Tinh bột Kháng";
    display: block;
    font-size: 12.5px;
    font-weight: 600;
    color: #059669;
    margin-top: 4px;
    margin-bottom: 12px;
  }
</style>
"""
            web_settings.save(ignore_permissions=True)
            print("✓ Configured Website Settings (BAKAERP branding: Logo, Favicon, Title prefix, Banner, Head CSS)")
    except Exception as e:
        print(f"! Website Settings notice: {e}")

    # 1.3. Cấu hình tiền tệ & Tỷ giá (Chỉ kích hoạt VND và USD, chuẩn hóa Bảng giá VND)
    try:
        frappe.db.sql("UPDATE `tabCurrency` SET enabled=0 WHERE name NOT IN ('VND', 'USD')")
        frappe.db.sql("UPDATE `tabCurrency` SET enabled=1 WHERE name IN ('VND', 'USD')")
        frappe.clear_cache(doctype="Currency")

        for pl in ["Standard Selling", "Standard Buying"]:
            if frappe.db.exists("Price List", pl):
                frappe.db.set_value("Price List", pl, "currency", "VND")
            else:
                frappe.get_doc({
                    "doctype": "Price List",
                    "price_list_name": pl,
                    "currency": "VND",
                    "selling": 1 if "Selling" in pl else 0,
                    "buying": 1 if "Buying" in pl else 0,
                    "enabled": 1
                }).insert(ignore_permissions=True)

        # Cập nhật Item Price về VND
        frappe.db.sql("UPDATE `tabItem Price` SET currency='VND' WHERE currency != 'VND'")

        # Cập nhật các chứng từ bán hàng / mua hàng cũ còn sót ZWL sang VND
        for dt in ["Sales Order", "Sales Invoice", "Delivery Note", "Purchase Order", "Purchase Invoice", "Purchase Receipt"]:
            if frappe.db.exists("DocType", dt):
                frappe.db.sql(f"UPDATE `tab{dt}` SET price_list_currency='VND', plc_conversion_rate=1.0 WHERE price_list_currency='ZWL'")

        # Thiết lập tỷ giá chuẩn USD <-> VND (Tỷ giá tham chiếu 25.400 VND/USD)
        exchange_rates = [
            {"from_currency": "USD", "to_currency": "VND", "exchange_rate": 25400.0},
            {"from_currency": "VND", "to_currency": "USD", "exchange_rate": round(1.0 / 25400.0, 8)},
            {"from_currency": "ZWL", "to_currency": "VND", "exchange_rate": 1.0},
        ]
        for ex in exchange_rates:
            if not frappe.db.exists("Currency Exchange", {"from_currency": ex["from_currency"], "to_currency": ex["to_currency"], "date": "2026-01-01"}):
                frappe.get_doc({
                    "doctype": "Currency Exchange",
                    "from_currency": ex["from_currency"],
                    "to_currency": ex["to_currency"],
                    "exchange_rate": ex["exchange_rate"],
                    "date": "2026-01-01",
                    "for_selling": 1,
                    "for_buying": 1
                }).insert(ignore_permissions=True)
        print("✓ Đã cấu hình chỉ cho phép 2 đồng tiền VND & USD, cập nhật bảng giá và tỷ giá quy đổi chuẩn")
    except Exception as e:
        print(f"! Currency & Exchange Rate setup notice: {e}")

    # 1.4. Phân quyền đọc dữ liệu dùng chung (Tiền tệ, Bảng giá, Trung tâm chi phí cho Kho và các bộ phận)
    try:
        from frappe.permissions import add_permission
        shared_perms = [
            ("Currency", "All", "read"),
            ("Currency", "Stock User", "read"),
            ("Currency", "Stock Manager", "read"),
            ("Currency Exchange", "All", "read"),
            ("Currency Exchange", "Stock User", "read"),
            ("Currency Exchange", "Stock Manager", "read"),
            ("Price List", "Stock User", "read"),
            ("Price List", "Stock Manager", "read"),
            ("Item Price", "Sales User", "read"),
            ("Item Price", "Stock User", "read"),
            ("Item Price", "Stock Manager", "read"),
            ("Cost Center", "Stock User", "read"),
            ("Cost Center", "Stock Manager", "read"),
            ("Customer Group", "Stock User", "read"),
            ("Customer Group", "Stock Manager", "read"),
        ]
        for dt, role, ptype in shared_perms:
            try:
                if not frappe.db.exists("Custom DocPerm", {"parent": dt, "role": role, "permlevel": 0}):
                    add_permission(dt, role, 0, ptype)
            except Exception:
                pass
        print("✓ Đã cấu hình phân quyền đọc dữ liệu danh mục Tiền tệ, Bảng giá, Trung tâm chi phí cho các bộ phận")
    except Exception as e:
        print(f"! Shared perms setup notice: {e}")

    # 2. Setup Vietnam Address Template
    from erpnext.regional.address_template.setup import update_address_template
    vn_template = """{{ address_line1 }}<br>
{% if address_line2 %}{{ address_line2 }}<br>{% endif -%}
{% if city %}{{ city }}, {% endif -%}{% if state %}{{ state }}{% endif -%}{% if pincode %} {{ pincode }}{% endif -%}<br>
Việt Nam"""
    update_address_template(country_name, vn_template, is_default=1)
    print(f"✓ Configured {country_name} Address Template as default")

    # 3. Tối giản hóa hệ thống (Workspaces, Shortcuts, Customer Groups, Item Groups, Domain Settings)
    print("--- Tối giản hóa hệ thống theo mô hình Bán thức uống cho Đại lý & Khách cuối ---")
    
    # 3.1. Ẩn toàn bộ Workspaces dư thừa (chỉ giữ 6 workspace chính: Home, Selling, Stock, CRM, Accounting, Users)
    bloat_workspaces = [
        "Integration", "Integrations", "Settings", "ERPNext Settings", 
        "ERPNext Integrations", "Non Profit", "Agriculture", "Healthcare", 
        "Hospitality", "Quality", "Build", "Welcome Workspace", "Tools", "Website",
        "Manufacturing", "Projects", "Assets", "Support",
        "Buying", "Payables", "Receivables", "Financial Reports"
    ]
    for ws in bloat_workspaces:
        if frappe.db.exists("Workspace", ws):
            frappe.db.set_value("Workspace", ws, "public", 0)

    core_workspaces = ["Home", "Selling", "Stock", "CRM", "Accounting", "Users"]
    for ws in core_workspaces:
        if frappe.db.exists("Workspace", ws):
            frappe.db.set_value("Workspace", ws, "public", 1)
            frappe.db.set_value("Workspace", ws, "is_hidden", 0)
    print("✓ Đã ẩn các Workspace dư thừa: Buying, Payables, Receivables, Financial Reports và các phân hệ ngoại vi.")

    # 3.2. Chuẩn hóa Nhóm khách hàng: Chỉ có "Đại lý" (B2B) và "Khách hàng cuối" (B2C)
    from frappe.utils.nestedset import rebuild_tree
    if not frappe.db.exists("Customer Group", "Đại lý"):
        frappe.get_doc({
            "doctype": "Customer Group",
            "customer_group_name": "Đại lý",
            "parent_customer_group": "All Customer Groups",
            "is_group": 0
        }).insert(ignore_permissions=True)

    if not frappe.db.exists("Customer Group", "Khách hàng cuối"):
        frappe.get_doc({
            "doctype": "Customer Group",
            "customer_group_name": "Khách hàng cuối",
            "parent_customer_group": "All Customer Groups",
            "is_group": 0
        }).insert(ignore_permissions=True)

    # Đổi tên khách hàng lẻ cũ nếu có
    if frappe.db.exists("Customer", "Chị Nguyễn Thị Lan (Khách sỉ)"):
        try:
            frappe.rename_doc("Customer", "Chị Nguyễn Thị Lan (Khách sỉ)", "Chị Nguyễn Thị Lan (Khách hàng cuối)", force=True)
            frappe.db.set_value("Customer", "Chị Nguyễn Thị Lan (Khách hàng cuối)", "customer_name", "Chị Nguyễn Thị Lan (Khách hàng cuối)")
        except Exception:
            pass

    # Đồng bộ Customer Group cho các chứng từ giao dịch
    frappe.db.sql("UPDATE `tabCustomer` SET customer_group='Khách hàng cuối' WHERE customer_name LIKE '%Lan%' OR customer_name LIKE '%cuối%' OR customer_group='Individual'")
    frappe.db.sql("UPDATE `tabCustomer` SET customer_group='Đại lý' WHERE customer_group NOT IN ('Đại lý', 'Khách hàng cuối')")
    frappe.db.sql("UPDATE `tabSales Order` SET customer_group='Khách hàng cuối' WHERE customer_name LIKE '%Lan%' OR customer_group='Individual'")
    frappe.db.sql("UPDATE `tabSales Order` SET customer_group='Đại lý' WHERE customer_group NOT IN ('Đại lý', 'Khách hàng cuối')")
    frappe.db.sql("UPDATE `tabSales Invoice` SET customer_group='Khách hàng cuối' WHERE customer_name LIKE '%Lan%' OR customer_group='Individual'")
    frappe.db.sql("UPDATE `tabSales Invoice` SET customer_group='Đại lý' WHERE customer_group NOT IN ('Đại lý', 'Khách hàng cuối')")
    frappe.db.sql("UPDATE `tabDelivery Note` SET customer_group='Khách hàng cuối' WHERE customer_name LIKE '%Lan%' OR customer_group='Individual'")
    frappe.db.sql("UPDATE `tabDelivery Note` SET customer_group='Đại lý' WHERE customer_group NOT IN ('Đại lý', 'Khách hàng cuối')")

    if frappe.db.exists("DocType", "Selling Settings"):
        frappe.db.set_single_value("Selling Settings", "customer_group", "Khách hàng cuối")

    for cg in ["Commercial", "Individual", "Government", "Non Profit"]:
        if frappe.db.exists("Customer Group", cg):
            try:
                frappe.delete_doc("Customer Group", cg, force=True, ignore_permissions=True)
            except Exception:
                pass

    try:
        rebuild_tree("Customer Group")
    except Exception:
        pass
    print("✓ Đã chuẩn hóa danh mục Nhóm khách hàng: 'Đại lý' và 'Khách hàng cuối'.")

    # 3.3. Chuẩn hóa Nhóm sản phẩm: Duy nhất 'Thức uống dinh dưỡng' trực tiếp dưới 'All Item Groups'
    if frappe.db.exists("Item Group", "Thức uống dinh dưỡng"):
        frappe.db.set_value("Item Group", "Thức uống dinh dưỡng", "parent_item_group", "All Item Groups")
    else:
        frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": "Thức uống dinh dưỡng",
            "parent_item_group": "All Item Groups",
            "is_group": 0
        }).insert(ignore_permissions=True)

    for it in ["TBK-PLUS", "TBK-CACAO", "TBK-TIBOKA"]:
        if frappe.db.exists("Item", it):
            frappe.db.set_value("Item", it, "item_group", "Thức uống dinh dưỡng")

    for ig in ["Raw Material", "Services", "Sub Assemblies", "Consumable", "Products"]:
        if frappe.db.exists("Item Group", ig):
            try:
                frappe.delete_doc("Item Group", ig, force=True, ignore_permissions=True)
            except Exception:
                pass

    try:
        rebuild_tree("Item Group")
    except Exception:
        pass
    print("✓ Đã chuẩn hóa danh mục Nhóm sản phẩm: Duy nhất 'Thức uống dinh dưỡng', loại bỏ nguyên liệu & dịch vụ.")

    # 3.4. Cấu hình Domain Settings: Kích hoạt Retail, tắt Manufacturing
    try:
        if frappe.db.exists("DocType", "Domain Settings"):
            ds = frappe.get_doc("Domain Settings")
            ds.set("active_domains", [{"domain": "Retail"}])
            ds.save(ignore_permissions=True)
            print("✓ Đã cấu hình Domain Settings: Kích hoạt Retail, tắt hoàn toàn phân hệ Manufacturing.")
    except Exception as e:
        print(f"! Domain settings notice: {e}")

    # 3.5. Dọn dẹp Shortcuts & Cards trên các Workspace
    try:
        if frappe.db.exists("Workspace", "Home"):
            home_ws = frappe.get_doc("Workspace", "Home")
            needed_shortcuts = ["Dashboard Quản Trị", "Item", "Customer", "Sales Invoice", "Leaderboard", "Cấu hình WiFi Chấm công"]
            home_ws.shortcuts = [s for s in home_ws.shortcuts if s.label in needed_shortcuts or s.link_to in needed_shortcuts]
            if not any(s.link_to == "baka-dashboard" for s in home_ws.shortcuts):
                home_ws.append("shortcuts", {
                    "label": "Dashboard Quản Trị",
                    "type": "Page",
                    "link_to": "baka-dashboard",
                    "color": "Blue"
                })
            home_ws.save(ignore_permissions=True)

        if frappe.db.exists("Workspace", "CRM"):
            crm_ws = frappe.get_doc("Workspace", "CRM")
            crm_ws.links = [l for l in crm_ws.links if l.label != "Maintenance" and l.link_to not in ["Maintenance Schedule", "Maintenance Visit", "Warranty Claim"]]
            crm_ws.save(ignore_permissions=True)

        if frappe.db.exists("Workspace", "Stock"):
            stock_ws = frappe.get_doc("Workspace", "Stock")
            stock_ws.shortcuts = [s for s in stock_ws.shortcuts if s.label not in ["Material Request", "Purchase Receipt", "Learn Inventory Management"]]
            irrelevant_stock = [
                "Installation Note", "Serial No Service Contract Expiry", "Serial No Warranty Expiry",
                "Subcontracted Raw Materials To Be Transferred", "Subcontracted Item To Be Received"
            ]
            stock_ws.links = [l for l in stock_ws.links if l.label not in irrelevant_stock and l.link_to not in irrelevant_stock]
            stock_ws.save(ignore_permissions=True)
        print("✓ Đã dọn dẹp các mục thừa trên giao diện Home, CRM, Kho hàng (loại bỏ bảo trì, yêu cầu mua nguyên liệu, hợp đồng dịch vụ).")
    except Exception as e:
        print(f"! Workspace links cleanup notice: {e}")

    # 4. Check Company and its Chart of Accounts
    companies = frappe.get_all("Company", fields=["name", "company_name", "chart_of_accounts", "default_currency"])
    print(f"Current companies: {companies}")
    
    gl_entries = frappe.db.count("GL Entry")
    print(f"Total GL entries in system: {gl_entries}")

    vn_coa_name = "Việt Nam - Hệ thống tài khoản theo Thông tư 200/133"

    for comp in companies:
        if comp.chart_of_accounts != vn_coa_name and gl_entries == 0:
            print(f"Updating Chart of Accounts for company '{comp.name}' to Vietnamese TT 200/133...")
            
            # Ensure company currency in DB is VND and cache is cleared FIRST
            frappe.db.set_value("Company", comp.name, "default_currency", "VND", update_modified=False)
            frappe.db.set_value("Company", comp.name, "country", country_name, update_modified=False)
            frappe.clear_document_cache("Company", comp.name)
            
            # Clear old company default account fields in database
            account_fields = [
                "default_bank_account", "default_cash_account", "default_receivable_account", 
                "default_payable_account", "default_expense_account", "default_income_account", 
                "round_off_account", "round_off_cost_center", "write_off_account", 
                "discount_allowed_account", "discount_received_account", "exchange_gain_loss_account", 
                "unrealized_exchange_gain_loss_account", "accumulated_depreciation_account", 
                "depreciation_expense_account", "disposal_account", "depreciation_cost_center", 
                "default_inventory_account", "stock_adjustment_account", "stock_received_but_not_billed", 
                "expenses_included_in_valuation", "capital_work_in_progress_account",
                "expenses_included_in_asset_valuation", "asset_received_but_not_billed"
            ]
            for f in account_fields:
                try:
                    frappe.db.set_value("Company", comp.name, f, None, update_modified=False)
                except Exception:
                    pass
            
            # Clear Mode of Payment Accounts for this company
            frappe.db.sql("DELETE FROM `tabMode of Payment Account` WHERE company=%s", comp.name)
            
            # Delete old accounts
            frappe.db.sql("DELETE FROM `tabAccount` WHERE company=%s", comp.name)
            frappe.db.commit()

            # Recreate accounts using Vietnam template
            from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import create_charts
            create_charts(comp.name, vn_coa_name)
            
            # Update all created accounts to VND if empty
            frappe.db.sql("UPDATE `tabAccount` SET account_currency='VND' WHERE company=%s AND (account_currency IS NULL OR account_currency='')", comp.name)
            frappe.clear_cache(doctype="Account")

        # Configure company default accounts cleanly
        comp_doc = frappe.get_doc("Company", comp.name)
        comp_doc.chart_of_accounts = vn_coa_name
        comp_doc.country = country_name
        comp_doc.default_currency = "VND"
        comp_doc.update_default_account = 1
        
        recv = frappe.db.get_value("Account", {"company": comp.name, "name": ["like", "1311%"]})
        pay = frappe.db.get_value("Account", {"company": comp.name, "name": ["like", "3311%"]})
        inv = frappe.db.get_value("Account", {"company": comp.name, "name": ["like", "1561%"]})
        cash = frappe.db.get_value("Account", {"company": comp.name, "name": ["like", "1111%"]})
        bank = frappe.db.get_value("Account", {"company": comp.name, "name": ["like", "1121%"]})

        comp_doc.set_default_accounts()
        comp_doc.set_mode_of_payment_account()

        if recv:
            comp_doc.default_receivable_account = recv
        if pay:
            comp_doc.default_payable_account = pay
        if inv:
            comp_doc.default_inventory_account = inv
        if cash:
            comp_doc.default_cash_account = cash
        if bank:
            comp_doc.default_bank_account = bank

        comp_doc.flags.ignore_mandatory = True
        comp_doc.save(ignore_permissions=True)
        
        # Ensure direct db_set for precision
        if pay:
            comp_doc.db_set("default_payable_account", pay)
        if recv:
            comp_doc.db_set("default_receivable_account", recv)
        if inv:
            comp_doc.db_set("default_inventory_account", inv)

        print(f"✓ Configured standard Vietnamese defaults for {comp.name}")

    # 5. Fix Dashboard Charts dynamic filters (Eliminate invalid frappe.sys_defaults expression)
    frappe.db.sql("""
        UPDATE `tabDashboard Chart` 
        SET dynamic_filters_json = REPLACE(dynamic_filters_json, 'frappe.sys_defaults.fiscal_year', 'erpnext.utils.get_fiscal_year()')
        WHERE dynamic_filters_json LIKE '%frappe.sys_defaults%'
    """)
    print("✓ Fixed all Dashboard Charts dynamic filters to use valid fiscal_year expression")

    # 6. Setup Standard Vietnamese Fiscal Years (Calendar Year: 01/01 to 31/12)
    for yr in [2025, 2026, 2027]:
        year_name = str(yr)
        start_date = f"{yr}-01-01"
        end_date = f"{yr}-12-31"
        if not frappe.db.exists("Fiscal Year", year_name):
            fy_doc = frappe.get_doc({
                "doctype": "Fiscal Year",
                "year": year_name,
                "year_start_date": start_date,
                "year_end_date": end_date,
                "companies": [{"company": "BAKA"}]
            })
            fy_doc.insert(ignore_permissions=True)
            print(f"✓ Created standard Vietnamese Fiscal Year: {year_name} ({start_date} to {end_date})")
        else:
            if not frappe.db.exists("Fiscal Year Company", {"parent": year_name, "company": "BAKA"}):
                frappe.get_doc({
                    "doctype": "Fiscal Year Company",
                    "parent": year_name,
                    "parenttype": "Fiscal Year",
                    "parentfield": "companies",
                    "company": "BAKA"
                }).insert(ignore_permissions=True)

    # Set 2026 as the active default fiscal year
    frappe.db.set_default("fiscal_year", "2026")
    if frappe.db.exists("DocType", "Global Defaults"):
        frappe.db.set_single_value("Global Defaults", "current_fiscal_year", "2026")
        frappe.db.set_single_value("Global Defaults", "default_currency", "VND")
        frappe.db.set_single_value("Global Defaults", "country", country_name)
        frappe.db.set_single_value("Global Defaults", "default_company", "BAKA")
    print("✓ Set default active Fiscal Year to 2026 and Global Defaults")

    frappe.db.commit()
    print("=== BAKAERP Vietnam Configuration Complete ===")
