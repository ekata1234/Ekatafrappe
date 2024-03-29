import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def get_no_of_bags(qty, bag_cat):
    print('\nkgs--------bag_cat---------\n', qty, bag_cat)
    Qty = float(qty)
    B_Cat = float(bag_cat)
    return Qty/B_Cat


@frappe.whitelist()
def create_stock_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.stock_entry_type = "Material Transfer"
		target.purpose = "Material Transfer"
		target.set_missing_values()
		print('\n\n----------source name type---------', source_name, type(source_name))

	doc = frappe.get_doc('Purchase Receipt', source_name)
	doclist = get_mapped_doc(
		"Purchase Receipt",
		source_name,
		{
			"Purchase Receipt": {
				"doctype": "Stock Entry",
			},
			"Purchase Receipt Item": {
				"doctype": "Stock Entry Detail",
				"field_map": {
					"warehouse": "s_warehouse",
					"parent": "reference_purchase_receipt",
					"batch_no": "batch_no",
					"coffee_processing": "coffee_processing_details",
				},
			},
		},
		target_doc,
		set_missing_values,
	)
	if doclist:
		doc = frappe.get_doc('Purchase Receipt', source_name)
		for i in doclist.items:
			i.receipt_no = doc.lot_no
			i.supplier = doc.supplier
			i.season = doc.season
		return doclist
