import os
from flask import Flask
from supabase import create_client, Client
from postgrest import APIError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    """Allow browser clients from any origin to call this API (no credentials)."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept"
    return response

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)

@app.route('/')
def index():
    try:
        response = supabase.table('users').select("*").execute()
    except APIError as error:
        return f'<p>Error loading users: {error.message}</p>'

    users = response.data

    html = '<h1>Users</h1><ul>'
    for user in users:
        html += f'<li>{user["email"]}</li>'
    html += '</ul>'

    return html

if __name__ == '__main__':
    app.run(debug=True)
