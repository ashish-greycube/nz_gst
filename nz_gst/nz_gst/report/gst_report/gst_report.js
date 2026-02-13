// Copyright (c) 2026, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["GST Report"] = {
	"filters": [
		{
			fieldname: "company",
			fieldtype: "Link",
			label: "Company",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
			get_query: function() {
				return {
					filters: {
						"default_currency": "NZD"
					}
				}
			}
		},
		{
			fieldname: "from_date",
			fieldtype: "Date",
			label: "From Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -2)
		},
		{
			fieldname: "to_date",
			fieldtype: "Date",
			label: "To Date",
			default: frappe.datetime.get_today()
		},
		{
			fieldname: "view_type",
			fieldtype: "Select",
			label: "View Type",
			options: "Detailed\nSummary",
			default: "Detailed",
			hidden: 1
		}
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && (data.date == "Total" || data.category == "Total")) {
			value = value.bold();
		}

		if (column && column.fieldname == "summary_section") {
			value = value.bold();
		}
		return value;
	},

	after_datatable_render: function (datatable) {
		$("div[title='Total']").css({
			"text-align": "right",
		})
	},

	onload: function (datatable) {
		console.log(datatable.get_filter_value("view_type"), "===frappe.query_report==")
		if ($("div[id='switch-buttons']").length == 0) {
			$('.layout-main-section').find(".page-form").after(
				`
				<div class="btn-group my-3" role="group" aria-label="Basic example" style="margin-left:68rem;" id="switch-buttons">
					<button type="button" class="btn btn-primary" id="detailed-btn">Detailed</button>
					<button type="button" class="btn btn-secondary" id="summary-btn">Summary</button>
				</div>
			`
			);
		}

		if (datatable.get_filter_value("view_type") == "Detailed"){
			$('button[id="detailed-btn"]').addClass("btn-primary").removeClass("btn-secondary");
			$('button[id="summary-btn"]').addClass("btn-secondary").removeClass("btn-primary");
		}
		else{
			$('button[id="detailed-btn"]').addClass("btn-secondary").removeClass("btn-primary");
			$('button[id="summary-btn"]').addClass("btn-primary").removeClass("btn-secondary");
		}

		$('button[id="detailed-btn"]').on("click", function () {
			frappe.query_report.set_filter_value("view_type", "Detailed")
			$('button[id="detailed-btn"]').addClass("btn-primary").removeClass("btn-secondary");
			$('button[id="summary-btn"]').addClass("btn-secondary").removeClass("btn-primary");
		});

		$('button[id="summary-btn"]').on("click", function () {
			frappe.query_report.set_filter_value("view_type", "Summary");
			$('button[id="detailed-btn"]').addClass("btn-secondary").removeClass("btn-primary");
			$('button[id="summary-btn"]').addClass("btn-primary").removeClass("btn-secondary");
		});
	}
};