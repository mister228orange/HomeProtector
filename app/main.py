from flask import Flask, render_template_string
from .config import settings
app = Flask(settings.APP_NAME)

@app.route('/')
def index():    
    return render_template_string('''<!DOCTYPE html>
                                  <html>\n<head>\n    <title>HomeProtector</title>\n</head>
                                  <body>\n    <h1>HomeProtector Security Dashboard</h1>
                                  \n    <p>This is a basic dashboard for monitoring Bluetooth activity.</p>\n\n</body>\n</html >''')\n\nif __name__ == '__main__':\n    app.run(debug=True)\n"