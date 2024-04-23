import frappe
from frappe.model.mapper import get_mapped_doc
import json

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

@frappe.whitelist()
def create_stock_entry_from_purchase_receipts(source_name, target_doc=None):
	print('\n\n----------PR List---------')
	data = frappe.flags.args.purchase_receipt_list
	items = []
	for pr_name in data:
		print('\n\n --------------', pr_name)

		purchase_receipt = frappe.get_doc("Purchase Receipt", pr_name.get('name'))
		for item in purchase_receipt.items:
			items.append({
				"item_code": item.item_code,
				"item_name": item.item_name,
				"qty": item.qty,
				"parent": purchase_receipt.name,
				"batch_no": item.batch_no,
				"uom": item.uom,
				"s_warehouse": item.warehouse,
				"coffee_processing_details": item.coffee_processing,
				"receipt_no": purchase_receipt.lot_no,
				"supplier": purchase_receipt.supplier,
				"season": purchase_receipt.season
			})

	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.stock_entry_type = "Bulking"
	stock_entry.set_posting_time = 1

	for item in items:
		stock_entry.append("items", item)
	return stock_entry


