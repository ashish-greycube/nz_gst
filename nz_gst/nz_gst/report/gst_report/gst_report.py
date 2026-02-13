# Copyright (c) 2026, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.accounts.utils import get_balance_on

def execute(filters=None):
	if not filters:
		filters = {}
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters)
	if not data:
		frappe.msgprint("No data found!", alert=True)
	return columns, data

def get_columns(filters):
	if filters.get("view_type") == "Detailed":
		columns = [
			dict(
				fieldname = 'section',
				fieldtype = "Data",
				label = "Section",
				width = 210
			),
			dict(
				fieldname = 'date',
				fieldtype = "Data",
				label = "Date",
				width = 110
			),
			dict(
				fieldname = 'invoice_ref',
				fieldtype = "Data",
				label = "Invoice Reference",
				width = 200
			),
			dict(
				fieldname = 'transaction_ref',
				fieldtype = "Data",
				label = "Transaction Reference",
				width = 200
			),
			dict(
				fieldname = 'excl_gst',
				fieldtype = "Currency",
				label = "Excl GST",
				width = 150
			),
			dict(
				fieldname = 'gst',
				fieldtype = "Currency",
				label = "GST",
				width = 150
			),
			dict(
				fieldname = 'incl_gst',
				fieldtype = "Currency",
				label = "Incl GST",
				width = 150
			),
			dict(
				fieldname = 'partner',
				fieldtype = "Data",
				label = "Partner",
				width = 212
			),
		]
	if filters.get("view_type") == "Summary":
		columns = [
			dict(
				fieldname = 'summary_section',
				fieldtype = "Data",
				label = "Summary Section",
				width = 250
			),
			dict(
				fieldname = 'category',
				fieldtype = "Data",
				label = "",
				width = 250
			),
			dict(
				fieldname = 'value_excl',
				fieldtype = "Currency",
				label = "Value Excl",
				width = 150
			),
			dict(
				fieldname = 'gst',
				fieldtype = "Currency",
				label = "GST",
				width = 150
			),
			dict(
				fieldname = 'value_incl',
				fieldtype = "Currency",
				label = "Value Incl",
				width = 150
			),
		]
	return columns

