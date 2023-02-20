frappe.ui.form.on('Employee', {
    refresh : function(frm) {
			if (frappe.user_roles.includes("HR Manager")) {
				frm.set_df_property('exit', 'hidden', 0)
			}else{
                frm.set_df_property('exit', 'hidden', 1)
            }
    }
});
