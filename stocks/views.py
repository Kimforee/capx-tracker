from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stock
from .serializers import StockSerializer
from django.http import JsonResponse
from .utils import get_stock_price, get_real_price
import requests
import random
from django.db.models import Sum
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class StockListCreateAPIView(APIView):
    """
    Handles listing all stocks and creating a new stock for the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        stocks = Stock.objects.filter(user=request.user)
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockDetailAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a single stock for the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Stock.objects.get(pk=pk, user=self.request.user)
        except Stock.DoesNotExist:
            return None

    def get(self, request, pk):
        stock = self.get_object(pk)
        if stock is None:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        stock = self.get_object(pk)
        if stock is None:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stock = self.get_object(pk)
        if stock is None:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)
        stock.delete()
        return Response({"message": "Stock deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PortfolioValueAPIView(APIView):
    """
    API to calculate the total portfolio value for the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Fetch all stocks for the authenticated user
        stocks = Stock.objects.filter(user=request.user)
        total_value = 0
        portfolio_details = []

        for stock in stocks:
            current_price = None

            try:
                price = [200, 443, 222]
                # current_price = get_stock_price(stock.ticker)
                current_price = random.choice(price)
                print("fetching from the api for the stock :------------ ", current_price)
            except Exception as e:
                # Handle case where API call fails (e.g., rate limit reached)
                print(f"Error fetching price for {stock.ticker}: {str(e)}")
            
            # If the API fails or rate limit is exceeded, use the stock's buy_price from the database
            if current_price is None:
                current_price = stock.buy_price  # Use the buy_price from the database

            # Calculate the stock's total value
            stock_value = current_price * stock.quantity
            total_value += stock_value  # Add to total portfolio value

            # Add the stock's details to the response
            portfolio_details.append({
                "name": stock.name,
                "ticker": stock.ticker,
                "quantity": stock.quantity,
                "buy_price": stock.buy_price,
                "current_price": current_price,
                "value": stock_value,
            })

        return Response(
            {
                "total_portfolio_value": total_value,
                "stocks": portfolio_details,
            },
            status=status.HTTP_200_OK,
        )

class PortfolioMetricsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stocks = Stock.objects.filter(user=request.user)
        portfolio_data = []

        for stock in stocks:
            try:
                response = requests.get(
                    "https://www.alphavantage.co/query",
                    params={
                        "function": "GLOBAL_QUOTE",
                        "symbol": stock.ticker,
                        "apikey": settings.ALPHA_VANTAGE_API_KEY,
                    }
                )
                data = response.json()
                global_quote = data.get("Global Quote", {})

                # Extract required fields
                current_price = float(global_quote.get("05. price", stock.buy_price))
                previous_close = float(global_quote.get("08. previous close", stock.buy_price))
                change = global_quote.get("09. change", "0.00")
                change_percent = global_quote.get("10. change percent", "0.00%")

                portfolio_data.append({
                    "ticker": stock.ticker,
                    "current_price": current_price,
                    "previous_close": previous_close,
                    "change": change,
                    "change_percent": change_percent,
                    "name": stock.name,
                })
            except Exception as e:
                print(f"Error: {str(e)}")
                portfolio_data.append({
                    "ticker": stock.ticker,
                    "current_price": stock.buy_price,
                    "previous_close": stock.buy_price,
                    "change": "0.00",
                    "change_percent": "0.00%",
                    "name": stock.name,
                })

        return Response({
            "stocks": portfolio_data,
        }, status=status.HTTP_200_OK)

class RandomStockAPIView(APIView):
    """
    API endpoint to fetch random stock tickers with their real-time prices.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # List of stock tickers
        stock_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NFLX', 'META', 'NVDA', 'BRK.B', 'V']
        random_tickers = random.sample(stock_tickers, 1)  # Pick 5 random tickers
        # print("Fetching from the random tickers:", random_tickers)
        print("Fetching from the random tickers:", 'NVDA')

        stocks = []
        for ticker in random_tickers:
            # price_data = get_real_price(ticker)  # Get full response dictionary
            price_data = {'Global Quote': {'01. symbol': 'NVDA', '02. open': '133.6500', '03. high': '136.4500', '04. low': '131.2900', '05. price': '136.2400', '06. volume': '185217338', '07. latest trading day': '2025-01-15', '08. previous close': '131.7600', '09. change': '4.4800', '10. change percent': '3.4001%'}}
            print("Fetching from the API", price_data)

            if price_data and 'Global Quote' in price_data:
                global_quote = price_data['Global Quote']
                stock = {
                    'ticker': global_quote.get('01. symbol', ticker),
                    'current_price': float(global_quote.get('05. price', 0)),
                    'previous_close': float(global_quote.get('08. previous close', 0)),
                    'change': global_quote.get('09. change', 'N/A'),
                    'change_percent': global_quote.get('10. change percent', 'N/A'),
                }
                stocks.append(stock)
                print(stocks)
            else:
                print(f"Invalid data for ticker {ticker}: {price_data}")

        return Response(stocks, status=status.HTTP_200_OK)

