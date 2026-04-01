frappe.ui.form.on('Ink Stock Count', {
	refresh: function(frm) {
		// Future: add "Fetch ERP Stock" button when comparison_mode is ERP Compare
	}
});

frappe.ui.form.on('Ink Stock Count Item', {
	item: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (!row.item) return;

		frappe.db.get_value(
			'Item',
			row.item,
			['item_code', 'item_name', 'stock_uom'],
			function(value) {
				if (!value) return;
				frappe.model.set_value(cdt, cdn, 'item_code', value.item_code);
				frappe.model.set_value(cdt, cdn, 'item_name', value.item_name);
				frappe.model.set_value(cdt, cdn, 'stock_uom', value.stock_uom);
				frappe.model.set_value(cdt, cdn, 'standard_uom', value.stock_uom);
			}
		);
	},

	closing_qty: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, 'physical_qty_std', row.closing_qty || 0);
	}
});
