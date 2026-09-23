// Copyright (c) 2026, Frappe Team and contributors
// For license information, please see license.txt

frappe.query_reports["Opportunity Pipeline"] = {
	filters: [
		{
			fieldname: "sales_owner",
			label: __("Sales Owner"),
			fieldtype: "Link",
			options: "User",
		},
		{
			fieldname: "stage",
			label: __("Stage"),
			fieldtype: "Select",
			options: "\nNew\nQualified\nProposal\nNegotiation\nWon\nLost",
		},
		{
			fieldname: "from_date",
			label: __("Expected Close From"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("Expected Close To"),
			fieldtype: "Date",
		},
	],
};
