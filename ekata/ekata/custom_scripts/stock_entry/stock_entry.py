import frappe

def on_submit(doc,method=None):
    for item in doc.items:
        frappe.db.set_value('Stock Ledger Entry',{'voucher_no':doc.name,'item_code':item.item_code},'supplier',item.supplier)