from gapfinder.fetch import extract

HTML = """<html><head><title>Pricing</title></head><body>
<nav>Home | Products | Login</nav>
<main><h1>Plans</h1><p>Our Team plan suits growing companies and includes SCIM provisioning,
audit logs and priority support for every workspace you manage.</p>
<table><tr><th>Plan</th><th>Price</th></tr><tr><td>Team</td><td>$25 per user/month</td></tr>
<tr><td>Enterprise</td><td>Contact sales</td></tr></table></main>
<footer>© Example</footer></body></html>"""


def test_extract_keeps_pricing_table_and_drops_chrome():
    text = extract(HTML)
    assert "$25 per user/month" in text
    assert "Contact sales" in text
    assert "Login" not in text
