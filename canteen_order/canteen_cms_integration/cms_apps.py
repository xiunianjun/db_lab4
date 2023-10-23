from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register  # register the application
class CustomerApphook(CMSApp):
    app_name = "customer"
    name = "Customer Application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["customer.urls"]