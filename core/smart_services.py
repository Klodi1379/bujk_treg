"""
Smart services for agricultural platform - AI-powered features for farmers and buyers
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import json
import requests
from decimal import Decimal

from .models import Product, FarmerProfile
from marketplace.models import Order, OrderItem
from farmer.models import ProductionLog, Crop


class PriceIntelligenceService:
    """AI-powered price recommendations based on market data"""
    
    @staticmethod
    def get_price_recommendation(product):
        """Calculate optimal price based on demand, season, competition"""
        try:
            # Get similar products for comparison
            similar_products = Product.objects.filter(
                category=product.category,
                is_organic=product.is_organic
            ).exclude(id=product.id)
            
            avg_price = similar_products.aggregate(
                avg_price=Avg('price')
            )['avg_price'] or product.price
            
            # Calculate demand score based on recent orders
            recent_orders = OrderItem.objects.filter(
                product=product,
                order__created_at__gte=timezone.now() - timedelta(days=30)
            ).count()
            
            # Seasonal adjustment
            seasonal_multiplier = PriceIntelligenceService._get_seasonal_multiplier(product)
            
            # Supply/demand ratio
            supply_demand_ratio = PriceIntelligenceService._calculate_supply_demand(product)
            
            # Calculate recommended price
            base_price = float(avg_price)
            demand_adjustment = 1 + (recent_orders * 0.02)  # 2% per recent order
            seasonal_adjustment = seasonal_multiplier
            supply_adjustment = supply_demand_ratio
            
            recommended_price = base_price * demand_adjustment * seasonal_adjustment * supply_adjustment
            
            # Round to nearest 10
            recommended_price = round(recommended_price / 10) * 10
            
            return {
                'current_price': float(product.price),
                'recommended_price': recommended_price,
                'price_change': recommended_price - float(product.price),
                'change_percentage': ((recommended_price - float(product.price)) / float(product.price)) * 100,
                'confidence': 85,  # AI confidence score
                'factors': {
                    'market_average': float(avg_price),
                    'recent_demand': recent_orders,
                    'seasonal_factor': seasonal_multiplier,
                    'supply_demand': supply_demand_ratio
                },
                'explanation': PriceIntelligenceService._generate_explanation(
                    product, recommended_price, float(product.price)
                )
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def _get_seasonal_multiplier(product):
        """Get seasonal price multiplier based on product and current month"""
        month = timezone.now().month
        
        seasonal_data = {
            'vegetables': {
                'spring': [3, 4, 5],
                'summer': [6, 7, 8], 
                'autumn': [9, 10, 11],
                'winter': [12, 1, 2]
            }
        }
        
        # Simplified seasonal logic
        if month in [6, 7, 8]:  # Summer - high supply for vegetables
            return 0.9
        elif month in [12, 1, 2]:  # Winter - low supply
            return 1.2
        else:
            return 1.0
    
    @staticmethod
    def _calculate_supply_demand(product):
        """Calculate supply vs demand ratio"""
        # Get total stock of similar products
        total_supply = Product.objects.filter(
            category=product.category,
            is_organic=product.is_organic,
            availability='in_stock'
        ).aggregate(total_stock=Sum('stock'))['total_stock'] or 0
        
        # Get recent demand
        recent_demand = OrderItem.objects.filter(
            product__category=product.category,
            order__created_at__gte=timezone.now() - timedelta(days=7)
        ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        
        if total_supply == 0:
            return 1.3  # High price if no supply
        
        demand_supply_ratio = float(recent_demand) / float(total_supply)
        
        if demand_supply_ratio > 0.8:
            return 1.2  # High demand, increase price
        elif demand_supply_ratio < 0.3:
            return 0.9  # Low demand, decrease price
        else:
            return 1.0
    
    @staticmethod
    def _generate_explanation(product, recommended_price, current_price):
        """Generate human-readable explanation for price recommendation"""
        if recommended_price > current_price:
            return f"Rekomandojmë rritjen e çmimit për {product.name} sepse kërkesa është e lartë dhe oferta e kufizuar."
        elif recommended_price < current_price:
            return f"Rekomandojmë uljen e çmimit për {product.name} për të rritur konkurrueshhmërinë në treg."
        else:
            return f"Çmimi aktual për {product.name} është optimal për kushtet aktuale të tregut."


class WeatherIntegrationService:
    """Weather data integration for farming recommendations"""
    
    @staticmethod
    def get_weather_data(location="Tirana"):
        """Get current weather and forecast"""
        try:
            # Simulate weather API call (replace with real API)
            weather_data = {
                'current': {
                    'temperature': 22,
                    'humidity': 65,
                    'description': 'I kthjellët',
                    'wind_speed': 5,
                    'visibility': 10,
                    'uv_index': 6
                },
                'forecast': [
                    {'day': 'Sot', 'high': 25, 'low': 15, 'condition': 'sunny', 'rain_chance': 10},
                    {'day': 'Nesër', 'high': 23, 'low': 14, 'condition': 'cloudy', 'rain_chance': 30},
                    {'day': 'Pasnesër', 'high': 20, 'low': 12, 'condition': 'rainy', 'rain_chance': 80},
                ],
                'alerts': [
                    {
                        'type': 'warning',
                        'message': 'Parashikohet shi i rrëmbyeshëm për të mërkurën',
                        'severity': 'medium'
                    }
                ]
            }
            return weather_data
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_farming_recommendations(weather_data, farmer_crops):
        """Generate farming recommendations based on weather"""
        recommendations = []
        
        current_weather = weather_data.get('current', {})
        forecast = weather_data.get('forecast', [])
        
        # Temperature-based recommendations
        if current_weather.get('temperature', 0) > 30:
            recommendations.append({
                'type': 'irrigation',
                'priority': 'high',
                'title': 'Ujitje e shtuar',
                'message': 'Temperaturat e larta kërkojnë ujitje më të shpeshtë.',
                'action': 'Ujisni bimët në orët e hershme të mëngjesit ose mbrëmjes.'
            })
        
        # Humidity-based recommendations
        if current_weather.get('humidity', 0) > 80:
            recommendations.append({
                'type': 'disease_prevention',
                'priority': 'medium',
                'title': 'Parandalim sëmundjesh',
                'message': 'Lagështira e lartë mund të shkaktojë sëmundje të bimëve.',
                'action': 'Kontrolloni bimët për shenja të kërpudhave dhe siguroni ajërim të mirë.'
            })
        
        # Rain forecast recommendations
        for day in forecast:
            if day.get('rain_chance', 0) > 70:
                recommendations.append({
                    'type': 'harvest',
                    'priority': 'high',
                    'title': f'Korrje urgjente për {day["day"]}',
                    'message': f'Parashikohet shi me probabilitet {day["rain_chance"]}%',
                    'action': 'Korni produktet e pjekura para se të fillojë shiu.'
                })
        
        return recommendations


class MarketInsightsService:
    """Market analysis and insights for farmers"""
    
    @staticmethod
    def get_market_trends():
        """Analyze market trends and popular products"""
        try:
            # Most sold products in last 30 days
            popular_products = OrderItem.objects.filter(
                order__created_at__gte=timezone.now() - timedelta(days=30)
            ).values('product__name', 'product__category__name').annotate(
                total_sold=Sum('quantity'),
                total_revenue=Sum('subtotal'),
                order_count=Count('order')
            ).order_by('-total_sold')[:10]
            
            # Price trends
            price_trends = Product.objects.values('category__name').annotate(
                avg_price=Avg('price'),
                product_count=Count('id')
            ).order_by('category__name')
            
            # Seasonal demand patterns
            seasonal_data = MarketInsightsService._analyze_seasonal_patterns()
            
            return {
                'popular_products': list(popular_products),
                'price_trends': list(price_trends),
                'seasonal_patterns': seasonal_data,
                'market_opportunities': MarketInsightsService._identify_opportunities()
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def _analyze_seasonal_patterns():
        """Analyze seasonal demand patterns"""
        current_month = timezone.now().month
        
        # Simulate seasonal analysis
        seasonal_data = {
            'current_season': 'autumn',
            'trending_up': ['apples', 'pumpkins', 'nuts'],
            'trending_down': ['tomatoes', 'cucumbers', 'peppers'],
            'recommendations': [
                'Rritni prodhimin e mollëve për sezonin e vjeshtës',
                'Filloni përgatitjet për produktet e dimrit',
                'Zvogëloni çmimet e produkteve verore'
            ]
        }
        
        return seasonal_data
    
    @staticmethod
    def _identify_opportunities():
        """Identify market opportunities for farmers"""
        # Find products with high demand but low supply
        opportunities = []
        
        # Simulate opportunity analysis
        opportunities = [
            {
                'product': 'Specat e kuq organikë',
                'opportunity_score': 85,
                'demand': 'high',
                'supply': 'low',
                'potential_profit': '25% më shumë se mesatarja',
                'action': 'Konsideroni kultivimin e specave organikë për sezonin e ardhshëm'
            },
            {
                'product': 'Bimë aromatike të freskëta',
                'opportunity_score': 78,
                'demand': 'growing',
                'supply': 'limited',
                'potential_profit': '30% më shumë se mesatarja',
                'action': 'Tregu për bimë aromatike po rritet shpejt'
            }
        ]
        
        return opportunities


class QualityAssuranceService:
    """Quality monitoring and assurance for products"""
    
    @staticmethod
    def analyze_product_quality(product):
        """Analyze product quality based on various factors"""
        try:
            quality_score = 0
            factors = {}
            
            # Image quality (simulated)
            if product.images.exists():
                factors['image_quality'] = 85
                quality_score += 20
            else:
                factors['image_quality'] = 0
            
            # Description completeness
            if len(product.description) > 100:
                factors['description_score'] = 90
                quality_score += 15
            elif len(product.description) > 50:
                factors['description_score'] = 70
                quality_score += 10
            else:
                factors['description_score'] = 40
                quality_score += 5
            
            # Farmer reputation
            farmer_rating = 4.5  # Simulated
            factors['farmer_reputation'] = farmer_rating * 20
            quality_score += farmer_rating * 10
            
            # Freshness indicator
            if product.harvest_date:
                days_since_harvest = (timezone.now().date() - product.harvest_date).days
                if days_since_harvest <= 1:
                    factors['freshness'] = 95
                    quality_score += 20
                elif days_since_harvest <= 3:
                    factors['freshness'] = 80
                    quality_score += 15
                else:
                    factors['freshness'] = 60
                    quality_score += 10
            
            # Organic certification
            if product.is_organic:
                factors['organic_certified'] = 100
                quality_score += 15
            
            # Stock availability
            if product.stock > 50:
                factors['availability'] = 90
                quality_score += 10
            elif product.stock > 20:
                factors['availability'] = 70
                quality_score += 5
            else:
                factors['availability'] = 40
            
            quality_score = min(quality_score, 100)  # Cap at 100
            
            recommendations = QualityAssuranceService._generate_quality_recommendations(
                product, factors, quality_score
            )
            
            return {
                'quality_score': quality_score,
                'grade': QualityAssuranceService._get_quality_grade(quality_score),
                'factors': factors,
                'recommendations': recommendations
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def _get_quality_grade(score):
        """Convert quality score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        else:
            return 'D'
    
    @staticmethod
    def _generate_quality_recommendations(product, factors, score):
        """Generate recommendations to improve product quality"""
        recommendations = []
        
        if factors.get('image_quality', 0) < 70:
            recommendations.append({
                'type': 'images',
                'priority': 'high',
                'message': 'Shtoni foto me cilësi më të lartë për produktin tuaj'
            })
        
        if factors.get('description_score', 0) < 70:
            recommendations.append({
                'type': 'description',
                'priority': 'medium',
                'message': 'Përshkruani më detajisht produktin tuaj'
            })
        
        if factors.get('freshness', 0) < 80:
            recommendations.append({
                'type': 'freshness',
                'priority': 'high',
                'message': 'Përditësoni datën e korrjes ose korni më shpesh'
            })
        
        return recommendations


