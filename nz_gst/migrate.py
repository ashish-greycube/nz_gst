import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_migration():
    custom_fields = {
        "Company" : [
            {
                "fieldname":"custom_gst_section",
                "fieldtype":"Section Break",
                "insert_after": "default_deferred_expense_account",
                "label": "GST Accounts",
                "is_custom_field":1,
                "is_system_generated":0
            },
            {
                "fieldname":"custom_default_account_for_gst_collected",
                "label":"Default Account for GST Collected",
                "fieldtype":"Link",
                "options": "Account",
                "insert_after": "custom_gst_section",
                "is_custom_field":1,
                "is_system_generated":0
            },
            {
                "fieldname":"custom_gst_column",
                "fieldtype":"Column Break",
                "insert_after": "custom_default_account_for_gst_collected",
                "is_custom_field":1,
                "is_system_generated":0
            },
            {
                "fieldname":"custom_default_account_for_gst_paid",
                "label":"Default Account for GST Paid",
                "fieldtype":"Link",
                "options": "Account",
                "insert_after": "custom_gst_column",
                "is_custom_field":1,
                "is_system_generated":0
            },
        ]
    }

    print("NZ GST: Adding Custom Fields In Following Doctypes.....")
    for dt, fields in custom_fields.items():
        print("**********\n %s: " % dt, [d.get("fieldname") for d in fields])
    create_custom_fields(custom_fields)