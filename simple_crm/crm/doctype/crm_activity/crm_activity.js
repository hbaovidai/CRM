// Copyright (c) 2026, Frappe Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("CRM Activity", {
	setup(frm) {
		frm.set_query("reference_doctype", () => {
			return {
				filters: {
					name: ["in", ["CRM Lead", "CRM Customer", "CRM Opportunity"]],
				},
			};
		});
	},
});
