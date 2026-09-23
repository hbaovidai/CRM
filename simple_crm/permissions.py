# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe

MANAGER_ROLES = {"System Manager", "CRM Admin", "CRM Sales Manager"}


def is_manager(user=None):
	user = user or frappe.session.user
	if user == "Administrator":
		return True
	user_roles = set(frappe.get_roles(user))
	return bool(MANAGER_ROLES & user_roles)


def get_lead_conditions(user):
	if is_manager(user):
		return ""
	return f"`tabCRM Lead`.sales_owner = {frappe.db.escape(user)}"


def has_lead_permission(doc, ptype="read", user=None):
	if is_manager(user):
		return True
	user = user or frappe.session.user
	return doc.sales_owner == user or doc.owner == user


def get_customer_conditions(user):
	if is_manager(user):
		return ""
	return f"`tabCRM Customer`.sales_owner = {frappe.db.escape(user)}"


def has_customer_permission(doc, ptype="read", user=None):
	if is_manager(user):
		return True
	user = user or frappe.session.user
	return doc.sales_owner == user or doc.owner == user


def get_opportunity_conditions(user):
	if is_manager(user):
		return ""
	return f"`tabCRM Opportunity`.sales_owner = {frappe.db.escape(user)}"


def has_opportunity_permission(doc, ptype="read", user=None):
	if is_manager(user):
		return True
	user = user or frappe.session.user
	return doc.sales_owner == user or doc.owner == user


def get_task_conditions(user):
	if is_manager(user):
		return ""
	return f"`tabCRM Task`.assigned_to = {frappe.db.escape(user)}"


def has_task_permission(doc, ptype="read", user=None):
	if is_manager(user):
		return True
	user = user or frappe.session.user
	return doc.assigned_to == user or doc.owner == user


def get_activity_conditions(user):
	if is_manager(user):
		return ""
	escaped_user = frappe.db.escape(user)
	return f"(`tabCRM Activity`.sales_owner = {escaped_user} OR `tabCRM Activity`.owner = {escaped_user})"


def has_activity_permission(doc, ptype="read", user=None):
	if is_manager(user):
		return True
	user = user or frappe.session.user
	return doc.sales_owner == user or doc.owner == user


def get_contact_conditions(user):
	if is_manager(user):
		return ""
	escaped_user = frappe.db.escape(user)
	return f"`tabCRM Contact`.customer in (SELECT name FROM `tabCRM Customer` WHERE sales_owner = {escaped_user})"


def has_contact_permission(doc, ptype="read", user=None):
	if is_manager(user):
		return True
	user = user or frappe.session.user
	cust_owner = frappe.db.get_value("CRM Customer", doc.customer, "sales_owner")
	return cust_owner == user or doc.owner == user
