# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMContact(Document):
	def validate(self):
		self.set_full_name()

	def on_update(self):
		self.handle_primary_contact()

	def set_full_name(self):
		self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()

	def handle_primary_contact(self):
		"""BR-06: Ensure at most one primary contact per customer."""
		if self.is_primary:
			# Unset other primary contacts for this customer
			frappe.db.sql(
				"""
				UPDATE `tabCRM Contact`
				SET is_primary = 0
				WHERE customer = %s AND name != %s AND is_primary = 1
				""",
				(self.customer, self.name),
			)
			# Update customer's primary_contact link
			frappe.db.set_value("CRM Customer", self.customer, "primary_contact", self.name)
