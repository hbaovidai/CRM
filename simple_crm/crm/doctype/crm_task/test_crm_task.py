# Copyright (c) 2026, Frappe Team and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, today


class TestCRMTask(IntegrationTestCase):
	def setUp(self):
		frappe.db.delete("CRM Task")
		frappe.db.delete("CRM Customer")

		self.customer = frappe.get_doc({
			"doctype": "CRM Customer",
			"customer_name": "Task Test Customer",
			"customer_type": "Organization",
			"sales_owner": "Administrator",
		}).insert()

	def test_task_creation_and_completion(self):
		task = frappe.get_doc({
			"doctype": "CRM Task",
			"subject": "Send proposal doc",
			"assigned_to": "Administrator",
			"due_date": add_days(today(), 3),
			"priority": "High",
			"status": "Open",
			"reference_doctype": "CRM Customer",
			"reference_name": self.customer.name,
		}).insert()

		self.assertTrue(task.name.startswith("CRM-TASK-"))
		self.assertIsNone(task.completed_on)

		# Mark completed
		task.status = "Completed"
		task.save()
		self.assertIsNotNone(task.completed_on)

	def test_task_invalid_reference_doctype(self):
		"""BR-14: Reference doctype must be CRM Lead, Customer, or Opportunity."""
		task = frappe.new_doc("CRM Task")
		task.subject = "Follow up with unknown"
		task.assigned_to = "Administrator"
		task.due_date = today()
		task.reference_doctype = "DocType"
		task.reference_name = "CRM Task"

		self.assertRaises(frappe.ValidationError, task.insert)

	def test_task_overdue_logic(self):
		"""BR-11: Task is overdue if due_date < today and not completed/cancelled."""
		overdue_task = frappe.get_doc({
			"doctype": "CRM Task",
			"subject": "Old overdue task",
			"assigned_to": "Administrator",
			"due_date": add_days(today(), -5),
			"status": "Open",
			"reference_doctype": "CRM Customer",
			"reference_name": self.customer.name,
		}).insert()

		self.assertTrue(overdue_task.is_overdue())

		# Once completed, it is no longer overdue
		overdue_task.status = "Completed"
		overdue_task.save()
		self.assertFalse(overdue_task.is_overdue())
