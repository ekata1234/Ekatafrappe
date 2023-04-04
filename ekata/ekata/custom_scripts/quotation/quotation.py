import frappe

def validate(self,method = None):
    if self.naming_series == "Q .##./.FY.":
        pass
        # if not frappe.db.exists('Quotation', 'Q 24/2022-23'):
        #     self.name = "Q 24/2022-23"
        #     frappe.db.sql("update `tabSeries` set current=24 where name = 'Q '")