def get_data(filters):
	res = []

	gst_doc = frappe.get_doc("Company", filters.get("company"))

	if not gst_doc.get("custom_pt2"):
		frappe.throw(_("Set Sales & Purchase Item Tax Templates In Company {0} to fetch data.").format(filters.get("company")))

	exempt_pi = get_purchase_invoice_data_with_item_tax_template(filters, gst_doc.get("custom_pt2"))
	exempt_si = get_sales_invoice_data_with_item_tax_template(filters, gst_doc.get("custom_st2"))
	gst_pi = get_purchase_invoice_data_with_item_tax_template(filters, gst_doc.get("custom_pt1"))
	get_si = get_sales_invoice_data_with_item_tax_template(filters, gst_doc.get("custom_st1"))
	zero_rated_pi = get_purchase_invoice_data_with_item_tax_template(filters, gst_doc.get("custom_pt0"))
	zero_rated_si = get_sales_invoice_data_with_item_tax_template(filters, gst_doc.get("custom_st0"))

	if filters.get("view_type") == "Detailed":
		# if not gst_doc.pt2:
		# 	frappe.throw("Set Item Tax Template for Exempt Purchases In <b>GST Settings</b>.")
		# else:
		if len(exempt_pi) > 0:
			res.append({"section": "<b>Exempt purchases</b>", "excl_gst": None, "gst": None, "incl_gst": None })
			for data in exempt_pi:
				if data.get("excl_gst") == 0:
					data["excl_gst"] = None
				if data.get("gst") == 0:
					data["gst"] = None
				if data.get("incl_gst") == 0:
					data["incl_gst"] = None

				res.append(data)
			# res.extend(exempt_pi)
			res.append({"excl_gst": None, "gst": None, "incl_gst": None})
	
		if len(exempt_si) > 0:
			res.append({"section": "<b>Exempt sales</b>", "excl_gst": None, "gst": None, "incl_gst": None })
			for data in exempt_si:
				if data.get("excl_gst") == 0:
					data["excl_gst"] = None
				if data.get("gst") == 0:
					data["gst"] = None
				if data.get("incl_gst") == 0:
					data["incl_gst"] = None
				res.append(data)
			res.append({"excl_gst": None, "gst": None, "incl_gst": None})

		if len(gst_pi) > 0:
			res.append({"section": "<b>Purchase 15%</b>", "excl_gst": None, "gst": None, "incl_gst": None })
			for data in gst_pi:
				if data.get("excl_gst") == 0:
					data["excl_gst"] = None
				if data.get("gst") == 0:
					data["gst"] = None
				if data.get("incl_gst") == 0:
					data["incl_gst"] = None
				res.append(data)
			res.append({"excl_gst": None, "gst": None, "incl_gst": None})

		if len(get_si) > 0:
			res.append({"section": "<b>Standard rate sales (15%)</b>", "excl_gst": None, "gst": None, "incl_gst": None })
			for data in get_si:
				if data.get("excl_gst") == 0:
					data["excl_gst"] = None
				if data.get("gst") == 0:
					data["gst"] = None
				if data.get("incl_gst") == 0:
					data["incl_gst"] = None
				res.append(data)
			res.append({"excl_gst": None, "gst": None, "incl_gst": None})

		if len(zero_rated_pi) > 0:
			res.append({"section": "<b>Zero rated purchases</b>", "excl_gst": None, "gst": None, "incl_gst": None })
			for data in zero_rated_pi:
				if data.get("excl_gst") == 0:
					data["excl_gst"] = None
				if data.get("gst") == 0:
					data["gst"] = None
				if data.get("incl_gst") == 0:
					data["incl_gst"] = None
				res.append(data)
			res.append({"excl_gst": None, "gst": None, "incl_gst": None})

		if len(zero_rated_si) > 0:
			res.append({"section": "<b>Zero rated sales</b>", "excl_gst": None, "gst": None, "incl_gst": None })
			for data in zero_rated_si:
				if data.get("excl_gst") == 0:
					data["excl_gst"] = None
				if data.get("gst") == 0:
					data["gst"] = None
				if data.get("incl_gst") == 0:
					data["incl_gst"] = None
				res.append(data)
			res.append({"excl_gst": None, "gst": None, "incl_gst": None})

	elif filters.get("view_type") == "Summary":
		total_gst_collected = 0
		total_gst_paid = 0

		total_val_excl = 0
		total_val_incl = 0
		total_gst = 0

		if len(exempt_pi) > 0:
			d = {
				"summary_section" : "PT2",
				"category" : "Exempt purchases",
				"value_excl" : exempt_pi[-1]['excl_gst'],
				"gst" : exempt_pi[-1]['gst'],
				"value_incl" : exempt_pi[-1]['incl_gst'],
			}
			total_val_excl = total_val_excl + d.get("value_excl")
			total_val_incl = total_val_incl + d.get("value_incl")
			total_gst = total_gst + d.get("gst")

			total_gst_paid = total_gst_paid + d.get("gst")

			res.append(d)

		if len(exempt_si) > 0:
			d = {
				"summary_section" : "ST2",
				"category" : "Exempt sales",
				"value_excl" : exempt_si[-1]['excl_gst'],
				"gst" : exempt_si[-1]['gst'],
				"value_incl" : exempt_si[-1]['incl_gst'],
			}
			total_val_excl = total_val_excl + d.get("value_excl")
			total_val_incl = total_val_incl + d.get("value_incl")
			total_gst = total_gst + d.get("gst")

			total_gst_collected = total_gst_collected + d.get("gst")
			
			res.append(d)
		
		if len(gst_pi) > 0:
			d = {
				"summary_section" : "PT1",
				"category" : "Purchase 15%",
				"value_excl" : gst_pi[-1]['excl_gst'],
				"gst" : gst_pi[-1]['gst'],
				"value_incl" : gst_pi[-1]['incl_gst'],
			}
			total_val_excl = total_val_excl + d.get("value_excl")
			total_val_incl = total_val_incl + d.get("value_incl")
			total_gst = total_gst + d.get("gst")

			total_gst_paid = total_gst_paid + d.get("gst")

			res.append(d)

		if len(get_si) > 0:
			d = {
				"summary_section" : "ST1",
				"category" : "Standard rate sales (15%)",
				"value_excl" : get_si[-1]['excl_gst'],
				"gst" : get_si[-1]['gst'],
				"value_incl" : get_si[-1]['incl_gst'],
			}
			total_val_excl = total_val_excl + d.get("value_excl")
			total_val_incl = total_val_incl + d.get("value_incl")
			total_gst = total_gst + d.get("gst")

			total_gst_collected = total_gst_collected + d.get("gst")
			
			res.append(d)

		if len(zero_rated_pi) > 0:
			d = {
				"summary_section" : "PT0",
				"category" : "Zero rated purchases",
				"value_excl" : zero_rated_pi[-1]['excl_gst'],
				"gst" : zero_rated_pi[-1]['gst'],
				"value_incl" : zero_rated_pi[-1]['incl_gst'],
			}
			total_val_excl = total_val_excl + d.get("value_excl")
			total_val_incl = total_val_incl + d.get("value_incl")
			total_gst = total_gst + d.get("gst")

			total_gst_paid = total_gst_paid + d.get("gst")

			res.append(d)

		if len(zero_rated_si) > 0:
			d = {
				"summary_section" : "ST0",
				"category" : "Zero rated sales",
				"value_excl" : zero_rated_si[-1]['excl_gst'],
				"gst" : zero_rated_si[-1]['gst'],
				"value_incl" : zero_rated_si[-1]['incl_gst'],
			}
			total_val_excl = total_val_excl + d.get("value_excl")
			total_val_incl = total_val_incl + d.get("value_incl")
			total_gst = total_gst + d.get("gst")

			total_gst_collected = total_gst_collected + d.get("gst")
			
			res.append(d)

		res.append({
			"category" : "Total",
			"value_excl" : total_val_excl,
			"gst" : total_gst,
			"value_incl" : total_val_incl
		})

		res.append({
			"value_excl" : None,
			"gst" : None,
			"value_incl" : None
		})

		res.append({
			"summary_section" : "GL Movement",
			"category": "GST Collected",
			"value_excl" : -total_gst_collected if total_gst_collected != 0 else 0,
			"gst" : None,
			"value_incl" : None
		})

		res.append({
			"category": "GST Paid",
			"value_excl" : -total_gst_paid if total_gst_paid != 0 else 0,
			"gst" : None,
			"value_incl" : None
		})
		
		res.append({
			"category": "Nett",
			"value_excl" : (-total_gst_collected + (-total_gst_paid)),
			"gst" : None,
			"value_incl" : None
		})

		get_gl_balances_rows(res, filters)
	
	return res


