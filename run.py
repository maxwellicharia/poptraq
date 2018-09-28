from poptraq import views


app = views.create_app()

if __name__ == '__main__':
    app.run(debug=True)
