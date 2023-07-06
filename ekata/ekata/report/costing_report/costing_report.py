# Copyright (c) 2023, Indictranstech and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from typing import Tuple

def execute(filters=None) -> Tuple:
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(filters, conditions)
    data_dict = frappe._dict({})
    crop_total_dict = frappe._dict({})

    for item in data:
        if item.debit:
            if item.voucher_no in data_dict:
                data_dict[item.voucher_no].append(
                    {
                        "posting_date": item.posting_date,
                        "voucher_no": item.voucher_no,
                        "voucher_type": item.voucher_type,
                        "project_description": item.project_description,
                        "amount": item.debit
                    }
                )
            else:
                data_dict[item.voucher_no] = [{
                    "posting_date": item.posting_date,
                    "voucher_no": item.voucher_no,
                    "voucher_type": item.voucher_type,
                    "project_description": item.project_description,
                    "amount": item.debit
                }]

            if item.voucher_no in crop_total_dict:
                crop_total_dict[item.voucher_no] += item.debit
            else:
                crop_total_dict[item.voucher_no] = item.debit

    grand_total_dict = frappe._dict({})
    for voucher_no, total_amount in crop_total_dict.items():
        grand_total_dict[voucher_no] = total_amount

    for voucher_no, items in data_dict.items():
        items.append({
            "posting_date": "",
            "voucher_no": "",
            "voucher_type": "",
            "project_description": "Grand Total",
            "amount": grand_total_dict[voucher_no]

        })

    data = []
    for voucher_no, items in data_dict.items():
        data.extend(items)

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
            gl.voucher_type,
            gl.voucher_no, 
            gl.debit,gl.credit,
            jla.project_description
            

            FROM `tabGL Entry` gl 
            LEFT JOIN `tabJournal Entry Account`jla 
            ON gl.voucher_no = jla.parent 

            WHERE  voucher_type not in ('Sales Invoice','Payment Entry','Stock Reconciliation','Stock Entry') 
            AND  1=1 {conditions}       
            ORDER BY posting_date
             """,as_dict=1,debug=1)

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
            "label": _("Amount (Debit/Credit)"),
            "fieldname": "amount",
            "fieldtype": "Float",
            "width": 180,
        },
    ]
    return columns



# # Copyright (c) 2023, Indictrans and contributors
# # For license information, please see license.txt

# # Copyright (c) 2023, Indictrans and contributors
# # For license information, please see license.txt

# import frappe
# from typing import Dict, List, Optional, Tuple

# Filters = frappe._dict
# def execute(filters: Optional[Filters] = None) -> Tuple:
#     columns = get_columns()
#     data = []
#     batch_list = get_batch_balance_report(filters)

#     data_dict = frappe._dict({})
#     crop_total_dict = frappe._dict({})

#     for item in batch_list:
#         total = item.debt + item.credit
#         if item.voucher_no in data_dict: 
#             data_dict[item.voucher_no].append(
#                     {
#                     "project":'',
#                     "posting_date":posting,
#                     "project_description": item.project_description,
#                     "voucher_no": item.voucher_no,
#                     "voucher_type": item.variety_type,
#                     "amount": item.debit,
#                     "grand_total" : total
#                 }
#             )
#         else:
#             data_dict[item.voucher_no] = [{
#                 "project":'',
#                 "posting_date":item.posting_date,
#                 "project_description": item.project_description,
#                 "voucher_no": item.voucher_no,
#                 "voucher_type": item.variety_type,
#                 "amount": item.debit,
#                 "grand_total" : total
#             }]  
#         g_total = item.gp_value + item.gf_value + item.gw_value + item.gotp_value + item.gotf_value + item.gotw_value + item.mp_value + item.mf_value + item.mw_value
#         if item.voucher_no in crop_total_dict:
#             crop_total_dict[item.voucher_no].project = ""
#             crop_total_dict[item.voucher_no].posting_date = ""
#             crop_total_dict[item.voucher_no].project_description = ""
#             crop_total_dict[item.voucher_no].voucher_no = item.voucher_no
#             crop_total_dict[item.voucher_no].voucher_type += item.voucher_type
#             crop_total_dict[item.voucher_no].amount = item.debit
#             crop_total_dict[item.voucher_no].grand_total += g_total 
#         else:       
#             crop_total_dict[item.voucher_no] = frappe._dict(
#                     {
#                     "project":'',
#                     "posting_date":item.posting_date,
#                     "project_description": item.project_description,
#                     "voucher_no": item.voucher_no,
#                     "voucher_type": item.variety_type,
#                     "amount": item.debit,
#                     "grand_total" : g_total 
#                 }
#             )
        
#     for i in crop_total_dict:
#         data_dict[i].append(crop_total_dict[i])

#     data = []
#     for i in data_dict:
#         data.extend(data_dict[i])

#     return columns, data

# def get_batch_balance_report(filters: Filters) -> List:
#     conditions = get_conditions(filters)    
#     batch_list = frappe.db.sql('''
#                 select 
#                      gl.voucher_no,gl.voucher_type,gl.posting_date,
#                      gl.debit,gl.credit,jla.project_description            
#                 from 
#                      `tabGL Entry` gl,
#                      `tabJournal Entry Account` jla  
#                 where 
#                      gl.voucher_no = jla.parent 
#                 order by gl.voucher_no, gl.creation   ''',  conditions, filters, as_dict=1)        
#     return batch_list

# def get_columns()-> List[Dict]:
#     return [        
#         {
#             'fieldname': 'posting_date',
#             'label': 'Posting Date',
#             'fieldtype': 'Data',
#             "width": 150
#         },
#         {
#             'fieldname': 'project_description',
#             'label': 'Project Remark',
#             'fieldtype': 'Data',
#             "width": 150
#         },
#         {
#             'fieldname': 'voucher_no',
#             'label': 'Voucher No',
#             'fieldtype': 'Data',
#             "width": 250
#         },
#         {
#             'fieldname': 'voucher_type',
#             'label': 'Voucher Type',
#             'fieldtype': 'Data',
#             "width": 250
#         },
#         {
#             'fieldname': 'total_amount',
#             'label': 'Amount Dr/Cr',
#             'fieldtype': 'Float',
#             "width": 150
#         },
        
#         {
#             'fieldname': 'grand_total',
#             'label': 'Grand Total',
#             'fieldtype': 'Float',
#             "width": 150
#         }
#     ]     
            
# def get_conditions(filters=None):
#     conditions = ''
#     # if filters.get('project'):
#     #     conditions += " and jla.project = '{0}'".format(filters.get('project'))
#     if filters.get("from_date") and filters.get("to_date"):
#         conditions += f" and gl.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"

        
#     return conditions


# # import copy
# # from collections import OrderedDict

# # import frappe
# # from frappe import _, qb
# # from frappe.query_builder import CustomFunction
# # from frappe.query_builder.functions import Max
# # from frappe.utils import date_diff, flt, getdate
# # import re
# # from typing import Dict, List, Optional, Tuple

# # def execute(filters=None)-> Tuple:
# #     columns = get_columns(filters)
# #     data = []
# #     conditions = get_conditions(filters)
# #     batch_list = get_data(filters,conditions)
# #     # print(f"\nbatch_list--{batch_list}\n")
# #     data_dict = frappe._dict({})
# #     crop_total_dict = frappe._dict({})
# #     total = 0
# #     g_total = 0

# #     for item in batch_list:
# #         # total += item.debit 
# #         if item.voucher_no in data_dict: 
# #             data_dict[item.voucher_no].append(
# #                     {
# #                     "posting_date":item.posting_date,
# #                     "project_description": item.project_description,
# #                     "voucher_no": item.voucher_no,
# #                     "voucher_type": item.voucher_type,                    
# #                     "amount": "",
# #                     "grand_total" : ""
# #                 }
# #             )
# #         else:
# #             data_dict[item.voucher_no] = [{
# #                 "posting_date":item.posting_date,
# #                 "project_description": item.project_description,
# #                 "voucher_no": item.voucher_no,
# #                 "voucher_type": item.voucher_type,
# #                 "amount" : "",
# #                 "grand_total" : ""
# #             }]  
# #         g_total += item.debit
# #         if item.voucher_no in crop_total_dict:
# #             crop_total_dict[item.voucher_no].posting_date = ""
# #             crop_total_dict[item.voucher_no].project_description = ""
# #             crop_total_dict[item.voucher_no].voucher_no = ""
# #             crop_total_dict[item.voucher_no].voucher_type = ""
# #             crop_total_dict[item.voucher_no].amount = ""
# #             crop_total_dict[item.voucher_no].grand_total = "" 
# #         else:       
# #             crop_total_dict[item.voucher_no] = frappe._dict(
# #                     {
# #                     "posting_date" : "",
# #                     "project_description" : "",
# #                     "voucher_no" : "",
# #                     "voucher_type" : "",
# #                     "amount" : "",
# #                     "grand_total" : "" 
# #                 }
# #             )
        
# #     print(f"\n crop_total_dict--{crop_total_dict}\n data_dict--{data_dict}\n")
# #     for i in crop_total_dict:
# #         data_dict[i].append(crop_total_dict[i])

# #     # data = []
# #     for i in data_dict:
# #         data.extend(data_dict[i])

# #     return columns, data

# # def get_conditions(filters):
# #     conditions = ""
# #     if filters.get("from_date") and filters.get("to_date"):
# #         conditions += f" and gl.posting_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
# #     if filters.get("project"):
# #       conditions += f" and gl.project = '{filters.get('project')}'"
    
# #     return conditions

# # def get_data(filters,conditions) -> List:
# #     data = frappe.db.sql(f"""SELECT  name as gl_entry,
# #             posting_date,
# #             voucher_type,
# #             voucher_no, 
# #             debit,credit
            
