from django.apps import AppConfig


class AgentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agents'

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List, Optional

@dataclass
class AppVO:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    avatar: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    rating: Optional[float] = None
    downloads: Optional[int] = None
    reviews: Optional[int] = None
    author: Optional[str] = None
    published_at: Optional[date] = None
    tags: Optional[List[str]] = None
    features: Optional[List[str]] = None
    scenarios: Optional[List[str]] = None