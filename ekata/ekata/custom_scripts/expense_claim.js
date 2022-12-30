frappe.ui.form.on('Expense Claim', {
    refresh : function(frm) {
        if ((frm.doc.__islocal) || !(frappe.session.user === 'finance@ekata.co.in')) {
            frm.set_df_property('approval_status', 'hidden', 1)
        }
    refresh_field("approval_status");
    },
    onload : function(frm) {
        if ((frm.doc.__islocal)  || !(frappe.session.user === 'finance@ekata.co.in')) {
            frm.set_df_property('approval_status', 'hidden', 1)
        }
    refresh_field("approval_status");
    }
});
