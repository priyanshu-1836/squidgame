from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'squid_secret_key'

@app.route('/')
def index():
    if 'position' not in session:
        session['position'] = 0
        session['message'] = "Game started! 🟢"
    light = random.choice(["green", "red"])
    session['light'] = light
    return render_template('index.html', position=session['position'], light=light, message=session['message'])

@app.route('/move', methods=['POST'])
def move():
    light = session['light']
    move = request.form['move']

    if light == "red" and move == "yes":
        session.clear()
        return render_template('index.html', position=0, light='red', message="💀 You moved on RED LIGHT! Game Over.")

    if light == "green" and move == "yes":
        step = random.randint(5, 15)
        session['position'] += step
        session['message'] = f"✅ You moved {step} steps!"

    elif move == "no":
        session['message'] = "😐 You stayed still."

    if session['position'] >= 100:
        session.clear()
        return render_template('index.html', position=100, light='green', message="🏁 You survived! Victory! 🥳")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
