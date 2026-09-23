# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, today

STAGE_PROBABILITY_MAP = {
	"New": 10,
	"Qualified": 25,
	"Proposal": 50,
	"Negotiation": 75,
	"Won": 100,
	"Lost": 0,
}


class CRMOpportunity(Document):
	def validate(self):
		self.validate_financials()
		self.set_probability_and_dates()
		self.validate_closed_state()

	def validate_financials(self):
		"""BR-07: amount must be >= 0."""
		if flt(self.amount) < 0:
			frappe.throw(_("Deal amount cannot be negative."))

		if self.stage not in ["Won", "Lost"] and not self.expected_close_date:
			frappe.throw(_("Expected Close Date is required for active opportunities."))

	def set_probability_and_dates(self):
		"""BR-08 & BR-09: Map probability and set actual_close_date when closing."""
		if self.stage in STAGE_PROBABILITY_MAP:
			self.probability = STAGE_PROBABILITY_MAP[self.stage]

		if self.stage in ["Won", "Lost"]:
			if not self.actual_close_date:
				self.actual_close_date = today()
			if self.stage == "Lost" and not self.lost_reason:
				frappe.throw(_("Lost Reason is mandatory when Opportunity is marked as Lost."))
		else:
			# Reset actual_close_date if reopened
			self.actual_close_date = None

	def validate_closed_state(self):
		"""Check permissions if a closed deal (Won/Lost) is being reopened."""
		if not self.is_new() and self.has_value_changed("stage"):
			old_stage = frappe.db.get_value("CRM Opportunity", self.name, "stage")
			if old_stage in ["Won", "Lost"] and self.stage not in ["Won", "Lost"]:
				settings = frappe.get_cached_doc("CRM Settings")
				if not settings.allow_sales_reopen_closed_deal:
					allowed_roles = {"System Manager", "CRM Admin", "CRM Sales Manager"}
					user_roles = set(frappe.get_roles(frappe.session.user))
					if not (allowed_roles & user_roles):
						frappe.throw(_("Only Sales Manager or Admin can reopen a closed Opportunity."))
