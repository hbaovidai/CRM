# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestCRMOpportunity(IntegrationTestCase):
	def setUp(self):
		frappe.db.delete("CRM Opportunity")
		frappe.db.delete("CRM Customer")
		if not frappe.db.exists("CRM Lost Reason", "High Price"):
			frappe.get_doc({
				"doctype": "CRM Lost Reason",
				"reason_name": "High Price",
				"is_active": 1,
			}).insert()

		self.customer = frappe.get_doc({
			"doctype": "CRM Customer",
			"customer_name": "Opportunity Test Customer",
			"customer_type": "Organization",
			"sales_owner": "Administrator",
		}).insert()

	def test_opportunity_negative_amount(self):
		"""BR-07: Opportunity amount must be >= 0."""
		opp = frappe.new_doc("CRM Opportunity")
		opp.opportunity_title = "Invalid Amount Deal"
		opp.customer = self.customer.name
		opp.sales_owner = "Administrator"
		opp.amount = -100
		opp.expected_close_date = "2026-12-31"

		self.assertRaises(frappe.ValidationError, opp.insert)

	def test_opportunity_stage_probability_mapping(self):
		"""BR-08: Probability defaults by stage."""
		opp = frappe.get_doc({
			"doctype": "CRM Opportunity",
			"opportunity_title": "Prob Mapping Deal",
			"customer": self.customer.name,
			"sales_owner": "Administrator",
			"stage": "New",
			"amount": 20000,
			"expected_close_date": "2026-11-30",
		}).insert()

		self.assertEqual(opp.probability, 10)

		opp.stage = "Proposal"
		opp.save()
		self.assertEqual(opp.probability, 50)

		opp.stage = "Negotiation"
		opp.save()
		self.assertEqual(opp.probability, 75)

		opp.stage = "Won"
		opp.save()
		self.assertEqual(opp.probability, 100)
		self.assertIsNotNone(opp.actual_close_date)

	def test_opportunity_lost_requires_reason(self):
		"""BR-09: Lost stage requires lost_reason."""
		opp = frappe.get_doc({
			"doctype": "CRM Opportunity",
			"opportunity_title": "Lost Deal Test",
			"customer": self.customer.name,
			"sales_owner": "Administrator",
			"stage": "Qualified",
			"amount": 15000,
			"expected_close_date": "2026-11-15",
		}).insert()

		opp.stage = "Lost"
		opp.lost_reason = None
		self.assertRaises(frappe.ValidationError, opp.save)

		opp.reload()
		opp.stage = "Lost"
		opp.lost_reason = "High Price"
		opp.save()
		self.assertEqual(opp.stage, "Lost")
		self.assertEqual(opp.probability, 0)
		self.assertIsNotNone(opp.actual_close_date)
