import frappe
from frappe import _

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

    # 1.1 Navbar Settings (Hide foreign/external Frappe/ERPNext help links)
    try:
        navbar_settings = frappe.get_single("Navbar Settings")
        for item in navbar_settings.help_dropdown:
            item.hidden = 1
        for item in navbar_settings.settings_dropdown:
            if any(term in (item.route or "").lower() for term in ["docs", "frappe", "erpnext", "discuss", "school", "issue"]):
                item.hidden = 1
        navbar_settings.save(ignore_permissions=True)
        print("✓ Configured Navbar Settings (App Name: BAKAERP, hid all external foreign links)")
    except Exception as e:
        print(f"! Navbar Settings notice: {e}")

    # 1.2 Website Settings (Clear old app footers and powered by)
    try:
        if frappe.db.exists("DocType", "Website Settings"):
            web_settings = frappe.get_single("Website Settings")
            web_settings.app_name = "BAKAERP"
            web_settings.copyright = "BAKAERP"
            web_settings.footer_powered = ""
            web_settings.hide_footer_signup = 1
            web_settings.save(ignore_permissions=True)
            print("✓ Configured Website Settings (BAKAERP branding, removed external footers)")
    except Exception as e:
        print(f"! Website Settings notice: {e}")

    # 2. Setup Vietnam Address Template
    from erpnext.regional.address_template.setup import update_address_template
    vn_template = """{{ address_line1 }}<br>
{% if address_line2 %}{{ address_line2 }}<br>{% endif -%}
{% if city %}{{ city }}, {% endif -%}{% if state %}{{ state }}{% endif -%}{% if pincode %} {{ pincode }}{% endif -%}<br>
Việt Nam"""
    update_address_template(country_name, vn_template, is_default=1)
    print(f"✓ Configured {country_name} Address Template as default")

    # 3. Hide bloat / irrelevant workspaces
    bloat_workspaces = [
        "Integration", "Integrations", "Settings", "ERPNext Settings", 
        "ERPNext Integrations", "Non Profit", "Agriculture", "Healthcare", 
        "Hospitality", "Quality", "Build", "Welcome Workspace", "Tools", "Website"
    ]
    for ws in bloat_workspaces:
        if frappe.db.exists("Workspace", ws):
            frappe.db.set_value("Workspace", ws, "public", 0)
    print(f"✓ Hidden unnecessary/foreign workspaces: {', '.join(bloat_workspaces)}")

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
    print("✓ Set default active Fiscal Year to 2026")

    frappe.db.commit()
    print("=== BAKAERP Vietnam Configuration Complete ===")
