import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    raise

# Vercel serverless function handler
def handler(request, response):
    return app(request, response)

# For local development
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)