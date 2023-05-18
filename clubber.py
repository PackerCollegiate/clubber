from app import app, db
from app.models import User, Club

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Club': Club. 'Post': Post}
