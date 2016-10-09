from flask import Flask, request, send_from_directory

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder='client/build/', static_url_path='')


@app.route('/')
def root():
    print("Hello World!")
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run()