# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime, validate_email_address


class CRMLead(Document):
	def validate(self):
		self.validate_contact_info()
		self.validate_status_transitions()
		self.check_duplicates()

	def validate_contact_info(self):
		"""BR-01: Lead must have lead_name and at least one of email or phone."""
		if not self.email and not self.phone:
			frappe.throw(_("Lead must have at least an Email or a Phone number."))

		if self.email:
			validate_email_address(self.email.strip(), throw=True)
			self.email = self.email.strip().lower()

		if self.phone:
			self.phone = self.phone.strip()

	def validate_status_transitions(self):
		"""BR-02 & BR-03: Manage status qualifications and conversion integrity."""
		# Prevent manually setting Converted status without linked customer
		if self.status == "Converted" and not self.converted_customer:
			frappe.throw(_("Status 'Converted' can only be set through the Lead Conversion action."))

		# Prevent reopening a converted lead
		if not self.is_new() and self.has_value_changed("status"):
			db_status = frappe.db.get_value("CRM Lead", self.name, "status")
			if db_status == "Converted":
				frappe.throw(_("A converted Lead cannot be reopened or edited."))

		# Stamp qualified_on when moving to Qualified
		if self.status == "Qualified" and not self.qualified_on:
			self.qualified_on = now_datetime()

		# Require unqualified_reason when Unqualified
		if self.status == "Unqualified" and not (self.unqualified_reason or "").strip():
			frappe.throw(_("Please provide an Unqualified Reason when marking a Lead as Unqualified."))

	def check_duplicates(self):
		"""Check for duplicate Leads based on CRM Settings configuration."""
		try:
			settings = frappe.get_cached_doc("CRM Settings")
		except Exception:
			return

		if settings.duplicate_check_email and self.email:
			existing = frappe.db.get_value(
				"CRM Lead",
				{
					"email": self.email,
					"name": ["!=", self.name or ""],
					"status": ["!=", "Unqualified"],
				},
				["name", "lead_name"],
				as_dict=True,
			)
			if existing:
				frappe.throw(
					_("A Lead with email '{0}' already exists: {1} ({2})").format(
						self.email, existing.lead_name, existing.name
					)
				)

		if settings.duplicate_check_phone and self.phone:
			existing = frappe.db.get_value(
				"CRM Lead",
				{
					"phone": self.phone,
					"name": ["!=", self.name or ""],
					"status": ["!=", "Unqualified"],
				},
				["name", "lead_name"],
				as_dict=True,
			)
			if existing:
				frappe.throw(
					_("A Lead with phone '{0}' already exists: {1} ({2})").format(
						self.phone, existing.lead_name, existing.name
					)
				)


@frappe.whitelist()
def convert_to_customer_and_opportunity(
	lead_id,
	customer_name=None,
	opportunity_title=None,
	amount=0,
	expected_close_date=None,
	create_opportunity=1,
):
	"""BR-04 & BR-05: Convert a Qualified Lead to Customer and Opportunity."""
	lead = frappe.get_doc("CRM Lead", lead_id)

	if lead.status != "Qualified":
		frappe.throw(_("Only Qualified Leads can be converted. Current status: {0}").format(lead.status))

	if lead.converted_customer:
		frappe.throw(_("This Lead has already been converted to Customer {0}.").format(lead.converted_customer))

	# 1. Create Customer
	final_customer_name = customer_name or lead.company_name or lead.lead_name
	customer = frappe.get_doc({
		"doctype": "CRM Customer",
		"customer_name": final_customer_name,
		"customer_type": "Organization" if lead.company_name else "Individual",
		"sales_owner": lead.sales_owner,
		"source_lead": lead.name,
		"email": lead.email,
		"phone": lead.phone,
		"status": "Active",
	}).insert()

	# 2. Create Primary Contact
	name_parts = (lead.lead_name or "").strip().split(" ", 1)
	first_name = name_parts[0]
	last_name = name_parts[1] if len(name_parts) > 1 else ""

	contact = frappe.get_doc({
		"doctype": "CRM Contact",
		"customer": customer.name,
		"first_name": first_name,
		"last_name": last_name,
		"email": lead.email,
		"phone": lead.phone,
		"is_primary": 1,
	}).insert()

	# 3. Create Opportunity (if requested)
	opportunity_name = None
	if frappe.parse_json(create_opportunity):
		from frappe.utils import add_days, flt, today

		final_opp_title = opportunity_title or _("Deal - {0}").format(final_customer_name)
		opp_close_date = expected_close_date or add_days(today(), 30)

		opp = frappe.get_doc({
			"doctype": "CRM Opportunity",
			"opportunity_title": final_opp_title,
			"customer": customer.name,
			"main_contact": contact.name,
			"source_lead": lead.name,
			"amount": flt(amount) or flt(lead.estimated_value) or 0,
			"expected_close_date": opp_close_date,
			"sales_owner": lead.sales_owner,
			"stage": "New",
		}).insert()
		opportunity_name = opp.name

	# 4. Update Lead to Converted
	lead.converted_customer = customer.name
	lead.converted_opportunity = opportunity_name
	lead.status = "Converted"
	lead.save()

	return {
		"customer": customer.name,
		"contact": contact.name,
		"opportunity": opportunity_name,
	}
