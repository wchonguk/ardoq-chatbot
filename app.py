import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ARDOQ_API_TOKEN = os.getenv("ARDOQ_API_TOKEN")
ARDOQ_API_HOST = "https://smartestenergy.ardoq.com"

headers = {
    "Authorization": f"Bearer {ARDOQ_API_TOKEN}",
    "Content-Type": "application/json"
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json["message"].strip()

    # Route by intent
    intent = interpret_command(user_input)
    if intent["intent"] == "list_workspaces":
        return list_workspaces()
    elif intent["intent"] == "list_components":
        return list_components_by_workspace(intent["workspace"])
    elif intent["intent"] == "get_component":
        return get_component(intent["component_id"])
    elif intent["intent"] == "query_filter":
        return jsonify({"response": f"🔍 Query: {intent['criteria']} — filter-based search coming soon."})
    else:
        return jsonify({
            "response": "🤖 I didn’t understand. Try:\n- list workspaces\n- list components in workspace Applications\n- get component <ID>"
        })


def interpret_command(text):
    text = text.lower()

    if "list workspaces" in text:
        return {"intent": "list_workspaces"}
    elif "list components in workspace" in text:
        name = text.split("workspace")[-1].strip()
        return {"intent": "list_components", "workspace": name}
    elif text.startswith("get component"):
        cid = text.split("component")[-1].strip()
        return {"intent": "get_component", "component_id": cid}
    elif "without expert" in text:
        return {"intent": "query_filter", "criteria": "missing_expert"}
    elif "supported by" in text:
        return {"intent": "query_filter", "criteria": text}
    else:
        return {"intent": "unknown"}


def list_workspaces():
    url = f"{ARDOQ_API_HOST}/api/workspace"
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        names = [w.get("name", "Unnamed") for w in data]
        sample = ', '.join(names[:3]) + ("..." if len(names) > 3 else "")
        return jsonify({
            "response": f"✅ Found {len(names)} workspaces. Examples: {sample}"
        })
    except Exception as e:
        return jsonify({"response": f"❌ Error fetching workspaces: {e}"}), 500


def list_components_by_workspace(workspace_name):
    try:
        r = requests.get(f"{ARDOQ_API_HOST}/api/workspace", headers=headers)
        r.raise_for_status()
        workspaces = r.json()
        match = next((w for w in workspaces if w.get("name", "").lower() == workspace_name.lower()), None)
        if not match:
            return jsonify({"response": f"⚠️ Workspace '{workspace_name}' not found."})

        ws_id = match["_id"]
        comp_url = f"{ARDOQ_API_HOST}/api/component?workspace={ws_id}"
        comp_res = requests.get(comp_url, headers=headers)
        comp_res.raise_for_status()
        comps = comp_res.json()
        names = [c.get("name", "Unnamed") for c in comps]
        preview = ', '.join(names[:3]) + ("..." if len(names) > 3 else "")
        return jsonify({
            "response": f"✅ {len(names)} components found in '{workspace_name}'. Examples: {preview}"
        })
    except Exception as e:
        return jsonify({"response": f"❌ Error listing components: {e}"}), 500


def get_component(comp_id):
    try:
        url = f"{ARDOQ_API_HOST}/api/component/{comp_id}"
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        c = r.json()
        return jsonify({
            "response": f"🧱 Component: {c.get('name', '(no name)')}\n- Type: {c.get('type')}\n- Workspace ID: {c.get('workspace')}\n- Description: {c.get('description', 'No description')}"
        })
    except Exception as e:
        return jsonify({"response": f"❌ Error retrieving component {comp_id}: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
