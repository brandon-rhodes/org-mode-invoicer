from datetime import datetime
from decimal import Decimal

raise_date = datetime(2012, 6, 20)

def compute_rate(date):
    return Decimal('60' if date < raise_date else '75')

address_paragraph = """
<i>From:</i><br/>
<br/>
<b>Example, Inc.</b><br/>
Main Street<br/>
solutions@example.com<br/>
<br/>
<i>Bill to:</i><br/>
<br/>
<b>Happy Customer, LLC</b><br/>
http://happy-customer.com/<br/>
<br/>
<i>Date:</i><br/><br/>July 20, 2013<br/><br/>
<i>Terms:</i><br/><br/>30 days<br/><br/>
"""
