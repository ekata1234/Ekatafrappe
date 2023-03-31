frappe.ui.form.on('Material Request', {
    refresh : function(frm) {
		frm.set_df_property('material_request_type', 'options', ['Purchase','Material Transfer','Material Issue','Manufacture','Customer Provided','RAW Coffee','Coffee Transfer','Coffee Issue','Coffee Manufacturing'])
    },
    supplier : function(frm){
        frm.clear_table('supplier_table');
        refresh_field('supplier_table');
        let rd = frm.add_child("supplier_table");
        rd.supplier = frm.doc.supplier
        refresh_field('supplier_table')
    }
});
