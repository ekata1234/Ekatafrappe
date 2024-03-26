# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.utils import cint, flt

from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos
from erpnext.stock.utils import (
	is_reposting_item_valuation_in_progress,
	update_included_uom_in_report,
)


def execute(filters=None):
	is_reposting_item_valuation_in_progress()
	include_uom = filters.get("include_uom")
	columns = get_columns()
	items = get_items(filters)
	sl_entries = get_stock_ledger_entries(filters, items)
	item_details = get_item_details(items, sl_entries, include_uom)
	opening_row = get_opening_balance(filters, columns, sl_entries)
	precision = cint(frappe.db.get_single_value("System Settings", "float_precision"))

	data = []
	conversion_factors = []
	if opening_row:
		data.append(opening_row)
		conversion_factors.append(0)

	actual_qty = stock_value = 0
	if opening_row:
		actual_qty = opening_row.get("qty_after_transaction")
		stock_value = opening_row.get("stock_value")

	available_serial_nos = {}
	for sle in sl_entries:
		item_detail = item_details[sle.item_code]

		sle.update(item_detail)
		# sle.update('')
		# sle.update('')
		sle.update({
			"receipt_no": sle.get("receipt_no"),
			"outturn_no": sle.get("outturn_no"),
			"season": sle.get("season"),
			"grower_code": sle.get("grower_code"),
			"bags": sle.get("bags"),
			"gunny": sle.get("gunny"),
<<<<<<< HEAD
			"location": sle.get("location"),
			"receipt_no_data": sle.get("receipt_no_data"),
=======
			"category": sle.get("category"),
			"sample_mc": sle.get("sample_mc"),
			"sample_ot": sle.get("sample_ot"),
			"sample_grade": sle.get("sample_grade"),
			"pb": sle.get("pb"),
			"a": sle.get("a"),
			"b": sle.get("b"),
			"c": sle.get("c"),
			"bbb": sle.get("bbb"),
			"coffee_processing": sle.get("coffee_processing"),
			"note": sle.get("note"),
>>>>>>> 7d535df (stock ledger report changes)
		})
		if filters.get("batch_no"):
			actual_qty += flt(sle.actual_qty, precision)
			stock_value += sle.stock_value_difference

			if sle.voucher_type == "Stock Reconciliation" and not sle.actual_qty:
				actual_qty = sle.qty_after_transaction
				stock_value = sle.stock_value

			sle.update({"qty_after_transaction": actual_qty, "stock_value": stock_value})

		sle.update({"in_qty": max(sle.actual_qty, 0), "out_qty": min(sle.actual_qty, 0)})

		if sle.serial_no:
			update_available_serial_nos(available_serial_nos, sle)

		data.append(sle)

		if include_uom:
			conversion_factors.append(item_detail.conversion_factor)

	update_included_uom_in_report(columns, data, include_uom, conversion_factors)
	return columns, data


def update_available_serial_nos(available_serial_nos, sle):
	serial_nos = get_serial_nos(sle.serial_no)
	key = (sle.item_code, sle.warehouse)
	if key not in available_serial_nos:
		available_serial_nos.setdefault(key, [])

	existing_serial_no = available_serial_nos[key]
	for sn in serial_nos:
		if sle.actual_qty > 0:
			if sn in existing_serial_no:
				existing_serial_no.remove(sn)
			else:
				existing_serial_no.append(sn)
		else:
			if sn in existing_serial_no:
				existing_serial_no.remove(sn)
			else:
				existing_serial_no.append(sn)

	sle.balance_serial_no = "\n".join(existing_serial_no)


