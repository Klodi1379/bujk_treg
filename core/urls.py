from django.urls import path
from . import smart_services

app_name = 'core'

urlpatterns = [
    # Smart Services URLs
    path('smart/price-intelligence/<int:product_id>/', smart_services.price_intelligence_view, name='price_intelligence'),
    path('smart/weather-dashboard/', smart_services.weather_dashboard_view, name='weather_dashboard'), 
    path('smart/market-insights/', smart_services.market_insights_view, name='market_insights'),
    path('smart/quality-analysis/<int:product_id>/', smart_services.quality_analysis_view, name='quality_analysis'),
    
    # API endpoints
    path('api/smart-search/', smart_services.smart_search_api, name='smart_search_api'),
    path('api/recommendations/<str:recommendation_type>/', smart_services.product_recommendations_api, name='product_recommendations'),
]
