frappe.listview_settings['Purchase Receipt'] = {
    onload: function(listview){

        listview.refresh()
        console.log(">>",listview)
        listview.page.add_action_item(__("Create Bulking"), function(){
            SelectFG(listview);
		});
    }
}

function SelectFG(listview) {
    let checked_items = listview.get_checked_items();
    console.log(checked_items);

    let dialog = new frappe.ui.Dialog({
        title: __('Select Finished Goods'),
        fields: [
            {
                label: __('Item Code'),
                fieldname: 'item_code',
                fieldtype: 'Link',
                options: 'Item',
                reqd: 1
            },
            {
                label: __('Target Warehouse'),
                fieldname: 'target_warehouse',
                fieldtype: 'Link',
                options: 'Warehouse',
                reqd: 1
            }
        ],
        primary_action: function() {
            let values = dialog.get_values();
            if (!values) return;
            CreateBulking(listview, values.item_code, values.target_warehouse);

            dialog.hide();
        },
        primary_action_label: __('Create')
    });
    dialog.show();
}



function CreateBulking(listview, item_code, target_warehouse){
    let checked_items = listview.get_checked_items();
    console.log(checked_items)
    frappe.call({
        method: 'ekata.ekata.custom_scripts.purchase_receipt.purchase_receipt_py.create_stock_entry_from_purchase_receipts',
        args: {
            purchase_receipt_lst: checked_items,
            item_code: item_code,
            target_warehouse: target_warehouse
        },
        callback: function(r) {
            console.log(">>>>",r.message);
            frappe.set_route('Form','Stock Entry',r.message)
        }
    });
}