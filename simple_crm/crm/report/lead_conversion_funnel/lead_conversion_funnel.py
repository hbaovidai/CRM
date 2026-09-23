# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary


def get_columns():
	return [
		{
			"label": _("Lead Source"),
			"fieldname": "source",
			"fieldtype": "Link",
			"options": "CRM Lead Source",
			"width": 180,
		},
		{
			"label": _("Total Leads"),
			"fieldname": "total_leads",
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"label": _("Contacted"),
			"fieldname": "contacted",
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"label": _("Qualified"),
			"fieldname": "qualified",
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"label": _("Converted"),
			"fieldname": "converted",
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"label": _("Conversion Rate (%)"),
			"fieldname": "conversion_rate",
			"fieldtype": "Percent",
			"width": 150,
		},
	]


def get_data(filters):
	conditions = []
	if filters.get("sales_owner"):
		conditions.append(f"sales_owner = {frappe.db.escape(filters.get('sales_owner'))}")
	if filters.get("from_date"):
		conditions.append(f"creation >= {frappe.db.escape(filters.get('from_date'))}")
	if filters.get("to_date"):
		conditions.append(f"creation <= {frappe.db.escape(filters.get('to_date') + ' 23:59:59')}")

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	sources = frappe.db.sql(
		f"""
		SELECT
			COALESCE(source, 'Unassigned') as source,
			COUNT(name) as total_leads,
			SUM(CASE WHEN status IN ('Contacted', 'Qualified', 'Converted') THEN 1 ELSE 0 END) as contacted,
			SUM(CASE WHEN status IN ('Qualified', 'Converted') THEN 1 ELSE 0 END) as qualified,
			SUM(CASE WHEN status = 'Converted' THEN 1 ELSE 0 END) as converted
		FROM `tabCRM Lead`
		{where_clause}
		GROUP BY source
		ORDER BY total_leads DESC
		""",
		as_dict=True,
	)

	for row in sources:
		total = flt(row.total_leads)
		conv = flt(row.converted)
		row.conversion_rate = (conv / total * 100) if total > 0 else 0

	return sources


def get_chart(data):
	if not data:
		return None

	labels = [d.get("source") for d in data]
	converted_values = [d.get("converted", 0) for d in data]
	total_values = [d.get("total_leads", 0) for d in data]

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": _("Total Leads"), "values": total_values},
				{"name": _("Converted"), "values": converted_values},
			],
		},
		"type": "bar",
		"colors": ["#5e64ff", "#28a745"],
	}


def get_summary(data):
	total_leads = sum(d.get("total_leads", 0) for d in data)
	total_converted = sum(d.get("converted", 0) for d in data)
	rate = (total_converted / total_leads * 100) if total_leads > 0 else 0

	return [
		{
			"value": total_leads,
			"indicator": "Blue",
			"label": _("Total Leads"),
			"datatype": "Int",
		},
		{
			"value": total_converted,
			"indicator": "Green",
			"label": _("Converted Leads"),
			"datatype": "Int",
		},
		{
			"value": round(rate, 2),
			"indicator": "Purple",
			"label": _("Conversion Rate (%)"),
			"datatype": "Percent",
		},
	]
