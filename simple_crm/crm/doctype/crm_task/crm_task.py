# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, today

ALLOWED_REFERENCE_DOCTYPES = ["CRM Lead", "CRM Customer", "CRM Opportunity"]


class CRMTask(Document):
	def validate(self):
		self.validate_reference_doctype()
		self.handle_completion_timestamp()

	def validate_reference_doctype(self):
		"""BR-14: Limit reference_doctype to CRM Lead, CRM Customer, and CRM Opportunity."""
		if self.reference_doctype not in ALLOWED_REFERENCE_DOCTYPES:
			frappe.throw(
				_("Reference DocType must be one of: {0}").format(", ".join(ALLOWED_REFERENCE_DOCTYPES))
			)

		if not frappe.db.exists(self.reference_doctype, self.reference_name):
			frappe.throw(_("{0} '{1}' does not exist.").format(self.reference_doctype, self.reference_name))

	def handle_completion_timestamp(self):
		"""Set completed_on timestamp when status becomes Completed."""
		if self.status == "Completed":
			if not self.completed_on:
				self.completed_on = now_datetime()
		else:
			self.completed_on = None

	def is_overdue(self):
		"""BR-11: A task is overdue if due_date < today and status is not Completed/Cancelled."""
		if not self.due_date:
			return False
		return getdate(self.due_date) < getdate(today()) and self.status not in ["Completed", "Cancelled"]
