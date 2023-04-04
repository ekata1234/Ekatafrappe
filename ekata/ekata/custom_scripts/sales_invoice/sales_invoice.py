import frappe
# from frappe.utils import flt
# from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals

# def custom_calculate_totals(self):
    
#     shipping_charges = 0
#     for courier in self.doc.courier_charges_and_others:
#         shipping_charges = shipping_charges + courier.amount
#     if shipping_charges:
#         if self.doc.get("taxes"):
#             self.doc.grand_total = flt(self.doc.get("taxes")[-1].total) + flt(self.doc.rounding_adjustment) + flt(shipping_charges)
#         else:
#             self.doc.grand_total = flt(self.doc.net_total) + flt(shipping_charges)
#     else:
#         if self.doc.get("taxes"):
#             self.doc.grand_total = flt(self.doc.get("taxes")[-1].total) + flt(self.doc.rounding_adjustment)
#         else:
#             self.doc.grand_total = flt(self.doc.net_total)

#     if self.doc.get("taxes"):
#         self.doc.total_taxes_and_charges = flt(
#             self.doc.grand_total - self.doc.net_total - flt(self.doc.rounding_adjustment),
#             self.doc.precision("total_taxes_and_charges"),
#         )
#     else:
#         self.doc.total_taxes_and_charges = 0.0

#     self._set_in_company_currency(self.doc, ["total_taxes_and_charges", "rounding_adjustment"])

#     if self.doc.doctype in [
#         "Quotation",
#         "Sales Order",
#         "Delivery Note",
#         "Sales Invoice",
#         "POS Invoice",
#     ]:
#         self.doc.base_grand_total = (
#             flt(self.doc.grand_total * self.doc.conversion_rate, self.doc.precision("base_grand_total"))
#             if self.doc.total_taxes_and_charges
#             else self.doc.base_net_total
#         )
#     else:
#         self.doc.taxes_and_charges_added = self.doc.taxes_and_charges_deducted = 0.0
#         for tax in self.doc.get("taxes"):
#             if tax.category in ["Valuation and Total", "Total"]:
#                 if tax.add_deduct_tax == "Add":
#                     self.doc.taxes_and_charges_added += flt(tax.tax_amount_after_discount_amount)
#                 else:
#                     self.doc.taxes_and_charges_deducted += flt(tax.tax_amount_after_discount_amount)

#         self.doc.round_floats_in(self.doc, ["taxes_and_charges_added", "taxes_and_charges_deducted"])

#         self.doc.base_grand_total = (
#             flt(self.doc.grand_total * self.doc.conversion_rate)
#             if (self.doc.taxes_and_charges_added or self.doc.taxes_and_charges_deducted)
#             else self.doc.base_net_total
#         )

#         self._set_in_company_currency(
#             self.doc, ["taxes_and_charges_added", "taxes_and_charges_deducted"]
#         )

#     self.doc.round_floats_in(self.doc, ["grand_total", "base_grand_total"])

#     self.set_rounded_total()

def validate(self,method = None):
    pass
    # if self.naming_series == "EEPL/E/.##./.FY.":
    #     if not frappe.db.exists('Sales Invoice', 'EEPL/E/14/22-23'):
    #         self.name = "EEPL/E/14/22-23"
    #         frappe.db.sql("update `tabSeries` set current=14 where name = 'EEPL/E/'")

    # if self.naming_series == "EEPL/L/.##./.FY.":
    #     if not frappe.db.exists('Sales Invoice', 'EEPL/L/08/22-23'):
    #         self.name = "EEPL/L/08/22-23"
    #         frappe.db.sql("update `tabSeries` set current=08 where name = 'EEPL/L/'")

    # if self.naming_series == "S/.###./.FY.":
    #     if not frappe.db.exists('Sales Invoice', 'S/088/2022'):
    #         self.name = "S/088/2022"
    #         frappe.db.sql("update `tabSeries` set current=088 where name = 'S/'")

    # if self.naming_series == "EEPL/R/.###./.FY.":
    #     if not frappe.db.exists('Sales Invoice', 'EEPL/R/001/22-23'):
    #         self.name = "EEPL/R/001/22-23"
    #         frappe.db.sql("update `tabSeries` set current=001 where name = 'EEPL/R/'")

    # if self.naming_series == "EEPL/ES/.##./.FY.":
    #     if not frappe.db.exists('Sales Invoice', 'EEPL/ES/01/22-23'):
    #         self.name = "EEPL/ES/01/22-23"
    #         frappe.db.sql("update `tabSeries` set current=01 where name = 'EEPL/ES/'")

    # if self.naming_series == "EEPL/CN/.##./.FY.":
    #     if not frappe.db.exists('Sales Invoice', 'EEPL/CN/01/22-23'):
    #         self.name = "EEPL/CN/01/22-23"
    #         frappe.db.sql("update `tabSeries` set current=01 where name = 'EEPL/CN/'")
    # calculate_taxes_and_totals.calculate_totals = custom_calculate_totals