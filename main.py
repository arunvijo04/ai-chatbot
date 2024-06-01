from flask import Flask, render_template, request, jsonify
from aiml import Kernel
import os

app = Flask(__name__)

# Initialize the AIML kernel once when the app starts
kernel = Kernel()
brain_file = "bot_brain.brn"

if os.path.isfile(brain_file):
    kernel.bootstrap(brainFile=brain_file)
else:
    kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"), commands="load aiml b")
    kernel.saveBrain(brain_file)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
    message = request.form['messageText'].strip()
    
    if message.lower() == "quit":
        return jsonify({'status': 'OK', 'answer': 'Goodbye!'})
    elif message.lower() == "save":
        kernel.saveBrain(brain_file)
        return jsonify({'status': 'OK', 'answer': 'Brain saved successfully!'})

    bot_response = kernel.respond(message)
    return jsonify({'status': 'OK', 'answer': bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
