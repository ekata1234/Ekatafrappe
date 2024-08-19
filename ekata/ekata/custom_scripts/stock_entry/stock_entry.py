import frappe
from frappe.model.mapper import get_mapped_doc

def on_submit(doc,method=None):
    for item in doc.items:
        frappe.db.set_value('Stock Ledger Entry',{'voucher_no':doc.name,'item_code':item.item_code},'supplier',item.supplier)

def validate(doc,method=None):
	print('\n\n--------------set basic rate--------------\n\n')
	if doc.stock_entry_type == 'Repack' or doc.stock_entry_type == 'Bulking':
		rm_amount = 0
		fg_qty = 0
		rate = 0
		last_fg_item = []
		for i in doc.items:
			if i.custom_is_process_loss:
				i.db_set('is_finished_item', 0)

			i.db_set('set_basic_rate_manually', 1)
			if not i.is_finished_item and not i.is_scrap_item and not i.custom_is_process_loss:
				rm_amount += i.amount
			if i.is_finished_item:
				print(i.qty)
				fg_qty += i.qty
			if i.custom_is_process_loss:
				i.db_set('basic_rate', 0)
				i.db_set('amount', 0)
		rate = rm_amount/fg_qty
		print('>>> gf qty', fg_qty)
		if rate > 0:
			for i in doc.items:
				if i.is_finished_item == 1:
					last_fg_item.append(i)
					amount = rate * i.qty
					print('>>> rate', rate, amount)
					i.db_set('basic_rate', rate)
					i.db_set('amount', amount)
					i.db_set('basic_amount', amount)

		doc.set_total_incoming_outgoing_value()


@frappe.whitelist()
def create_repack_entry(source_name, target_doc=None):
	print('>>> create repack entry >>>')
	doc = frappe.flags.args.doc
	SEDoc = frappe.get_doc('Stock Entry', doc['name'])
	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.stock_entry_type = "Repack"
	stock_entry.set_posting_time = 1
	for item in SEDoc.items:
		print('\n\n >>>> ', item)
		if item.is_finished_item == 1:
			stock_entry.append('items', {
				's_warehouse': item.t_warehouse,
				'item_code': item.item_code,
				'qty': item.qty,
				'uom': item.uom,
				'stock_uom': item.stock_uom,
				'basic_rate': item.basic_rate,
				'batch_no': item.batch_no,
				'receipt_no': item.receipt_no,
				'outturn_no': item.outturn_no,
				'season': item.season,
				'coffee_processing_details': item.coffee_processing_details
			})
	return stock_entry

