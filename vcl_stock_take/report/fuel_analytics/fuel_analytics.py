import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	
	columns = get_columns()
	data = get_data(filters)
	
	chart = get_chart_data(data)
	report_summary = get_report_summary(data)
	
	return columns, data, None, chart, report_summary

def get_columns():
	return [
		{"fieldname": "vehicle", "label": _("Vehicle"), "fieldtype": "Link", "options": "Vehicle", "width": 150},
		{"fieldname": "total_issued", "label": _("Total Fuel Issued (L)"), "fieldtype": "Float", "width": 160},
		{"fieldname": "total_cost", "label": _("Total Cost"), "fieldtype": "Currency", "width": 150},
		{"fieldname": "distance_covered", "label": _("Distance Logged (KM)"), "fieldtype": "Float", "width": 160},
		{"fieldname": "efficiency", "label": _("Efficiency (KM/L)"), "fieldtype": "Float", "width": 130}
	]

def get_data(filters):
	# Basic aggregation logic for the report
	# We aggregate all Issue transactions and group by vehicle
	conditions = "transaction_type = 'Issue' AND docstatus = 1"
	if filters and filters.get("from_date"):
		conditions += f" AND transaction_date >= '{filters.get('from_date')}'"
	if filters and filters.get("to_date"):
		conditions += f" AND transaction_date <= '{filters.get('to_date')}'"
		
	sql = f"""
		SELECT 
			vehicle,
			SUM(fuel_issued) as total_issued,
			SUM(total_amount) as total_cost,
			MAX(current_odometer) - MIN(current_odometer) as distance_covered
		FROM `tabFuel Tracker`
		WHERE {conditions}
		GROUP BY vehicle
		HAVING vehicle IS NOT NULL
	"""
	
	raw_data = frappe.db.sql(sql, as_dict=True)
	
	# calculate efficiency
	for row in raw_data:
		if row.total_issued and row.total_issued > 0 and row.distance_covered:
			row.efficiency = flt(row.distance_covered) / flt(row.total_issued)
		else:
			row.efficiency = 0.0
			
	return raw_data

def get_chart_data(data):
	if not data:
		return None
		
	labels = [d.vehicle for d in data]
	values = [d.total_issued for d in data]
	
	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": "Fuel Issued (Liters)", "values": values}]
		},
		"type": "bar",
		"colors": ["#1abc9c"]
	}

def get_report_summary(data):
	total_fuel = sum([d.total_issued for d in data]) if data else 0
	total_cost = sum([d.total_cost for d in data]) if data else 0
	
	return [
		{
			"value": total_fuel,
			"indicator": "Blue",
			"label": _("Total Fuel Issued (Liters)"),
			"datatype": "Float",
		},
		{
			"value": total_cost,
			"indicator": "Green",
			"label": _("Total Fuel Cost"),
			"datatype": "Currency",
		}
	]

def flt(val):
	try:
		return float(val)
	except (ValueError, TypeError):
		return 0.0
