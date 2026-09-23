# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime

ALLOWED_REFERENCE_DOCTYPES = ["CRM Lead", "CRM Customer", "CRM Opportunity"]


class CRMActivity(Document):
	reference_doctype: str
	reference_name: str
	status: str
	activity_date: str | None

	def validate(self):
		self.validate_reference_doctype()

	def on_update(self):
		self.update_lead_last_contact()

	def validate_reference_doctype(self):
		"""BR-14: Limit reference_doctype to CRM Lead, CRM Customer, and CRM Opportunity."""
		if self.reference_doctype not in ALLOWED_REFERENCE_DOCTYPES:
			frappe.throw(
				_("Reference DocType must be one of: {0}").format(", ".join(ALLOWED_REFERENCE_DOCTYPES))
			)

		if not frappe.db.exists(self.reference_doctype, self.reference_name):
			frappe.throw(_("{0} '{1}' does not exist.").format(self.reference_doctype, self.reference_name))

	def update_lead_last_contact(self):
		"""Update last_contact_date on referenced Lead if activity is completed."""
		if self.status == "Completed" and self.reference_doctype == "CRM Lead" and self.reference_name:
			frappe.db.set_value(
				"CRM Lead",
				self.reference_name,
				"last_contact_date",
				self.activity_date or now_datetime(),
			)