def get_columns():
	columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Datetime", "width": 150},
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100,
		},
		{"label": _("Item Name"), "fieldname": "item_name", "width": 100},
		{
			"label": _("Stock UOM"),
			"fieldname": "stock_uom",
			"fieldtype": "Link",
			"options": "UOM",
			"width": 90,
		},
		{
			"label": _("In Qty"),
			"fieldname": "in_qty",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty",
		},
		{
			"label": _("Out Qty"),
			"fieldname": "out_qty",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty",
		},
		{
			"label": _("Balance Qty"),
			"fieldname": "qty_after_transaction",
			"fieldtype": "Float",
			"width": 100,
			"convertible": "qty",
		},
		{
			"label": _("Voucher #"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 150,
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150,
		},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 100,
		},
		{
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "Link",
			"options": "Brand",
			"width": 100,
		},
		{"label": _("Description"), "fieldname": "description", "width": 200},
		{
			"label": _("Incoming Rate"),
			"fieldname": "incoming_rate",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "rate",
		},
		{
			"label": _("Valuation Rate"),
			"fieldname": "valuation_rate",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "rate",
		},
		{
			"label": _("Balance Value"),
			"fieldname": "stock_value",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
		},
		{
			"label": _("Value Change"),
			"fieldname": "stock_value_difference",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
		},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 110},
		{
			"label": _("Voucher #"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 100,
		},
		{
			"label": _("Batch"),
			"fieldname": "batch_no",
			"fieldtype": "Link",
			"options": "Batch",
			"width": 100,
		},
		{
			"label": _("Serial No"),
			"fieldname": "serial_no",
			"fieldtype": "Link",
			"options": "Serial No",
			"width": 100,
		},
		{"label": _("Balance Serial No"), "fieldname": "balance_serial_no", "width": 100},
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 100,
		},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 110,
		},
		{
			"label": _("Outturn No"),
			"fieldname": "outturn_no",
			"fieldtype": "Link",
			"options": "Outturn No",
			"width": 100,
		},
		{
			"label": _("Lot No"),
			"fieldname": "receipt_no",
			"fieldtype": "Link",
			"options": "Receipt No",
			"width": 100,
		},
		{
			"label": _("Season"),
			"fieldname": "season",
			"fieldtype": "Link",
			"options": "Season",
			"width": 100,
		},
		{
			"label": _("Grower Code"),
			"fieldname": "grower_code",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Bags"),
			"fieldname": "bags",
			"fieldtype": "Float",
			"width": 100,
		},
<<<<<<< HEAD
		{
			"label": _("Location"),
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Receipt No"),
			"fieldname": "receipt_no_data",
			"fieldtype": "Data",
			"width": 100,
		},
		# {
		# 	"label": _("KGs"),
		# 	"fieldname": "kgs",
		# 	"fieldtype": "Float",
		# 	"width": 100,
		# },
=======
>>>>>>> 7d535df (stock ledger report changes)
		{
			"label": _("Gunny"),
			"fieldname": "gunny",
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"label": _("Category"),
			"fieldname": "category",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Bags"),
			"fieldname": "bags",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Sample MC"),
			"fieldname": "sample_mc",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Sample OT"),
			"fieldname": "sample_ot",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Sample Grade"),
			"fieldname": "sample_grade",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("PB (%)"),
			"fieldname": "pb",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("A (%)"),
			"fieldname": "a",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("B (%)"),
			"fieldname": "b",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("C (%)"),
			"fieldname": "c",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("BBB (%)"),
			"fieldname": "bbb",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Coffee Processing"),
			"fieldname": "coffee_processing",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Note"),
			"fieldname": "note",
			"fieldtype": "Data",
			"width": 100,
		},
	]

	return columns


def get_stock_ledger_entries(filters, items):
	item_conditions_sql = ""
	if items:
		item_conditions_sql = "and sle.item_code in ({})".format(
			", ".join(frappe.db.escape(i) for i in items)
		)

	sl_entries = frappe.db.sql(
		"""
		SELECT
			concat_ws(" ", posting_date, posting_time) AS date,
			item_code,
			warehouse,
			actual_qty,
			qty_after_transaction,
			incoming_rate,
			valuation_rate,
			stock_value,
			voucher_type,
			voucher_no,
			batch_no,
			serial_no,
			company,
			project,
			stock_value_difference,
			receipt_no,
			outturn_no,
			season,
			grower_code,
			bags,
			gunny,
<<<<<<< HEAD
			location,
			receipt_no_data
=======
			category,
			sample_mc,
			sample_ot,
			sample_grade,
			pb,
			a,
			b,
			c,
			bbb,
			coffee_processing,
			note
>>>>>>> 7d535df (stock ledger report changes)
		FROM
			`tabStock Ledger Entry` sle
		WHERE
			company = %(company)s
				AND is_cancelled = 0 AND posting_date BETWEEN %(from_date)s AND %(to_date)s
				{sle_conditions}
				{item_conditions_sql}
		ORDER BY
			posting_date asc, posting_time asc, creation asc
		""".format(
			sle_conditions=get_sle_conditions(filters), item_conditions_sql=item_conditions_sql
		),
		filters,
		as_dict=1,
	)

	return sl_entries


