from package import server

app = server()

if __name__ == "__main__":
    app.run(debug=True)
