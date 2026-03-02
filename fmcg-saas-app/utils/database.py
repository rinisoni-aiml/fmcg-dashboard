"""Database integration with Supabase PostgreSQL."""

import os
from datetime import datetime
from typing import Dict, Optional, List
import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()


class Company(Base):
    """Company model for storing onboarding data."""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False, unique=True)
    industry = Column(String(100), default="FMCG")
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    services = Column(Text)  # JSON string of selected services
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ForecastHistory(Base):
    """Store forecast results for historical tracking."""
    __tablename__ = "forecast_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    product_id = Column(String(100))
    region = Column(String(100))
    forecast_date = Column(DateTime, default=datetime.utcnow)
    horizon_days = Column(Integer)
    forecast_data = Column(Text)  # JSON string
    confidence_level = Column(Float)
    model_type = Column(String(50), default="prophet")


class InventoryAlert(Base):
    """Store inventory alerts and recommendations."""
    __tablename__ = "inventory_alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    product_id = Column(String(100), nullable=False)
    warehouse_id = Column(String(100))
    alert_type = Column(String(50))  # stockout, overstock, reorder
    current_stock = Column(Float)
    recommended_action = Column(Text)
    priority = Column(String(20))  # high, medium, low
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


class DatabaseService:
    """Database service for managing connections and operations."""

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "").strip()
        self.engine = None
        self.Session = None
        self._initialize()

    def _initialize(self):
        """Initialize database connection."""
        if not self.database_url:
            return

        try:
            # For Supabase/Neon, use NullPool to avoid connection issues
            self.engine = create_engine(
                self.database_url,
                poolclass=NullPool,
                connect_args={"sslmode": "require"} if "supabase" in self.database_url or "neon" in self.database_url else {}
            )
            self.Session = sessionmaker(bind=self.engine)
            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"Database initialization failed: {e}")
            self.engine = None
            self.Session = None

    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self.engine is not None and self.Session is not None

    def save_company(self, company_data: Dict) -> bool:
        """Save or update company information."""
        if not self.is_connected():
            return False

        try:
            session = self.Session()
            existing = session.query(Company).filter_by(
                company_name=company_data["company_name"]
            ).first()

            if existing:
                existing.industry = company_data.get("industry", "FMCG")
                existing.contact_email = company_data.get("contact_email")
                existing.contact_phone = company_data.get("contact_phone")
                existing.services = json.dumps(company_data.get("services", []))
                existing.updated_at = datetime.utcnow()
            else:
                company = Company(
                    company_name=company_data["company_name"],
                    industry=company_data.get("industry", "FMCG"),
                    contact_email=company_data.get("contact_email"),
                    contact_phone=company_data.get("contact_phone"),
                    services=json.dumps(company_data.get("services", []))
                )
                session.add(company)

            session.commit()
            session.close()
            return True
        except Exception as e:
            print(f"Error saving company: {e}")
            return False

    def get_company(self, company_name: str) -> Optional[Dict]:
        """Retrieve company information."""
        if not self.is_connected():
            return None

        try:
            session = self.Session()
            company = session.query(Company).filter_by(company_name=company_name).first()
            session.close()

            if company:
                return {
                    "id": company.id,
                    "company_name": company.company_name,
                    "industry": company.industry,
                    "contact_email": company.contact_email,
                    "contact_phone": company.contact_phone,
                    "services": json.loads(company.services) if company.services else [],
                    "created_at": company.created_at,
                    "updated_at": company.updated_at
                }
            return None
        except Exception as e:
            print(f"Error retrieving company: {e}")
            return None

    def save_forecast(self, forecast_data: Dict) -> bool:
        """Save forecast results."""
        if not self.is_connected():
            return False

        try:
            session = self.Session()
            forecast = ForecastHistory(
                company_name=forecast_data["company_name"],
                product_id=forecast_data.get("product_id"),
                region=forecast_data.get("region"),
                horizon_days=forecast_data["horizon_days"],
                forecast_data=json.dumps(forecast_data["forecast"]),
                confidence_level=forecast_data.get("confidence_level", 0.0),
                model_type=forecast_data.get("model_type", "prophet")
            )
            session.add(forecast)
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(f"Error saving forecast: {e}")
            return False

    def save_inventory_alert(self, alert_data: Dict) -> bool:
        """Save inventory alert."""
        if not self.is_connected():
            return False

        try:
            session = self.Session()
            alert = InventoryAlert(
                company_name=alert_data["company_name"],
                product_id=alert_data["product_id"],
                warehouse_id=alert_data.get("warehouse_id"),
                alert_type=alert_data["alert_type"],
                current_stock=alert_data.get("current_stock", 0),
                recommended_action=alert_data.get("recommended_action", ""),
                priority=alert_data.get("priority", "medium")
            )
            session.add(alert)
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(f"Error saving alert: {e}")
            return False

    def get_active_alerts(self, company_name: str) -> List[Dict]:
        """Get active inventory alerts for a company."""
        if not self.is_connected():
            return []

        try:
            session = self.Session()
            alerts = session.query(InventoryAlert).filter_by(
                company_name=company_name,
                is_resolved=False
            ).order_by(InventoryAlert.created_at.desc()).limit(50).all()
            session.close()

            return [{
                "id": alert.id,
                "product_id": alert.product_id,
                "warehouse_id": alert.warehouse_id,
                "alert_type": alert.alert_type,
                "current_stock": alert.current_stock,
                "recommended_action": alert.recommended_action,
                "priority": alert.priority,
                "created_at": alert.created_at
            } for alert in alerts]
        except Exception as e:
            print(f"Error retrieving alerts: {e}")
            return []


# Singleton instance
db_service = DatabaseService()
