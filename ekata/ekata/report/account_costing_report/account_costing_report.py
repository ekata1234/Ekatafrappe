
import frappe
from frappe import _
from typing import Tuple

def execute(filters=None) -> Tuple:
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(filters, conditions)
    # print(f"\n data in execute--{data}\n")
    return columns, data, None


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date") and filters.get("to_date"):
        conditions += f" and gl.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
    if filters.get("project"):
      conditions += f" and gl.project = '{filters.get('project')}'"
    
    return conditions

def get_data(filters,conditions):

    data = frappe.db.sql(f"""SELECT gl.name as gl_entry,
            gl.posting_date,
            gl.voucher_type,gl.credit,
            gl.voucher_no,gl.project,
            gl.debit
            
            FROM `tabGL Entry` gl 
            
            WHERE gl.voucher_type not in ('Sales Invoice','Payment Entry','Stock Reconciliation','Stock Entry') 
            AND  1=1 {conditions}
            ORDER BY gl.posting_date
             """,as_dict=1,debug=1)
    voucher_no_list = [item.voucher_no for item in data]

    data2 = frappe.db.sql(""" 
    		SELECT
    		 parent,project_description from `tabJournal Entry Account`
    		WHERE parent in {0}
    	""".format(tuple(voucher_no_list)),as_dict=1,debug=1)
    filtered_list = [dictionary for dictionary in data2 if all(value is not None for value in dictionary.values())]

    # print(f"\ndata2--{filtered_list}\n{type(filtered_list)}")
    for row in data:
    	for row2 in filtered_list:
    		if row.get('voucher_no')==row2.get('parent'):
    			print(f"\n row2--{row2.get('project_description')}\n")
    			row.update({'remarks':row2.get('project_description')})

    data3 = frappe.db.sql(""" 
    		SELECT
    		 name,project_description from `tabPurchase Invoice`
    		WHERE name in {0}
    	""".format(tuple(voucher_no_list)),as_dict=1,debug=1)
    filtered_pi_list = [dictionary for dictionary in data3 if all(value is not None for value in dictionary.values())]
    for row in data:
    	for row3 in filtered_pi_list:
    		if row.get('voucher_no')==row3.get('name'):
    			print(f"\n row2--{row3.get('project_description')}\n")
    			row.update({'remarks':row3.get('project_description')})

    data4 = frappe.db.sql(""" 
    		SELECT
    		 name,project_description from `tabExpense Claim`
    		WHERE name in {0}
    	""".format(tuple(voucher_no_list)),as_dict=1,debug=1)
    filtered_ec_list = [dictionary for dictionary in data4 if all(value is not None for value in dictionary.values())]
    for row in data:
    	for row4 in filtered_ec_list:
    		if row.get('voucher_no')==row4.get('name'):
    			print(f"\n row2--{row4.get('project_description')}\n")
    			row.update({'remarks':row4.get('project_description')})

    data5 = frappe.db.sql(""" 
    		SELECT
    		 parent,project_description from `tabPurchase Receipt Item`
    		WHERE parent in {0}
    	""".format(tuple(voucher_no_list)),as_dict=1,debug=1)
    filtered_pr_list = [dictionary for dictionary in data5 if all(value is not None for value in dictionary.values())]

    # print(f"\ndata2--{filtered_list}\n{type(filtered_list)}")
    for row in data:
    	for row5 in filtered_pr_list:
    		if row.get('voucher_no')==row5.get('parent'):
    			print(f"\n row2--{row5.get('project_description')}\n")
    			row.update({'remarks':row5.get('project_description')})
    print(f"\n data3in get_data--{filtered_pr_list}\n")

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
            "label": _("Project"),
            "fieldname": "project",
            "fieldtype": "data",
            "width": 120,
        },
        {
            "label": _("Project Remarks/Description"),
            "fieldname": "remarks",
            "fieldtype": "data",
            "width": 110,
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
        {
            "label": _("Debit"),
            "fieldname": "debit",
            "fieldtype": "Float",
            "width": 180,
        },
        {
            "label": _("Credit)"),
            "fieldname": "credit",
            "fieldtype": "Float",
            "width": 180,
        }
    ]
    return columns







# # Copyright (c) 2023, kiran.c@indictrans.in and contributors
# # For license information, please see license.txt

# import frappe
# from frappe import _, qb
# from frappe.utils import date_diff, flt, getdate



# def execute(filters=None):
# 	columns = get_columns(filters)
# 	#conditions = get_conditions(filters)
# 	data = get_data(filters)
# 	return columns, data, None

# def get_data(filters):
	
# 	gl_data = frappe.db.sql("""SELECT 
#                 gl.voucher_no,gl.voucher_type,gl.posting_date,gl.project,gl.debit as gl_debit,
#                 gl.credit as gl_credit
#             FROM 
#                 `tabGL Entry`gl 
            
