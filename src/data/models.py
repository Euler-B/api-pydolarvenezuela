from sqlalchemy import (
    Column, 
    Integer, 
    Float, 
    String, 
    DateTime, 
    Boolean, 
    ForeignKey
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'

    id   = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url  = Column(String, nullable=False)

class Currency(Base):
    __tablename__ = 'currencies'

    id   = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)

class Monitor(Base):
    __tablename__ = 'monitors'

    id          = Column(Integer, primary_key=True)
    page_id     = Column(Integer, ForeignKey('pages.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    key         = Column(String, nullable=True)
    title       = Column(String, nullable=False)
    price       = Column(Float, nullable=False)
    price_old   = Column(Float, nullable=True)
    last_update = Column(DateTime(timezone=True), nullable=False)
    image       = Column(String, nullable=True)
    percent     = Column(Float, nullable=True, default=0.0)
    change      = Column(Float, nullable=True, default=0.0)
    color       = Column(String, nullable=True, default="neutral")
    symbol      = Column(String, nullable=True, default="")

class MonitorPriceHistory(Base):
    __tablename__ = 'monitor_price_history'

    id          = Column(Integer, primary_key=True)
    monitor_id  = Column(Integer, ForeignKey('monitors.id'), nullable=False)
    price       = Column(Float, nullable=False)
    last_update = Column(DateTime(timezone=True), nullable=False)

class User(Base):
    __tablename__ = 'users'

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    token           = Column(String(64), nullable=False)
    is_premium      = Column(Boolean, default=False)
    created_at      = Column(DateTime, nullable=False)

    webhooks = relationship("Webhook", back_populates="user")

class UserPetition(Base):
    __tablename__ = 'user_petitions'

    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer, ForeignKey('users.id'), nullable=False)
    path            = Column(String, nullable=False)
    total_petitions = Column(Integer, nullable=False)
    created_at      = Column(DateTime, nullable=False)

class Webhook(Base):
    __tablename__ = 'webhooks'

    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer, ForeignKey('users.id'), nullable=False)
    url             = Column(String, nullable=False)
    token           = Column(String, nullable=False)
    certificate_ssl = Column(Boolean, default=False)
    status          = Column(Boolean, default=True)
    created_at      = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="webhooks")
    monitors = relationship("MonitorsWebhooks", back_populates="webhook")

class MonitorsWebhooks(Base):
    __tablename__ = 'monitors_webhooks'

    webhook_id      = Column(Integer, ForeignKey('webhooks.id'), primary_key=True)
    monitor_id      = Column(Integer, ForeignKey('monitors.id'), primary_key=True)

    webhook = relationship("Webhook", back_populates="monitors")