import frappe

@frappe.whitelist()
def get_no_of_bags(kgs, bag_cat):
    print('kgs--------bag_cat---------', kgs, bag_cat)
    KG = float(kgs)
    B_Cat = float(bag_cat)
    return KG/B_Cat