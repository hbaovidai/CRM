// Copyright (c) 2026, Frappe Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("CRM Task", {
	setup(frm) {
		frm.set_query("reference_doctype", () => {
			return {
				filters: {
					name: ["in", ["CRM Lead", "CRM Customer", "CRM Opportunity"]],
				},
			};
		});
	},

	refresh(frm) {
		if (!frm.is_new() && frm.doc.status === "Open") {
			frm.add_custom_button(__("Mark as Completed"), () => {
				frm.set_value("status", "Completed");
				frm.save();
			}, __("Actions")).addClass("btn-success");
		}
	},
});
