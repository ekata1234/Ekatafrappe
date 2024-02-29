frappe.ui.form.on("Purchase Receipt Item", {
    kgs: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.kgs){
            console.log(">>>> in kgs >>>>");
            frappe.call({
                method: 'ekata.ekata.custom_scripts.purchase_receipt.purchase_receipt_py.get_no_of_bags',
                args: {
                    kgs : row.kgs,
                    bag_cat : row.bag_category,
                },
                callback: function(r) {
                    console.log(">>>>",r.message);
                    if(r.message){
                        row.bags = r.message
                        frm.refresh_field('items');
                    }
                }
            });
        }
    }
});