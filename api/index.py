from app.main import app

# Vercel entry point
def handler(event, context):
    return app

# For local development
if __name__ == '__main__':
    app.run(debug=True)