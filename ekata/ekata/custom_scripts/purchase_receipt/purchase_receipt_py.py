import frappe

@frappe.whitelist()
def get_no_of_bags(qty, bag_cat):
    print('\nkgs--------bag_cat---------\n', qty, bag_cat)
    Qty = float(qty)
    B_Cat = float(bag_cat)
    return Qty/B_Cat