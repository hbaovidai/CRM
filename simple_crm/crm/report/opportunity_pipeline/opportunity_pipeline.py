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
			"label": _("Opportunity"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "CRM Opportunity",
			"width": 160,
		},
		{
			"label": _("Title"),
			"fieldname": "opportunity_title",
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "CRM Customer",
			"width": 160,
		},
		{
			"label": _("Sales Owner"),
			"fieldname": "sales_owner",
			"fieldtype": "Link",
			"options": "User",
			"width": 140,
		},
		{
			"label": _("Stage"),
			"fieldname": "stage",
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"label": _("Expected Close Date"),
			"fieldname": "expected_close_date",
			"fieldtype": "Date",
			"width": 140,
		},
		{
			"label": _("Deal Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Probability (%)"),
			"fieldname": "probability",
			"fieldtype": "Percent",
			"width": 120,
		},
		{
			"label": _("Weighted Amount"),
			"fieldname": "weighted_amount",
			"fieldtype": "Currency",
			"width": 140,
		},
	]


def get_data(filters):
	conditions = []
	if filters.get("sales_owner"):
		conditions.append(f"sales_owner = {frappe.db.escape(filters.get('sales_owner'))}")
	if filters.get("stage"):
		conditions.append(f"stage = {frappe.db.escape(filters.get('stage'))}")
	else:
		# By default, only show active pipeline (exclude Won and Lost unless filtered)
		conditions.append("stage NOT IN ('Won', 'Lost')")

	if filters.get("from_date"):
		conditions.append(f"expected_close_date >= {frappe.db.escape(filters.get('from_date'))}")
	if filters.get("to_date"):
		conditions.append(f"expected_close_date <= {frappe.db.escape(filters.get('to_date'))}")

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	opportunities = frappe.db.sql(
		f"""
		SELECT
			name,
			opportunity_title,
			customer,
			sales_owner,
			stage,
			expected_close_date,
			amount,
			probability
		FROM `tabCRM Opportunity`
		{where_clause}
		ORDER BY expected_close_date ASC
		""",
		as_dict=True,
	)

	for row in opportunities:
		amt = flt(row.amount)
		prob = flt(row.probability)
		row.weighted_amount = (amt * prob) / 100

	return opportunities


def get_chart(data):
	if not data:
		return None

	stages = ["New", "Qualified", "Proposal", "Negotiation"]
	stage_totals = {s: 0.0 for s in stages}

	for d in data:
		s = d.get("stage")
		if s in stage_totals:
			stage_totals[s] += flt(d.get("amount", 0))

	return {
		"data": {
			"labels": list(stage_totals.keys()),
			"datasets": [
				{"name": _("Pipeline Value"), "values": list(stage_totals.values())},
			],
		},
		"type": "bar",
		"colors": ["#4a90e2"],
	}


def get_summary(data):
	total_deals = len(data)
	total_amount = sum(flt(d.get("amount", 0)) for d in data)
	total_weighted = sum(flt(d.get("weighted_amount", 0)) for d in data)

	return [
		{
			"value": total_deals,
			"indicator": "Blue",
			"label": _("Active Deals"),
			"datatype": "Int",
		},
		{
			"value": total_amount,
			"indicator": "Green",
			"label": _("Total Pipeline Value"),
			"datatype": "Currency",
		},
		{
			"value": total_weighted,
			"indicator": "Purple",
			"label": _("Weighted Pipeline"),
			"datatype": "Currency",
		},
	]
