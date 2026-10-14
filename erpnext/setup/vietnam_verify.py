import frappe

def verify():
    comp = frappe.get_doc("Company", "BAKA")
    print(f"Company: {comp.name}")
    print(f"  Country: {comp.country}")
    print(f"  Currency: {comp.default_currency}")
    print(f"  Chart of Accounts: {comp.chart_of_accounts}")
    print(f"  Default Bank Account: {comp.default_bank_account}")
    print(f"  Default Cash Account: {comp.default_cash_account}")
    print(f"  Default Receivable Account: {comp.default_receivable_account}")
    print(f"  Default Payable Account: {comp.default_payable_account}")
    print(f"  Default Inventory Account: {comp.default_inventory_account}")
    print(f"  Default Income Account: {comp.default_income_account}")
    print(f"  Default Expense Account: {comp.default_expense_account}")
    print(f"  Round Off Account: {comp.round_off_account}")
    
    accounts = frappe.get_all("Account", filters={"company": "BAKA"}, fields=["name", "account_name", "account_type", "root_type"], limit=20)
    print(f"Total accounts in BAKA: {frappe.db.count('Account', {'company': 'BAKA'})}")
    payables = frappe.get_all("Account", filters={"company": "BAKA", "account_type": "Payable"}, fields=["name", "account_name"])
    print("All Payable accounts in BAKA:")
    for p in payables:
        print(f"  * {p.name}")

    public_workspaces = frappe.get_all("Workspace", filters={"public": 1}, pluck="name")
    print("\nPublic Workspaces currently visible:")
    for w in sorted(public_workspaces):
        print(f"  - {w}")

    sys = frappe.get_doc("System Settings")
    print(f"\nSystem Settings:")
    print(f"  App Name: {sys.app_name}")
    print(f"  Country: {sys.country}")
    print(f"  Language: {sys.language}")
    print(f"  Timezone: {sys.time_zone}")
    print(f"  Date Format: {sys.date_format}")
    print(f"  Number Format: {sys.number_format}")

    nav = frappe.get_doc("Navbar Settings")
    visible_help = [i.item_label for i in nav.help_dropdown if not i.hidden]
    print(f"\nNavbar Settings:")
    print(f"  Visible Help Items: {visible_help}")

    if frappe.db.exists("DocType", "Website Settings"):
        web = frappe.get_doc("Website Settings")
        print(f"\nWebsite Settings:")
        print(f"  App Name: {web.app_name}")
        print(f"  Copyright: {web.copyright}")
        print(f"  Footer Powered: {web.footer_powered}")

    fys = frappe.get_all("Fiscal Year", fields=["name", "year_start_date", "year_end_date"])
    print(f"\nFiscal Years: {fys}")
    
    from erpnext.accounts.utils import get_fiscal_years
    now = frappe.utils.nowdate()
    print(f"\nNow date: {now}")
    print(f"Default fiscal year: {frappe.db.get_default('fiscal_year')}")
    print(f"Fiscal year for {now} and BAKA: {get_fiscal_years(now, company='BAKA', boolean=True)}")
    print(f"Fiscal Year Company records: {frappe.get_all('Fiscal Year Company', fields=['*'])}")

    # Check Dashboard Charts with from_fiscal_year
    charts = frappe.get_all("Dashboard Chart", fields=["name", "dynamic_filters_json", "filters_json"])
    print(f"\nDashboard Charts with dynamic filters:")
    for c in charts:
        if c.dynamic_filters_json and "fiscal_year" in c.dynamic_filters_json:
            print(f"  Chart: {c.name} -> {c.dynamic_filters_json}")
