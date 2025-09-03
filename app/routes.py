from flask import Blueprint, request, jsonify
import pandas as pd
from .services import calculate_stdev, calculate_avg

bp = Blueprint("api", __name__)

@bp.route("/upload/avg", methods=["POST"])
def upload_avg():
    """
    Upload CSV and calculate average sales per item
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Average sales per item
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    try:
        df = pd.read_csv(file, sep=None, engine="python")
        result = calculate_avg(df)
        return result.to_json(orient="records")
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@bp.route("/upload/stdev", methods=["POST"])
def upload_stdev():
    """
    Upload CSV and calculate sales standard deviation per item
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Sales stdev per item
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    try:
        df = pd.read_csv(file, sep=None, engine="python")
        result = calculate_stdev(df)
        return result.to_json(orient="records")
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@bp.route("/upload/summary", methods=["POST"])
def upload_summary():
    """
    Upload CSV and summarize sales per item
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Summary per item (first/last date, totals, active days, duration)
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    try:
        df = pd.read_csv(file, sep=None, engine="python")
        from .services import summarize_items
        result = summarize_items(df)
        return result.to_json(orient="records")
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
