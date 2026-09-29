# 🌾 AGRI SMART AI

AGRI SMART AI is a comprehensive, farmer-centric decision-support web platform built with **Python 3.13**, **Django 5/6**, and **SQLite**. It brings together crop recommendation, soil health guidance, farm financial tracking, profit forecasting, government agricultural scheme directories, live/demo weather forecasts, and crop-aware IoT soil water monitoring.

---

## 🚀 Tech Stack

- **Backend**: Python 3.13, Django (>=5.1, <6.2)
- **Database**: SQLite (`db.sqlite3`)
- **Frontend**: Django Template Language (DTL), Vanilla CSS (`static/css/app.css`), Canvas API (`static/js/dashboard-charts.js`)
- **Machine Learning**: `joblib` for model persistence & inference, with rule-based heuristics fallback
- **External Services**: OpenWeatherMap API (with fallback demo data)
- **Internationalization**: Dual-language support (English & Hindi) via custom session-based templatetags

---

## 📁 Project Architecture & Directory Structure

```text
Agri-Smart/
├── manage.py                          # Django management entry point
├── requirements.txt                   # Project dependencies (Django, joblib, python-dotenv)
├── .env / .env.example                # Environment configuration
├── db.sqlite3                         # Local SQLite database
├── config/                            # Core Django configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/                      # Farmer profile & authentication
│   ├── chatbot/                       # Advisory AI chatbot (keyword heuristics + LLM provider hooks)
│   ├── crop_recommendation/           # ML-based crop recommendation + rule-based fallback
│   │   └── ml/                        # predictor.py, preprocessing.py
│   ├── dashboard/                     # Farmer dashboard, landing page, i18n
│   │   └── templatetags/              # agri_i18n.py (English / Hindi dictionary)
│   ├── expenses/                      # Expense management & category aggregation
│   ├── iot/                           # IoT device management & crop-aware water alerts
│   ├── land/                          # Farm profiles (area, soil type, irrigation, current crop)
│   ├── profit/                        # Cost, revenue, and profit forecasting calculator
│   ├── schemes/                       # Government scheme directory filtered by farmer state
│   ├── soil/                          # N-P-K nutrient & pH guidance
│   └── weather/                       # Live OpenWeather integration with demo fallback
├── data/
│   ├── README.md
│   └── crop_remmendation_dataset.csv  # 10,000-row ML dataset
├── ml_models/
│   └── crop_recommendation/           # Directory for trained model.pkl
├── static/
│   ├── css/app.css                    # Unified styling
│   └── js/dashboard-charts.js         # Canvas-based expense charts
└── templates/
    ├── base.html                      # Root layout, navigation & flash messages
    ├── accounts/                      # register.html, profile.html
    ├── chatbot/                       # chat.html
    ├── crop_recommendation/           # form.html, result.html
    ├── dashboard/                     # home.html
    ├── expenses/                      # list.html, form.html
    ├── iot/                           # monitor.html
    ├── land/                          # list.html, form.html
    ├── partials/                      # form.html, confirm_delete.html
    ├── profit/                        # predict.html
    ├── public/                        # landing.html, about.html, contact.html, guide.html, legal.html
    ├── schemes/                       # list.html
    ├── soil/                          # guidance.html
    └── weather/                       # overview.html
```

---

## 🛠️ Module Breakdown & Core Logic

### 1. `apps/accounts`
- **Models**: `FarmerProfile` (OneToOne with `User`), tracks `phone`, `state`, `district`, `category` (used to filter relevant government schemes), and `role` (`farmer` or `admin`).
- **Features**: Registration auto-provisions a `FarmerProfile` and logs the user in directly.

### 2. `apps/land`
- **Models**: `Farm` (`owner` FK to User, `name`, `area_acres`, `soil_type`, `irrigation_type`, `location`, `current_crop`).
- **Features**: Complete CRUD operations for farm records with user-level isolation via `OwnerQuerysetMixin`.

### 3. `apps/crop_recommendation`
- **Models**: `Recommendation` logs inputs (N, P, K, pH, moisture, soil type, climate, season) along with recommended `crop`, `confidence`, and `source` (`ml` vs `fallback`).
- **Inference Logic**:
  - Checks if `ML_MODEL_PATH` exists (`ml_models/crop_recommendation/model.pkl`).
  - If present, loads model via `joblib` and returns predicted crop + probability confidence.
  - If absent or corrupt, falls back to a transparent rule-based heuristic (`fallback_prediction`) clearly labeled for the user.

### 4. `apps/soil`
- **Features**: Analyzes Nitrogen, Phosphorus, Potassium, pH, and soil moisture.
- **Guidance Logic**: Classifies nutrients (Low < 30, Adequate 30–70, High > 70) and pH (Acidic, Alkaline, Neutral), recommending customized fertilizer actions and irrigation warnings.

### 5. `apps/weather`
- **Features**: Queries the OpenWeatherMap API for live conditions, temperature, humidity, wind, and rainfall.
- **Resilience**: If `OPENWEATHER_API_KEY` is missing or the external API call fails, automatically displays demo data with an informational notice so UI never crashes.

