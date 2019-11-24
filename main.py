from app import app

if __name__ == "__main__":
    app.run(port = 80 , host='localhost' , debug=True , ssl_context=('cert.pem', 'key.pem'))