from Server import app, db
import os

if __name__ == '__main__':
    if not os.path.exists("/Server/site.db"):
        db.create_all()
        db.session.commit()
    app.run(debug=True)