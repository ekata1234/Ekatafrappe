frappe.ui.form.on('Stock Entry', {
   refresh: function(frm) {
        frm.add_custom_button(__("Custom Stock Ledger"), function() {
                frappe.route_options = {
                    voucher_no: frm.doc.name,
                };
                frappe.set_route("query-report", "Custom Stock Ledger");
        }, __(""));
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
   validate: function(frm){
        if (frm.doc.outturn_no) {
            frm.events.updateItems(frm, 'outturn_no', frm.doc.outturn_no);
        }
        if (frm.doc.lot_no) {
            frm.events.updateItems(frm, 'receipt_no', frm.doc.lot_no);
        }
   },
   updateItems: function(frm, field, value) {
        if (frm.doc.items && frm.doc.items.length) {
            let doctype = frm.doc.items[0].doctype;
            $.each(frm.doc.items || [], function(i, item) {
                frappe.model.set_value(doctype, item.name, field, value);
            });
        }
   },

   outturn_no: function(frm) {
        if (frm.doc.outturn_no) {
            frm.events.updateItems(frm, 'outturn_no', frm.doc.outturn_no);
        }
   },

   lot_no: function(frm) {
        if (frm.doc.lot_no) {
            frm.events.updateItems(frm, 'receipt_no', frm.doc.lot_no);
        }
   }
});