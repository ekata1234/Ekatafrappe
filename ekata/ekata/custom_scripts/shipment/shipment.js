frappe.ui.form.on('Shipment', {
    refresh : function(frm) {
        
        frm.set_df_property('incoterm', 'options', ['EXW (Ex Works)', 'FCA (Free Carrier)', 'CPT (Carriage Paid To)', 'CIP (Carriage and Insurance Paid to)', 'DPU (Delivered At Place Unloaded)', 'DAP (Delivered At Place)', 'DDP (Delivered Duty Paid)', 'FOB', 'CIF', 'EX-FACTORY'])
        refresh_field("incoterm");
        
    },
    onload : function(frm) {

            frm.set_df_property('incoterm', 'options', ['EXW (Ex Works)', 'FCA (Free Carrier)', 'CPT (Carriage Paid To)', 'CIP (Carriage and Insurance Paid to)', 'DPU (Delivered At Place Unloaded)', 'DAP (Delivered At Place)', 'DDP (Delivered Duty Paid)', 'FOB', 'CIF', 'EX-FACTORY'])

    refresh_field("incoterm");

    
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
