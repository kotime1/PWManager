from app import app, setup_db

if __name__ == '__main__':
    setup_db()
    app.run()