# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestCRMActivity(IntegrationTestCase):
	def setUp(self):
		frappe.db.delete("CRM Activity")
		frappe.db.delete("CRM Lead")

		if not frappe.db.exists("CRM Lead Source", "Website"):
			frappe.get_doc({
				"doctype": "CRM Lead Source",
				"source_name": "Website",
				"is_active": 1,
			}).insert()

		self.lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"lead_name": "Activity Prospect",
			"email": "activity@example.com",
			"source": "Website",
			"sales_owner": "Administrator",
		}).insert()

	def test_activity_creation_valid(self):
		act = frappe.get_doc({
			"doctype": "CRM Activity",
			"activity_type": "Call",
			"subject": "Discovery call with prospect",
			"reference_doctype": "CRM Lead",
			"reference_name": self.lead.name,
			"sales_owner": "Administrator",
			"status": "Completed",
		}).insert()

		self.assertTrue(act.name.startswith("CRM-ACT-"))

		# Verify lead last_contact_date updated
		self.lead.reload()
		self.assertIsNotNone(self.lead.last_contact_date)

	def test_invalid_reference_doctype(self):
		"""BR-14: Reference doctype cannot be arbitrary doctypes like User or ToDo."""
		act = frappe.new_doc("CRM Activity")
		act.activity_type = "Meeting"
		act.subject = "Invalid reference test"
		act.reference_doctype = "User"
		act.reference_name = "Administrator"
		act.sales_owner = "Administrator"

		self.assertRaises(frappe.ValidationError, act.insert)
