import frappe
from frappe.model.mapper import get_mapped_doc

def validate(doc,method=None):
    if doc.voucher_type == "Purchase Receipt":
        print('\n\nvoucher type ------------ ', doc.voucher_type)
        PRDoc = frappe.get_doc('Purchase Receipt', doc.voucher_no)
        if PRDoc:
            print('\n\n PRDoc -------------------------------', PRDoc)
            if PRDoc.lot_no:
                print('\n\n PRDoc lot_no---------------------', PRDoc.lot_no)
                doc.receipt_no = PRDoc.lot_no
            if PRDoc.season:
                doc.season = PRDoc.season
            if PRDoc.grower_code:
                doc.grower_code = PRDoc.grower_code
            if PRDoc.receipt_no:
                doc.receipt_no_data = PRDoc.receipt_no

            for i in PRDoc.items:
                print('\n\n item ---------------------------------------', i.item_code, i.outturn_no)

                if i.item_code == doc.item_code:
                    # doc.outturn_no = i.outturn_no
                    doc.bags = i.bags
                    doc.gunny = i.bags

                    doc.location = i.location
                    doc.category = i.bag_category
                    doc.sample_mc = i.sample_mc
                    doc.sample_ot = i.sample_ot
                    doc.sample_grade = i.sample_grade
                    doc.pb = i.pb
                    doc.a = i.a
                    doc.b = i.b
                    doc.c = i.c
                    doc.bbb = i.bbb
                    doc.coffee_processing = i.coffee_processing
                    doc.note = i.note

    if doc.voucher_type == "Stock Entry":
        print('\n\nvoucher type ------------ ', doc.voucher_type)
        SEDoc = frappe.get_doc('Stock Entry', doc.voucher_no)
        if SEDoc:
            print('\n\n PRDoc -----------', SEDoc)

            for i in SEDoc.items:
                print('\n\n item -----------', i.item_code, i.outturn_no)

                if i.item_code == doc.item_code:
                    print(i.outturn_no, i.receipt_no)
                    doc.outturn_no = i.outturn_no
                    doc.receipt_no = i.receipt_no
                    doc.coffee_processing = i.coffee_processing_details
                    doc.season = i.season



