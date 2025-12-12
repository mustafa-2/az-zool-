// JavaScript للزول

// تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    console.log('الزول الذكي يعمل!');
    
    // إضافة تأثيرات للبطاقات
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        card.addEventListener('touchend', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // البحث الصوتي
    const voiceSearchBtn = document.getElementById('voiceSearch');
    if (voiceSearchBtn) {
        voiceSearchBtn.addEventListener('click', startVoiceSearch);
    }
});

// البحث الصوتي
function startVoiceSearch() {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'ar-SA';
        recognition.start();
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            const searchInput = document.querySelector('input[name="q"]');
            if (searchInput) {
                searchInput.value = transcript;
                showMessage('🎤 تم التعرف على: ' + transcript, 'success');
            }
        };
        
        recognition.onerror = function(event) {
            showMessage('حدث خطأ في التعرف على الصوت', 'error');
        };
    } else {
        showMessage('المتصفح لا يدعم البحث الصوتي', 'warning');
    }
}

// مشاركة العرض
function shareListing(title, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            text: 'شاهد هذا العرض على الزول',
            url: url
        });
    } else {
        navigator.clipboard.writeText(url);
        showMessage('تم نسخ الرابط للحافظة', 'info');
    }
}

// عرض الرسائل
function showMessage(text, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${text}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '70px';
    alertDiv.style.right = '10px';
    alertDiv.style.left = '10px';
    alertDiv.style.zIndex = '9999';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// حفظ البحث
function saveSearch(query) {
    let searches = JSON.parse(localStorage.getItem('recentSearches') || '[]');
    searches.unshift({
        query: query,
        timestamp: new Date().toISOString()
    });
    
    // حفظ آخر 10 عمليات بحث فقط
    searches = searches.slice(0, 10);
    localStorage.setItem('recentSearches', JSON.stringify(searches));
}

// جلب عمليات البحث المحفوظة
function getRecentSearches() {
    return JSON.parse(localStorage.getItem('recentSearches') || '[]');
}

// الكشف عن الجوال
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}
