from flask import Flask
from flask import url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>\n<p>Available links so far:</p>\n\
        <ul style='list-style-type:none'><li><a href='/index'>Index</a>\
            </li><li><a href='/u/<script type=\'text/javascript\'>alert<'boo'>'>Unsanitized variable usage</a>\
                </li><li><a href='/<script type=\'text/javascript\'>alert<'boo'>'>Sanitized variable usage</a>\
                    </li><li><a href='/user/dock_the_wayne_bronson'>Profile example</a>\
                        </li><li><a href='/post/001'>Post example</a>\
                            </li><li><a href='/path/however/long/i/want/this/to/be/breadcrumbs/yay'>Pathing/breadcrumbs demo</a>\
                                </li><li><a href='/demo_url_for'>Demo of url_for</a>\
                                    </li><li>\
                                        </li><li>\
                                            </li><li>\
                                                </li></ul>"

@app.route("/index")
def hello_index():
    return "<p><b>Hi, this is the index route!</b></p><p>Bottom text</p>"

@app.route("/u/<name>")
def hello_unsan(name):
    # Try inserting: "<script>alert("Gotcha!")" !
    return f"Hello, {name}!"

@app.route("/<name>")
def hello_san(name):
    return f"Hello, {escape(name)}!"

@app.route("/user/<username>")
def show_profile(username):
    return f"Profile: {escape(username)}"

@app.route("/post/<int:post_id>")
def show_post(post_id: int):
    # Other options for typing are string, float, path, and uuid
    return f"Post: {escape(post_id)}"

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    return f"Subpath (after /path/): {escape(subpath)}"

@app.route("/demo_url_for")
def demo_url_for_method():
    text = "Base level URLs, based on functions:\n\n"
    urls = ['hello_index', 'demo_url_for_method']
    with app.test_request_context():
        for url in urls:
            text += f"<p>{url_for(url)}</p>\n"
        text += "\n<p>Using vars:</p>\n\n"
        text += '\n' + url_for('show_profile', username='Brock Oli', next='/')

    return text


if __name__ =="__main__":
    app.run()
    # hello_world()