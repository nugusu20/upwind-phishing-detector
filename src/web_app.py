from flask import Flask, render_template, request

from phishing_detector import analyze_email


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    findings = None
    filename = None
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("email_file")

        if not uploaded_file or uploaded_file.filename == "":
            error = "Please upload a text file containing email content."
        else:
            filename = uploaded_file.filename
            email_content = uploaded_file.read().decode("utf-8")
            findings = analyze_email(email_content)

    return render_template(
        "index.html",
        findings=findings,
        filename=filename,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
