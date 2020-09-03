from flask import Flask, render_template
import spotipy, genres

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/auth')
def get_token():
    tiers = genres.generateTiers()
    return render_template("home.html", username="Champion", genres=tiers)


if __name__ == "__main__":
    app.run()