def get_sales_invoice_data_with_item_tax_template(filters, tax_template):
	data = frappe.db.sql(
		f'''
			SELECT 
				si.posting_date AS date, 
				si.name AS invoice_ref,
				si.name AS transaction_ref,
				IF(SUM(tsi.base_net_amount) > 0, SUM(tsi.base_net_amount), null) AS excl_gst,
				SUM(tsi.base_net_amount) AS excl_gst11,
				(SUM(tsi.base_net_amount) * (itt.tax_rate/100))  AS gst,
				(SUM(tsi.base_net_amount) + (SUM(tsi.base_net_amount) * (itt.tax_rate/100)) ) AS incl_gst,
				si.customer AS partner,
				1 AS indent
			FROM 
				`tabSales Invoice` si
			INNER JOIN `tabSales Invoice Item` tsi ON si.name = tsi.parent 
			INNER JOIN `tabItem Tax Template Detail` itt ON itt.parent = tsi.item_tax_template
			WHERE
				si.company = "{filters.get("company")}"
			AND 
				si.docstatus = 1
			AND 
				si.posting_date BETWEEN "{filters.get("from_date")}" AND "{filters.get("to_date")}"
			AND 
				tsi.item_tax_template = "{tax_template}"
			GROUP BY tsi.item_tax_template , si.name 
		''', as_dict = True)
	
	if len(data) > 0:
		total_gst = 0
		total_excl_gst = 0
		total_incl_gst = 0
		for d in data:
			total_gst = total_gst + d.gst
			total_excl_gst = total_excl_gst + d.excl_gst
			total_incl_gst = total_incl_gst + d.incl_gst
		data.append({
			"date": "Total",
			"excl_gst": total_excl_gst,
			"gst": total_gst,
			"incl_gst": total_incl_gst,
		})
	return data

