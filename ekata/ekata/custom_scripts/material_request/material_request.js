frappe.ui.form.on('Material Request', {
    refresh : function(frm) {
				frm.set_df_property('material_request_type', 'options', ['Purchase','Material Transfer','Material Issue','Manufacture','Customer Provided','RAW Coffee','Coffee Transfer','Coffee Issue','Coffee Manufacturing'])
    }
});
