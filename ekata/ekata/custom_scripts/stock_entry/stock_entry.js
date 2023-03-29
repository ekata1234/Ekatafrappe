frappe.ui.form.on('Stock Entry', {
refresh: function(frm) {

    
    if(frm.doc.docstatus > 0) {
        setTimeout(() => {
            frm.remove_custom_button('Stock Ledger', 'View');
            }, 10);

        cur_frm.add_custom_button(__("New Stock Ledger"), function() {
            frappe.route_options = {
                voucher_no: frm.doc.name,
                from_date: frm.doc.posting_date,
                to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
                company: frm.doc.company,
                show_cancelled_entries: frm.doc.docstatus === 2
            };
            frappe.set_route("query-report", "New Stock Ledger");
        }, __("View"));
    }

},
})