frappe.ui.form.on("Sales Invoice", "refresh", function(frm) {
    
	var wrapper = frm.get_field("preview_html").$wrapper;
	var is_viewable = frappe.utils.is_image_file(frm.doc.attachment);

	frm.toggle_display("preview", is_viewable);
	frm.toggle_display("preview_html", is_viewable);

	if(is_viewable){
		wrapper.html('<div class="img_preview">\
			<img class="img-responsive" src="'+frm.doc.attachment+'"></img>\
			</div>');
            frm.set_df_property('authorized_by', 'hidden', 1)
	} else {
		wrapper.empty();
        frm.set_df_property('authorized_by', 'hidden', 0)
	}
});
