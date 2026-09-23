# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_days, today


def run():
	"""Seed demo users, leads, customers, opportunities, activities, and tasks."""
	print("--- Seeding Simple CRM Demo Data ---")
	create_test_users()
	create_demo_leads()
	create_demo_customers_and_opportunities()
	print("--- Simple CRM Demo Data Seeded Successfully ---")


def create_test_users():
	users = [
		{
			"email": "admin_crm@example.com",
			"first_name": "Admin",
			"last_name": "CRM",
			"roles": ["System Manager", "CRM Admin"],
		},
		{
			"email": "manager_crm@example.com",
			"first_name": "Manager",
			"last_name": "CRM",
			"roles": ["CRM Sales Manager"],
		},
		{
			"email": "sales_crm@example.com",
			"first_name": "Sales",
			"last_name": "CRM",
			"roles": ["CRM Sales User"],
		},
	]

	for u in users:
		if not frappe.db.exists("User", u["email"]):
			user = frappe.new_doc("User")
			user.email = u["email"]
			user.first_name = u["first_name"]
			user.last_name = u["last_name"]
			user.send_welcome_email = 0
			user.flags.ignore_password_policy = True
			user.new_password = "Crm@Sales#2026!"
			user.insert(ignore_permissions=True)

			from frappe.utils.password import update_password
			update_password(u["email"], "Crm@Sales#2026!")
			print(f"Created user: {u['email']}")
		else:
			user = frappe.get_doc("User", u["email"])

		# Assign roles
		for role in u["roles"]:
			if not frappe.db.exists("Has Role", {"parent": user.name, "role": role}):
				user.append("roles", {"role": role})
		user.save(ignore_permissions=True)


def create_demo_leads():
	leads = [
		{
			"lead_name": "Trần Minh Quang",
			"company_name": "Quang Minh Trading",
			"email": "quang@quangminh.vn",
			"phone": "0901112233",
			"source": "Website",
			"status": "New",
			"sales_owner": "sales_crm@example.com",
			"estimated_value": 50000,
		},
		{
			"lead_name": "Lê Thu Hà",
			"company_name": "Ha Thu Fashion",
			"email": "ha@hathufashion.com",
			"phone": "0912223344",
			"source": "Social Media",
			"status": "Contacted",
			"sales_owner": "sales_crm@example.com",
			"estimated_value": 75000,
		},
		{
			"lead_name": "Phạm Quốc Bảo",
			"company_name": "Bao An Security",
			"email": "bao@baoan.vn",
			"phone": "0983334455",
			"source": "Referral",
			"status": "Qualified",
			"sales_owner": "sales_crm@example.com",
			"estimated_value": 120000,
		},
		{
			"lead_name": "Vũ Thị Mai",
			"company_name": "Mai Vu Cosmetics",
			"email": "mai@maicosmetics.vn",
			"phone": "0974445566",
			"source": "Cold Call",
			"status": "Unqualified",
			"unqualified_reason": "Customer budget too low",
			"sales_owner": "sales_crm@example.com",
			"estimated_value": 30000,
		},
		{
			"lead_name": "Hoàng Anh Tuấn",
			"company_name": "Tuan Phat Construction",
			"email": "tuan@tuanphat.vn",
			"phone": "0965556677",
			"source": "Event",
			"status": "Qualified",
			"sales_owner": "sales_crm@example.com",
			"estimated_value": 200000,
		},
	]

	for item in leads:
		if not frappe.db.exists("CRM Lead", {"email": item["email"]}):
			item["doctype"] = "CRM Lead"
			frappe.get_doc(item).insert(ignore_permissions=True)
			print(f"Created Lead: {item['lead_name']}")


