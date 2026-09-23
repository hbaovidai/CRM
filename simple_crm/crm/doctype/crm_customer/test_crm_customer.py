# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestCRMCustomer(IntegrationTestCase):
	def setUp(self):
		frappe.db.delete("CRM Opportunity")
		frappe.db.delete("CRM Contact")
		frappe.db.delete("CRM Customer")

	def test_customer_creation(self):
		cust = frappe.get_doc({
			"doctype": "CRM Customer",
			"customer_name": "ABC Technology Joint Stock Co",
			"customer_type": "Organization",
			"sales_owner": "Administrator",
			"status": "Active",
		}).insert()

		self.assertTrue(cust.name.startswith("CRM-CUST-"))
		self.assertEqual(cust.status, "Active")

	def test_prevent_deletion_with_active_opportunity(self):
		"""BR-15: Prevent deleting customer when it has linked opportunities."""
		cust = frappe.get_doc({
			"doctype": "CRM Customer",
			"customer_name": "Deletable Customer",
			"customer_type": "Organization",
			"sales_owner": "Administrator",
		}).insert()

		opp = frappe.get_doc({
			"doctype": "CRM Opportunity",
			"opportunity_title": "ERP Implementation",
			"customer": cust.name,
			"sales_owner": "Administrator",
			"stage": "Proposal",
			"amount": 50000,
			"expected_close_date": "2026-10-31",
		}).insert()

		self.assertRaises(frappe.ValidationError, cust.delete)

		# If opportunity is removed first, deletion should succeed
		opp.delete()
		cust.delete()
		self.assertFalse(frappe.db.exists("CRM Customer", cust.name))
