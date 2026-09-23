# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestCRMContact(IntegrationTestCase):
	def setUp(self):
		frappe.db.delete("CRM Contact")
		frappe.db.delete("CRM Customer")
		self.customer = frappe.get_doc({
			"doctype": "CRM Customer",
			"customer_name": "Test Customer for Contacts",
			"customer_type": "Organization",
			"sales_owner": "Administrator",
		}).insert()

	def test_contact_full_name_generation(self):
		contact = frappe.get_doc({
			"doctype": "CRM Contact",
			"customer": self.customer.name,
			"first_name": "Nguyen",
			"last_name": "Van B",
			"email": "vanb@example.com",
		}).insert()

		self.assertTrue(contact.name.startswith("CRM-CONT-"))
		self.assertEqual(contact.full_name, "Nguyen Van B")

	def test_primary_contact_uniqueness(self):
		"""BR-06: A customer can have multiple contacts, at most one marked primary."""
		contact1 = frappe.get_doc({
			"doctype": "CRM Contact",
			"customer": self.customer.name,
			"first_name": "Contact",
			"last_name": "One",
			"is_primary": 1,
		}).insert()

		self.customer.reload()
		self.assertEqual(self.customer.primary_contact, contact1.name)

		contact2 = frappe.get_doc({
			"doctype": "CRM Contact",
			"customer": self.customer.name,
			"first_name": "Contact",
			"last_name": "Two",
			"is_primary": 1,
		}).insert()

		contact1.reload()
		contact2.reload()
		self.customer.reload()

		self.assertEqual(contact1.is_primary, 0)
		self.assertEqual(contact2.is_primary, 1)
		self.assertEqual(self.customer.primary_contact, contact2.name)
