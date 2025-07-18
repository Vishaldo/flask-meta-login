from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>🏠 Flask is running on Render!</h2><br><a href='/login'>Login with Facebook</a>"

@app.route("/login")
def login():
    client_id = "YOUR_APP_ID"
    redirect_uri = "https://your-render-app.onrender.com/callback"
    scope = "instagram_basic,instagram_content_publish,instagram_manage_comments,instagram_manage_insights,pages_show_list,pages_read_engagement"
    extras = '{"setup":{"channel":"IG_API_ONBOARDING"}}'
    encoded_extras = extras.replace('"', '%22').replace('{', '%7B').replace(
        '}', '%7D').replace(':', '%3A').replace(',', '%2C')

    fb_login_url = (f"https://www.facebook.com/v23.0/dialog/oauth"
                    f"?client_id={client_id}"
                    f"&display=page"
                    f"&extras={encoded_extras}"
                    f"&redirect_uri={redirect_uri}"
                    f"&response_type=token"
                    f"&scope={scope}")

    return f'<a href="{fb_login_url}">Click here to log in with Facebook</a>'

@app.route("/callback")
def callback():
    return '''
    <h2>✅ Login successful!</h2>
    <p>Processing your access token...</p>
    <script>
        const fragment = window.location.hash.substring(1);
        const params = new URLSearchParams(fragment);
        const accessToken = params.get("access_token");

        if (accessToken) {
            fetch("/save-token", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ token: accessToken })
            })
            .then(response => response.text())
            .then(data => {
                document.body.innerHTML += "<p><strong>✅ Token saved:</strong> " + data + "</p>";
            })
            .catch(err => {
                document.body.innerHTML += "<p><strong>❌ Error saving token:</strong> " + err + "</p>";
            });
        } else {
            document.body.innerHTML += "<p><strong>❌ No token found in URL.</strong></p>";
        }
    </script>
    '''

@app.route("/save-token", methods=["POST"])
def save_token():
    token = request.json.get("token")
    with open("access_token.txt", "w") as f:
        f.write(token)
    return "Token received and saved."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)