# #             FROM `tabGL Entry` gl  
# #             WHERE voucher_type not in ('Sales Invoice','Payment Entry','Stock Reconciliation','Stock Entry') 
# #             AND  1=1 {conditions}       
# #             ORDER BY posting_date
# #              """,as_dict=1,debug=1)
# #     # for row in data:
# #     #     # print('hi')
# #     #     if row.debit:
# #     #         row.update({'amount':flt(row.get('debit'))})
# #     #     if row.credit:
# #     #         row.update({'amount':flt(row.get('credit'))})

# #     return data

# # def get_columns(filters)-> List[Dict]:
# #     columns = [
        
        
# #         # {
# #         #     "label": _("Posting Date"),
# #         #     "fieldname": "posting_date",
# #         #     "fieldtype": "date",
# #         #     "width": 120,
# #         # },
# #         # {
# #         #     "label": _("Project Remarks/Description"),
# #         #     "fieldname": "project_description",
# #         #     "fieldtype": "data",
# #         #     "width": 110,
# #         # },
# #         {
# #                 "label": _("Voucher No"),
# #                 "fieldname": "voucher_no",
# #                 "fieldtype": "Dynamic Link",
# #                 "options": "voucher_type",
# #                 "width": 170,
# #         },
# #         {
# #             "label": _("Voucher Type"),
# #             "fieldname": "voucher_type",
# #             "fieldtype": "data",
# #             "width": 130,
# #         },
# #         {
# #             "label": _("Amount (Debit/Credit)"),
# #             "fieldname": "amount",
# #             "fieldtype": "Float",
# #             "width": 180,
# #         },
        
# #         {
# #             'fieldname': 'grand_total',
# #             'label': 'Grand Total',
# #             'fieldtype': 'Float',
# #             "width": 150
# #         }

        
# #     ]
# #     return columns
