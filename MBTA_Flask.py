from flask import Flask, render_template, request
import Final_Project

app = Flask(__name__)

@app.route('/')
def student():
   return render_template('location.html')

'''@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html", result = result)
'''
@app.route('/', methods = ['POST'])
def test():
   if request.method == 'POST':
      result = request.form['Name']
      answer = Final_Project.answer(result)
      return answer

if __name__ == '__main__':
   app.run(debug = True)