# View functions for smart services
@login_required
def price_intelligence_view(request, product_id):
    """View for price intelligence recommendations"""
    try:
        product = Product.objects.get(id=product_id, farmer__user=request.user)
        recommendation = PriceIntelligenceService.get_price_recommendation(product)
        return JsonResponse(recommendation)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


@login_required
def weather_dashboard_view(request):
    """Weather dashboard for farmers"""
    farmer = request.user.farmer_profile
    
    # Get weather data
    weather_data = WeatherIntegrationService.get_weather_data()
    
    # Get farmer's crops
    farmer_crops = farmer.farmercrop_set.all()
    
    # Get farming recommendations
    recommendations = WeatherIntegrationService.get_farming_recommendations(
        weather_data, farmer_crops
    )
    
    return render(request, 'farmer/weather_dashboard.html', {
        'weather_data': weather_data,
        'recommendations': recommendations,
        'farmer': farmer
    })


@login_required
def market_insights_view(request):
    """Market insights dashboard"""
    insights = MarketInsightsService.get_market_trends()
    
    return render(request, 'farmer/market_insights.html', {
        'insights': insights
    })


@login_required
def quality_analysis_view(request, product_id):
    """Product quality analysis"""
    try:
        product = Product.objects.get(id=product_id, farmer__user=request.user)
        analysis = QualityAssuranceService.analyze_product_quality(product)
        return JsonResponse(analysis)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


