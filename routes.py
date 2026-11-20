from flask import Blueprint, request, jsonify, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip().lower()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    if len(message) > 4000:
        return jsonify({"error": "Message is too long."}), 400

    risk_score = 0
    warnings = []
    advice = []

    rules = [
        (["registration fee", "processing fee", "pay ₹", "pay rs", "payment required"],
         3, "The message asks for money or a registration fee."),
        (["urgent", "immediately", "within 24 hours", "limited time"],
         2, "The message uses urgency or pressure."),
        (["selected for internship", "job offer", "offer letter", "congratulations"],
         1, "The message makes an employment or selection claim."),
        (["otp", "password", "bank details", "credit card", "upi pin"],
         3, "The message requests sensitive personal or financial information."),
        (["click here", "verify your account", "login now"],
         2, "The message asks you to click or verify something."),
        (["whatsapp", "telegram", "personal number"],
         1, "The message directs you to an external messaging contact.")
    ]

    for keywords, points, warning in rules:
        if any(word in message for word in keywords):
            risk_score += points
            warnings.append(warning)

    if "http://" in message or "https://" in message or "www." in message:
        risk_score += 2
        warnings.append("The message contains a web link. Check its destination carefully.")

    if risk_score >= 5:
        risk_level = "HIGH"
        advice = [
            "Do not pay any money.",
            "Do not share OTPs, passwords or bank details.",
            "Verify the organization using its official website.",
            "Avoid clicking suspicious links."
        ]
    elif risk_score >= 2:
        risk_level = "MEDIUM"
        advice = [
            "Verify the sender's identity.",
            "Check the offer through official channels.",
            "Do not share personal information unnecessarily."
        ]
    else:
        risk_level = "LOW"
        advice = [
            "Stay alert even if no major warning signs were detected.",
            "Verify important claims independently.",
            "Never share passwords or OTPs."
        ]

    if not warnings:
        warnings.append("No predefined warning patterns were detected.")

    reply = f"""RISK LEVEL: {risk_level}

RISK SCORE: {risk_score}

WARNING SIGNS:
- """ + "\n- ".join(warnings) + """

SAFETY RECOMMENDATIONS:
- """ + "\n- ".join(advice) + """

Note: This is a rule-based preliminary analysis, not a guarantee that a message is safe or fraudulent."""

    return jsonify({"reply": reply})
