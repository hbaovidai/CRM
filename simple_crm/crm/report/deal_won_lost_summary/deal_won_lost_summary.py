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
			"label": _("Sales Owner"),
			"fieldname": "sales_owner",
			"fieldtype": "Link",
			"options": "User",
			"width": 180,
		},
		{
			"label": _("Won Deals"),
			"fieldname": "won_deals",
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"label": _("Won Value"),
			"fieldname": "won_amount",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Lost Deals"),
			"fieldname": "lost_deals",
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"label": _("Lost Value"),
			"fieldname": "lost_amount",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Win Rate (%)"),
			"fieldname": "win_rate",
			"fieldtype": "Percent",
			"width": 130,
		},
	]


def get_data(filters):
	conditions = ["stage IN ('Won', 'Lost')"]

	if filters.get("sales_owner"):
		conditions.append(f"sales_owner = {frappe.db.escape(filters.get('sales_owner'))}")
	if filters.get("from_date"):
		conditions.append(f"actual_close_date >= {frappe.db.escape(filters.get('from_date'))}")
	if filters.get("to_date"):
		conditions.append(f"actual_close_date <= {frappe.db.escape(filters.get('to_date'))}")

	where_clause = f"WHERE {' AND '.join(conditions)}"

	owners = frappe.db.sql(
		f"""
		SELECT
			sales_owner,
			SUM(CASE WHEN stage = 'Won' THEN 1 ELSE 0 END) as won_deals,
			SUM(CASE WHEN stage = 'Won' THEN amount ELSE 0 END) as won_amount,
			SUM(CASE WHEN stage = 'Lost' THEN 1 ELSE 0 END) as lost_deals,
			SUM(CASE WHEN stage = 'Lost' THEN amount ELSE 0 END) as lost_amount
		FROM `tabCRM Opportunity`
		{where_clause}
		GROUP BY sales_owner
		ORDER BY won_amount DESC
		""",
		as_dict=True,
	)

	for row in owners:
		won = flt(row.won_deals)
		lost = flt(row.lost_deals)
		total_closed = won + lost
		row.win_rate = (won / total_closed * 100) if total_closed > 0 else 0

	return owners


def get_chart(data):
	if not data:
		return None

	labels = [d.get("sales_owner") for d in data]
	won_values = [flt(d.get("won_amount", 0)) for d in data]
	lost_values = [flt(d.get("lost_amount", 0)) for d in data]

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": _("Won Amount"), "values": won_values},
				{"name": _("Lost Amount"), "values": lost_values},
			],
		},
		"type": "bar",
		"colors": ["#28a745", "#dc3545"],
	}


def get_summary(data):
	total_won_deals = sum(d.get("won_deals", 0) for d in data)
	total_lost_deals = sum(d.get("lost_deals", 0) for d in data)
	total_won_amount = sum(flt(d.get("won_amount", 0)) for d in data)
	total_closed = total_won_deals + total_lost_deals
	overall_win_rate = (total_won_deals / total_closed * 100) if total_closed > 0 else 0

	return [
		{
			"value": total_won_deals,
			"indicator": "Green",
			"label": _("Total Won Deals"),
			"datatype": "Int",
		},
		{
			"value": total_won_amount,
			"indicator": "Green",
			"label": _("Total Won Value"),
			"datatype": "Currency",
		},
		{
			"value": round(overall_win_rate, 2),
			"indicator": "Blue",
			"label": _("Overall Win Rate"),
			"datatype": "Percent",
		},
	]
