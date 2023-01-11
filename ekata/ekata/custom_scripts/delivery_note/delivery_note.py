import frappe

def validate(self,method = None):
    if self.naming_series == "EEPL/DC/.##./.FY.":
        if not frappe.db.exists('Delivery Note', 'EEPL/DC/02/22-23'):
            self.name = "EEPL/DC/02/22-23"
            frappe.db.sql("update `tabSeries` set current=02 where name = 'EEPL/DC/'")
