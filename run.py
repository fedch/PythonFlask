from app import app
from db import db

db.init_app(app)

# Create all databases - for users, items and stores
@app.before_first_request
def create_tables():
    db.create_all()
