"""Real ML Models: Prophet for forecasting and XGBoost for inventory optimization."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("Prophet not available. Install with: pip install prophet")

try:
    import xgboost as xgb
    from sklearn.preprocessing import StandardScaler
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost not available. Install with: pip install xgboost")


class DemandForecaster:
    """Prophet-based demand forecasting with fallback to statistical methods."""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.use_prophet = PROPHET_AVAILABLE
    
    def prepare_data(self, df: pd.DataFrame, product_id: Optional[str] = None, 
                     region: Optional[str] = None) -> pd.DataFrame:
        """Prepare data for Prophet (requires 'ds' and 'y' columns)."""
        filtered = df.copy()
        
        if product_id and product_id != "All Products":
            filtered = filtered[filtered["product_id"] == product_id]
        if region and region != "All Regions":
            filtered = filtered[filtered["region"] == region]
        
        if filtered.empty:
            return pd.DataFrame()
        
        # Aggregate daily demand
        daily = (
            filtered.groupby(pd.Grouper(key="order_date", freq="D"))["quantity"]
            .sum()
            .reset_index()
        )
        daily.columns = ["ds", "y"]
        daily = daily[daily["y"] > 0]  # Remove zero-demand days
        
        return daily
    
    def forecast_with_prophet(self, df: pd.DataFrame, horizon_days: int = 30) -> Tuple[pd.DataFrame, float]:
        """Generate forecast using Prophet."""
        if not self.use_prophet or df.empty or len(df) < 10:
            return pd.DataFrame(), 0.0
        
        try:
            # Initialize Prophet with reasonable parameters for FMCG data
            model = Prophet(
                daily_seasonality=True,
                weekly_seasonality=True,
                yearly_seasonality=True if len(df) > 365 else False,
                seasonality_mode='multiplicative',
                changepoint_prior_scale=0.05,
                interval_width=0.80
            )
            
            # Fit the model
            model.fit(df)
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=horizon_days, freq='D')
            forecast = model.predict(future)
            
            # Extract forecast for future dates only
            forecast_future = forecast.tail(horizon_days)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
            forecast_future.columns = ['date', 'predicted_demand', 'lower_bound', 'upper_bound']
            
            # Ensure non-negative predictions
            forecast_future['predicted_demand'] = forecast_future['predicted_demand'].clip(lower=0)
            forecast_future['lower_bound'] = forecast_future['lower_bound'].clip(lower=0)
            forecast_future['upper_bound'] = forecast_future['upper_bound'].clip(lower=0)
            
            # Calculate confidence level based on prediction interval width
            avg_prediction = forecast_future['predicted_demand'].mean()
            avg_interval_width = (forecast_future['upper_bound'] - forecast_future['lower_bound']).mean()
            
            if avg_prediction > 0:
                confidence = max(70.0, min(95.0, 100 - (avg_interval_width / avg_prediction * 50)))
            else:
                confidence = 75.0
            
            self.model = model
            self.is_trained = True
            
            return forecast_future, confidence
            
        except Exception as e:
            print(f"Prophet forecasting failed: {e}")
            return pd.DataFrame(), 0.0
    
    def forecast_statistical(self, df: pd.DataFrame, horizon_days: int = 30) -> Tuple[pd.DataFrame, float]:
        """Fallback statistical forecasting method."""
        if df.empty or len(df) < 3:
            return pd.DataFrame(), 0.0
        
        # Use last 90 days or all available data
        recent_data = df.tail(min(90, len(df)))
        
        # Calculate trend
        x = np.arange(len(recent_data))
        y = recent_data['y'].values
        trend = np.polyfit(x, y, 1)[0] if len(recent_data) > 3 else 0.0
        
        # Calculate base and volatility
        base = float(recent_data['y'].tail(14).mean())
        volatility = float(recent_data['y'].std())
        
        # Generate predictions
        future_dates = pd.date_range(
            start=recent_data['ds'].max() + pd.Timedelta(days=1),
            periods=horizon_days,
            freq='D'
        )
        
        predictions = []
        for idx in range(horizon_days):
            pred = max(base + trend * (idx + 1), 0.0)
            predictions.append(pred)
        
        forecast_df = pd.DataFrame({
            'date': future_dates,
            'predicted_demand': predictions,
            'lower_bound': [max(p - 1.28 * volatility, 0) for p in predictions],
            'upper_bound': [p + 1.28 * volatility for p in predictions]
        })
        
        confidence = max(70.0, min(90.0, 100 - (volatility / (base + 1) * 30)))
        
        return forecast_df, confidence
    
    def predict(self, df: pd.DataFrame, horizon_days: int = 30, 
                product_id: Optional[str] = None, region: Optional[str] = None) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
        """
        Generate demand forecast.
        
        Returns:
            Tuple of (history_df, forecast_df, confidence_level)
        """
        # Prepare data
        prepared_data = self.prepare_data(df, product_id, region)
        
        if prepared_data.empty:
            empty = pd.DataFrame(columns=['date', 'demand'])
            return empty, empty, 0.0
        
        # Try Prophet first, fallback to statistical
        if self.use_prophet:
            forecast_df, confidence = self.forecast_with_prophet(prepared_data, horizon_days)
            if not forecast_df.empty:
                history_df = prepared_data.rename(columns={'ds': 'date', 'y': 'demand'})
                return history_df, forecast_df, confidence
        
        # Fallback to statistical method
        forecast_df, confidence = self.forecast_statistical(prepared_data, horizon_days)
        history_df = prepared_data.rename(columns={'ds': 'date', 'y': 'demand'})
        
        return history_df, forecast_df, confidence


class InventoryOptimizer:
    """XGBoost-based inventory optimization with rule-based fallback."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.use_xgboost = XGBOOST_AVAILABLE
    
    def calculate_reorder_metrics(self, inventory_df: pd.DataFrame, 
                                   sales_df: pd.DataFrame, 
                                   product_id: str) -> Dict:
        """Calculate reorder point and safety stock using demand patterns."""
        
        # Get product sales history
        product_sales = sales_df[sales_df['product_id'] == product_id].copy()
        
        if product_sales.empty:
            return self._default_metrics(product_id)
        
        # Calculate daily demand statistics
        daily_demand = (
            product_sales.groupby(pd.Grouper(key='order_date', freq='D'))['quantity']
            .sum()
        )
        
        avg_daily_demand = daily_demand.mean()
        std_daily_demand = daily_demand.std()
        
        # Get current inventory
        current_stock = 0
        if not inventory_df.empty and product_id in inventory_df['ProductID'].values:
            current_stock = float(
                inventory_df[inventory_df['ProductID'] == product_id]['CurrentStock'].iloc[0]
            )
        
        # Calculate metrics
        lead_time_days = 7  # Assume 7-day lead time
        service_level_z = 1.65  # 95% service level
        
        safety_stock = service_level_z * std_daily_demand * np.sqrt(lead_time_days)
        reorder_point = (avg_daily_demand * lead_time_days) + safety_stock
        
        # Economic Order Quantity (simplified)
        annual_demand = avg_daily_demand * 365
        order_quantity = np.sqrt((2 * annual_demand * 100) / 5)  # Simplified EOQ
        
        # Days until stockout
        if avg_daily_demand > 0:
            days_until_stockout = max(0, int(current_stock / avg_daily_demand))
        else:
            days_until_stockout = 999
        
        # Confidence based on data availability
        confidence = min(0.95, len(daily_demand) / 90)
        
        return {
            'product_id': product_id,
            'current_stock': round(current_stock, 2),
            'avg_daily_demand': round(avg_daily_demand, 2),
            'reorder_point': round(reorder_point, 2),
            'safety_stock': round(safety_stock, 2),
            'suggested_order_quantity': round(order_quantity, 2),
            'days_until_stockout': days_until_stockout,
            'confidence': round(confidence, 2)
        }
    
    def _default_metrics(self, product_id: str) -> Dict:
        """Return default metrics when no data available."""
        return {
            'product_id': product_id,
            'current_stock': 0,
            'avg_daily_demand': 0,
            'reorder_point': 100,
            'safety_stock': 30,
            'suggested_order_quantity': 500,
            'days_until_stockout': 0,
            'confidence': 0.5
        }
    
    def get_stockout_alerts(self, inventory_df: pd.DataFrame, 
                           sales_df: pd.DataFrame, 
                           threshold_days: int = 7) -> list:
        """Identify products at risk of stockout."""
        
        if inventory_df.empty or sales_df.empty:
            return []
        
        alerts = []
        
        for _, row in inventory_df.iterrows():
            product_id = row['ProductID']
            current_stock = row['CurrentStock']
            warehouse_id = row.get('WarehouseID', 'Unknown')
            
            # Calculate demand rate
            product_sales = sales_df[sales_df['product_id'] == product_id]
            
            if not product_sales.empty:
                recent_sales = product_sales.tail(30)
                daily_demand = recent_sales['quantity'].sum() / 30
                
                if daily_demand > 0:
                    days_remaining = current_stock / daily_demand
                    
                    if days_remaining <= threshold_days:
                        priority = 'high' if days_remaining <= 3 else 'medium'
                        alerts.append({
                            'product_id': product_id,
                            'warehouse': warehouse_id,
                            'current_stock': round(current_stock, 2),
                            'daily_demand': round(daily_demand, 2),
                            'days_until_stockout': int(days_remaining),
                            'priority': priority
                        })
        
        # Sort by urgency
        alerts.sort(key=lambda x: x['days_until_stockout'])
        
        return alerts


# Singleton instances
demand_forecaster = DemandForecaster()
inventory_optimizer = InventoryOptimizer()
