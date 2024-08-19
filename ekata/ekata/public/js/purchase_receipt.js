frappe.ui.form.on("Purchase Receipt", {
    refresh: function(frm) {
        frm.add_custom_button(__('View Custom Stock Ledger'), function(){
            var url = "/app/ekata/ekata/query-report/Custom Stock Ledger?voucher_no=" + encodeURIComponent(frm.doc.name)
                +"&receipt_no="+ encodeURIComponent(frm.doc.lot_no);
              frappe.set_route(url);
        },)
    }
});
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
                    if(r.message){
                        row.bags = r.message
                        frm.refresh_field('items');
                    }
                }
            });
        }
    },
    bag_category: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.qty && row.bag_category){
            console.log(">>>> in bag category >>>>");
            frappe.call({
                method: 'ekata.ekata.custom_scripts.purchase_receipt.purchase_receipt_py.get_no_of_bags',
                args: {
                    qty : row.qty,
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
