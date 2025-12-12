import os


structure = {
    'app.py': '',
    'config.py': '',
    'requirements.txt': '',
    'Procfile': 'web: gunicorn app:app',
    'runtime.txt': 'python-3.11.0',
    '.gitignore': 'venv/\n__pycache__/\n*.pyc\n.env\n*.log\n',
    
    'static/': {
        'css/': {
            'style.css': '',
            'mobile.css': ''
        },
        'js/': {
            'main.js': '',
            'voice.js': ''
        },
        'images/': {
            'logo.png': '',
            'favicon.ico': ''
        },
        'uploads/': {
            '.gitkeep': ''
        }
    },
    
    'templates/': {
        'base.html': '',
        'index.html': '',
        'search.html': '',
        'results.html': '',
        'about.html': '',
        'contact.html': ''
    },
    
    'data/': {
        'locations.json': '',
        'listings.json': '',
        'categories.json': ''
    },
    
    'modules/': {
        '__init__.py': '',
        'scraper.py': '',
        'chatbot.py': ''
    },
    
    'logs/': {
        '.gitkeep': ''
    }
}


def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
           
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"✅ تم إنشاء: {path}")


create_structure('.', structure)
print("🎉 تم إنشاء هيكل المشروع بنجاح!")
