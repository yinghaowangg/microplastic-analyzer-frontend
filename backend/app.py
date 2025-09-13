from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from utils.image_processor import detect_particles
from utils.report_generator import generate_conclusion

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = os.path.join("backend", "static", "results", "pred")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/test-gpt', methods=['GET'])
def test_gpt():
    test_summary = {"PP": 8, "PS": 4}
    result = generate_conclusion(test_summary)
    return jsonify({"result": result})

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(filepath)

    detection_result = detect_particles(filepath)

    material_count = detection_result["counts"]
    output_image = detection_result["output_image"]

    conclusion = generate_conclusion(material_count)

    return jsonify({
        "summary": material_count,
        "output_image": output_image,
        "conclusion": conclusion
    })

@app.route('/results/<path:filename>')
def get_result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

@app.route('/results/pred/<path:filename>')
def get_pred_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

# ✅ 调试模型是否存在
@app.route("/debug-model")
def debug_model():
    model_path = os.path.abspath("backend/models/best.pt")
    exists = os.path.exists(model_path)
    return {"model_path": model_path, "exists": exists}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)