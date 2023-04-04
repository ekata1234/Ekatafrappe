frappe.ui.form.on('Material Request', {
    supplier : function(frm){
        frm.clear_table('supplier_table');
        refresh_field('supplier_table');
        let rd = frm.add_child("supplier_table");
        rd.supplier = frm.doc.supplier
        refresh_field('supplier_table')
    }
});
