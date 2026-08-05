from django.contrib.sitemaps import Sitemap
from shared_lib.sfs_core.models import BP



# Dynamic Blueprint Pages
class BlueprintSitemap(Sitemap):

    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return BP.objects.filter(status="approved").order_by('-id')

    def location(self, obj):
        return f"/sfs/blueprints/blueprint?bp_id={obj.bp_id}"

""" 
# Static Pages
class StaticViewSitemap(Sitemap):

    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            '/',
            '/home',
            '/favorites',
            '/categories',
            '/upload',
            '/about',
            '/privacy-policy',
            '/terms-and-conditions',
        ]

    def location(self, item):
        return item """