def get_items(filters):
	conditions = []
	if filters.get("item_code"):
		conditions.append("item.name=%(item_code)s")
	else:
		if filters.get("brand"):
			conditions.append("item.brand=%(brand)s")
		if filters.get("item_group"):
			conditions.append(get_item_group_condition(filters.get("item_group")))

	items = []
	if conditions:
		items = frappe.db.sql_list(
			"""select name from `tabItem` item where {}""".format(" and ".join(conditions)), filters
		)
	return items


def get_item_details(items, sl_entries, include_uom):
	item_details = {}
	if not items:
		items = list(set(d.item_code for d in sl_entries))

	if not items:
		return item_details

	cf_field = cf_join = ""
	if include_uom:
		cf_field = ", ucd.conversion_factor"
		cf_join = (
			"left join `tabUOM Conversion Detail` ucd on ucd.parent=item.name and ucd.uom=%s"
			% frappe.db.escape(include_uom)
		)

	res = frappe.db.sql(
		"""
		select
			item.name, item.item_name, item.description, item.item_group, item.brand, item.stock_uom {cf_field}
		from
			`tabItem` item
			{cf_join}
		where
			item.name in ({item_codes})
	""".format(
			cf_field=cf_field, cf_join=cf_join, item_codes=",".join(["%s"] * len(items))
		),
		items,
		as_dict=1,
	)

	for item in res:
		item_details.setdefault(item.name, item)

	return item_details


def get_sle_conditions(filters):
	conditions = []
	if filters.get("warehouse"):
		warehouse_condition = get_warehouse_condition(filters.get("warehouse"))
		if warehouse_condition:
			conditions.append(warehouse_condition)
	if filters.get("voucher_no"):
		conditions.append("voucher_no=%(voucher_no)s")
	if filters.get("batch_no"):
		conditions.append("batch_no=%(batch_no)s")
	if filters.get("project"):
		conditions.append("project=%(project)s")
	if filters.get("receipt_no"):
		conditions.append("receipt_no=%(receipt_no)s")
	if filters.get("outturn_no"):
		conditions.append("outturn_no=%(outturn_no)s")

	return "and {}".format(" and ".join(conditions)) if conditions else ""


def get_opening_balance(filters, columns, sl_entries):
	if not (filters.item_code and filters.warehouse and filters.from_date):
		return

	from erpnext.stock.stock_ledger import get_previous_sle

	last_entry = get_previous_sle(
		{
			"item_code": filters.item_code,
			"warehouse_condition": get_warehouse_condition(filters.warehouse),
			"posting_date": filters.from_date,
			"posting_time": "00:00:00",
		}
	)

	# check if any SLEs are actually Opening Stock Reconciliation
	for sle in list(sl_entries):
		if (
			sle.get("voucher_type") == "Stock Reconciliation"
			and sle.get("date").split()[0] == filters.from_date
			and frappe.db.get_value("Stock Reconciliation", sle.voucher_no, "purpose") == "Opening Stock"
		):
			last_entry = sle
			sl_entries.remove(sle)

	row = {
		"item_code": _("'Opening'"),
		"qty_after_transaction": last_entry.get("qty_after_transaction", 0),
		"valuation_rate": last_entry.get("valuation_rate", 0),
		"stock_value": last_entry.get("stock_value", 0),
	}

	return row


def get_warehouse_condition(warehouse):
	warehouse_details = frappe.db.get_value("Warehouse", warehouse, ["lft", "rgt"], as_dict=1)
	if warehouse_details:
		return (
			" exists (select name from `tabWarehouse` wh \
			where wh.lft >= %s and wh.rgt <= %s and warehouse = wh.name)"
			% (warehouse_details.lft, warehouse_details.rgt)
		)

	return ""


def get_item_group_condition(item_group):
	item_group_details = frappe.db.get_value("Item Group", item_group, ["lft", "rgt"], as_dict=1)
	if item_group_details:
		return (
			"item.item_group in (select ig.name from `tabItem Group` ig \
			where ig.lft >= %s and ig.rgt <= %s and item.item_group = ig.name)"
			% (item_group_details.lft, item_group_details.rgt)
		)

	return ""
