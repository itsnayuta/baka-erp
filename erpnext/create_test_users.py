import frappe
from frappe.utils.password import update_password

TEST_USERS = [
    {
        "email": "ketoan@baka.vn",
        "first_name": "Nguyễn",
        "last_name": "Kế Toán",
        "roles": ["Accounts Manager", "Accounts User", "Item Manager"],
        "password": "123",
        "role_desc": "Kế toán trưởng / Kế toán viên (Quản lý thu chi, sổ sách, công nợ, hóa đơn)"
    },
    {
        "email": "banhang@baka.vn",
        "first_name": "Trần",
        "last_name": "Bán Hàng",
        "roles": ["Sales Manager", "Sales User", "Stock User"],
        "password": "123",
        "role_desc": "Nhân viên / Quản lý bán hàng (Báo giá, đơn hàng bán, khách hàng, CRM)"
    },
    {
        "email": "muahang@baka.vn",
        "first_name": "Lê",
        "last_name": "Mua Hàng",
        "roles": ["Purchase Manager", "Purchase User", "Stock User"],
        "password": "123",
        "role_desc": "Nhân viên / Quản lý mua hàng (Đơn mua hàng, nhà cung cấp, yêu cầu vật tư)"
    },
    {
        "email": "kho@baka.vn",
        "first_name": "Phạm",
        "last_name": "Quản Kho",
        "roles": ["Stock Manager", "Stock User"],
        "password": "123",
        "role_desc": "Thủ kho / Quản lý kho (Phiếu xuất nhập kho, tồn kho, kiểm kê, điều chuyển)"
    },
    {
        "email": "sanxuat@baka.vn",
        "first_name": "Hoàng",
        "last_name": "Sản Xuất",
        "roles": ["Manufacturing Manager", "Manufacturing User", "Stock User"],
        "password": "123",
        "role_desc": "Quản đốc sản xuất (Định mức BOM, lệnh sản xuất, kế hoạch sản xuất)"
    },
    {
        "email": "nhansu@baka.vn",
        "first_name": "Vũ",
        "last_name": "Nhân Sự",
        "roles": ["HR Manager", "HR User", "Leave Approver"],
        "password": "123",
        "role_desc": "Quản lý nhân sự (Nhân viên, chấm công, tính lương, tuyển dụng)"
    },
]

def run():
    print("=== Creating Test Users for ERPNext ===")

    # Ensure Administrator has standard password and language
    try:
        update_password("Administrator", "admin")
        admin = frappe.get_doc("User", "Administrator")
        admin.language = "vi"
        admin.save(ignore_permissions=True)
        print("Updated Administrator account (password: admin, language: vi)")
    except Exception as e:
        print(f"Error updating Administrator: {e}")

    for u in TEST_USERS:
        email = u["email"]
        try:
            if not frappe.db.exists("User", email):
                doc = frappe.get_doc({
                    "doctype": "User",
                    "email": email,
                    "first_name": u["first_name"],
                    "last_name": u["last_name"],
                    "enabled": 1,
                    "send_welcome_email": 0,
                    "language": "vi",
                    "user_type": "System User"
                })
                doc.insert(ignore_permissions=True)
            else:
                doc = frappe.get_doc("User", email)
                doc.first_name = u["first_name"]
                doc.last_name = u["last_name"]
                doc.enabled = 1
                doc.language = "vi"
                doc.user_type = "System User"
                doc.save(ignore_permissions=True)

            # Assign roles
            existing_roles = [r.role for r in doc.roles]
            for r in u["roles"]:
                if frappe.db.exists("Role", r) and r not in existing_roles:
                    doc.append("roles", {"role": r})
            
            doc.save(ignore_permissions=True)

            # Set password
            update_password(email, u["password"])
            print(f"Created/Updated test user: {email} (password: {u['password']})")
        except Exception as e:
            print(f"Error creating {email}: {e}")

    frappe.db.commit()
    print("=== Done Creating Test Users ===")
