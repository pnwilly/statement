from pathlib import Path
from types import SimpleNamespace

from jinja2 import Environment


def test_statement_preserves_opening_transactions_and_closing_balance():
	path = Path(__file__).parents[1] / "statement/templates/process_statement_of_accounts_gl.html"
	template = Environment().from_string(path.read_text())
	rows = [
		{"account": "Opening", "balance": 100},
		{
			"posting_date": "2026-10-28",
			"voucher_type": "Sales Invoice",
			"voucher_no": "INV-1",
			"debit": 50,
			"credit": 0,
			"balance": 150,
		},
		{"account": "Total", "balance": 50},
		{"account": "Closing", "balance": 150},
	]
	frappe = SimpleNamespace(
		format=lambda value, kind: value,
		utils=SimpleNamespace(fmt_money=lambda value, currency: f"{value:.2f}"),
	)
	html = template.render(
		data=rows,
		filters={
			"party_name": ["Customer"],
			"party": ["C-1"],
			"from_date": "2026-10-01",
			"to_date": "2026-10-28",
			"presentation_currency": "KES",
		},
		frappe=frappe,
		_=lambda value: value,
	)
	assert "Opening Balance" in html
	assert "Closing Balance" in html
	assert "INV-1" in html
	assert "100.00" in html
	assert "150.00" in html
