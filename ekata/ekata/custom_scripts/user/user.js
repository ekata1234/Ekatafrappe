frappe.ui.form.on('User', {
	validate:function(frm) {
		console.log("in user------------------")
		cur_frm.doc.roles.forEach(function(h){
			console.log("in users.js")
    		if (h.role=='Bank Holiday User'){
				frappe.call({
					// /home/indictrans/Ekata_Earth/Ekata_Earth_project/frappe-bench/apps/ekata/ekata/ekata/custom/holiday_list.py
					method: "ekata.ekata.custom.holiday_list.send_notifications_mail",
					args: {
						email: frm.doc.email,

					},
					callback: function(r) {
						console.log("r in send_notifications_mail--",r.message)
					}
				});
			}
	
		})
	}
})


