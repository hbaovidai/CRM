// Copyright (c) 2026, Frappe Team and contributors
// For license information, please see license.txt

frappe.query_reports["Deal Won/Lost Summary"] = {
	filters: [
		{
			fieldname: "sales_owner",
			label: __("Sales Owner"),
			fieldtype: "Link",
			options: "User",
		},
		{
			fieldname: "from_date",
			label: __("Closed From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("Closed To Date"),
			fieldtype: "Date",
		},
	],
};
