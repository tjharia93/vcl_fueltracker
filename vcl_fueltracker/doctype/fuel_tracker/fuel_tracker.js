frappe.ui.form.on('Fuel Tracker', {
	refresh: function(frm) {
		// Code to run when the form is loaded
	},
	
	quantity_received: function(frm) {
		calculate_total(frm);
	},
	
	rate: function(frm) {
		calculate_total(frm);
	}
});

function calculate_total(frm) {
	if (frm.doc.quantity_received && frm.doc.rate) {
		frm.set_value('total_amount', frm.doc.quantity_received * frm.doc.rate);
	} else {
		frm.set_value('total_amount', 0);
	}
}
