from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import fields, pre_dump
from ..consts import TIME_ZONE
ma = Marshmallow()

class BaseSchema(ma.Schema):
    def __init__(self, *args, **kwargs):
        self.custom_format = kwargs.pop('custom_format', 'default')
        super().__init__(*args, **kwargs)
    
    def _adjust_timezone_not_object(self, data):
        last_update_str = data.get('last_update')
        if last_update_str:
            last_update = datetime.fromisoformat(data['last_update']).astimezone(TIME_ZONE)
            if self.custom_format == 'iso':
                data['last_update'] = last_update.isoformat()
            elif self.custom_format == 'timestamp':
                data['last_update'] = last_update.timestamp()
            else:
                data['last_update'] = last_update.strftime('%d/%m/%Y, %I:%M %p')
        return data
    
    def _adjust_timezone_object(self, data): 
        if hasattr(data, 'last_update') and data.last_update:
            last_update = data.last_update.astimezone(TIME_ZONE)
            data.last_update = last_update.isoformat()
        
        if hasattr(data, 'created_at') and data.created_at:
            created_at = data.created_at.astimezone(TIME_ZONE)
            data.created_at = created_at.isoformat()
        return data

    @pre_dump
    def adjust_timezone(self, data, **kwargs):
        if isinstance(data, dict):
            return self._adjust_timezone_not_object(data)
        return self._adjust_timezone_object(data)

class UserSchema(BaseSchema):
    class Meta:
        fields = ("id", "name", "token", "is_premium", "created_at")

class MonitorSchema(BaseSchema):
    last_update = fields.String()
    price_old = fields.Float(missing=0.0, allow_none=True, default=0.0)
    
    class Meta:
        fields = ("key", "title", "price", "price_old", "last_update", "image", "percent", "change", "color", "symbol")

class HistoryPriceSchema(BaseSchema):
    last_update = fields.String()
    
    class Meta:
        fields = ("price", "price_high", "price_low", "last_update")

class DailyChangeSchema(BaseSchema):
    last_update = fields.String()
    
    class Meta:
        fields = ("price", "last_update")

class MonitorsWebhooksSchema(ma.Schema):

    class Meta:
        fields = ("monitor_id", )

class WebhookSchema(BaseSchema):
    monitors = fields.Nested(MonitorsWebhooksSchema, many=True)
    class Meta:
        fields = ("id", "url", "token", "certificate_ssl", "status", "monitors", "created_at")

