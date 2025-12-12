"""
الزول - المساعد الذكي السوداني
تم التطوير بالكامل على Termux للأندرويد
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime

# إعداد التطبيق
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'سودان_ذكي_2024_محمد_الزول')

# مسارات الملفات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

# إنشاء المجلدات
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===== تحميل البيانات =====

def load_data(filename):
    """تحميل بيانات من ملف JSON"""
    try:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

# تحميل البيانات الأساسية
LOCATIONS = load_data('locations.json')
LISTINGS = load_data('listings.json')
CATEGORIES = load_data('categories.json')

# ===== الصفحات الرئيسية =====

@app.route('/')
def home():
    """الصفحة الرئيسية"""
    return render_template('index.html',
                         title='الزول - المساعد السوداني',
                         locations=LOCATIONS.get('states', []),
                         listings=LISTINGS[:6] if LISTINGS else [])

@app.route('/search')
def search():
    """صفحة البحث"""
    return render_template('search.html',
                         categories=CATEGORIES.get('categories', []),
                         locations=LOCATIONS.get('cities', []))

@app.route('/results')
def results():
    """صفحة النتائج"""
    query = request.args.get('q', '')
    location = request.args.get('loc', '')
    category = request.args.get('cat', '')
    
    # فلترة النتائج
    filtered = []
    if LISTINGS:
        for item in LISTINGS:
            matches = True
            
            if query and query not in item.get('title', '') + item.get('description', ''):
                matches = False
            
            if location and location not in item.get('location', ''):
                matches = False
            
            if category and category != item.get('category', ''):
                matches = False
            
            if matches:
                filtered.append(item)
    
    return render_template('results.html',
                         query=query,
                         location=location,
                         results=filtered[:20],
                         count=len(filtered))

@app.route('/listing/<int:listing_id>')
def listing_detail(listing_id):
    """تفاصيل العرض"""
    listing = None
    if LISTINGS and 0 <= listing_id < len(LISTINGS):
        listing = LISTINGS[listing_id]
    
    if not listing:
        return "العرض غير موجود", 404
    
    return render_template('listing_detail.html', listing=listing)

@app.route('/about')
def about():
    """صفحة عن الموقع"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """صفحة الاتصال"""
    return render_template('contact.html')

# ===== APIs =====

@app.route('/api/search', methods=['POST'])
def api_search():
    """API للبحث"""
    data = request.json
    query = data.get('query', '')
    location = data.get('location', '')
    
    results = []
    if LISTINGS:
        for item in LISTINGS:
            if query in item.get('title', '') or query in item.get('description', ''):
                if not location or location in item.get('location', ''):
                    results.append(item)
    
    return jsonify({
        'success': True,
        'results': results[:10],
        'count': len(results)
    })

@app.route('/api/locations')
def api_locations():
    """API للمواقع"""
    return jsonify(LOCATIONS)

@app.route('/api/categories')
def api_categories():
    """API للفئات"""
    return jsonify(CATEGORIES)

# ===== ملفات ثابتة =====

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """خدمة الملفات المرفوعة"""
    return send_from_directory(UPLOAD_DIR, filename)

# ===== تشغيل التطبيق =====

if __name__ == '__main__':
    # إعداد المنفذ
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 بدء تشغيل الزول على المنفذ {port}...")
    print(f"🌐 افتح: http://localhost:{port}")
    print(f"📱 أو افتح: http://[عنوان-IP-جهازك]:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
