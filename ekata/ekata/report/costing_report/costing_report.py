
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
            gl.debit,gl.credit
            
            FROM `tabGL Entry` gl 
            
            WHERE  voucher_type not in ('Sales Invoice','Payment Entry','Stock Reconciliation','Stock Entry') 
            AND  1=1 {conditions}       


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


