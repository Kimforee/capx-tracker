from django.urls import path
from .views import StockListCreateAPIView, StockDetailAPIView, PortfolioValueAPIView, RandomStockAPIView 

urlpatterns = [
    path('stocks/', StockListCreateAPIView.as_view(), name='stock-list-create'),
    path('stocks/<int:pk>/', StockDetailAPIView.as_view(), name='stock-detail'),
    path('portfolio/value/', PortfolioValueAPIView.as_view(), name='portfolio-value'),
    path('stocks/random/', RandomStockAPIView.as_view(), name='random-stocks'),
]
