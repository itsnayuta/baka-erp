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
    print(f"  Country: {sys.country}")
    print(f"  Language: {sys.language}")
    print(f"  Timezone: {sys.time_zone}")
    print(f"  Date Format: {sys.date_format}")
    print(f"  Number Format: {sys.number_format}")