def create_demo_customers_and_opportunities():
	# Customer 1
	if not frappe.db.exists("CRM Customer", {"customer_name": "VinFast Trading Ltd"}):
		cust1 = frappe.get_doc({
			"doctype": "CRM Customer",
			"customer_name": "VinFast Trading Ltd",
			"customer_type": "Organization",
			"sales_owner": "sales_crm@example.com",
			"email": "sales@vinfast.vn",
			"phone": "1900232389",
		}).insert(ignore_permissions=True)

		cont1 = frappe.get_doc({
			"doctype": "CRM Contact",
			"customer": cust1.name,
			"first_name": "Nguyễn",
			"last_name": "Văn Hùng",
			"email": "hung@vinfast.vn",
			"phone": "0909998877",
			"is_primary": 1,
		}).insert(ignore_permissions=True)

		opp1 = frappe.get_doc({
			"doctype": "CRM Opportunity",
			"opportunity_title": "VinFast CRM Deployment",
			"customer": cust1.name,
			"main_contact": cont1.name,
			"sales_owner": "sales_crm@example.com",
			"stage": "Proposal",
			"amount": 250000,
			"expected_close_date": add_days(today(), 30),
		}).insert(ignore_permissions=True)

		# Task for Opp 1
		frappe.get_doc({
			"doctype": "CRM Task",
			"subject": "Send proposal document to VinFast",
			"assigned_to": "sales_crm@example.com",
			"due_date": add_days(today(), 2),
			"priority": "High",
			"status": "Open",
			"reference_doctype": "CRM Opportunity",
			"reference_name": opp1.name,
		}).insert(ignore_permissions=True)

	# Customer 2
	if not frappe.db.exists("CRM Customer", {"customer_name": "FPT Software Solution"}):
		cust2 = frappe.get_doc({
			"doctype": "CRM Customer",
			"customer_name": "FPT Software Solution",
			"customer_type": "Organization",
			"sales_owner": "sales_crm@example.com",
			"email": "contact@fpt.vn",
			"phone": "02473007300",
		}).insert(ignore_permissions=True)

		cont2 = frappe.get_doc({
			"doctype": "CRM Contact",
			"customer": cust2.name,
			"first_name": "Trần",
			"last_name": "Mai Phương",
			"email": "phuong@fpt.vn",
			"phone": "0908887766",
			"is_primary": 1,
		}).insert(ignore_permissions=True)

		opp2 = frappe.get_doc({
			"doctype": "CRM Opportunity",
			"opportunity_title": "FPT Cloud ERP Integration",
			"customer": cust2.name,
			"main_contact": cont2.name,
			"sales_owner": "sales_crm@example.com",
			"stage": "Negotiation",
			"amount": 180000,
			"expected_close_date": add_days(today(), 15),
		}).insert(ignore_permissions=True)

		# Overdue Task for Opp 2 (to test Overdue Follow-ups report)
		frappe.get_doc({
			"doctype": "CRM Task",
			"subject": "Review NDA and SLA terms with legal",
			"assigned_to": "sales_crm@example.com",
			"due_date": add_days(today(), -3),
			"priority": "High",
			"status": "Open",
			"reference_doctype": "CRM Opportunity",
			"reference_name": opp2.name,
		}).insert(ignore_permissions=True)

	# Customer 3 (Won deal)
	if not frappe.db.exists("CRM Customer", {"customer_name": "Viettel Telecom Branch"}):
		cust3 = frappe.get_doc({
			"doctype": "CRM Customer",
			"customer_name": "Viettel Telecom Branch",
			"customer_type": "Organization",
			"sales_owner": "sales_crm@example.com",
			"email": "info@viettel.vn",
			"phone": "18008098",
		}).insert(ignore_permissions=True)

		cont3 = frappe.get_doc({
			"doctype": "CRM Contact",
			"customer": cust3.name,
			"first_name": "Đỗ",
			"last_name": "Gia Huy",
			"email": "huy@viettel.vn",
			"phone": "0907776655",
			"is_primary": 1,
		}).insert(ignore_permissions=True)

		opp3 = frappe.get_doc({
			"doctype": "CRM Opportunity",
			"opportunity_title": "Viettel Security Audit Project",
			"customer": cust3.name,
			"main_contact": cont3.name,
			"sales_owner": "sales_crm@example.com",
			"stage": "Won",
			"amount": 150000,
			"expected_close_date": today(),
			"actual_close_date": today(),
		}).insert(ignore_permissions=True)

		frappe.get_doc({
			"doctype": "CRM Activity",
			"activity_type": "Meeting",
			"subject": "Kickoff meeting with Viettel team",
			"reference_doctype": "CRM Opportunity",
			"reference_name": opp3.name,
			"contact": cont3.name,
			"sales_owner": "sales_crm@example.com",
			"status": "Completed",
			"outcome": "Project kicked off smoothly",
		}).insert(ignore_permissions=True)
