
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent


# Include the static files for the frontend
STATICFILES_DIRS = [
    STATIC_DIR / 'node_modules/@fortawesome',
    STATIC_DIR / 'dist',
    ('weather-icons', STATIC_DIR / 'node_modules/weather-icons'),
    ('bootstrap', STATIC_DIR / 'node_modules/bootstrap/dist'),
    ('jquery', STATIC_DIR / 'node_modules/jquery/dist')
]