### 6. `apps/iot`
- **Models**:
  - `Device`: IoT sensor hardware associated with a specific `Farm`.
  - `IoTReading`: Telemetry for `soil_moisture`, `water_level`, `temperature`, `humidity`, and `simulated` flag.
  - `IoTAlert`: Stores `LOW` or `HIGH` water alerts with status flags (`resolved`).
- **Crop-Aware Alert Logic**:
  - Compares reading against crop-specific moisture thresholds (e.g., Rice: 60–85%, Wheat: 35–55%, Maize: 40–60%, Sugarcane: 55–75%).
  - Generates automated warnings for low water (drought stress) or excess water (poor drainage / over-irrigation).
  - Automatically resolves previous alerts once soil moisture normalizes.
  - Contains a simulation action (`/iot/<pk>/simulate/`) with `normal`, `low`, and `high` modes for interactive demonstration.

### 7. `apps/expenses`
- **Models**: `Expense` (`farmer`, `category`, `amount`, `date`, `note`).
- **Features**: Tracks expenditures across 8 categories (Seeds, Fertilizer, Pesticides, Labour, Irrigation, Machinery, Transport, Other) with date-range and category filters.

### 8. `apps/profit`
- **Features**: Takes inputs for expected crop yield, market price, and production expenses to calculate total cost, estimated revenue, net profit, and return per acre.

### 9. `apps/schemes`
- **Models**: `Scheme` (name, description, state, eligibility, benefits, official_url, category, min_land_acres, crop).
- **Features**: Automatically filters verified national and state-specific agricultural schemes based on the farmer's profile.

### 10. `apps/chatbot`
- **Features**: Agricultural query interface. Contains rule-based heuristics for soil, fertilizer, and irrigation prompts, with an explicit extension point in `apps/chatbot/services.py` for plugging in external AI APIs (`AI_API_KEY`, `AI_PROVIDER`).

### 11. `apps/dashboard`
- **Dashboard Home**: Aggregates total land area, active farms, total expenditure, and latest recommendations.
- **Visualizations**: Custom HTML5 Canvas charts (`static/js/dashboard-charts.js`) rendering category expenditure breakdowns and monthly spending trends.
- **Multilingual Support**: Session-based language toggle (English / Hindi) using custom template tag `{% tr '...' %}` (`apps/dashboard/templatetags/agri_i18n.py`).

---

## 🧭 URL Routing Reference

| Endpoint | View / Handler | App | Access | Purpose |
|---|---|---|---|---|
| `/` | `landing` | `dashboard` | Public | Home / Marketing page |
| `/about/` | `about` | `dashboard` | Public | About Us |
| `/contact/` | `contact` | `dashboard` | Public | Contact Form |
| `/privacy/` | `privacy` | `dashboard` | Public | Privacy Policy |
| `/terms/` | `terms` | `dashboard` | Public | Terms & Conditions |
| `/guide/` | `guide` | `dashboard` | Public | In-app user guide |
| `/language/toggle/` | `toggle_language` | `dashboard` | Public | Toggle English / Hindi |
| `/accounts/register/` | `register` | `accounts` | Public | Farmer registration |
| `/accounts/login/` | `login` | `accounts` | Public | Farmer login |
| `/accounts/logout/` | `logout` | `accounts` | Authenticated | Farmer logout |
| `/accounts/profile/` | `profile` | `accounts` | Authenticated | Farmer profile management |
| `/dashboard/` | `home` | `dashboard` | Authenticated | Farmer dashboard & analytics |
| `/farm/` | `list` | `land` | Authenticated | List all farms |
| `/farm/add/` | `add` | `land` | Authenticated | Add a new farm |
| `/farm/<pk>/edit/` | `edit` | `land` | Authenticated | Update farm details |
| `/farm/<pk>/delete/` | `delete` | `land` | Authenticated | Delete a farm |
| `/crops/` | `create` | `crop_recommendation` | Authenticated | Crop recommendation engine |
| `/soil/` | `guidance` | `soil` | Authenticated | Soil & fertilizer advisor |
| `/profit/` | `predict` | `profit` | Authenticated | Profit prediction calculator |
| `/expenses/` | `list` | `expenses` | Authenticated | Expense ledger & filters |
| `/expenses/add/` | `add` | `expenses` | Authenticated | Add expense |
| `/expenses/<pk>/edit/` | `edit` | `expenses` | Authenticated | Edit expense |
| `/expenses/<pk>/delete/` | `delete` | `expenses` | Authenticated | Delete expense |
| `/schemes/` | `list` | `schemes` | Authenticated | Government schemes catalog |
| `/assistant/` | `chat` | `chatbot` | Authenticated | Advisory chatbot |
| `/iot/` | `monitor` | `iot` | Authenticated | Sensor readings & water alerts |
| `/iot/<pk>/simulate/` | `simulate` | `iot` | Authenticated | Simulate IoT sensor telemetry |
| `/weather/` | `overview` | `weather` | Authenticated | Live / demo weather overview |
| `/admin/` | Admin Site | `django.contrib.admin` | Staff | Django Administration |

---

## ⚙️ Environment Configuration (`.env`)

```ini
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ML_MODEL_PATH=ml_models/crop_recommendation/model.pkl
AI_API_KEY=
AI_PROVIDER=
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

---

## 💻 Local Setup & Execution

1. **Activate Virtual Environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Verify Project Health**:
   ```bash
   python manage.py check
   ```

5. **Start Development Server**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
