from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    browser = db.Column(db.String(100), nullable=True)
    browser_version = db.Column(db.String(100), nullable=True)
    os = db.Column(db.String(100), nullable=True)
    os_version = db.Column(db.String(100), nullable=True)
    device_type = db.Column(db.String(50), nullable=True)
    device_memory = db.Column(db.String(20), nullable=True)
    hardware_concurrency = db.Column(db.String(20), nullable=True)
    screen_resolution = db.Column(db.String(50), nullable=True)
    viewport_size = db.Column(db.String(50), nullable=True)
    color_depth = db.Column(db.String(20), nullable=True)
    timezone = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(50), nullable=True)
    platform = db.Column(db.String(100), nullable=True)
    do_not_track = db.Column(db.String(10), nullable=True)
    cookies_enabled = db.Column(db.Boolean, nullable=True)
    local_storage_available = db.Column(db.Boolean, nullable=True)
    session_storage_available = db.Column(db.Boolean, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    country = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    connection_type = db.Column(db.String(50), nullable=True)
    isp = db.Column(db.String(100), nullable=True)
    referrer = db.Column(db.Text, nullable=True)
    visit_time = db.Column(db.DateTime, default=datetime.utcnow)
    canvas_fingerprint = db.Column(db.Text, nullable=True)
    webgl_fingerprint = db.Column(db.Text, nullable=True)
    audio_fingerprint = db.Column(db.Text, nullable=True)
    fonts = db.Column(db.Text, nullable=True)
    plugins = db.Column(db.Text, nullable=True)
    touch_support = db.Column(db.Boolean, nullable=True)
    battery_level = db.Column(db.Float, nullable=True)
    battery_charging = db.Column(db.Boolean, nullable=True)
    
    def __repr__(self):
        return f'<Visitor {self.id} - {self.ip_address}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'browser': self.browser,
            'browser_version': self.browser_version,
            'os': self.os,
            'os_version': self.os_version,
            'device_type': self.device_type,
            'device_memory': self.device_memory,
            'hardware_concurrency': self.hardware_concurrency,
            'screen_resolution': self.screen_resolution,
            'viewport_size': self.viewport_size,
            'color_depth': self.color_depth,
            'timezone': self.timezone,
            'language': self.language,
            'platform': self.platform,
            'do_not_track': self.do_not_track,
            'cookies_enabled': self.cookies_enabled,
            'local_storage_available': self.local_storage_available,
            'session_storage_available': self.session_storage_available,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'country': self.country,
            'region': self.region,
            'city': self.city,
            'connection_type': self.connection_type,
            'isp': self.isp,
            'referrer': self.referrer,
            'visit_time': self.visit_time.strftime('%Y-%m-%d %H:%M:%S') if self.visit_time else None,
            'canvas_fingerprint': self.canvas_fingerprint,
            'webgl_fingerprint': self.webgl_fingerprint,
            'audio_fingerprint': self.audio_fingerprint,
            'fonts': self.fonts,
            'plugins': self.plugins,
            'touch_support': self.touch_support,
            'battery_level': self.battery_level,
            'battery_charging': self.battery_charging
        }
