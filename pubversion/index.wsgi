import sae
sae.add_vendor_dir('vendor')
from pubversion import wsgi

application = sae.create_wsgi_app(wsgi.application)
