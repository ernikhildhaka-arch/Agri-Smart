import json, os
from pathlib import Path
from django.conf import settings
from .preprocessing import numeric_vector
def predict_crop(features):
    path=Path(os.getenv('ML_MODEL_PATH', settings.BASE_DIR/'ml_models/crop_recommendation/model.pkl'))
    if path.exists():
        try:
            import joblib
            model=joblib.load(path); prediction=model.predict(numeric_vector(features))[0]; confidence=None
            if hasattr(model,'predict_proba'): confidence=float(max(model.predict_proba(numeric_vector(features))[0]))
            return {'crop':str(prediction),'confidence':confidence,'source':'ml'}
        except Exception as exc: return fallback_prediction(features, f'Model unavailable: {exc}')
    return fallback_prediction(features)
def fallback_prediction(f, note=None):
    # Transparent rule-based demonstration only; replace with a validated local model.
    if f['rainfall'] > 180 and f['moisture'] > 45: crop='Rice'
    elif f['ph'] < 6.2: crop='Potato'
    elif f['temperature'] > 28 and f['rainfall'] < 120: crop='Millet'
    elif f['nitrogen'] > 70: crop='Maize'
    else: crop='Pigeon pea'
    return {'crop':crop,'confidence':None,'source':'fallback','note':note or 'No trained model found; this is a rule-based demo, not an ML prediction.'}
