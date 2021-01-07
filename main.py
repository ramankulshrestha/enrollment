from application import app
app.config['SECRET_KEY'] = 'abcd'
if __name__ == '__main__':
    app.run(debug=True)