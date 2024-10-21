import os

history_all_time_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml"
history_90_days_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
currencies_url = "https://supply-xml.booking.com/hotels/xml/currencies"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
