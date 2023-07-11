// Copyright (c) 2023, kiran.c@indictrans.in and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Account Costing Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 0,
			
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 0,
			
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options":"Project",
			"width": "80",
			"reqd": 0,
			
		},

	]
};
