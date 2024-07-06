from flask import Flask, request, render_template, send_file
from gtts import gTTS
from langdetect import detect
import os

app = Flask(__name__)

# Diccionario de idiomas soportados por gTTS
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'nl': 'Dutch',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'ru': 'Russian'
}

# Diccionario de TLDs para diferentes tonos (ejemplo de inglés)
TLD_OPTIONS = {
    'en': {
        'com': 'US (English)',
        'co.uk': 'UK (English)',
        'com.au': 'AU (English)',
        'ca': 'CA (English)',
        'co.in': 'IN (English)',
        'ie': 'IE (English)'
    },
    'es': {
        'es': 'Spain (Spanish)',
        'com.mx': 'Mexico (Spanish)'
    },
    'fr': {
        'fr': 'France (French)',
        'ca': 'Canada (French)'
    },
    'de': {
        'de': 'Germany (German)'
    },
    'it': {
        'it': 'Italy (Italian)'
    },
    'pt': {
        'pt': 'Portugal (Portuguese)',
        'com.br': 'Brazil (Portuguese)'
    },
    'nl': {
        'nl': 'Netherlands (Dutch)'
    },
    'ja': {
        'co.jp': 'Japan (Japanese)'
    },
    'ko': {
        'co.kr': 'Korea (Korean)'
    },
    'zh-cn': {
        'com.hk': 'Hong Kong (Chinese Simplified)'
    },
    'zh-tw': {
        'tw': 'Taiwan (Chinese Traditional)'
    },
    'ru': {
        'ru': 'Russia (Russian)'
    }
}

@app.route('/')
def index():
    return render_template('index.html', languages=SUPPORTED_LANGUAGES, tld_options=TLD_OPTIONS)

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']
    detected_lang = detect(text)
    
    if detected_lang not in SUPPORTED_LANGUAGES:
        return "Language not supported", 400
    
    tld = request.form.get('tld', 'com')
    slow = request.form.get('slow', 'false') == 'true'
    
    tts = gTTS(text=text, lang=detected_lang, tld=tld, slow=slow)
    audio_path = "static/output.mp3"
    tts.save(audio_path)
    
    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
