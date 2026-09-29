from django import template

register = template.Library()

HI = {
    'Dashboard': 'डैशबोर्ड', 'My Farm': 'मेरा खेत', 'Profile': 'प्रोफ़ाइल', 'Logout': 'लॉग आउट',
    'Crop Recommendation': 'फसल सुझाव', 'Soil & Fertilizer': 'मिट्टी और उर्वरक',
    'Profit Prediction': 'लाभ अनुमान', 'Expenses': 'खर्च', 'Government Schemes': 'सरकारी योजनाएँ',
    'AI Assistant': 'एआई सहायक', 'IoT Monitoring': 'आईओटी निगरानी', 'About Us': 'हमारे बारे में',
    'Contact Us': 'संपर्क करें', 'Privacy Policy': 'गोपनीयता नीति', 'Terms & Conditions': 'नियम व शर्तें',
    'Get Started': 'शुरू करें', 'Log in': 'लॉग इन', 'English': 'English', 'हिंदी': 'हिंदी',
    'Smart farming decisions, made simpler.': 'स्मार्ट खेती के निर्णय, अब आसान।',
    'Your farm. Better decisions.': 'आपका खेत। बेहतर निर्णय।',
    'Built for practical farm planning.': 'व्यावहारिक कृषि योजना के लिए बनाया गया।',
    'Send message': 'संदेश भेजें', 'Name': 'नाम', 'Email': 'ईमेल', 'Message': 'संदेश',
    'Hello': 'नमस्ते', 'Quick start': 'त्वरित शुरुआत', 'Total land': 'कुल भूमि', 'Farms': 'खेत',
    'Recorded expenses': 'दर्ज खर्च', 'Latest crop': 'नवीनतम फसल', 'Recent expenses': 'हाल के खर्च',
    'Add farm': 'खेत जोड़ें', 'Get crop guidance': 'फसल मार्गदर्शन लें', 'Add expense': 'खर्च जोड़ें',
    'Estimate profit': 'लाभ का अनुमान', 'No expenses recorded yet.': 'अभी तक कोई खर्च दर्ज नहीं है।',
    'Date': 'तारीख', 'Category': 'श्रेणी', 'Amount': 'राशि',
}

@register.simple_tag(takes_context=True)
def tr(context, text):
    return HI.get(text, text) if context.get('site_language') == 'hi' else text
