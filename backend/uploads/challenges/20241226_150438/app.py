from flask import Flask, render_template_string
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Web Security Challenge</title>
        <style>
            body { 
                font-family: Arial, sans-serif;
                margin: 40px;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Web Security Challenge</h1>
            <p>Try to find the vulnerability!</p>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)