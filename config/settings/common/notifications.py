import os

DEFAULT_FROM_EMAIL = 'social-network'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER','itbooks527@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'nissanvy-12')
EMAIL_USE_TLS = True
