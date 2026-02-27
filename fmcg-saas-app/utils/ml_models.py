"""
ML Models Integration Template
YOUR MODELS GO HERE - Replace with your Prophet and XGBoost implementations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DemandForecaster:
    """
    Demand Forecasting Model
    REPLACE THIS with your Prophet + LSTM implementation
    """
    
    def __init__(self):
        self.model = None
        self.is_trained = False
    
    def train(self, sales_data: pd.DataFrame):
        """
        Train the forecasting model
        
        Args:
            sales_data: DataFrame with columns [date, product_id, quantity]
        """
        # YOUR PROPHET/LSTM TRAINING CODE HERE
        print("Training demand forecasting model...")
        self.is_trained = True
        return True
    
    def predict(self, product_id: str, days_ahead: int = 30):
        """
        Generate demand forecast
        
        Args:
            product_id: Product to forecast
            days_ahead: Number of days to forecast
            
        Returns:
            DataFrame with [date, predicted_demand, lower_bound, upper_bound]
        """
        # YOUR PREDICTION CODE HERE
        dates = pd.date_range(start=datetime.now(), periods=days_ahead, freq='D')
        
        # Mock predictions - REPLACE THIS
        predictions = [100 + i*2.5 + np.random.randn()*5 for i in range(days_ahead)]
        
        return pd.DataFrame({
            'date': dates,
            'predicted_demand': predictions,
            'lower_bound': [p * 0.9 for p in predictions],
            'upper_bound': [p * 1.1 for p in predictions],
        })
    
    def get_accuracy_metrics(self):
        """Return model accuracy metrics"""
        # YOUR ACCURACY CALCULATION HERE
        return {
            'mape': 8.0,
            'accuracy': 92.0,
            'rmse': 12.5
        }


class InventoryOptimizer:
    """
    Inventory Optimization Model
    REPLACE THIS with your XGBoost implementation
    """
    
    def __init__(self):
        self.model = None
        self.is_trained = False
    
    def train(self, inventory_data: pd.DataFrame, sales_data: pd.DataFrame):
        """
        Train the inventory optimization model
        
        Args:
            inventory_data: Current inventory levels
            sales_data: Historical sales data
        """
        # YOUR XGBOOST TRAINING CODE HERE
        print("Training inventory optimization model...")
        self.is_trained = True
        return True
    
    def calculate_reorder_points(self, product_id: str):
        """
        Calculate optimal reorder point and safety stock
        
        Args:
            product_id: Product to optimize
            
        Returns:
            Dict with reorder_point, safety_stock, suggested_order_quantity
        """
        # YOUR OPTIMIZATION CODE HERE
        
        # Mock results - REPLACE THIS
        return {
            'product_id': product_id,
            'current_stock': 45,
            'reorder_point': 100,
            'safety_stock': 30,
            'suggested_order_quantity': 500,
            'days_until_stockout': 3,
            'confidence': 0.89
        }
    
    def get_stockout_alerts(self, inventory_df: pd.DataFrame):
        """
        Get list of products at risk of stockout
        
        Args:
            inventory_df: Current inventory DataFrame
            
        Returns:
            List of products with stockout risk
        """
        # YOUR ALERT LOGIC HERE
        
        # Mock alerts - REPLACE THIS
        return [
            {'product_id': 'SKU-123', 'warehouse': 'Delhi', 'current_stock': 5, 'days_until_stockout': 2},
            {'product_id': 'SKU-456', 'warehouse': 'Mumbai', 'current_stock': 0, 'days_until_stockout': 0},
        ]


# Singleton instances
demand_forecaster = DemandForecaster()
inventory_optimizer = InventoryOptimizer()
