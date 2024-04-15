from Server import Flaskserver

server: Flaskserver = Flaskserver()
app = server.server_run()


if __name__ == "__main__":
    app.run(debug=True)
    # server.serve_forever()
