"""Enhanced chatbot integration using Groq with real data context."""

from __future__ import annotations

import os
from typing import Dict, List, Optional
import json

from groq import Groq


class ChatbotService:
    """Groq integration with data-driven responses."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def get_response(
        self,
        user_query: str,
        company_data: Optional[Dict] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Return assistant response from Groq API with real data context."""
        if not self.client:
            self.api_key = os.getenv("GROQ_API_KEY", "").strip()
            if self.api_key:
                try:
                    self.client = Groq(api_key=self.api_key)
                except Exception as e:
                    print(f"Failed to initialize Groq client: {e}")
            
        if not self.client:
            return self._fallback_response(user_query, company_data)

        try:
            messages = self._build_messages(user_query, company_data, history or [])
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=800,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip()
        except Exception as e:
            print(f"Groq API error: {e}")
            return self._fallback_response(user_query, company_data)
        return self._fallback_response(user_query, company_data)

    def _build_messages(
        self,
        user_query: str,
        company_data: Optional[Dict],
        history: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """Build message context with rich company data."""
        context = self._build_context(company_data)
        
        system_prompt = f"""You are an expert FMCG analytics assistant for {company_data.get('company_name', 'the company') if company_data else 'the company'}.

Your role:
- Provide actionable insights based on the actual data provided
- Be specific with numbers and metrics from the context
- Recommend concrete actions for inventory, forecasting, and operations
- Explain trends and patterns you observe in the data
- Be concise but thorough (3-5 sentences typically)

CRITICAL RULES:
- ONLY use data from the context provided below
- If data is not available, clearly state that
- Never invent or hallucinate numbers
- Reference specific products, regions, and metrics when available
- Provide practical recommendations based on the data

{context}"""

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]

        # Add conversation history (last 6 exchanges)
        for msg in history[-12:]:
            role = msg.get("role", "")
            if role not in {"user", "assistant"}:
                continue
            messages.append({"role": role, "content": msg.get("content", "")})

        messages.append({"role": "user", "content": user_query})
        return messages

    def _build_context(self, company_data: Optional[Dict]) -> str:
        """Build rich context from company data."""
        if not company_data:
            return "No company data available yet. Please upload data first."

        kpis = company_data.get("kpis", {})
        insights = company_data.get("insights", [])
        top_regions = company_data.get("top_regions", [])
        alerts = company_data.get("alerts", [])
        
        context_parts = [
            f"\n=== COMPANY CONTEXT ===",
            f"Company: {company_data.get('company_name', 'Unknown')}",
            f"Industry: {company_data.get('industry', 'FMCG')}",
            f"Dataset Size: {company_data.get('rows', 0):,} orders",
            f"\n=== KEY METRICS ===",
            f"Total Revenue: ${kpis.get('total_revenue', 0):,.2f}",
            f"Active Products: {kpis.get('active_products', 0)}",
            f"Stockout Alerts: {kpis.get('stockout_alerts', 0)}",
            f"Forecast Accuracy: {kpis.get('forecast_accuracy', 0)}%",
        ]
        
        if top_regions:
            context_parts.append(f"\n=== TOP REGIONS BY DEMAND ===")
            for i, region in enumerate(top_regions[:5], 1):
                context_parts.append(
                    f"{i}. {region.get('region', 'Unknown')}: "
                    f"{region.get('total_quantity', 0):,.0f} units, "
                    f"${region.get('total_revenue', 0):,.2f} revenue"
                )
        
        if alerts:
            context_parts.append(f"\n=== ACTIVE ALERTS ===")
            for alert in alerts[:5]:
                context_parts.append(
                    f"[{alert.get('severity', 'info').upper()}] "
                    f"{alert.get('title', '')}: {alert.get('message', '')}"
                )
        
        if insights:
            context_parts.append(f"\n=== KEY INSIGHTS ===")
            for insight in insights[:5]:
                context_parts.append(f"• {insight}")
        
        # Add inventory summary if available
        inventory = company_data.get("inventory", {})
        if inventory:
            cards = inventory.get("cards", {})
            if cards:
                context_parts.append(f"\n=== INVENTORY STATUS ===")
                context_parts.append(f"Optimal Stock: {cards.get('optimal', 0)} products")
                context_parts.append(f"Low Stock: {cards.get('low_stock', 0)} products")
                context_parts.append(f"Stockout Risk: {cards.get('stockout', 0)} products")
                context_parts.append(f"Overstock: {cards.get('overstock', 0)} products")
        
        return "\n".join(context_parts)

    def _fallback_response(self, query: str, company_data: Optional[Dict]) -> str:
        """Enhanced fallback response with actual data when API unavailable."""
        query_lower = query.lower()
        
        if not company_data:
            return (
                "I need data to provide insights. Please upload your sales data first, "
                "then I can analyze inventory, forecasts, and provide recommendations."
            )
        
        kpis = company_data.get("kpis", {})
        insights = company_data.get("insights", [])
        
        # Stock/Inventory queries
        if any(word in query_lower for word in ["stock", "inventory", "reorder"]):
            stockout_count = kpis.get("stockout_alerts", 0)
            if stockout_count > 0:
                return (
                    f"You have {stockout_count} products at stockout risk. "
                    f"Check the Inventory page for specific reorder recommendations. "
                    f"Note: Add GROQ_API_KEY for detailed AI analysis."
                )
            return (
                "Your inventory levels look stable. No immediate stockout risks detected. "
                "Add GROQ_API_KEY for detailed inventory optimization insights."
            )
        
        # Forecast queries
        if any(word in query_lower for word in ["forecast", "demand", "predict", "future"]):
            accuracy = kpis.get("forecast_accuracy", 0)
            if insights:
                return (
                    f"Current forecast confidence: {accuracy}%. {insights[0]} "
                    f"Visit the Forecasting page for detailed predictions. "
                    f"Add GROQ_API_KEY for AI-powered demand analysis."
                )
            return (
                f"Forecast accuracy is {accuracy}%. Check the Forecasting page for "
                f"product-specific predictions. Add GROQ_API_KEY for deeper insights."
            )
        
        # Revenue/Sales queries
        if any(word in query_lower for word in ["revenue", "sales", "performance"]):
            revenue = kpis.get("total_revenue", 0)
            products = kpis.get("active_products", 0)
            return (
                f"Total revenue: ${revenue:,.2f} across {products} active products. "
                f"Add GROQ_API_KEY for detailed sales analysis and recommendations."
            )
        
        # General query
        if insights:
            return (
                f"Key insight: {insights[0]} "
                f"Add GROQ_API_KEY to unlock full conversational analytics with AI-powered insights."
            )
        
        return (
            "I can analyze your FMCG data for inventory optimization, demand forecasting, "
            "and sales insights. Add GROQ_API_KEY to enable full AI-powered analytics. "
            "Try asking about specific products, regions, or inventory status."
        )


chatbot_service = ChatbotService()
