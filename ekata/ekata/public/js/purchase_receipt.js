frappe.ui.form.on("Purchase Receipt Item", {
    qty: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.qty && row.bag_category){
            console.log(">>>> in kgs >>>>");
            frappe.call({
                method: 'ekata.ekata.custom_scripts.purchase_receipt.purchase_receipt_py.get_no_of_bags',
                args: {
                    qty : row.qty,
                    bag_cat : row.bag_category,
                },
                callback: function(r) {
                    console.log(">>>>",r.message);
                    alert('okk');
                    if(r.message){
                        row.bags = r.message
                        frm.refresh_field('items');
                    }
                }
            });
        }
    }
});