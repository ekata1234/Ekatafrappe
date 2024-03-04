import frappe
from frappe.model.mapper import get_mapped_doc

def validate(doc,method=None):
    if doc.voucher_type == "Purchase Receipt":
        print('\n\nvoucher type ------------ ', doc.voucher_type)
        PRDoc = frappe.get_doc('Purchase Receipt', doc.voucher_no)
        if PRDoc:
            print('\n\n PRDoc -----------', PRDoc)
            if PRDoc.lot_no:
                print('\n\n PRDoc lot_no-----------', PRDoc.lot_no)
                doc.receipt_no = PRDoc.lot_no

            for i in PRDoc.items:
                print('\n\n item -----------', i.item_code, i.outturn_no)

                if i.item_code == doc.item_code and i.outturn_no:
                    doc.outturn_no = i.outturn_no
    if doc.voucher_type == "Stock Entry":
        print('\n\nvoucher type ------------ ', doc.voucher_type)
        SEDoc = frappe.get_doc('Stock Entry', doc.voucher_no)
        if SEDoc:
            print('\n\n PRDoc -----------', SEDoc)

            for i in SEDoc.items:
                print('\n\n item -----------', i.item_code, i.outturn_no)

                if i.item_code == doc.item_code and i.outturn_no:
                    doc.outturn_no = i.outturn_no
                    doc.receipt_no = i.receipt_no
