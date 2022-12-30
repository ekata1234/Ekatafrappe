// frappe.ui.form.on('Courier charges and Others', {
//  amount : function(frm, cdt, cdn) {
//  console.log("========checking=========")
//  var d = locals[cdt][cdn];
 // let total_amount = 0;
 // $.each(frm.doc.courier_charges_and_others, function(idx, val){
 //  if (val.amount) total_amount = frm.doc.outstanding_amount + val.amount;
 // });
//  frappe.call({
//      method:
//          "sales_invoice.custom_calculate_totals",
         // "erpnext.accounts.doctype.bank_statement_import.bank_statement_import.upload_bank_statement",
    //  args: {
    //      self:frm,
         // dt: frm.doc.doctype,
         // dn: frm.doc.name,
         // company: frm.doc.company,
         // bank_account: frm.doc.bank_account,
    //  },
     // callback: function (r) {
     //  if (!r.exc) {
     //      var doc = frappe.model.sync(r.message);
     //      frappe.set_route(
     //          "Form",
     //          doc[0].doctype,
     //          doc[0].name
     //      );
     //  }
     // },
//  })
 // console.log("========checking1=========",total_amount)
 // frm.set_value('outstanding_amount', total_amount);
 // frm.doc.outstanding_amount = total_amount
 // frm.refresh_field('outstanding_amount');
//  }
// });
frappe.ui.form.on('Courier charges and Others', {
    amount : function(frm, cdt, cdn) {
    console.log("========checking=========")
    var d = locals[cdt][cdn];
    var total = 0;
    frm.doc.courier_charges_and_others.forEach(function(d) { total += d.amount; });
    frm.set_value("total", frm.doc.total + total);
    refresh_field("total");
    }
});
// frappe.ui.form.on("Costing BOQ Items", {
//     amount:function(frm, cdt, cdn){
//     var d = locals[cdt][cdn];
//     var total = 0;
//     frm.doc.costing_boq_items.forEach(function(d) { total += d.amount; });

//     frm.set_value("total", total);
//     refresh_field("total");

//     frm.set_value("base_total", total);
//     refresh_field("base_total");

//     frm.set_value("base_net_total", total);
//     refresh_field("base_net_total");

//     frm.set_value("net_total", total);
//     refresh_field("net_total");
//   },
//   costing_boq_items:function(frm, cdt, cdn){
//     var d = locals[cdt][cdn];
//     var total = 0;
//     frm.doc.costing_boq_items.forEach(function(d) { total += d.amount; });
//     frm.set_value("total", total);
//     refresh_field("total");
        
//     frm.set_value("base_total", total);
//     refresh_field("base_total");

//     frm.set_value("base_net_total", total);
//     refresh_field("base_net_total");

//     frm.set_value("net_total", total);
//     refresh_field("net_total");

//     }
//     });