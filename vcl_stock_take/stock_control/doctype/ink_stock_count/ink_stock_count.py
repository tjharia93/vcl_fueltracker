import frappe
from frappe.model.document import Document


class InkStockCount(Document):
	def validate(self):
		self.validate_items()
		self.set_physical_qty_std()
		self.calculate_totals()

	def validate_items(self):
		if not self.items:
			frappe.throw("At least one item line is required.")

		for row in self.items:
			if (row.closing_qty or 0) < 0:
				frappe.throw(f"Row {row.idx}: Closing Qty cannot be negative.")

		if self.comparison_mode == "ERP Compare":
			for row in self.items:
				if not row.erp_warehouse and not self.location_store:
					frappe.throw(
						f"Row {row.idx}: ERP Warehouse is required when Comparison Mode is ERP Compare."
					)

	def set_physical_qty_std(self):
		for row in self.items:
			row.physical_qty_std = row.closing_qty or 0
			if not row.standard_uom and row.stock_uom:
				row.standard_uom = row.stock_uom

	def calculate_totals(self):
		self.total_lines = len(self.items)
		self.total_variance_lines = sum(
			1 for row in self.items if (row.variance_qty or 0) != 0
		)
		self.total_variance_value = sum(row.variance_value or 0 for row in self.items)