#             WHERE 
#                 voucher_type not in ('Sales Invoice','Payment Entry','Stock Reconciliation','Stock Entry')
# 	        ORDER BY gl.voucher_no
#                """.format(),as_dict=1,debug=1)
               
# 	voucher_no_list = [item.voucher_no for item in gl_data]
# 	# print(f"\n\ndata--{data}\n\n voucher_no_list--{voucher_no_list}")

# 	jl_data = frappe.db.sql("""	SELECT 
# 			jl.name,jla.debit,jla.credit,jl.total_debit,jl.docstatus,
# 			jl.total_credit,jl.posting_date,jla.project_description 
# 		FROM 
# 			`tabJournal Entry` jl 
# 		JOIN 
# 			`tabJournal Entry Account` jla 
# 		ON 
# 			jl.name=jla.parent 
# 		WHERE 
# 			jl.name in {0} 
# 		""".format(tuple(voucher_no_list)),as_dict=1,debug=1)
# 		# """.format(filters.get('from_date'), filters.get('to_date'),filters.get('project'),tuple(voucher_no_list)),as_dict=1,debug=1)

# 	print(f"\n\n jl_data--{jl_data}\n\n")

# 	# expense_data = frappe.db.sql(""" SELECT
# 	# 		ec.name,ecd.description,ecd.amount,
# 	# 		ec.total_claimed_amount,ec.posting_date
# 	# 	FROM 
# 	# 		`tabExpense Claim` ec 
# 	# 	JOIN 
# 	# 		`tabExpense Claim Detail`ecd 
# 	# 	ON 
# 	# 		ec.name=ecd.parent
# 	# 	WHERE
# 	# 		 ec.status not in ('Cancelled','Return','Rejected')
# 	# """,as_dict=1,debug=1)

# 	# pi_data = frappe.db.sql(""" SELECT
# 	# 		pi.name,pi.project,pii.amount,pii.rate,pi.total,pi.posting_date 
# 	# 	FROM 
# 	# 		`tabPurchase Invoice` pi 
# 	# 	JOIN
# 	# 		`tabPurchase Invoice Item` pii 
# 	# 	ON 
# 	# 		pi.name=pii.parent 
# 	# 	WHERE
# 	# 		pi.status not in ('Cancelled','Return')""",as_dict=1,debug=1)
	
# 	# data = []
# 	# for voucher_no, items in jl_data:
# 	# 	data.extend(items)

	
# 	# for row in data:
# 	for row1 in gl_data:
# 		total =0.0
# 		for row2 in jl_data:
# 			if row1.get('voucher_no')==row2.get('name'):
# 				# print(f"\n same voucher_no--{row1.get('voucher_no')}\n")
# 				# row1.update({'name':row2.get('voucher_no')})
# 				total += flt(row2.get('debit'))
# 				# print(f"\net_total--{total}\n")
# 				row1.update({'total':total})
# 				# row.update(row1)

# 	# print(f"\n\n final_data--{gl_data}\n\n")
# 	return gl_data

	
	

# def get_columns(filters):
# 	columns = [
# 		{
#             "label": _("Posting Date"),
#             "fieldname": "posting_date",
#             "fieldtype": "Date",
#             "width": 180,
#         },
#         {
#             "label": _("Project Description"),
#             "fieldname": "project_description",
#             "fieldtype": "Data",
#             "width": 180,
#         },
# 		{
#             "label": _("Voucher No"),
#             "fieldname": "voucher_no",
#             "fieldtype": "Dynamic Link",
#             "options": "Journal Entry",
#             "width": 170,
#         },
#         {
#             "label": _("Debit"),
#             "fieldname": "gl_debit",
#             "fieldtype": "Float",
#             "width": 180,
#         },
#         {
#             "label": _("Credit"),
#             "fieldname": "gl_credit",
#             "fieldtype": "Float",
#             "width": 180,
#         },
#         {
#             "label": _("Total"),
#             "fieldname": "total",
#             "fieldtype": "Float",
#             "width": 180,
#         },
#     ]
# 	return columns





# # data = frappe.db.sql("""SELECT 
# #                 gl.voucher_no,gl.voucher_type,gl.posting_date,gl.project
# #             FROM 
# #                 `tabGL Entry`gl 
            
# #             WHERE 
# #                 voucher_type not in ('Sales Invoice','Payment Entry','Stock Reconciliation','Stock Entry')
# # 	           	AND posting_date BETWEEN '{0}' and '{1}' 
# # 	    		AND gl.project ='{2}'      
# #                """.format(filters.get('from_date'), filters.get('to_date'),filters.get('project')),as_dict=1,debug=1)
# #                # """.format(filters.get('from_date'), filters.get('to_date'),filters.get('project')),as_dict=1,debug=1)
# # 	