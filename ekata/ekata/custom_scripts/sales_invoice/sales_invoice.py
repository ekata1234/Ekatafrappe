import frappe
from frappe.utils import flt
from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals

def custom_calculate_totals(self):
    
    shipping_charges = 0
    for courier in self.doc.courier_charges_and_others:
        shipping_charges = shipping_charges + courier.amount
    if shipping_charges:
        if self.doc.get("taxes"):
            self.doc.grand_total = flt(self.doc.get("taxes")[-1].total) + flt(self.doc.rounding_adjustment) + flt(shipping_charges)
        else:
            self.doc.grand_total = flt(self.doc.net_total) + flt(shipping_charges)
    else:
        if self.doc.get("taxes"):
            self.doc.grand_total = flt(self.doc.get("taxes")[-1].total) + flt(self.doc.rounding_adjustment)
        else:
            self.doc.grand_total = flt(self.doc.net_total)

    if self.doc.get("taxes"):
        self.doc.total_taxes_and_charges = flt(
            self.doc.grand_total - self.doc.net_total - flt(self.doc.rounding_adjustment),
            self.doc.precision("total_taxes_and_charges"),
        )
    else:
        self.doc.total_taxes_and_charges = 0.0

    self._set_in_company_currency(self.doc, ["total_taxes_and_charges", "rounding_adjustment"])

    if self.doc.doctype in [
        "Quotation",
        "Sales Order",
        "Delivery Note",
        "Sales Invoice",
        "POS Invoice",
    ]:
        self.doc.base_grand_total = (
            flt(self.doc.grand_total * self.doc.conversion_rate, self.doc.precision("base_grand_total"))
            if self.doc.total_taxes_and_charges
            else self.doc.base_net_total
        )
    else:
        self.doc.taxes_and_charges_added = self.doc.taxes_and_charges_deducted = 0.0
        for tax in self.doc.get("taxes"):
            if tax.category in ["Valuation and Total", "Total"]:
                if tax.add_deduct_tax == "Add":
                    self.doc.taxes_and_charges_added += flt(tax.tax_amount_after_discount_amount)
                else:
                    self.doc.taxes_and_charges_deducted += flt(tax.tax_amount_after_discount_amount)

        self.doc.round_floats_in(self.doc, ["taxes_and_charges_added", "taxes_and_charges_deducted"])

        self.doc.base_grand_total = (
            flt(self.doc.grand_total * self.doc.conversion_rate)
            if (self.doc.taxes_and_charges_added or self.doc.taxes_and_charges_deducted)
            else self.doc.base_net_total
        )

        self._set_in_company_currency(
            self.doc, ["taxes_and_charges_added", "taxes_and_charges_deducted"]
        )

    self.doc.round_floats_in(self.doc, ["grand_total", "base_grand_total"])

    self.set_rounded_total()

# @frappe.whitelist()
# def validate(self,method = None):
#     amount = 0
#     for courier in self.courier_charges_and_others:
#         amount = amount + courier.amount
#     self.grand_total = self.outstanding_amount + amount
#     self.doc = self
#     calculate_taxes_and_totals.set_rounded_total(self.doc)

def validate(self,method = None):
    calculate_taxes_and_totals.calculate_totals = custom_calculate_totals