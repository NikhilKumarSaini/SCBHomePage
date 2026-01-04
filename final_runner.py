from scoring.ela_score import compute_ela_score
from scoring.noise_score import compute_noise_score
from scoring.compression_score import compute_compression_score
from scoring.font_alignment_score import compute_font_alignment_score
from scoring.final_score import compute_final_score
from ml.predict_xgb import predict_risk


def run_scoring(record_id, forensics_output_dir, pdf_metadata):
    # ---- Individual forensic scores ----
    ela_score = compute_ela_score(forensics_output_dir)
    noise_score = compute_noise_score(forensics_output_dir)
    compression_score = compute_compression_score(forensics_output_dir)
    font_score = compute_font_alignment_score(forensics_output_dir)

    # ---- Final forensic aggregation ----
    forensic_risk = compute_final_score(
        ela_score=ela_score,
        noise_score=noise_score,
        compression_score=compression_score,
        font_score=font_score
    )

    # ---- ML Prediction ----
    ml_result = predict_risk({
        "ela_score": ela_score,
        "noise_score": noise_score,
        "compression_score": compression_score,
        "cnn_f1": forensic_risk,   # proxy feature
        "cnn_f2": font_score
    })

    # ---- Final decision ----
    final_risk = round(
        0.6 * forensic_risk + 0.4 * ml_result["ml_probability"], 3
    )

    verdict = (
        "Likely Manipulated" if final_risk >= 0.6
        else "Possibly Clean"
    )

    return {
        "record_id": record_id,
        "risk_score": final_risk,
        "verdict": verdict,
        "ela_score": round(ela_score, 3),
        "noise_score": round(noise_score, 3),
        "compression_score": round(compression_score, 3),
        "font_score": round(font_score, 3),
        "ml_probability": ml_result["ml_probability"]
    }