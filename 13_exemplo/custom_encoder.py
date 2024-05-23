import json
from decimal import Decimal

class CustomEncoder(json.JSONDecoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        
        return json.JSONDecoder.default(self, obj)
    