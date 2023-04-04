import frappe

def validate(self,method = None):
    pass
    # if self.naming_series == "EEPL/DC/.##./.FY.":
    #     if not frappe.db.exists('Delivery Note', 'EEPL/DC/01/22-23'):
    #         self.name = "EEPL/DC/01/22-23"
    #         frappe.db.sql("update `tabSeries` set current=01 where name = 'EEPL/DC/'")
