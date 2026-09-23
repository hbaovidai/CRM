# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CRMCustomer(Document):
	def on_trash(self):
		"""BR-15: Prevent destructive deletion if transactions/history exist."""
		has_opp = frappe.db.exists("CRM Opportunity", {"customer": self.name})
		if has_opp:
			frappe.throw(_("Cannot delete Customer {0} because it has associated Opportunities.").format(self.name))