def get_purchase_invoice_data_with_item_tax_template(filters, tax_template):
	data = frappe.db.sql(
		f'''
			SELECT 
				pi.posting_date AS date, 
				pi.name AS invoice_ref,
				pi.name AS transaction_ref,
				-1 * SUM(tpi.base_net_amount) AS excl_gst,
				-1 * (SUM(tpi.base_net_amount) * (itt.tax_rate/100)) AS gst,
				-1 * (SUM(tpi.base_net_amount) + (SUM(tpi.base_net_amount) * (itt.tax_rate/100)) ) AS incl_gst,
				pi.supplier AS partner,
				1 AS indent
			FROM 
				`tabPurchase Invoice` pi
			INNER JOIN `tabPurchase Invoice Item` tpi ON tpi.parent = pi.name 
			INNER JOIN `tabItem Tax Template Detail` itt ON itt.parent = tpi.item_tax_template
			WHERE
				pi.docstatus = 1
			AND 
				pi.company = "{filters.get("company")}"
			AND 
				pi.posting_date BETWEEN "{filters.get("from_date")}" AND "{filters.get("to_date")}"
			AND 
				tpi.item_tax_template = "{tax_template}"
			GROUP BY tpi.item_tax_template , pi.name
		''', as_dict = True)
	
	if len(data) > 0:
		total_gst = 0
		total_excl_gst = 0
		total_incl_gst = 0
		for d in data:
			total_gst = total_gst + d.gst
			total_excl_gst = total_excl_gst + d.excl_gst
			total_incl_gst = total_incl_gst + d.incl_gst
		data.append({
			"date": "Total",
			"excl_gst": total_excl_gst,
			"gst": total_gst,
			"incl_gst": total_incl_gst,
		})

	return data

def get_gl_balances_rows(res, filters):
	default_account_for_gst_collected = frappe.get_value("Company", filters.get("company"), "custom_default_account_for_gst_collected")
	default_account_for_gst_paid = frappe.get_value("Company", filters.get("company"), "custom_default_account_for_gst_paid")

	collected_balance = get_balance_on(account = default_account_for_gst_collected, company = filters.get("company"))
	paid_balance = get_balance_on(account = default_account_for_gst_paid, company = filters.get("company"))
	
	res.append({
		"value_excl" : None,
		"gst" : None,
		"value_incl" : None
	})

	res.append({
		"summary_section" : "GL Balances",
		"category": "GST Collected",
		"value_excl" : collected_balance if collected_balance else 0,
		"gst" : None,
		"value_incl" : None
	})

	res.append({
		"category": "GST Paid",
		"value_excl" : paid_balance if paid_balance else 0,
		"gst" : None,
		"value_incl" : None
	})

	res.append({
		"category": "Balance",
		"value_excl" : (collected_balance + paid_balance) if collected_balance and paid_balance else 0,
		"gst" : None,
		"value_incl" : None
	})

	if not default_account_for_gst_collected or not default_account_for_gst_paid:
		frappe.msgprint(_("GL Balances are not calculated as the Default Accounts are not set in Company {0}.").format(filters.get("company")), alert=True)