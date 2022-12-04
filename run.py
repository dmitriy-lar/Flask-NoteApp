from src import app
from flask import render_template


# Main Routes
@app.route('/')
def home_page_view():
    return render_template('src/home_page.html')


if __name__ == '__main__':
    app.run()
