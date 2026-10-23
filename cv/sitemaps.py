
from django.contrib.sitemaps import Sitemap

from .views import read_portfolio_detail


class PublicSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        # Основные публичные страницы
        urls = [
            "/",
            "/en/",
            "/ru/",
        ]

        # Публичные страницы портфолио на двух языках
        portfolio_items = read_portfolio_detail()

        for portfolio_name in portfolio_items:
            for lang in ("en", "ru"):
                urls.append(
                    f"/portfolio_details/{lang}/{portfolio_name}"
                )

        return urls

    def location(self, item):
        return item
