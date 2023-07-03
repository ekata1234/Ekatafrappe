import copy
from collections import OrderedDict

import frappe
from frappe import _, qb
from frappe.query_builder import CustomFunction
from frappe.query_builder.functions import Max
from frappe.utils import date_diff, flt, getdate
import re


def execute(filters=None):
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(filters,conditions)
    return columns, data, None

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" and gl.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
    if filters.get("project"):
      conditions += f" and gl.project = '{filters.get('project')}'"
    
    return conditions

def get_data(filters,conditions):
    data = frappe.db.sql(f"""SELECT name as gl_entry,
            posting_date,
            voucher_type,
            voucher_no, 
            debit,credit,
            account_currency,
            remarks, against,
            is_opening,creation 
            FROM `tabGL Entry` gl WHERE 1=1  AND gl.docstatus = 1 AND
            voucher_type not in ('Sales Invoice','Payment Entry','Stock Reconciliation','Stock Entry') GROUP BY voucher_no
            {conditions}                     
             """,as_dict=1,debug=1)
    for row in data:
        # print('hi')
        if row.debit:
            row.update({'amount':flt(row.get('debit'))})
        if row.credit:
            row.update({'amount':flt(row.get('credit'))})

    return data

def get_columns(filters):
    columns = [
        
        
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "date",
            "width": 120,
        },
        {
            "label": _("Project Remarks/Description"),
            "fieldname": "project_description",
            "fieldtype": "data",
            "width": 110,
        },
        {
            "label": _("Amount (Debit/Credit)"),
            "fieldname": "amount",
            "fieldtype": "Float",
            "width": 180,
        },
        {
                "label": _("Voucher No"),
                "fieldname": "voucher_no",
                "fieldtype": "Dynamic Link",
                "options": "voucher_type",
                "width": 170,
            },
        {
            "label": _("Voucher Type"),
            "fieldname": "voucher_type",
            "fieldtype": "data",
            "width": 130,
        },

        
    ]
    return columns




# import copy
# from collections import OrderedDict

# import frappe
# from frappe import _, qb
# from frappe.query_builder import CustomFunction
# from frappe.query_builder.functions import Max
# from frappe.utils import date_diff, flt, getdate
# import re


# def execute(filters=None):
#     columns = get_columns(filters)
#     conditions = get_conditions(filters)
#     data = get_data(filters,conditions)
#     return columns, data, None

# def get_conditions(filters):
#     conditions = ""
#     if filters.get("from_date") and filters.get("to_date"):
#         conditions += f" and gl.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
#     if filters.get("project"):
#     	conditions += f" and gl.project = '{filters.get('project')}'"
    
#     return conditions

# def get_data(filters,conditions):
#     data = frappe.db.sql(f"""SELECT name as gl_entry,
#             posting_date,
#             voucher_type,
#             voucher_no, 
#             debit,credit,
#             account_currency,
#             remarks, against,
#             is_opening,creation 
#             FROM `tabGL Entry` gl WHERE 1=1  AND 
#             voucher_type not in ('Sales Invoice','Payment Entry','Stock Reconciliation','Stock Entry') GROUP BY voucher_no
#             {conditions}                     
#              """,as_dict=1,debug=1)

#     voucher_no_list = [voucher.voucher_no for voucher in data]

#     # # print(f"\n\n voucher_no_list-----{voucher_no_list}\n\n")
#     # data1 = frappe.db.sql(""" SELECT ec.name as expense_claim FROM `tabExpense Claim` ec 
#     #     where  ec.name in {0}
#     #  and ec.status not in ('Cancelled', 'Return','Draft','Debit Note Issued')
#     #  """.format(tuple(voucher_no_list)),as_dict=1,debug=1)
    
#     # print(f"\n\n data1-----{data1}\n\n")

#     # data2 = frappe.db.sql(""" SELECT pi.name as purchase_invoice FROM `tabPurchase Invoice` pi where  pi.name in {0}
#     #  and pi.status not in ('Cancelled', 'Return','Draft','Debit Note Issued')
#     #  """.format(tuple(voucher_no_list)),as_dict=1,debug=1)
    
#     # print(f"\n\n data2-----{data2}\n\n")


#     for row in data:
#         if row.debit:
#             row.update({'amount':flt(row.get('debit'))})
#         if row.credit:
#             row.update({'amount':flt(row.get('credit'))})
#         # if row.debit:
#         #     balance =0
#         #     row.update({'balance':(flt(row.get('debit')-row.get('credit')))})
#         #     balance += row.get('debit', 0) - row.get('credit', 0)
#         #     row.update({'balance':balance})
#     return data
# def get_columns(filters):
#     columns = [
    	
    	
#         {
#             "label": _("Posting Date"),
#             "fieldname": "posting_date",
#             "fieldtype": "date",
#             "width": 120,
#         },
#         {
#             "label": _("Project Remarks/Description"),
#             "fieldname": "project_description",
#             "fieldtype": "data",
#             "width": 110,
#         },
        
#   #       {
# 		# 	# "label": _("Debit ({0})").format(currency),
# 		# 	"label": _("Debit"),
# 		# 	"fieldname": "debit",
# 		# 	"fieldtype": "Float",
# 		# 	"width": 100,
# 		# },
# 		# {
# 		# 	# "label": _("Credit ({0})").format(currency),
# 		# 	"label": _("Credit"),
# 		# 	"fieldname": "credit",
# 		# 	"fieldtype": "Float",
# 		# 	"width": 100,
# 		# },
# 		{
# 			# "label": _("Balance ({0})").format(currency),
# 			"label": _("Amount (Debit/Credit)"),
# 			"fieldname": "amount",
# 			"fieldtype": "Float",
# 			"width": 130,
# 		},
#         # {
#         #     # "label": _("Balance ({0})").format(currency),
#         #     "label": _("Balance"),
#         #     "fieldname": "balance",
#         #     "fieldtype": "Float",
#         #     "width": 130,
#         # },
#         {
#                 "label": _("Voucher No"),
#                 "fieldname": "voucher_no",
#                 "fieldtype": "Dynamic Link",
#                 "options": "voucher_type",
#                 "width": 180,
#             },
#         {
#             "label": _("Voucher Type"),
#             "fieldname": "voucher_type",
#             "fieldtype": "data",
#             "width": 130,
#         },

        
#     ]
#     return columns