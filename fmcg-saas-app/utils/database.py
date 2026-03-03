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
    contact_name = Column(String(255))
    services = Column(Text)  # JSON string of selected services
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserLogin(Base):
    """Track login events."""
    __tablename__ = "user_logins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    email = Column(String(255))
    login_type = Column(String(50))  # signup, login
    logged_at = Column(DateTime, default=datetime.utcnow)


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
    diagnostics = Column(Text)  # JSON string


class ChatMessage(Base):
    """Store chatbot conversation messages."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)


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
            connect_args = {}
            if "supabase" in self.database_url or "neon" in self.database_url:
                connect_args = {"sslmode": "require"}

            self.engine = create_engine(
                self.database_url,
                poolclass=NullPool,
                connect_args=connect_args,
            )
            self.Session = sessionmaker(bind=self.engine)
            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"Database initialization failed: {e}")
            self.engine = None
            self.Session = None

    def is_connected(self) -> bool:
        """Check if database is connected, attempt re-initialization if not."""
        if self.engine is None or self.Session is None:
            # Refresh standard DATABASE_URL from environment
            self.database_url = os.getenv("DATABASE_URL", "").strip()
            if self.database_url:
                self._initialize()
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
                existing.contact_name = company_data.get("contact_name")
                existing.services = json.dumps(company_data.get("services", []))
                existing.updated_at = datetime.utcnow()
            else:
                company = Company(
                    company_name=company_data["company_name"],
                    industry=company_data.get("industry", "FMCG"),
                    contact_email=company_data.get("contact_email"),
                    contact_phone=company_data.get("contact_phone"),
                    contact_name=company_data.get("contact_name"),
                    services=json.dumps(company_data.get("services", []))
                )
                session.add(company)

            session.commit()
            session.close()
            return True
        except Exception as e:
            print(f"Error saving company: {e}")
            return False

    # Alias for backward compatibility with settings page
    def upsert_company(self, company_name: str, contact_name: str, email: str,
                       phone: str, industry: str) -> Optional[Company]:
        """Upsert a company record. Returns the company object or None."""
        data = {
            "company_name": company_name,
            "industry": industry,
            "contact_email": email,
            "contact_phone": phone,
            "contact_name": contact_name,
        }
        success = self.save_company(data)
        if success:
            return self.get_company_obj(company_name)
        return None

    def get_company(self, company_name: str) -> Optional[Dict]:
        """Retrieve company information as a dict."""
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
                    "contact_name": company.contact_name,
                    "services": json.loads(company.services) if company.services else [],
                    "created_at": company.created_at,
                    "updated_at": company.updated_at,
                }
            return None
        except Exception as e:
            print(f"Error retrieving company: {e}")
            return None

    def get_company_obj(self, company_name: str) -> Optional[Company]:
        """Retrieve the raw Company ORM object."""
        if not self.is_connected():
            return None
        try:
            session = self.Session()
            company = session.query(Company).filter_by(company_name=company_name).first()
            session.close()
            return company
        except Exception:
            return None

    def save_login_event(self, company_name: str, email: str = "", login_type: str = "login") -> bool:
        """Record a login/signup event."""
        if not self.is_connected():
            return False
        try:
            session = self.Session()
            login = UserLogin(
                company_name=company_name,
                email=email,
                login_type=login_type,
            )
            session.add(login)
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(f"Error saving login event: {e}")
            return False

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
                model_type=forecast_data.get("model_type", "prophet"),
                diagnostics=json.dumps(forecast_data.get("diagnostics", {})),
            )
            session.add(forecast)
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(f"Error saving forecast: {e}")
            return False

    def save_chat_message(self, company_name: str, role: str, content: str) -> bool:
        """Save a single chat message."""
        if not self.is_connected():
            return False
        try:
            session = self.Session()
            msg = ChatMessage(
                company_name=company_name,
                role=role,
                content=content,
            )
            session.add(msg)
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(f"Error saving chat message: {e}")
            return False

    def get_chat_history(self, company_name: str, limit: int = 50) -> List[Dict]:
        """Retrieve recent chat messages for a company."""
        if not self.is_connected():
            return []
        try:
            session = self.Session()
            messages = (
                session.query(ChatMessage)
                .filter_by(company_name=company_name)
                .order_by(ChatMessage.sent_at.desc())
                .limit(limit)
                .all()
            )
            session.close()
            result = [
                {"role": m.role, "content": m.content, "sent_at": m.sent_at.isoformat()}
                for m in reversed(messages)
            ]
            return result
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            return []

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
