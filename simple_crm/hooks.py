app_name = "simple_crm"
app_title = "Simple CRM"
app_publisher = "Frappe Team"
app_description = "Simple CRM for Frappe Framework v16"
app_email = "dev@crm.localhost"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "simple_crm",
# 		"logo": "/assets/simple_crm/logo.png",
# 		"title": "Simple CRM",
# 		"route": "/simple_crm",
# 		"has_permission": "simple_crm.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/simple_crm/css/simple_crm.css"
# app_include_js = "/assets/simple_crm/js/simple_crm.js"

# include js, css files in header of web template
# web_include_css = "/assets/simple_crm/css/simple_crm.css"
# web_include_js = "/assets/simple_crm/js/simple_crm.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "simple_crm/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "simple_crm/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "simple_crm.utils.jinja_methods",
# 	"filters": "simple_crm.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "simple_crm.install.before_install"
# after_install = "simple_crm.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "simple_crm.uninstall.before_uninstall"
# after_uninstall = "simple_crm.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "simple_crm.utils.before_app_install"
# after_app_install = "simple_crm.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "simple_crm.utils.before_app_uninstall"
# after_app_uninstall = "simple_crm.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "simple_crm.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "simple_crm.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["simple_crm.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"simple_crm.tasks.all"
# 	],
# 	"daily": [
# 		"simple_crm.tasks.daily"
# 	],
# 	"hourly": [
# 		"simple_crm.tasks.hourly"
# 	],
# 	"weekly": [
# 		"simple_crm.tasks.weekly"
# 	],
# 	"monthly": [
# 		"simple_crm.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "simple_crm.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "simple_crm.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "simple_crm.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "simple_crm.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["simple_crm.utils.before_request"]
# after_request = ["simple_crm.utils.after_request"]

# Job Events
# ----------
# before_job = ["simple_crm.utils.before_job"]
# after_job = ["simple_crm.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"simple_crm.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

# Fixtures
# --------
fixtures = [
	"Role",
	"CRM Lead Source",
	"CRM Lost Reason"
]

# Permissions
# -----------
permission_query_conditions = {
	"CRM Lead": "simple_crm.permissions.get_lead_conditions",
	"CRM Customer": "simple_crm.permissions.get_customer_conditions",
	"CRM Opportunity": "simple_crm.permissions.get_opportunity_conditions",
	"CRM Task": "simple_crm.permissions.get_task_conditions",
	"CRM Activity": "simple_crm.permissions.get_activity_conditions",
	"CRM Contact": "simple_crm.permissions.get_contact_conditions",
}

has_permission = {
	"CRM Lead": "simple_crm.permissions.has_lead_permission",
	"CRM Customer": "simple_crm.permissions.has_customer_permission",
	"CRM Opportunity": "simple_crm.permissions.has_opportunity_permission",
	"CRM Task": "simple_crm.permissions.has_task_permission",
	"CRM Activity": "simple_crm.permissions.has_activity_permission",
	"CRM Contact": "simple_crm.permissions.has_contact_permission",
}

