import os

os.environ['SYSTEM_ENVIRONMENT'] = 'local'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_PORT'] = '5432'
os.environ['POSTGRES_USER'] = 'user'
os.environ['POSTGRES_PASSWORD'] = 'pass'
os.environ['POSTGRES_DATABASE'] = 'db'
os.environ['GOOGLE_CLIENT_SECRET'] = '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'
os.environ['GOOGLE_REDIRECT_URI'] = 'http://localhost:8000/auth/google/callback'
os.environ['JWT_SECRET_KEY'] = 'secret-key'
os.environ['JWT_ALGORITHM'] = 'HS256'
os.environ['JWT_EXPIRATION_HOURS'] = '12'
