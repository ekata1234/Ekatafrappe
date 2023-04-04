frappe.ui.form.on('Shipment', {
    onload : function(frm) {
    
    let options = ['Invoice Cum Packing List', 'Photo Certificate', 'Certificate of Origin - From Chamber of Commerce', 'Ico Permit', 'Weight and Quality Certificate', 'Fumigation Certificate', 'Insurance', 'Shipping Bills', 'Bl - Bill of Landing', 'Certificate of Conformity', 'Eto Analysis Report', 'Health Certification', 'Container Survey Report'];

        if (frm.doc.shipment_document.length === 0){
            frm.clear_table('shipment_document');
        for(let i = 0; i < options.length; i ++){
            let row = frm.add_child('shipment_document', {
                document:options[i],
            });
           
          };
        }
        refresh_field("shipment_document");
    }
});
