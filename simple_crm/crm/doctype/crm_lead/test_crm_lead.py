# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestCRMLead(IntegrationTestCase):
	def setUp(self):
		frappe.db.delete("CRM Lead")
		# Ensure at least one Lead Source exists
		if not frappe.db.exists("CRM Lead Source", "Website"):
			frappe.get_doc({
				"doctype": "CRM Lead Source",
				"source_name": "Website",
				"is_active": 1,
			}).insert()

		# Ensure CRM Settings has duplicate checks enabled
		settings = frappe.get_single("CRM Settings")
		settings.duplicate_check_email = 1
		settings.duplicate_check_phone = 1
		settings.save()

	def test_lead_contact_info_mandatory(self):
		"""BR-01: Lead must have lead_name and at least one of email or phone."""
		lead = frappe.new_doc("CRM Lead")
		lead.lead_name = "Test Prospect"
		lead.source = "Website"
		lead.sales_owner = "Administrator"
		lead.email = None
		lead.phone = None

		self.assertRaises(frappe.ValidationError, lead.insert)

	def test_lead_creation_valid(self):
		"""Test successful creation and naming series generation."""
		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"lead_name": "Nguyen Van A",
			"company_name": "Acme Corp",
			"email": "nguyenvana@example.com",
			"phone": "0901234567",
			"source": "Website",
			"sales_owner": "Administrator",
			"status": "New",
		}).insert()

		self.assertTrue(lead.name.startswith("CRM-LEAD-"))
		self.assertEqual(lead.status, "New")

	def test_lead_duplicate_email(self):
		"""Check duplicate email prevention."""
		frappe.get_doc({
			"doctype": "CRM Lead",
			"lead_name": "First Lead",
			"email": "duplicate@example.com",
			"source": "Website",
			"sales_owner": "Administrator",
		}).insert()

		second_lead = frappe.new_doc("CRM Lead")
		second_lead.lead_name = "Second Lead"
		second_lead.email = "duplicate@example.com"
		second_lead.source = "Website"
		second_lead.sales_owner = "Administrator"

		self.assertRaises(frappe.ValidationError, second_lead.insert)

	def test_lead_qualification_timestamp(self):
		"""BR-02: Moving to Qualified automatically sets qualified_on timestamp."""
		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"lead_name": "Qualify Prospect",
			"email": "qualify@example.com",
			"source": "Website",
			"sales_owner": "Administrator",
			"status": "New",
		}).insert()

		self.assertIsNone(lead.qualified_on)

		lead.status = "Qualified"
		lead.save()

		self.assertIsNotNone(lead.qualified_on)

	def test_lead_unqualified_reason_required(self):
		"""Marking as Unqualified requires an unqualified_reason."""
		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"lead_name": "Unqualified Prospect",
			"email": "unqualified@example.com",
			"source": "Website",
			"sales_owner": "Administrator",
			"status": "New",
		}).insert()

		lead.status = "Unqualified"
		lead.unqualified_reason = None
		self.assertRaises(frappe.ValidationError, lead.save)

		lead.reload()
		lead.status = "Unqualified"
		lead.unqualified_reason = "No budget this year"
		lead.save()
		self.assertEqual(lead.status, "Unqualified")

	def test_cannot_manually_set_converted(self):
		"""BR-02 & BR-04: Cannot manually change status to Converted without conversion action."""
		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"lead_name": "Prospect Convert Test",
			"email": "convert_manual@example.com",
			"source": "Website",
			"sales_owner": "Administrator",
			"status": "Qualified",
		}).insert()

		lead.status = "Converted"
		self.assertRaises(frappe.ValidationError, lead.save)

	def test_lead_conversion_success(self):
		"""BR-04 & BR-05: Convert a Qualified Lead to Customer + Contact + Opportunity."""
		from simple_crm.crm.doctype.crm_lead.crm_lead import convert_to_customer_and_opportunity

		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"lead_name": "Nguyen Hoang Long",
			"company_name": "Long Hoang Logistics",
			"email": "long@logistics.vn",
			"phone": "0988776655",
			"source": "Website",
			"sales_owner": "Administrator",
			"estimated_value": 120000,
			"status": "Qualified",
		}).insert()

		result = convert_to_customer_and_opportunity(
			lead_id=lead.name,
			customer_name="Long Hoang Logistics Ltd",
			opportunity_title="Logistics Management Software",
			amount=120000,
			expected_close_date="2026-12-15",
			create_opportunity=1,
		)

		self.assertTrue(result["customer"].startswith("CRM-CUST-"))
		self.assertTrue(result["contact"].startswith("CRM-CONT-"))
		self.assertTrue(result["opportunity"].startswith("CRM-OPP-"))

		# Verify Customer
		customer = frappe.get_doc("CRM Customer", result["customer"])
		self.assertEqual(customer.customer_name, "Long Hoang Logistics Ltd")
		self.assertEqual(customer.primary_contact, result["contact"])

		# Verify Contact
		contact = frappe.get_doc("CRM Contact", result["contact"])
		self.assertEqual(contact.first_name, "Nguyen")
		self.assertEqual(contact.last_name, "Hoang Long")
		self.assertEqual(contact.is_primary, 1)

		# Verify Opportunity
		opp = frappe.get_doc("CRM Opportunity", result["opportunity"])
		self.assertEqual(opp.amount, 120000)
		self.assertEqual(opp.customer, customer.name)
		self.assertEqual(opp.main_contact, contact.name)

		# Verify Lead updated
		lead.reload()
		self.assertEqual(lead.status, "Converted")
		self.assertEqual(lead.converted_customer, customer.name)
		self.assertEqual(lead.converted_opportunity, opp.name)

	def test_cannot_convert_unqualified_lead(self):
		"""Lead must be in Qualified status before conversion."""
		from simple_crm.crm.doctype.crm_lead.crm_lead import convert_to_customer_and_opportunity

		lead = frappe.get_doc({
			"doctype": "CRM Lead",
			"lead_name": "Not Qualified Prospect",
			"email": "notqual@example.com",
			"source": "Website",
			"sales_owner": "Administrator",
			"status": "Contacted",
		}).insert()

		self.assertRaises(
			frappe.ValidationError,
			convert_to_customer_and_opportunity,
			lead_id=lead.name,
		)
