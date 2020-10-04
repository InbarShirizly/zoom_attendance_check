from server import app, db
import os

if __name__ == '__main__':
    if not os.path.exists("/server/site.db"):
        db.create_all()
        db.session.commit()
    app.run(debug=True)