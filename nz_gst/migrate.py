import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_migration():
    custom_fields = {
        "Company" : [
            {
                "fieldname":"custom_gst_tab",
                "fieldtype":"Tab Break",
                "insert_after": "default_operating_cost_account",
                "label": "GST",
                "is_custom_field":1,
                "is_system_generated":0
            },
            {
                "fieldname":"custom_default_account_for_gst_collected",
                "label":"Default Account for GST Collected",
                "fieldtype":"Link",
                "options": "Account",
                "insert_after": "custom_gst_tab",
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
            {
                "fieldname":"custom_item_tax_template_section",
                "fieldtype":"Section Break",
                "insert_after": "custom_default_account_for_gst_paid",
                "label": "Item Tax Templates",
                "is_custom_field":1,
                "is_system_generated":0
            },
            {
                "fieldname":"custom_purchase_tax_col",
                "fieldtype":"Column Break",
                "insert_after": "custom_item_tax_template_section",
                "is_custom_field":1,
                "is_system_generated":0,
                "label": "Purchase Item Tax Templates"
            },
            {
                "fieldname":"custom_pt2",
                "fieldtype": "Link",
                "insert_after": "custom_purchase_tax_col",
                "label": "PT2",
                "options": "Item Tax Template",
                "is_custom_field":1,
                "is_system_generated":0,
                "reqd": 1
            },
            {
                "fieldname":"custom_pt1",
                "fieldtype": "Link",
                "insert_after": "custom_pt2",
                "label": "PT1",
                "options": "Item Tax Template",
                "is_custom_field":1,
                "is_system_generated":0,
                "reqd": 1
            },
            {
                "fieldname":"custom_pt0",
                "fieldtype": "Link",
                "insert_after": "custom_pt1",
                "label": "PT0",
                "options": "Item Tax Template",
                "is_custom_field":1,
                "is_system_generated":0,
                "reqd": 1
            },
            {
                "fieldname":"custom_sales_tax_col",
                "fieldtype":"Column Break",
                "insert_after": "custom_pt0",
                "is_custom_field":1,
                "is_system_generated":0,
                "label": "Sales Item Tax Templates"
            },
            {
                "fieldname":"custom_st2",
                "fieldtype": "Link",
                "insert_after": "custom_sales_tax_col",
                "label": "ST2",
                "options": "Item Tax Template",
                "is_custom_field":1,
                "is_system_generated":0,
                "reqd": 1
            },
            {
                "fieldname":"custom_st1",
                "fieldtype": "Link",
                "insert_after": "custom_st2",
                "label": "ST1",
                "options": "Item Tax Template",
                "is_custom_field":1,
                "is_system_generated":0,
                "reqd": 1
            },
            {
                "fieldname":"custom_st0",
                "fieldtype": "Link",
                "insert_after": "custom_st1",
                "label": "ST0",
                "options": "Item Tax Template",
                "is_custom_field":1,
                "is_system_generated":0,
                "reqd": 1
            },

        ]
    }

    print("NZ GST: Adding Custom Fields In Following Doctypes.....")
    for dt, fields in custom_fields.items():
        print("**********\n %s: " % dt, [d.get("fieldname") for d in fields])
    create_custom_fields(custom_fields)