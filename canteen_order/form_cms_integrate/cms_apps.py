from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register  # register the application
class FormsApphook(CMSApp):
    app_name = "djangocms_forms"
    name = "Forms Application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["djangocms_forms.urls"]