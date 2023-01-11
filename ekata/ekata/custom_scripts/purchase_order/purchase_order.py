import frappe

def validate(self,method = None):
    if self.naming_series == "PO .##./.FY.":
        if not frappe.db.exists('Purchase Order', 'PO 34/2022-23'):
            self.name = "PO 34/2022-23"
            frappe.db.sql("update `tabSeries` set current=34 where name = 'PO '")
