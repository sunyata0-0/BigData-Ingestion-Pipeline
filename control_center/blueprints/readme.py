from services.readme_services import ReadmeService

@readme_bp.route("/readme")
def readme():

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify({
        "success": True,
        "content": content
    })