// Copyright (c) 2026, Frappe Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("CRM Lead", {
	refresh(frm) {
		if (frm.is_new()) {
			return;
		}

		// If lead is converted, show informative banner and lock editing
		if (frm.doc.converted_customer) {
			frm.dashboard.set_headline_alert(
				__("This Lead has been converted to Customer <a href='/app/crm-customer/{0}'><b>{0}</b></a>.", [
					frm.doc.converted_customer,
				]),
				"green"
			);
			frm.disable_save();
			return;
		}

		// Show 'Convert' button only when Qualified and not yet converted
		if (frm.doc.status === "Qualified" && !frm.doc.converted_customer) {
			frm.add_custom_button(__("Convert to Customer / Deal"), () => {
				frm.trigger("show_conversion_dialog");
			}, __("Actions")).addClass("btn-primary");
		}

		// Quick Actions to log Activity and Task
		frm.add_custom_button(__("Log Activity"), () => {
			frappe.new_doc("CRM Activity", {
				reference_doctype: "CRM Lead",
				reference_name: frm.doc.name,
				sales_owner: frappe.session.user,
			});
		}, __("Create"));

		frm.add_custom_button(__("Add Task"), () => {
			frappe.new_doc("CRM Task", {
				reference_doctype: "CRM Lead",
				reference_name: frm.doc.name,
				assigned_to: frm.doc.sales_owner || frappe.session.user,
			});
		}, __("Create"));

		frm.trigger("toggle_unqualified_reason");
	},

	status(frm) {
		frm.trigger("toggle_unqualified_reason");
	},

	toggle_unqualified_reason(frm) {
		const is_unqualified = frm.doc.status === "Unqualified";
		frm.set_df_property("unqualified_reason", "reqd", is_unqualified ? 1 : 0);
	},

	show_conversion_dialog(frm) {
		const d = new frappe.ui.Dialog({
			title: __("Convert Lead to Customer & Deal"),
			fields: [
				{
					fieldname: "customer_name",
					fieldtype: "Data",
					label: __("Customer Name"),
					reqd: 1,
					default: frm.doc.company_name || frm.doc.lead_name,
				},
				{
					fieldname: "cb1",
					fieldtype: "Column Break",
				},
				{
					fieldname: "create_opportunity",
					fieldtype: "Check",
					label: __("Create Opportunity"),
					default: 1,
				},
				{
					fieldname: "sec_opp",
					fieldtype: "Section Break",
					label: __("Opportunity Details"),
					depends_on: "eval:doc.create_opportunity",
				},
				{
					fieldname: "opportunity_title",
					fieldtype: "Data",
					label: __("Opportunity Title"),
					default: __("Deal - {0}", [frm.doc.company_name || frm.doc.lead_name]),
					depends_on: "eval:doc.create_opportunity",
				},
				{
					fieldname: "amount",
					fieldtype: "Currency",
					label: __("Amount"),
					default: frm.doc.estimated_value || 0,
					depends_on: "eval:doc.create_opportunity",
				},
				{
					fieldname: "cb2",
					fieldtype: "Column Break",
				},
				{
					fieldname: "expected_close_date",
					fieldtype: "Date",
					label: __("Expected Close Date"),
					default: frappe.datetime.add_days(frappe.datetime.get_today(), 30),
					depends_on: "eval:doc.create_opportunity",
				},
			],
			primary_action_label: __("Convert"),
			primary_action(values) {
				d.hide();
				frappe.call({
					method: "simple_crm.crm.doctype.crm_lead.crm_lead.convert_to_customer_and_opportunity",
					args: {
						lead_id: frm.doc.name,
						customer_name: values.customer_name,
						opportunity_title: values.opportunity_title,
						amount: values.amount,
						expected_close_date: values.expected_close_date,
						create_opportunity: values.create_opportunity,
					},
					freeze: true,
					freeze_message: __("Converting Lead..."),
					callback(r) {
						if (r.message) {
							frappe.show_alert({
								message: __("Lead converted successfully!"),
								indicator: "green",
							});
							frm.reload_doc();
						}
					},
				});
			},
		});

		d.show();
	},
});
