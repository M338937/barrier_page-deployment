from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
import json
from src.models.visitor import db, Visitor
from functools import wraps
import datetime
import pandas as pd
import os

admin_bp = Blueprint('admin', __name__)

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# Rate limiting decorator
def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.remote_addr
        current_time = datetime.datetime.now()
        
        # Check if IP is in session
        if 'rate_limit' not in session:
            session['rate_limit'] = {}
        
        if ip in session['rate_limit']:
            last_attempt, attempts = session['rate_limit'][ip]
            last_attempt = datetime.datetime.fromisoformat(last_attempt)
            
            # Reset attempts if more than 15 minutes have passed
            if (current_time - last_attempt).total_seconds() > 900:
                session['rate_limit'][ip] = (current_time.isoformat(), 1)
            # Block if more than 5 attempts in 15 minutes
            elif attempts >= 5:
                flash('Too many login attempts. Please try again later.', 'danger')
                return redirect(url_for('admin.login'))
            # Increment attempts
            else:
                session['rate_limit'][ip] = (last_attempt.isoformat(), attempts + 1)
        else:
            session['rate_limit'][ip] = (current_time.isoformat(), 1)
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
@rate_limit
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            session['last_activity'] = datetime.datetime.now().isoformat()
            return redirect(url_for('admin.dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template('login.html', error=error)

@admin_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('last_activity', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Check session timeout (30 minutes)
    if 'last_activity' in session:
        last_activity = datetime.datetime.fromisoformat(session['last_activity'])
        if (datetime.datetime.now() - last_activity).total_seconds() > 1800:
            session.pop('logged_in', None)
            flash('Session expired. Please log in again.', 'warning')
            return redirect(url_for('admin.login'))
        else:
            session['last_activity'] = datetime.datetime.now().isoformat()
    
    # Get visitor count
    visitor_count = Visitor.query.count()
    
    # Get recent visitors (last 10)
    recent_visitors = Visitor.query.order_by(Visitor.visit_time.desc()).limit(10).all()
    
    # Get visitor count by browser
    browser_stats = db.session.query(
        Visitor.browser, 
        db.func.count(Visitor.id).label('count')
    ).group_by(Visitor.browser).all()
    
    # Get visitor count by OS
    os_stats = db.session.query(
        Visitor.os, 
        db.func.count(Visitor.id).label('count')
    ).group_by(Visitor.os).all()
    
    # Get visitor count by device type
    device_stats = db.session.query(
        Visitor.device_type, 
        db.func.count(Visitor.id).label('count')
    ).group_by(Visitor.device_type).all()
    
    # Get visitor count by country
    country_stats = db.session.query(
        Visitor.country, 
        db.func.count(Visitor.id).label('count')
    ).group_by(Visitor.country).all()
    
    # Get visitor count by day
    day_stats = db.session.query(
        db.func.date(Visitor.visit_time).label('day'),
        db.func.count(Visitor.id).label('count')
    ).group_by('day').order_by('day').all()
    
    # Get visitor count by hour
    hour_stats = db.session.query(
        db.func.extract('hour', Visitor.visit_time).label('hour'),
        db.func.count(Visitor.id).label('count')
    ).group_by('hour').order_by('hour').all()
    
    # Format data for charts
    browser_labels = [b[0] if b[0] else 'Unknown' for b in browser_stats]
    browser_data = [b[1] for b in browser_stats]
    
    os_labels = [o[0] if o[0] else 'Unknown' for o in os_stats]
    os_data = [o[1] for o in os_stats]
    
    device_labels = [d[0] if d[0] else 'Unknown' for d in device_stats]
    device_data = [d[1] for d in device_stats]
    
    country_labels = [c[0] if c[0] else 'Unknown' for c in country_stats]
    country_data = [c[1] for c in country_stats]
    
    day_labels = [str(d[0]) for d in day_stats]
    day_data = [d[1] for d in day_stats]
    
    hour_labels = [str(h[0]) for h in hour_stats]
    hour_data = [h[1] for h in hour_stats]
    
    return render_template(
        'dashboard.html',
        visitor_count=visitor_count,
        recent_visitors=recent_visitors,
        browser_labels=json.dumps(browser_labels),
        browser_data=json.dumps(browser_data),
        os_labels=json.dumps(os_labels),
        os_data=json.dumps(os_data),
        device_labels=json.dumps(device_labels),
        device_data=json.dumps(device_data),
        country_labels=json.dumps(country_labels),
        country_data=json.dumps(country_data),
        day_labels=json.dumps(day_labels),
        day_data=json.dumps(day_data),
        hour_labels=json.dumps(hour_labels),
        hour_data=json.dumps(hour_data)
    )

@admin_bp.route('/visitors')
@login_required
def visitors():
    # Check session timeout
    if 'last_activity' in session:
        last_activity = datetime.datetime.fromisoformat(session['last_activity'])
        if (datetime.datetime.now() - last_activity).total_seconds() > 1800:
            session.pop('logged_in', None)
            flash('Session expired. Please log in again.', 'warning')
            return redirect(url_for('admin.login'))
        else:
            session['last_activity'] = datetime.datetime.now().isoformat()
    
    # Get all visitors
    visitors = Visitor.query.order_by(Visitor.visit_time.desc()).all()
    
    return render_template('visitors.html', visitors=visitors)

@admin_bp.route('/visitor/<int:visitor_id>')
@login_required
def visitor_detail(visitor_id):
    # Check session timeout
    if 'last_activity' in session:
        last_activity = datetime.datetime.fromisoformat(session['last_activity'])
        if (datetime.datetime.now() - last_activity).total_seconds() > 1800:
            session.pop('logged_in', None)
            flash('Session expired. Please log in again.', 'warning')
            return redirect(url_for('admin.login'))
        else:
            session['last_activity'] = datetime.datetime.now().isoformat()
    
    # Get visitor by ID
    visitor = Visitor.query.get_or_404(visitor_id)
    
    # Parse JSON fields
    try:
        fonts = json.loads(visitor.fonts) if visitor.fonts else []
    except:
        fonts = []
    
    try:
        plugins = json.loads(visitor.plugins) if visitor.plugins else []
    except:
        plugins = []
    
    return render_template('visitor_detail.html', visitor=visitor, fonts=fonts, plugins=plugins)

@admin_bp.route('/export', methods=['GET'])
@login_required
def export_data():
    # Check session timeout
    if 'last_activity' in session:
        last_activity = datetime.datetime.fromisoformat(session['last_activity'])
        if (datetime.datetime.now() - last_activity).total_seconds() > 1800:
            session.pop('logged_in', None)
            flash('Session expired. Please log in again.', 'warning')
            return redirect(url_for('admin.login'))
        else:
            session['last_activity'] = datetime.datetime.now().isoformat()
    
    format_type = request.args.get('format', 'csv')
    
    # Get all visitors
    visitors = Visitor.query.all()
    
    # Convert to list of dictionaries
    visitor_data = [v.to_dict() for v in visitors]
    
    # Create DataFrame
    df = pd.DataFrame(visitor_data)
    
    # Create export directory if it doesn't exist
    export_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'exports')
    os.makedirs(export_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format_type == 'csv':
        filename = f'visitor_data_{timestamp}.csv'
        filepath = os.path.join(export_dir, filename)
        df.to_csv(filepath, index=False)
    elif format_type == 'excel':
        filename = f'visitor_data_{timestamp}.xlsx'
        filepath = os.path.join(export_dir, filename)
        df.to_excel(filepath, index=False)
    elif format_type == 'json':
        filename = f'visitor_data_{timestamp}.json'
        filepath = os.path.join(export_dir, filename)
        df.to_json(filepath, orient='records')
    else:
        return jsonify({'error': 'Invalid format type'}), 400
    
    # Return file download URL
    download_url = url_for('static', filename=f'exports/{filename}')
    return redirect(download_url)
