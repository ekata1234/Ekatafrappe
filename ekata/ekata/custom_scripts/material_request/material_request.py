import frappe
from frappe.model.mapper import get_mapped_doc

def validate(doc,method=None):
    if doc.supplier_table:
        for supp in doc.supplier_table:
            if supp.supplier:
                parent = frappe.db.get_value('Dynamic Link',{"link_title":supp.supplier},['parent'])
                supp.contact = parent
                email = frappe.db.get_value('Contact',parent,['email_id'])
                supp.email_id = email

@frappe.whitelist()
def make_request_for_quotation(source_name, target_doc=None):

	doclist = get_mapped_doc(
		"Material Request",
		source_name,
		{
			"Material Request": {
				"doctype": "Request for Quotation",
				"validation": {"docstatus": ["=", 1], "material_request_type": ["=", "Purchase"]},
			},
			"Material Request Item": {
				"doctype": "Request for Quotation Item",
				"field_map": [
					["name", "material_request_item"],
					["parent", "material_request"],
					["uom", "uom"],
				],
			},
			"Request for Quotation Supplier": {
				"doctype": "Request for Quotation Supplier",
				"field_map": [
					["supplier", "supplier"],
					["contact", "contact"],
					["email_id", "email_id"],
				],
			},
		},
		target_doc,
	)

	return doclist