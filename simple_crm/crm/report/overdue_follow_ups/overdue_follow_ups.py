# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff, getdate, today


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	summary = get_summary(data)
	return columns, data, None, None, summary


def get_columns():
	return [
		{
			"label": _("Task ID"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "CRM Task",
			"width": 160,
		},
		{
			"label": _("Subject"),
			"fieldname": "subject",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Assigned To"),
			"fieldname": "assigned_to",
			"fieldtype": "Link",
			"options": "User",
			"width": 150,
		},
		{
			"label": _("Due Date"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"label": _("Days Overdue"),
			"fieldname": "days_overdue",
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"label": _("Priority"),
			"fieldname": "priority",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 110,
		},
		{
			"label": _("Reference DocType"),
			"fieldname": "reference_doctype",
			"fieldtype": "Link",
			"options": "DocType",
			"width": 140,
		},
		{
			"label": _("Reference Name"),
			"fieldname": "reference_name",
			"fieldtype": "Dynamic Link",
			"options": "reference_doctype",
			"width": 180,
		},
	]


def get_data(filters):
	conditions = [
		f"due_date < {frappe.db.escape(today())}",
		"status NOT IN ('Completed', 'Cancelled')",
	]

	if filters.get("assigned_to"):
		conditions.append(f"assigned_to = {frappe.db.escape(filters.get('assigned_to'))}")
	if filters.get("priority"):
		conditions.append(f"priority = {frappe.db.escape(filters.get('priority'))}")

	where_clause = f"WHERE {' AND '.join(conditions)}"

	tasks = frappe.db.sql(
		f"""
		SELECT
			name,
			subject,
			assigned_to,
			due_date,
			priority,
			status,
			reference_doctype,
			reference_name
		FROM `tabCRM Task`
		{where_clause}
		ORDER BY due_date ASC
		""",
		as_dict=True,
	)

	today_date = getdate(today())
	for row in tasks:
		row.days_overdue = date_diff(today_date, getdate(row.due_date))

	return tasks


def get_summary(data):
	total_overdue = len(data)
	critical_count = sum(1 for d in data if d.get("priority") == "High")

	return [
		{
			"value": total_overdue,
			"indicator": "Red" if total_overdue > 0 else "Green",
			"label": _("Total Overdue Tasks"),
			"datatype": "Int",
		},
		{
			"value": critical_count,
			"indicator": "Orange",
			"label": _("High Priority Overdue"),
			"datatype": "Int",
		},
	]
