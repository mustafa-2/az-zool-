"""
مجمع بيانات للزول - يعمل على Termux
"""

import requests
from bs4 import BeautifulSoup
import json
import time

class SudanScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Android 13; Mobile) AppleWebKit/537.36'
        })
    
    def search(self, query, location='السودان', limit=10):
        """بحث عن عروض"""
        print(f"🔍 البحث عن: {query} في {location}")
        
        # محاكاة بيانات للاختبار
        results = []
        
        for i in range(min(limit, 5)):
            result = {
                'id': i + 1,
                'title': f'{query} في {location} - عرض {i+1}',
                'description': f'وصف {query} في {location}. هذا عرض تجريبي للزول.',
                'price': f'{i+1},000,000 جنيه' if 'عقار' in query else f'{i+1}00,000 جنيه',
                'location': location,
                'category': 'real_estate' if 'عقار' in query or 'شقة' in query else 'general',
                'contact': f'09{i+1}2345678',
                'features': {
                    'الحالة': 'جديد',
                    'التوفر': 'مباشر'
                },
                'date': '2024-01-15'
            }
            results.append(result)
        
        return results
    
    def fetch_from_file(self, filename):
        """جلب بيانات من ملف محلي"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_to_file(self, data, filename):
        """حفظ البيانات في ملف"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False

# اختبار الوحدة
if __name__ == '__main__':
    scraper = SudanScraper()
    results = scraper.search('شقة للإيجار', 'الخرطوم', 3)
    print(f"✅ تم جمع {len(results)} نتيجة")
