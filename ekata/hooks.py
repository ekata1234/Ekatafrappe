from . import __version__ as app_version

app_name = "ekata"
app_title = "Ekata"
app_publisher = "kiran.c@indictrans.in"
app_description = "Ekata"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "kiran.c@indictrans.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ekata/css/ekata.css"
# app_include_js = "/assets/ekata/js/ekata.js"

# include js, css files in header of web template
# web_include_css = "/assets/ekata/css/ekata.css"
# web_include_js = "/assets/ekata/js/ekata.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ekata/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
	"Expense Claim" : "ekata/custom_scripts/expense_claim.js",
	"Sales Invoice" : "ekata/custom_scripts/sales_invoice/sales_invoice.js",
	"Sales Order" : "ekata/custom_scripts/sales_order/sales_order.js",
	"Delivery Note" : "ekata/custom_scripts/delivery_note/delivery_note.js",
	"Employee" : "ekata/custom_scripts/employee/employee.js",
	"Material Request" : "ekata/custom_scripts/material_request/material_request.js",
	"Job Offer" : "ekata/custom_scripts/job_offer/job_offer.js",
	"Stock Entry":"ekata/custom_scripts/stock_entry/stock_entry.js",
	"Shipment":"ekata/custom_scripts/shipment/shipment.js",
	"Purchase Order":"ekata/custom_scripts/purchase_order/purchase_order.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ekata.install.before_install"
# after_install = "ekata.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ekata.uninstall.before_uninstall"
# after_uninstall = "ekata.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ekata.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }
fixtures = [
	# 'Custom Field',
	# 'Property Setter',
	# 'Print Format',
	# 'Role',
	# 'Letter Head',
	# 'Print Style',
	# 'Print Settings',
	# 'Email Template',
	# 'Client Script',
	# 'Workflow',
	# 'Workflow State',
	# 'Notification',
	# 'Warehouse',
	# 'Leave Type',
	# 'Holiday List',
	# 'Salary Structure',
	# 'Interview Round',
	# 'Interview Type',
	# 'Designation'
]


fixtures = [{"dt":'Custom Field',"filters":[["name", "in", ("Purchase Order-section_break_62","Purchase Order-subject", "Purchase Order-column_break_64","Purchase Order-other_content","Purchase Order-authorization","Purchase Order-attachment","Purchase Order-preview_html")]]}]
# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }
override_doctype_class = {
	"Naming Series": "ekata.ekata.custom_scripts.naming_series.naming_series.CustomNamingSeries"
}
# ekata.custom_scripts.naming_series.naming_series.get_current
# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }
doc_events = {
	"Sales Invoice" : {
		"validate":"ekata.ekata.custom_scripts.sales_invoice.sales_invoice.validate"
	},
	"Purchase Order" : {
		"validate":"ekata.ekata.custom_scripts.purchase_order.purchase_order.validate"
	},
	"Quotation" : {
		"validate":"ekata.ekata.custom_scripts.quotation.quotation.validate"
	},
	"Delivery Note" : {
		"validate":"ekata.ekata.custom_scripts.delivery_note.delivery_note.validate"
	},
	"Sales Order" : {
		"validate":"ekata.ekata.custom_scripts.sales_order.sales_order.validate"
	},
	"Supplier Quotation" : {
		"validate":"ekata.ekata.custom_scripts.supplier_quotation.supplier_quotation.validate"
	},
	"Stock Entry" : {
		"on_submit":"ekata.ekata.custom_scripts.stock_entry.stock_entry.on_submit"
	},
	"Material Request" : {
		"validate":"ekata.ekata.custom_scripts.material_request.material_request.validate"
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
#		"ekata.tasks.all"
		"ekata.custom.holiday_list.send_notifications_mail"

	],
	# "daily": [
	# 	#"ekata.tasks.daily"
	# 	"ekata.custom.holiday_list.send_notifications_mail"
	# 	],
# 	"hourly": [
# #		"ekata.tasks.hourly"
# 		"ekata.custom.holiday_list.send_notifications_mail"
# 	],
#	"weekly": [
#		"ekata.tasks.weekly"
#	]
#	"monthly": [
#		"ekata.tasks.monthly"
#	]
 }

# Testing
# -------

# before_tests = "ekata.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "ekata.event.get_events"
# }
#
override_whitelisted_methods = {
	"erpnext.stock.doctype.material_request.material_request.make_request_for_quotation":"ekata.ekata.custom_scripts.material_request.material_request.make_request_for_quotation"
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "ekata.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"ekata.auth.validate"
# ]