def smart_search_api(request):
    """AI-powered smart search for products"""
    query = request.GET.get('q', '')
    
    if not query:
        return JsonResponse({'products': [], 'suggestions': []})
    
    # Enhanced search with AI-like features
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(farmer__farm_name__icontains=query) |
        Q(category__name__icontains=query)
    ).select_related('farmer', 'category').prefetch_related('images')
    
    # Smart suggestions
    suggestions = []
    if 'organik' in query.lower():
        suggestions.append('Produkte organike të certifikuara')
    if 'domatë' in query.lower():
        suggestions.extend(['Domate cherry', 'Domate të kuqe', 'Domate të verdha'])
    if 'spec' in query.lower():
        suggestions.extend(['Speca të kuq', 'Speca të gjelbër', 'Speca djegës'])
    
    # Serialize products
    products_data = []
    for product in products[:20]:  # Limit to 20 results
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'farmer_name': product.farmer.farm_name,
            'image_url': product.images.first().image.url if product.images.exists() else None,
            'is_organic': product.is_organic,
            'location': str(product.farmer.location) if product.farmer.location else 'Unknown'
        })
    
    return JsonResponse({
        'products': products_data,
        'suggestions': suggestions,
        'count': len(products_data)
    })


def product_recommendations_api(request, recommendation_type):
    """Get product recommendations based on type"""
    
    if recommendation_type == 'popular':
        # Most popular products
        products = Product.objects.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:12]
    
    elif recommendation_type == 'nearby':
        # Products from nearby farmers (simulated)
        products = Product.objects.filter(
            farmer__location__city='Tirana'  # Simulate nearby
        )[:12]
    
    elif recommendation_type == 'new':
        # Recently added products
        products = Product.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-created_at')[:12]
    
    elif recommendation_type == 'discounted':
        # Products with discounts
        products = Product.objects.filter(
            discount_price__isnull=False
        ).order_by('-created_at')[:12]
    
    else:
        products = Product.objects.none()
    
    # Serialize products
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'discount_price': float(product.discount_price) if product.discount_price else None,
            'farmer_name': product.farmer.farm_name,
            'image_url': product.images.first().image.url if product.images.exists() else None,
            'is_organic': product.is_organic,
            'slug': product.slug
        })
    
    return JsonResponse({
        'products': products_data,
        'count': len(products_data)
    })
