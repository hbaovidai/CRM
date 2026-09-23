// Copyright (c) 2026, Frappe Team and contributors
// For license information, please see license.txt

frappe.query_reports["Overdue Follow-ups"] = {
	filters: [
		{
			fieldname: "assigned_to",
			label: __("Assigned To"),
			fieldtype: "Link",
			options: "User",
		},
		{
			fieldname: "priority",
			label: __("Priority"),
			fieldtype: "Select",
			options: "\nLow\nMedium\nHigh",
		},
	],
};
