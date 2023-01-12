import frappe

def validate(self,method = None):
    if self.naming_series == "EEPL/PI/.##./.FY.":
        if not frappe.db.exists('Sales Order', 'EEPL/PI/01/22-23'):
            self.name = "EEPL/PI/01/22-23"
            frappe.db.sql("update `tabSeries` set current=01 where name = 'EEPL/PI/'")
