"""CDSS thuyên tắc phổi cấp theo AHA/ACC 2026.

Bản FINAL cho tiếp cận ban đầu tại cấp cứu. Phần lõi không phụ thuộc Streamlit để có thể kiểm thử tự động.
Phạm vi: người lớn >=18 tuổi, từ nghi ngờ PE -> xác nhận -> phân nhóm AHA/ACC A-E + R -> điều trị ban đầu. Không thay thế đánh giá lâm sàng/PERT/quy trình bệnh viện.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Literal

GUIDELINE = "2026 AHA/ACC/ACCP/ACEP/CHEST/SCAI/SHM/SIR/SVM/SVN Guideline for Acute Pulmonary Embolism"
GUIDELINE_DOI = "10.1161/CIR.0000000000001415"
RELEASE_CANDIDATE = "FINAL-2026.08.22"

# ---------- TIỆN ÍCH ----------

def _bool(x: bool) -> int:
    return 1 if x else 0


def cockcroft_gault(age: float, weight_kg: float, creat_mg_dl: float, female: bool) -> Optional[float]:
    """CrCl Cockcroft-Gault. Chỉ dùng khi các đầu vào hợp lệ.

    Lưu ý: chọn loại cân nặng trong hình thể cực đoan cần thẩm định theo quy trình thuốc.
    Hàm này không tự quyết định cân nặng lý tưởng/điều chỉnh.
    """
    if age <= 0 or weight_kg <= 0 or creat_mg_dl <= 0:
        return None
    crcl = ((140 - age) * weight_kg) / (72 * creat_mg_dl)
    if female:
        crcl *= 0.85
    return max(crcl, 0.0)


def creat_umol_to_mgdl(creat_umol_l: float) -> Optional[float]:
    if creat_umol_l <= 0:
        return None
    return creat_umol_l / 88.4


# ---------- XÁC SUẤT TIỀN NGHIỆM / CHẨN ĐOÁN ----------

def wells_score(*, dvt_signs=False, pe_most_likely=False, hr_gt_100=False,
                immobilization_or_surgery=False, prior_dvt_pe=False,
                hemoptysis=False, cancer=False) -> float:
    return (
        3.0 * _bool(dvt_signs)
        + 3.0 * _bool(pe_most_likely)
        + 1.5 * _bool(hr_gt_100)
        + 1.5 * _bool(immobilization_or_surgery)
        + 1.5 * _bool(prior_dvt_pe)
        + 1.0 * _bool(hemoptysis)
        + 1.0 * _bool(cancer)
    )


def wells_category(score: float) -> str:
    if score < 2:
        return "thấp"
    if score <= 6:
        return "trung bình"
    return "cao"


def wells_modified(score: float) -> str:
    return "PE ít khả năng" if score <= 4 else "PE có khả năng"


def simplified_geneva_score(*, age_gt_65=False, prior_dvt_pe=False,
                            surgery_or_lower_limb_fracture=False, active_cancer=False,
                            unilateral_leg_pain=False, hemoptysis=False,
                            hr_75_94=False, hr_ge_95=False,
                            deep_vein_tenderness_and_unilateral_edema=False) -> int:
    # Theo Table 3 của guideline 2026: bản simplified cho 1 điểm ở cả hai mức HR;
    # hai mức nhịp tim phải được xem là loại trừ lẫn nhau trên giao diện.
    hr_point = 1 if (hr_75_94 or hr_ge_95) else 0
    return sum([
        _bool(age_gt_65), _bool(prior_dvt_pe), _bool(surgery_or_lower_limb_fracture),
        _bool(active_cancer), _bool(unilateral_leg_pain), _bool(hemoptysis),
        hr_point, _bool(deep_vein_tenderness_and_unilateral_edema)
    ])


def simplified_geneva_category(score: int) -> str:
    if score <= 1:
        return "thấp"
    if score <= 4:
        return "trung bình"
    return "cao"


def perc_result(*, gestalt_lt_15: bool, age: float, hr: float, spo2: float,
                hemoptysis: bool, estrogen_use: bool, prior_dvt_pe: bool,
                unilateral_leg_swelling: bool, recent_surgery_trauma_hospitalized: bool) -> Dict[str, object]:
    if not gestalt_lt_15:
        return {"applicable": False, "negative": False,
                "message": "PERC không áp dụng vì xác suất tiền nghiệm không <15%."}
    positive = []
    if age >= 50: positive.append("tuổi ≥50")
    if hr >= 100: positive.append("nhịp tim ≥100/phút")
    if spo2 < 95: positive.append("SpO₂ <95%")
    if hemoptysis: positive.append("ho ra máu")
    if estrogen_use: positive.append("đang sử dụng estrogen")
    if prior_dvt_pe: positive.append("tiền sử DVT/PE")
    if unilateral_leg_swelling: positive.append("sưng chân một bên")
    if recent_surgery_trauma_hospitalized: positive.append("phẫu thuật/chấn thương cần nhập viện trong 4 tuần")
    return {
        "applicable": True,
        "negative": len(positive) == 0,
        "positive_criteria": positive,
        "message": "PERC âm tính: không cần xét nghiệm thêm để loại trừ PE." if not positive
                   else "PERC dương tính: không thể loại trừ PE bằng PERC."
    }


def age_adjusted_ddimer_cutoff(age: float) -> float:
    """Ngưỡng ng/mL FEU (= μg/L FEU)."""
    return 500.0 if age <= 50 else age * 10.0


def years_cutoff(years_count: int) -> float:
    if years_count < 0 or years_count > 3:
        raise ValueError("YEARS phải từ 0 đến 3")
    return 1000.0 if years_count == 0 else 500.0


def ddimer_strategy_result(*, strategy: Literal["age_adjusted", "years"], age: float,
                           ddimer_feu_ng_ml: float, low_or_intermediate_pretest: bool,
                           therapeutic_anticoagulation_within_24h: bool,
                           years_count: int = 0) -> Dict[str, object]:
    if therapeutic_anticoagulation_within_24h:
        return {"usable": False, "rule_out": False,
                "message": "Không dùng chiến lược D-dimer này để tự động loại trừ PE: các nghiên cứu chính loại bệnh nhân dùng kháng đông điều trị trong 24 giờ trước."}
    if strategy == "age_adjusted":
        if not low_or_intermediate_pretest:
            return {"usable": False, "rule_out": False,
                    "message": "D-dimer hiệu chỉnh theo tuổi chỉ áp dụng cho xác suất tiền nghiệm thấp/trung bình (<50%)."}
        cutoff = age_adjusted_ddimer_cutoff(age)
    elif strategy == "years":
        if not low_or_intermediate_pretest:
            return {"usable": False, "rule_out": False,
                    "message": "Theo lưu đồ AHA/ACC 2026, xác suất tiền nghiệm cao (>50%) cần hình ảnh; không dùng YEARS để trì hoãn hình ảnh."}
        cutoff = years_cutoff(years_count)
    else:
        raise ValueError("Chiến lược D-dimer không hợp lệ")
    return {
        "usable": True,
        "cutoff": cutoff,
        "rule_out": ddimer_feu_ng_ml < cutoff,
        "message": f"D-dimer {'dưới' if ddimer_feu_ng_ml < cutoff else 'từ'} ngưỡng {cutoff:g} ng/mL FEU."
    }


def pregnancy_adapted_years_decision(*, dvt_symptoms: bool, cus_result: Literal["not_done", "negative", "positive"],
                                      hemoptysis: bool, pe_most_likely: bool,
                                      ddimer_feu_ng_ml: Optional[float]) -> Dict[str, object]:
    """Nhánh pregnancy-adapted YEARS chỉ từ logic được guideline mô tả rõ."""
    if dvt_symptoms and cus_result == "not_done":
        return {"status": "need_cus", "rule_out": False, "needs_chest_imaging": False,
                "message": "Có triệu chứng DVT: cần siêu âm chèn ép tĩnh mạch chi dưới trước."}
    if dvt_symptoms and cus_result == "positive":
        return {"status": "dvt_positive", "rule_out": False, "needs_chest_imaging": False,
                "message": "Siêu âm chèn ép dương tính: có thể điều trị kháng đông và không nhất thiết cần CTPA theo pregnancy-adapted YEARS."}
    if ddimer_feu_ng_ml is None:
        return {"status": "need_ddimer", "rule_out": False, "needs_chest_imaging": False,
                "message": "Cần D-dimer định lượng theo FEU để hoàn tất pregnancy-adapted YEARS."}
    count = sum(map(_bool, [dvt_symptoms, hemoptysis, pe_most_likely]))
    cutoff = years_cutoff(count)
    ruled_out = ddimer_feu_ng_ml < cutoff
    return {"status": "rule_out" if ruled_out else "imaging", "years_count": count, "cutoff": cutoff,
            "rule_out": ruled_out, "needs_chest_imaging": not ruled_out,
            "message": "Có thể tránh hình ảnh theo pregnancy-adapted YEARS." if ruled_out else "Không loại trừ PE bằng pregnancy-adapted YEARS; cần hình ảnh."}


def diagnostic_imaging_interpretation(result: str) -> Dict[str, object]:
    """Chỉ tự động hóa các kết quả mà guideline mô tả rõ.

    result: positive_ctpa, negative_ctpa, high_probability_vq, normal_vq_spect,
            nondiagnostic_vq, other_indeterminate
    """
    if result in {"positive_ctpa", "high_probability_vq"}:
        return {"confirmed": True, "excluded": False, "indeterminate": False}
    if result in {"negative_ctpa", "normal_vq_spect"}:
        return {"confirmed": False, "excluded": True, "indeterminate": False}
    return {"confirmed": False, "excluded": False, "indeterminate": True}


# ---------- THANG ĐIỂM TIÊN LƯỢNG ----------

def pesi_score(*, age: int, male=False, cancer=False, heart_failure=False,
               chronic_lung_disease=False, hr_ge_110=False, sbp_lt_100=False,
               rr_ge_30=False, temp_lt_36=False, altered_mental_status=False,
               spo2_lt_90=False) -> int:
    return int(age + 10*_bool(male) + 30*_bool(cancer) + 10*_bool(heart_failure)
               + 10*_bool(chronic_lung_disease) + 20*_bool(hr_ge_110)
               + 30*_bool(sbp_lt_100) + 20*_bool(rr_ge_30) + 20*_bool(temp_lt_36)
               + 60*_bool(altered_mental_status) + 20*_bool(spo2_lt_90))


def pesi_class(score: int) -> str:
    if score <= 65: return "I"
    if score <= 85: return "II"
    if score <= 105: return "III"
    if score <= 125: return "IV"
    return "V"


def pesi_low(score: int) -> bool:
    return score <= 85


def spesi_score(*, age_gt_80=False, cancer=False, chronic_cardiopulmonary_disease=False,
                sbp_lt_100=False, hr_ge_110=False, spo2_lt_90=False) -> int:
    return sum(map(_bool, [age_gt_80, cancer, chronic_cardiopulmonary_disease,
                           sbp_lt_100, hr_ge_110, spo2_lt_90]))


def bova_score(*, sbp_90_100=False, troponin_elevated=False,
               rv_dysfunction=False, hr_ge_110=False) -> int:
    return 2*_bool(sbp_90_100) + 2*_bool(troponin_elevated) + 2*_bool(rv_dysfunction) + _bool(hr_ge_110)


def bova_stage(score: int) -> str:
    if score <= 2: return "I"
    if score <= 4: return "II"
    return "III"


def hestia_positive(criteria: Dict[str, bool]) -> bool:
    # Tiêu chí phải được xây dựng đúng 11 mục ở UI/test.
    return any(bool(v) for v in criteria.values())


def cpes_score(*, troponin_elevated=False, bnp_elevated=False,
               moderate_severe_rv_dysfunction=False, saddle_pe=False,
               concomitant_dvt=False, hr_ge_100=False) -> int:
    return sum(map(_bool, [troponin_elevated, bnp_elevated, moderate_severe_rv_dysfunction,
                           saddle_pe, concomitant_dvt, hr_ge_100]))


# ---------- DẪN XUẤT NGƯỠNG HUYẾT ĐỘNG ----------

def derive_hypotension_flags(*, sbp_mm_hg: float, sbp_drop_from_baseline_mm_hg: float,
                             duration_min: float, responds_to_iv_fluids: bool,
                             recurrent: bool) -> Dict[str, bool]:
    """Dẫn xuất D1/E từ ngưỡng Figure 2, không thay thế đánh giá sốc tim."""
    hypotension_criterion = (sbp_mm_hg < 90) or (sbp_drop_from_baseline_mm_hg > 40)
    transient = hypotension_criterion and ((duration_min < 15) or responds_to_iv_fluids)
    persistent = hypotension_criterion and (duration_min >= 15) and (not responds_to_iv_fluids)
    return {
        "hypotension_criterion": hypotension_criterion,
        "transient": transient,
        "persistent": persistent,
        # recurrent=True có nghĩa là đã có các đợt tụt HA tái diễn đáp ứng định nghĩa,
        # dù thời điểm nhập số hiện tại có thể đã hồi phục huyết áp.
        "recurrent": bool(recurrent),
    }


def derive_hypoperfusion_flags(*, lactate_mmol_l: Optional[float], aki: bool,
                                urine_output_ml_kg_h: Optional[float], mental_status_change: bool,
                                cardiac_index_l_min_m2: Optional[float], map_mm_hg: Optional[float],
                                increased_shock_score_stage: bool) -> Dict[str, bool]:
    return {
        "lactate_gt_2": lactate_mmol_l is not None and lactate_mmol_l > 2,
        "acute_kidney_injury": bool(aki),
        "urine_output_lt_05_mlkg_h": urine_output_ml_kg_h is not None and urine_output_ml_kg_h < 0.5,
        "mental_status_change": bool(mental_status_change),
        "cardiac_index_lt_22": cardiac_index_l_min_m2 is not None and cardiac_index_l_min_m2 < 2.2,
        "map_lt_60": map_mm_hg is not None and map_mm_hg < 60,
        "increased_shock_score_stage": bool(increased_shock_score_stage),
    }

# ---------- PHÂN LOẠI AHA/ACC 2026 ----------
@dataclass
class ClassificationInput:
    confirmed_pe: bool
    symptomatic: bool = True
    incidental: bool = False
    clot_location: Literal["subsegmental", "segmental_or_proximal", "unknown"] = "unknown"
    severity_known: bool = False
    severity_low: Optional[bool] = None
    rv_status: Literal["normal", "abnormal", "unknown"] = "unknown"
    biomarker_status: Literal["normal", "abnormal", "unknown"] = "unknown"
    transient_hypotension: bool = False
    persistent_hypotension: bool = False
    recurrent_hypotension: bool = False
    cardiogenic_shock: bool = False
    refractory_cardiogenic_shock: bool = False
    cardiac_arrest_no_rosc_30min: bool = False
    cardiac_arrest_with_rosc_before_30min: bool = False
    lactate_gt_2: bool = False
    acute_kidney_injury: bool = False
    urine_output_lt_05_mlkg_h: bool = False
    mental_status_change: bool = False
    cardiac_index_lt_22: bool = False
    map_lt_60: bool = False
    increased_shock_score_stage: bool = False
    # Các dấu hô hấp phải là bất thường liên quan đợt PE hiện tại, không phải nền mạn tính.
    spo2_lt_90: bool = False
    rr_ge_30: bool = False
    supplemental_oxygen_for_pe: bool = False
    nasal_cannula_flow_l_min: float = 0.0
    nonrebreather: bool = False
    positive_pressure_ventilation: bool = False  # NIV hoặc IMV

@dataclass
class ClassificationResult:
    category: str
    base_category: str
    respiratory_level: Optional[str]
    complete: bool
    warnings: List[str] = field(default_factory=list)
    rationale: List[str] = field(default_factory=list)


def _hypoperfusion(i: ClassificationInput) -> bool:
    return any([
        i.lactate_gt_2, i.acute_kidney_injury, i.urine_output_lt_05_mlkg_h,
        i.mental_status_change, i.cardiac_index_lt_22, i.map_lt_60,
        i.increased_shock_score_stage,
    ])


def _resp_level(i: ClassificationInput) -> Optional[str]:
    if i.positive_pressure_ventilation:
        return "E"
    if i.nonrebreather or i.nasal_cannula_flow_l_min > 6:
        return "D"
    if i.spo2_lt_90 or i.rr_ge_30 or i.supplemental_oxygen_for_pe:
        return "C"
    return None


def _letter(cat: str) -> Optional[str]:
    if not cat:
        return None
    for ch in "ABCDE":
        if cat.startswith(ch):
            return ch
    return None


def classify_pe(i: ClassificationInput) -> ClassificationResult:
    if not i.confirmed_pe:
        return ClassificationResult("CHƯA_PHÂN_LOẠI", "CHƯA_PHÂN_LOẠI", None, False,
                                    ["Chỉ phân nhóm AHA/ACC sau khi PE được xác nhận."], [])

    warnings: List[str] = []
    rationale: List[str] = []
    hp = _hypoperfusion(i)

    # Huyết động/tim phổi nặng nhất trước.
    if i.refractory_cardiogenic_shock or i.cardiac_arrest_no_rosc_30min:
        base = "E2"
        rationale.append("Sốc tim kháng trị hoặc ngừng tuần hoàn không ROSC sau ≥30 phút.")
    elif i.cardiac_arrest_with_rosc_before_30min:
        base = "E?"
        warnings.append("Có ngừng tuần hoàn nhưng ROSC trước 30 phút. Figure 2 xếp 'cardiac arrest' dưới E2, trong khi phần diễn giải văn bản mô tả E2 khi không ROSC sau 30 phút; công cụ không tự động hạ bệnh nhân xuống nhóm B/C. Cần PERT và phân nhóm lại theo trạng thái hiện tại.")
    elif (i.persistent_hypotension or i.recurrent_hypotension) and i.cardiogenic_shock:
        base = "E1"
        rationale.append("Tụt huyết áp tái diễn/kéo dài kèm sốc tim.")
    elif i.persistent_hypotension and not i.cardiogenic_shock:
        base = "E?"
        warnings.append("Có tụt huyết áp kéo dài nhưng chưa xác nhận sốc tim: chưa đủ dữ liệu để tự động gán E1; cần đánh giá lại nguyên nhân và tưới máu.")
    elif i.cardiogenic_shock and not (i.persistent_hypotension or i.recurrent_hypotension):
        base = "D2"
        rationale.append("Có sốc/giảm tưới máu khi chưa có tụt huyết áp kéo dài: phù hợp trạng thái sốc huyết áp còn bảo tồn.")
    elif hp:
        base = "D2"
        rationale.append("Có ít nhất một chỉ dấu giảm tưới máu/rối loạn chức năng cơ quan.")
    elif i.transient_hypotension or i.recurrent_hypotension:
        base = "D1"
        rationale.append("Tụt huyết áp thoáng qua/tái diễn nhưng ngắn hoặc đáp ứng dịch, không có giảm tưới máu và không có sốc tim.")
    elif not i.symptomatic and i.incidental:
        base = "A"
        rationale.append("PE tình cờ phát hiện và không triệu chứng.")
    elif not i.symptomatic and not i.incidental:
        base = "A?"
        warnings.append("Bệnh nhân được khai là không triệu chứng nhưng PE không phải phát hiện tình cờ; dữ liệu không phù hợp định nghĩa A/B/C nên không tự động phân nhóm.")
    else:
        if not i.severity_known or i.severity_low is None:
            base = "C?"
            warnings.append("Chưa có thang điểm mức độ lâm sàng hợp lệ để phân B hay C.")
        elif i.severity_low:
            if i.clot_location == "subsegmental":
                base = "B1"
            elif i.clot_location == "segmental_or_proximal":
                base = "B2"
            else:
                base = "B?"
                warnings.append("Nguy cơ lâm sàng thấp nhưng chưa xác định vị trí huyết khối để phân B1/B2.")
        else:
            if i.rv_status == "unknown" or i.biomarker_status == "unknown":
                base = "C?"
                warnings.append("Nguy cơ lâm sàng tăng nhưng thiếu đánh giá RV hoặc biomarker để phân C1/C2/C3.")
            else:
                rv_abn = i.rv_status == "abnormal"
                bm_abn = i.biomarker_status == "abnormal"
                if not rv_abn and not bm_abn:
                    base = "C1"
                elif rv_abn and bm_abn:
                    base = "C3"
                else:
                    base = "C2"

    resp = _resp_level(i)
    base_letter = _letter(base)
    levels = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}

    # Nếu base không xác định nhưng hô hấp xác định được mức C/D/E thì dùng R độc lập.
    if resp and (base_letter is None or resp and levels[resp] > levels.get(base_letter, -1)):
        final = f"{resp}R"
        rationale.append(f"Bất thường hô hấp đạt mức {resp}-R và là chỉ dấu nặng hơn phân nhóm nền.")
    elif resp and base in {"C?", "E?"} and base_letter == resp:
        # Guideline cho phép R đứng như một phân nhóm riêng khi bất thường hô hấp nổi trội.
        final = f"{resp}R"
        rationale.append(f"Phân nhóm nền chưa hoàn tất nhưng bất thường hô hấp đủ để xác định {resp}-R độc lập.")
    elif resp and base_letter == resp:
        final = f"{base}R"
        rationale.append(f"Có modifier hô hấp R ở cùng mức {resp}.")
    else:
        final = base

    complete = "?" not in final and final != "CHƯA_PHÂN_LOẠI"
    return ClassificationResult(final, base, resp, complete, warnings, rationale)


# ---------- QUYẾT ĐỊNH NGOẠI TRÚ ----------
def outpatient_management_assessment(*, category: str, low_risk_decision_tool_confirmed: bool,
                                     immediate_anticoagulant_access: bool,
                                     rapid_reliable_expert_followup: bool,
                                     aligns_with_patient_goals: bool) -> Dict[str, object]:
    """Không dùng riêng phân nhóm A/B để quyết định xuất viện.

    AHA/ACC 2026 yêu cầu công cụ quyết định (Hestia/PESI/sPESI) và điều kiện
    tiếp cận thuốc + theo dõi tin cậy; đây chỉ trả về 'có thể cân nhắc', không phải lệnh xuất viện.
    """
    clean = category.replace("R", "")
    if clean not in {"A", "B1", "B2"}:
        return {"reasonable": False, "missing": ["Không thuộc nhóm A/B phù hợp để xem xét ngoại trú theo khuyến cáo này."]}
    missing: List[str] = []
    if not low_risk_decision_tool_confirmed:
        missing.append("Chưa xác nhận nguy cơ thấp bằng Hestia, PESI hoặc sPESI.")
    if not immediate_anticoagulant_access:
        missing.append("Chưa xác nhận có thuốc kháng đông ngay khi xuất viện.")
    if not rapid_reliable_expert_followup:
        missing.append("Chưa xác nhận kế hoạch theo dõi chuyên môn nhanh và tin cậy.")
    if not aligns_with_patient_goals:
        missing.append("Chưa xác nhận điều trị ngoại trú phù hợp mục tiêu/nguyện vọng người bệnh.")
    return {"reasonable": len(missing) == 0, "missing": missing}


# ---------- ĐIỀU TRỊ NÂNG CAO ----------
ADVANCED_THERAPY_TABLE: Dict[str, Dict[str, Tuple[str, str]]] = {
    "A-C1": {
        "Tiêu sợi huyết toàn thân": ("3: Có hại, LOE A", "Không dùng thay kháng đông đơn thuần."),
        "Tiêu sợi huyết qua catheter": ("3: Không lợi ích, LOE C-EO", "Không khuyến cáo thay kháng đông đơn thuần."),
        "Lấy huyết khối cơ học": ("3: Không lợi ích, LOE C-EO", "Không khuyến cáo thay kháng đông đơn thuần."),
        "Phẫu thuật lấy huyết khối": ("3: Không lợi ích, LOE C-EO", "Không khuyến cáo thay kháng đông đơn thuần."),
    },
    "C2": {
        "Tiêu sợi huyết toàn thân": ("3: Có hại, LOE B-R", "Không dùng thay kháng đông đơn thuần."),
        "Tiêu sợi huyết qua catheter": ("2b, LOE C-LD", "Lợi ích chưa rõ."),
        "Lấy huyết khối cơ học": ("2b, LOE C-LD", "Lợi ích chưa rõ."),
        "Phẫu thuật lấy huyết khối": ("3: Không lợi ích, LOE C-EO", "Không khuyến cáo."),
    },
    "C3": {
        "Tiêu sợi huyết toàn thân": ("2b, LOE C-LD", "Lợi ích chưa rõ; chỉ cân nhắc chọn lọc khi đang xem xét điều trị nâng cao và nguy cơ chảy máu chấp nhận được."),
        "Tiêu sợi huyết qua catheter": ("2b, LOE C-LD", "Lợi ích chưa rõ."),
        "Lấy huyết khối cơ học": ("2b, LOE C-LD", "Lợi ích chưa rõ."),
        "Phẫu thuật lấy huyết khối": ("3: Không lợi ích, LOE C-EO", "Không khuyến cáo."),
    },
    "D1-2": {
        "Tiêu sợi huyết toàn thân": ("2b, LOE C-LD", "Có thể cân nhắc khi đang xem xét điều trị nâng cao và nguy cơ chảy máu chấp nhận được."),
        "Tiêu sợi huyết qua catheter": ("2b, LOE B-NR", "Có thể cân nhắc."),
        "Lấy huyết khối cơ học": ("2b, LOE B-NR", "Có thể cân nhắc."),
        "Phẫu thuật lấy huyết khối": ("2b, LOE C-LD", "Lợi ích chưa rõ; có thể cân nhắc ở bệnh nhân chọn lọc."),
    },
    "E1": {
        "Tiêu sợi huyết toàn thân": ("2a, LOE C-LD", "Hợp lý khi nguy cơ chảy máu chấp nhận được và đang xem xét điều trị nâng cao."),
        "Tiêu sợi huyết qua catheter": ("2a, LOE C-LD", "Hợp lý."),
        "Lấy huyết khối cơ học": ("2a, LOE B-NR", "Hợp lý."),
        "Phẫu thuật lấy huyết khối": ("2a, LOE B-NR", "Hợp lý."),
    },
    "E2": {
        "Tiêu sợi huyết toàn thân": ("2a, LOE C-LD", "Hợp lý khi nguy cơ chảy máu chấp nhận được."),
        "Tiêu sợi huyết qua catheter": ("N/A", "Không có khuyến cáo phân loại trong Bảng 7 cho E2."),
        "Lấy huyết khối cơ học": ("N/A", "Không có khuyến cáo phân loại trong Bảng 7 cho E2."),
        "Phẫu thuật lấy huyết khối": ("3: Không lợi ích, LOE B-NR", "Nếu E2 chưa có hỗ trợ tuần hoàn cơ học, không khuyến cáo hơn các liệu pháp nâng cao khác."),
    },
}


def advanced_group(category: str) -> Optional[str]:
    c = category.replace("R", "")
    if c in {"A", "B1", "B2", "C1"}: return "A-C1"
    if c == "C2": return "C2"
    if c == "C3": return "C3"
    if c in {"D1", "D2"}: return "D1-2"
    if c == "E1": return "E1"
    if c == "E2": return "E2"
    # Standalone respiratory categories do not map cleanly to Table 7; do not infer.
    return None


# ---------- THUỐC / AN TOÀN ----------
@dataclass
class MedicationContext:
    absolute_contraindication_to_anticoag: bool = False
    high_bleeding_risk_nonabsolute: bool = False
    pregnant: bool = False
    breastfeeding: bool = False
    thrombotic_aps: bool = False
    single_low_risk_aps_antibody_only: bool = False
    brain_tumor: bool = False
    ckd_stage: Literal["none", "2", "3", "4", "5", "eskd"] = "none"
    crcl_ml_min: Optional[float] = None
    child_pugh: Literal["none", "A", "B", "C"] = "none"
    bariatric_surgery_within_4_weeks: bool = False
    documented_hit: bool = False
    bmi: Optional[float] = None
    weight_kg: Optional[float] = None
    interaction_review_completed: bool = False
    relevant_drug_interaction_present: bool = False
    dose_inputs_confirmed: bool = False


def anticoagulation_strategy(ctx: MedicationContext, category: str) -> Dict[str, object]:
    """Định hướng kháng đông cấp tính với các cổng an toàn trước khi hiện liều uống cụ thể.

    Nguyên tắc quan trọng: khuyến cáo chung theo nhóm A–E không được phép ghi đè
    các ngoại lệ như thai kỳ, cho con bú, APS, HIT hay suy gan/thận nặng.
    """
    out: Dict[str, object] = {"recommendations": [], "warnings": [], "exact_oral_dose_allowed": False}
    rec: List[str] = out["recommendations"]  # type: ignore
    warn: List[str] = out["warnings"]  # type: ignore

    if ctx.absolute_contraindication_to_anticoag:
        warn.append("Có chống chỉ định tuyệt đối với kháng đông: không tự động kê kháng đông; cân nhắc lưới lọc tĩnh mạch chủ dưới có thể thu hồi nếu cần, và đánh giá chuyên khoa.")
        return out

    rec.append("PE cấp đã xác nhận: khởi trị kháng đông nếu không có chống chỉ định tuyệt đối.")
    if ctx.high_bleeding_risk_nonabsolute:
        warn.append("Có nguy cơ chảy máu cao nhưng chưa phải chống chỉ định tuyệt đối: cần cân bằng lợi ích–nguy cơ và theo dõi sát; không tự động xem đây là chống chỉ định kháng đông.")

    clean = category.replace("R", "")
    hard_oral_exception = any([
        ctx.pregnant,
        ctx.breastfeeding,
        ctx.thrombotic_aps and not ctx.single_low_risk_aps_antibody_only,
        ctx.ckd_stage in {"4", "5", "eskd"},
        ctx.child_pugh in {"B", "C"},
        ctx.bariatric_surgery_within_4_weeks,
    ])

    # Khuyến cáo theo mức độ PE, nhưng không để một câu chung gây mâu thuẫn với ngoại lệ bên dưới.
    if clean in {"A", "B1", "B2"}:
        if not hard_oral_exception:
            rec.append("Nếu đủ điều kiện dùng thuốc uống và không có ngoại lệ/chống chỉ định, DOAC được ưu tiên hơn VKA; nhóm A/B thường có thể khởi trị DOAC.")
        else:
            rec.append("Nhóm A/B thường có thể dùng thuốc uống, nhưng bệnh nhân này có yếu tố đặc biệt nên phải áp dụng ngoại lệ kháng đông bên dưới thay vì tự động chọn DOAC.")
        if clean == "B1":
            warn.append("B1 là PE dưới phân thùy. Guideline nhấn mạnh vị trí huyết khối và DVT đồng thời có thể làm thay đổi quyết định ngoại trú/nhập viện và quyết định kháng đông; công cụ không tự động suy diễn chiến lược không kháng đông.")
    elif clean in {"C1", "C2", "C3", "D1", "D2", "E1"}:
        if ctx.documented_hit:
            warn.append("Khuyến cáo LMWH hơn UFH ở C1–E1 giả định heparin có thể sử dụng. Có tiền sử HIT: không tự động chọn LMWH/UFH; cần đánh giá tình trạng HIT và hướng dẫn HIT riêng.")
        else:
            rec.append("Nếu cần kháng đông đường tiêm ban đầu, LMWH được khuyến cáo hơn UFH.")
    elif clean == "E2":
        if ctx.documented_hit:
            warn.append("E2 thường cần kháng đông đường tiêm, nhưng có tiền sử HIT nên không tự động chọn LMWH/UFH; cần đánh giá theo hướng dẫn HIT riêng.")
        else:
            rec.append("E2: lựa chọn kháng đông đường tiêm cần cá thể hóa trong hồi sức/PERT; Hình 3 cho phép LMWH hoặc UFH.")
    elif clean in {"C", "D", "E"}:
        warn.append("Phân nhóm R độc lập không ánh xạ hoàn toàn vào tiểu nhóm huyết động của Figure 3; vẫn phải kháng đông nếu không chống chỉ định, nhưng lựa chọn khởi đầu cần PERT/toàn cảnh lâm sàng.")

    # Các ngoại lệ được xử lý trước khi cho phép hiện liều DOAC.
    if ctx.pregnant:
        rec.append("Thai kỳ: LMWH hoặc UFH; không dùng DOAC hoặc warfarin.")
        return out
    if ctx.breastfeeding:
        rec.append("Cho con bú: LMWH, UFH hoặc warfarin được ưu tiên hơn DOAC.")
        return out
    if ctx.thrombotic_aps and not ctx.single_low_risk_aps_antibody_only:
        rec.append("Hội chứng kháng phospholipid huyết khối: VKA được ưu tiên hơn DOAC.")
        return out
    if ctx.single_low_risk_aps_antibody_only:
        rec.append("Chỉ một kháng thể anticardiolipin hoặc β2-GPI nguy cơ thấp: DOAC có thể là lựa chọn thay thế VKA (COR 2b), nếu không có chống chỉ định khác.")
    if ctx.brain_tumor:
        rec.append("U não nguyên phát/di căn và đủ điều kiện thuốc uống: DOAC có thể được cân nhắc hơn LMWH để giảm nguy cơ xuất huyết nội sọ (COR 2b).")
    if ctx.bmi is not None and ctx.bmi > 30:
        rec.append("Béo phì BMI >30: nếu dùng thuốc uống, DOAC hợp lý hơn VKA (COR 2a).")
    if ctx.documented_hit and clean in {"A", "B1", "B2"}:
        warn.append("Tiền sử HIT: Hestia xem đây là yếu tố không phù hợp ngoại trú; nếu heparin/LMWH bị chống chỉ định, lựa chọn thuốc không heparin cần theo hướng dẫn HIT riêng.")

    if ctx.child_pugh == "C":
        warn.append("Child-Pugh C: AHA/ACC xếp DOAC là có hại; không tự động đề xuất DOAC.")
        return out
    if ctx.ckd_stage in {"4", "5", "eskd"}:
        warn.append("CKD giai đoạn 4–5/ESKD: AHA/ACC cho rằng lợi ích apixaban so với VKA còn chưa chắc chắn; không tự động chọn DOAC/liều cụ thể.")
        return out
    if ctx.child_pugh == "B":
        warn.append("Child-Pugh B: AHA/ACC nói DOAC có thể hợp lý, nhưng nhãn từng thuốc khác nhau; không tự động chọn thuốc/liều cụ thể.")
        return out
    if ctx.bariatric_surgery_within_4_weeks:
        warn.append("Trong 4 tuần sau phẫu thuật giảm béo: tránh DOAC do lo ngại hấp thu; cần chiến lược khác.")
        return out
    if ctx.crcl_ml_min is not None and ctx.crcl_ml_min < 30 and ctx.ckd_stage == "none":
        warn.append("CrCl <30 mL/phút nhưng giai đoạn CKD chưa được xác nhận; tạm không tự động chọn liều DOAC cụ thể cho đến khi làm rõ chức năng thận và nhãn thuốc.")
        return out
    if clean not in {"A", "B1", "B2"}:
        warn.append("Trong pha cấp của nhóm C–E/R nặng, công cụ không tự động hiển thị DOAC uống như lựa chọn khởi đầu; đánh giá chuyển sang thuốc uống sau ổn định.")
        return out
    if not ctx.dose_inputs_confirmed:
        warn.append("Chưa xác nhận các đầu vào dùng cho liều/độ an toàn (cân nặng, CrCl và tình trạng thận/gan); không hiển thị liều DOAC cụ thể.")
        return out
    if not ctx.interaction_review_completed:
        warn.append("Chưa xác nhận tương tác thuốc theo nhãn sản phẩm; không hiển thị liều DOAC cụ thể.")
        return out
    if ctx.relevant_drug_interaction_present:
        warn.append("Có tương tác thuốc có thể cần tránh hoặc chỉnh liều DOAC: công cụ không tự động sửa liều theo tương tác; cần đối chiếu nhãn thuốc/dược lâm sàng trước khi kê.")
        return out

    out["exact_oral_dose_allowed"] = True
    return out

def apixaban_label_vte_dose(child_pugh: str = "none") -> Dict[str, object]:
    if child_pugh == "C":
        return {"eligible": False, "reason": ["Nhãn apixaban: không khuyến cáo Child-Pugh C."]}
    if child_pugh == "B":
        return {"eligible": False, "reason": ["Nhãn apixaban: Child-Pugh B không có khuyến cáo liều do kinh nghiệm hạn chế/rối loạn đông máu nội tại."]}
    return {"eligible": True, "initiation": "10 mg uống 2 lần/ngày trong 7 ngày",
            "maintenance": "sau đó 5 mg uống 2 lần/ngày",
            "extended": "2,5 mg uống 2 lần/ngày sau ít nhất 6 tháng nếu chọn điều trị kéo dài"}


def rivaroxaban_label_vte_dose(crcl_ml_min: float, child_pugh: str = "none") -> Dict[str, object]:
    if crcl_ml_min < 15:
        return {"eligible": False, "reason": ["CrCl <15 mL/phút: tránh rivaroxaban theo nhãn."]}
    if child_pugh in {"B", "C"}:
        return {"eligible": False, "reason": ["Nhãn rivaroxaban: tránh Child-Pugh B hoặc C."]}
    out = {"eligible": True, "initiation": "15 mg uống 2 lần/ngày cùng thức ăn trong 21 ngày",
           "maintenance": "sau đó 20 mg uống 1 lần/ngày cùng thức ăn",
           "extended": "10 mg uống 1 lần/ngày sau ít nhất 6 tháng nếu chọn điều trị kéo dài"}
    if 15 <= crcl_ml_min < 30:
        out["caution"] = "CrCl 15–<30 mL/phút: dữ liệu lâm sàng hạn chế; nhãn khuyến cáo theo dõi sát dấu hiệu mất máu/chảy máu."
    return out


def dabigatran_label_vte_dose(crcl_ml_min: float) -> Dict[str, object]:
    if crcl_ml_min <= 30:
        return {"eligible": False, "reason": ["DVT/PE: nhãn dabigatran không cung cấp khuyến cáo liều khi CrCl ≤30 mL/phút."]}
    return {"eligible": True, "prerequisite": "sau 5–10 ngày kháng đông đường tiêm",
            "maintenance": "150 mg uống 2 lần/ngày"}


def edoxaban_label_vte_dose(crcl_ml_min: float, weight_kg: float, relevant_pgp_inhibitor: bool = False, child_pugh: str = "none") -> Dict[str, object]:
    if crcl_ml_min < 15:
        return {"eligible": False, "reason": ["CrCl <15 mL/phút: edoxaban không được khuyến cáo theo nhãn."]}
    if child_pugh in {"B", "C"}:
        return {"eligible": False, "reason": ["Nhãn edoxaban: không khuyến cáo Child-Pugh B hoặc C."]}
    reduce = (15 <= crcl_ml_min <= 50) or (weight_kg <= 60) or relevant_pgp_inhibitor
    return {"eligible": True, "prerequisite": "sau 5–10 ngày kháng đông đường tiêm",
            "maintenance": "30 mg uống 1 lần/ngày" if reduce else "60 mg uống 1 lần/ngày"}


def enoxaparin_label_pe_dose(weight_kg: float, crcl_ml_min: float) -> Dict[str, object]:
    if weight_kg <= 0:
        return {"eligible": False, "reason": ["Cần cân nặng hợp lệ."]}
    if crcl_ml_min < 30:
        return {"eligible": True, "dose": f"1 mg/kg SC mỗi 24 giờ (≈ {weight_kg:g} mg mỗi 24 giờ)"}
    return {"eligible": True, "dose": f"1 mg/kg SC mỗi 12 giờ (≈ {weight_kg:g} mg mỗi 12 giờ); nhãn cũng có phác đồ nội trú 1,5 mg/kg mỗi 24 giờ"}


def apixaban_vte_dose(ctx: MedicationContext) -> Dict[str, object]:
    s = anticoagulation_strategy(ctx, "B2")
    if not s["exact_oral_dose_allowed"]:
        return {"eligible": False, "reason": s["warnings"]}
    return apixaban_label_vte_dose(ctx.child_pugh)

def rivaroxaban_vte_dose(ctx: MedicationContext) -> Dict[str, object]:
    s = anticoagulation_strategy(ctx, "B2")
    if not s["exact_oral_dose_allowed"]:
        return {"eligible": False, "reason": s["warnings"]}
    if ctx.crcl_ml_min is None:
        return {"eligible": False, "reason": ["Cần CrCl để áp dụng nhãn rivaroxaban cho DVT/PE."]}
    return rivaroxaban_label_vte_dose(ctx.crcl_ml_min, ctx.child_pugh)

def dabigatran_vte_dose(ctx: MedicationContext) -> Dict[str, object]:
    s = anticoagulation_strategy(ctx, "B2")
    if not s["exact_oral_dose_allowed"]:
        return {"eligible": False, "reason": s["warnings"]}
    if ctx.crcl_ml_min is None:
        return {"eligible": False, "reason": ["Cần CrCl để áp dụng nhãn dabigatran cho DVT/PE."]}
    return dabigatran_label_vte_dose(ctx.crcl_ml_min)

def edoxaban_vte_dose(ctx: MedicationContext, relevant_pgp_inhibitor: bool = False) -> Dict[str, object]:
    s = anticoagulation_strategy(ctx, "B2")
    if not s["exact_oral_dose_allowed"]:
        return {"eligible": False, "reason": s["warnings"]}
    if ctx.crcl_ml_min is None or ctx.weight_kg is None:
        return {"eligible": False, "reason": ["Cần CrCl và cân nặng để áp dụng nhãn edoxaban."]}
    return edoxaban_label_vte_dose(ctx.crcl_ml_min, ctx.weight_kg, relevant_pgp_inhibitor, ctx.child_pugh)

def enoxaparin_pe_dose(ctx: MedicationContext) -> Dict[str, object]:
    if ctx.absolute_contraindication_to_anticoag:
        return {"eligible": False, "reason": ["Có chống chỉ định tuyệt đối với kháng đông."]}
    if ctx.documented_hit:
        return {"eligible": False, "reason": ["Có tiền sử HIT: không tự động đề xuất heparin/LMWH; xử trí HIT nằm ngoài phạm vi guideline PE này."]}
    if ctx.pregnant:
        return {"eligible": False, "reason": ["Thai kỳ: AHA/ACC khuyến cáo LMWH hoặc UFH nhưng không cung cấp một phác đồ liều thai kỳ duy nhất; thay đổi dược động học làm việc tự động hóa liều không phù hợp. Cần dùng quy trình sản khoa/huyết khối và nhãn thuốc hiện hành."]}
    if not ctx.dose_inputs_confirmed:
        return {"eligible": False, "reason": ["Chưa xác nhận cân nặng và chức năng thận dùng để tính liều enoxaparin."]}
    if ctx.weight_kg is None or ctx.weight_kg <= 0:
        return {"eligible": False, "reason": ["Cần cân nặng để tính liều enoxaparin."]}
    if ctx.crcl_ml_min is None:
        return {"eligible": False, "reason": ["Cần CrCl để kiểm tra chỉnh liều enoxaparin."]}
    label = enoxaparin_label_pe_dose(ctx.weight_kg, ctx.crcl_ml_min)
    if ctx.crcl_ml_min < 30:
        label["renal"] = "CrCl <30 mL/phút: chỉnh còn 1 lần/ngày theo nhãn; AHA/ACC: có thể theo dõi anti-Xa để hướng dẫn chỉnh liều."
    else:
        label["renal"] = "CrCl ≥30 mL/phút: không cần chỉnh liều theo nhãn."
    if ctx.bmi is not None and ctx.bmi > 40:
        label["obesity"] = "BMI >40: AHA/ACC cho rằng giảm liều LMWH có thể hợp lý; công cụ không tự giảm liều vì bằng chứng còn hạn chế và cần cá thể hóa."
    return label


def ufh_vte_initial_dose(ctx: MedicationContext) -> Dict[str, object]:
    """Liều khởi đầu UFH IV theo nomogram VTE cân nặng kinh điển (không phải liều riêng của AHA/ACC 2026).

    Nguồn dosing: Raschke et al., Ann Intern Med 1993; CHEST parenteral anticoagulant guidance;
    ASH review of acute VTE treatment. AHA/ACC 2026 chỉ quy định vị trí của UFH so với LMWH.
    Sau liều khởi đầu phải chỉnh theo aPTT/anti-Xa và nomogram của cơ sở.
    """
    if ctx.absolute_contraindication_to_anticoag:
        return {"eligible": False, "reason": ["Có chống chỉ định tuyệt đối với kháng đông."]}
    if ctx.documented_hit:
        return {"eligible": False, "reason": ["Có tiền sử/chẩn đoán HIT: không tự động dùng UFH; cần chiến lược kháng đông không heparin theo hướng dẫn HIT."]}
    if not ctx.dose_inputs_confirmed or ctx.weight_kg is None or ctx.weight_kg <= 0:
        return {"eligible": False, "reason": ["Chưa xác nhận cân nặng và dữ liệu bệnh nhân dùng để tính liều UFH."]}
    bolus = 80.0 * ctx.weight_kg
    infusion = 18.0 * ctx.weight_kg
    return {
        "eligible": True,
        "bolus_units": bolus,
        "infusion_units_per_hour": infusion,
        "dose": f"Bolus {bolus:,.0f} đơn vị IV, sau đó truyền {infusion:,.0f} đơn vị/giờ",
        "monitoring": "Kiểm tra và chỉnh liều theo aPTT hoặc anti-Xa/nomogram UFH của cơ sở; theo dõi tiểu cầu và chảy máu.",
        "note": "Nomogram khởi đầu VTE 80 đơn vị/kg bolus + 18 đơn vị/kg/giờ. Không tự làm tròn/cap liều vì quy tắc làm tròn và cap phải theo quy trình bệnh viện.",
    }


def alteplase_label_pe_dose(*, contraindications: List[str], acceptable_bleeding_risk: bool) -> Dict[str, object]:
    """Chỉ là cổng an toàn + liều theo nhãn; KHÔNG tự xác định chỉ định tiêu sợi huyết."""
    if contraindications:
        return {"eligible": False, "reason": contraindications}
    if not acceptable_bleeding_risk:
        return {"eligible": False, "reason": ["Nguy cơ chảy máu chưa được đánh giá là chấp nhận được."]}
    return {"eligible": True, "dose": "Alteplase 100 mg truyền tĩnh mạch trong 2 giờ",
            "note": "Liều chuẩn theo nhãn cho PE cấp khi đã có quyết định dùng alteplase. Guideline cho phép cân nhắc liều thấp hơn trong một số trường hợp nhưng công cụ không tự động tính liều thấp."}


def systemic_thrombolysis_decision(*, category: str, clinician_selected_systemic_lysis: bool,
                                   contraindications: List[str], acceptable_bleeding_risk: bool) -> Dict[str, object]:
    """Gộp *chỉ định theo AHA/ACC* và *cổng liều theo nhãn* để tránh hiện liều như một chỉ định tự động."""
    clean = category.replace("R", "")
    grp = advanced_group(category)
    if grp in {None, "A-C1", "C2"}:
        return {"dose_visible": False, "guideline_position": "không khuyến cáo/có hại",
                "reason": ["Phân nhóm này không phù hợp để tự động hiển thị liều tiêu sợi huyết toàn thân thay kháng đông."]}
    if grp == "C3":
        position = "C3: lợi ích tiêu sợi huyết toàn thân còn chưa chắc chắn (COR 2b, LOE C-LD)."
    elif grp == "D1-2":
        position = "D1–D2: tiêu sợi huyết toàn thân có thể được cân nhắc khi đang xem xét điều trị nâng cao và nguy cơ chảy máu chấp nhận được (COR 2b, LOE C-LD)."
    elif grp in {"E1", "E2"}:
        position = f"{clean}: tiêu sợi huyết toàn thân là lựa chọn hợp lý khi nguy cơ chảy máu chấp nhận được (COR 2a, LOE C-LD)."
    else:
        position = "Không có ánh xạ chỉ định tự động."

    if not clinician_selected_systemic_lysis:
        return {"dose_visible": False, "guideline_position": position,
                "reason": ["Chỉ hiển thị liều sau khi bác sĩ/PERT đã quyết định chọn tiêu sợi huyết toàn thân cho ca này."]}

    label = alteplase_label_pe_dose(contraindications=contraindications,
                                    acceptable_bleeding_risk=acceptable_bleeding_risk)
    if not label["eligible"]:
        return {"dose_visible": False, "guideline_position": position, "reason": label["reason"]}
    return {"dose_visible": True, "guideline_position": position,
            "dose": label["dose"], "note": label["note"], "reason": []}


# ---------- LƯỚI LỌC TĨNH MẠCH CHỦ ----------
def ivc_filter_recommendation(*, cannot_anticoagulate: bool, therapeutic_anticoagulation: bool,
                              recurrent_pe_despite_optimal_anticoag: bool,
                              category: str, undergoing_advanced_intervention: bool) -> List[str]:
    rec: List[str] = []
    if therapeutic_anticoagulation and not recurrent_pe_despite_optimal_anticoag:
        rec.append("Không đặt lưới lọc thường quy khi bệnh nhân đang được kháng đông điều trị hiệu quả (Class 3: Harm).")
    if cannot_anticoagulate:
        rec.append("Nếu cần lưới lọc vì không thể dùng kháng đông, ưu tiên loại có thể thu hồi; lấy ra sớm khi nguy cơ PE giảm và có thể dùng lại kháng đông.")
    if recurrent_pe_despite_optimal_anticoag and _letter(category.replace("R", "")) in {"B", "C", "D", "E"}:
        rec.append("PE tái phát dù kháng đông tối ưu ở B–E: có thể cân nhắc lưới lọc (2b).")
    if undergoing_advanced_intervention and _letter(category.replace("R", "")) in {"D", "E"}:
        rec.append("D–E đang can thiệp nâng cao: lợi ích đặt lưới lọc thường quy chưa chắc chắn (2b).")
    return rec


# ---------- THEO DÕI ----------
def extended_anticoagulation_plan(risk_factor: Literal["none", "major_reversible", "minor_reversible", "persistent"],
                                  cancer: bool, doac_contraindicated_or_refused: bool) -> List[str]:
    out = ["Pha điều trị ban đầu: 3–6 tháng."]
    if risk_factor == "major_reversible":
        out.append("Yếu tố nguy cơ đảo ngược lớn: khuyến cáo dừng kháng đông cuối pha 3–6 tháng.")
    elif risk_factor == "minor_reversible":
        out.append("Yếu tố nguy cơ đảo ngược nhỏ: quyết định chung về dừng hay kéo dài sau 3–6 tháng.")
    elif risk_factor == "none":
        out.append("Không xác định được yếu tố nguy cơ: khuyến cáo tiếp tục kháng đông sang pha kéo dài nếu không có chống chỉ định.")
    elif risk_factor == "persistent":
        out.append("Có yếu tố nguy cơ dai dẳng: tiếp tục kháng đông sang pha kéo dài là hợp lý nếu lợi ích vượt nguy cơ.")
    if cancer:
        out.append("Nếu điều trị kéo dài và có ung thư: DOAC hoặc LMWH được ưu tiên hơn VKA.")
    elif doac_contraindicated_or_refused:
        out.append("Không ung thư, có chống chỉ định DOAC nhưng vẫn cần pha kéo dài: VKA được ưu tiên hơn aspirin/không điều trị; nếu từ chối/chống chỉ định mọi kháng đông, aspirin liều thấp hợp lý hơn không điều trị.")
    else:
        out.append("Nếu điều trị kéo dài: DOAC được ưu tiên hơn VKA; apixaban hoặc rivaroxaban liều giảm một nửa được khuyến cáo để giảm chảy máu khi phù hợp.")
    return out


# ---------- STREAMLIT UI ----------
def run_app() -> None:
    import streamlit as st

    st.set_page_config(page_title="CDSS thuyên tắc phổi cấp AHA/ACC 2026", layout="wide")
    st.title("🩺 CDSS THUYÊN TẮC PHỔI CẤP — AHA/ACC 2026")
    st.caption("Công cụ hỗ trợ bác sĩ; không thay thế đánh giá lâm sàng, PERT, nhãn thuốc hoặc quy trình bệnh viện.")
    st.info("Phạm vi: người lớn ≥18 tuổi. Mọi liều thuốc cụ thể phải được đối chiếu nhãn sản phẩm, chống chỉ định và tương tác trước khi dùng.")

    tab1, tab2, tab3 = st.tabs(["1. Nghi ngờ / xác nhận PE", "2. Phân tầng AHA/ACC", "3. Điều trị ban đầu"])

    with tab1:
        st.header("1. Tiếp cận chẩn đoán PE cấp")
        pregnant = st.checkbox("Đang mang thai", key="dx_preg")
        on_ac = st.checkbox("Đã dùng kháng đông liều điều trị trong 24 giờ trước", key="dx_ac24")

        st.subheader("Xác suất tiền nghiệm")
        st.caption("Trước khi áp dụng thang điểm, cần bệnh sử có mục tiêu và khám toàn diện để xác định xác suất tiền nghiệm; thang điểm không thay thế đánh giá lâm sàng.")
        pretest_method = st.selectbox("Phương pháp đánh giá", ["Wells", "Geneva giản lược", "Đánh giá lâm sàng"], key="dx_method")
        very_low = False
        nonhigh = True
        high = False
        pretest_uncertain = False
        if pretest_method == "Wells":
            w1 = st.checkbox("Dấu hiệu lâm sàng DVT", key="w1")
            w2 = st.checkbox("PE khả dĩ hơn chẩn đoán khác", key="w2")
            w3 = st.checkbox("Nhịp tim >100/phút", key="w3")
            w4 = st.checkbox("Bất động ≥3 ngày hoặc phẫu thuật trong 4 tuần", key="w4")
            w5 = st.checkbox("Tiền sử DVT/PE", key="w5")
            w6 = st.checkbox("Ho ra máu", key="w6")
            w7 = st.checkbox("Ung thư", key="w7")
            ws = wells_score(dvt_signs=w1, pe_most_likely=w2, hr_gt_100=w3, immobilization_or_surgery=w4, prior_dvt_pe=w5, hemoptysis=w6, cancer=w7)
            wc = wells_category(ws)
            st.write(f"Wells = **{ws:g}** — nguy cơ {wc}; phân loại 2 mức: **{wells_modified(ws)}**")
            very_low = ws < 2
            high = ws > 6
            nonhigh = not high
        elif pretest_method == "Geneva giản lược":
            g_age = st.checkbox("Tuổi >65", key="g_age")
            g_prev = st.checkbox("Tiền sử DVT/PE", key="g_prev")
            g_surg = st.checkbox("Phẫu thuật gây mê hoặc gãy chi dưới trong 1 tháng", key="g_surg")
            g_ca = st.checkbox("Ung thư hoạt động", key="g_ca")
            g_leg = st.checkbox("Đau một bên chi dưới", key="g_leg")
            g_hemo = st.checkbox("Ho ra máu", key="g_hemo")
            g_hr = st.selectbox("Nhịp tim", ["<75", "75–94", "≥95"], key="g_hr")
            g_dvt = st.checkbox("Đau khi ấn tĩnh mạch sâu và phù một bên", key="g_dvt")
            gs = simplified_geneva_score(age_gt_65=g_age, prior_dvt_pe=g_prev, surgery_or_lower_limb_fracture=g_surg, active_cancer=g_ca, unilateral_leg_pain=g_leg, hemoptysis=g_hemo, hr_75_94=(g_hr=="75–94"), hr_ge_95=(g_hr=="≥95"), deep_vein_tenderness_and_unilateral_edema=g_dvt)
            gc = simplified_geneva_category(gs)
            st.write(f"Geneva giản lược = **{gs}** — nguy cơ {gc}")
            high = gs >= 5
            nonhigh = not high
            very_low = st.checkbox("Bác sĩ đánh giá xác suất thực sự <15% để xét PERC", key="g_gestalt15") if not pregnant else False
        else:
            gestalt = st.selectbox("Đánh giá xác suất lâm sàng", ["<15%", "15–<50%", ">50%", "quanh 50%/không chắc"], key="dx_gestalt")
            very_low = gestalt == "<15%"
            high = gestalt == ">50%"
            nonhigh = gestalt in {"<15%", "15–<50%"}
            if gestalt == "quanh 50%/không chắc":
                pretest_uncertain = True
                st.warning("Xác suất quanh ngưỡng 50% hoặc chưa chắc chắn: không tự động áp dụng D-dimer hiệu chỉnh theo tuổi; cần đánh giá lâm sàng và cân nhắc hình ảnh.")

        pretest_confirmed = st.checkbox("Đã nhập và xác nhận đầy đủ dữ liệu dùng để xác định xác suất tiền nghiệm; không dùng các giá trị mặc định", key="dx_pretest_ok")
        if not pretest_confirmed:
            st.warning("Chưa xác nhận dữ liệu xác suất tiền nghiệm: hệ thống không tự động dùng PERC, D-dimer hoặc pregnancy-adapted YEARS để loại trừ PE.")

        perc_ruled_out = False
        if pretest_confirmed and very_low and not pregnant:
            st.subheader("PERC")
            age = st.number_input("Tuổi", 18, 120, 49, key="perc_age")
            hr = st.number_input("Nhịp tim (/phút)", 20, 250, 80, key="perc_hr")
            spo2 = st.number_input("SpO₂ (%)", 50, 100, 98, key="perc_spo2")
            perc_h = st.checkbox("Ho ra máu", key="perc_h")
            perc_e = st.checkbox("Đang sử dụng estrogen", key="perc_e")
            perc_prev = st.checkbox("Tiền sử DVT/PE", key="perc_prev")
            perc_leg = st.checkbox("Sưng chân một bên", key="perc_leg")
            perc_surg = st.checkbox("Phẫu thuật/chấn thương cần nhập viện trong 4 tuần", key="perc_surg")
            perc_inputs_ok = st.checkbox("Đã nhập và xác nhận đủ 8 tiêu chí PERC", key="perc_inputs_ok")
            if perc_inputs_ok:
                pperc = perc_result(
                    gestalt_lt_15=True, age=age, hr=hr, spo2=spo2,
                    hemoptysis=perc_h, estrogen_use=perc_e, prior_dvt_pe=perc_prev,
                    unilateral_leg_swelling=perc_leg, recent_surgery_trauma_hospitalized=perc_surg,
                )
                perc_ruled_out = bool(pperc["negative"])
                st.success(pperc["message"]) if perc_ruled_out else st.warning(pperc["message"])
            else:
                st.info("PERC chưa được diễn giải cho đến khi xác nhận đủ 8 tiêu chí.")

        needs_imaging = False
        pregnancy_dvt_treat = False
        if not pretest_confirmed:
            st.info("Hãy hoàn tất và xác nhận xác suất tiền nghiệm trước khi hệ thống diễn giải chiến lược loại trừ PE.")
        elif high:
            st.error("Xác suất tiền nghiệm cao: cần hình ảnh để xác nhận hoặc loại trừ PE; không dùng D-dimer để trì hoãn hình ảnh.")
            needs_imaging = True
        elif pretest_uncertain:
            needs_imaging = True
        elif perc_ruled_out:
            st.success("Đã loại trừ PE bằng PERC trong đúng quần thể áp dụng; không cần D-dimer/hình ảnh vì PE.")
        elif on_ac:
            st.warning("Không tự động dùng D-dimer để loại trừ PE vì bệnh nhân đã dùng kháng đông điều trị trong 24 giờ trước; quyết định hình ảnh dựa vào xác suất lâm sàng và bối cảnh.")
            needs_imaging = True
        elif pregnant:
            st.subheader("YEARS hiệu chỉnh cho thai kỳ")
            dvt_sym = st.checkbox("Có triệu chứng chi dưới gợi ý DVT", key="preg_dvt")
            cus = "không cần"
            if dvt_sym:
                cus = st.selectbox("Siêu âm chèn ép tĩnh mạch chi dưới", ["chưa làm", "âm tính", "dương tính"], key="preg_cus")
                if cus == "dương tính":
                    pregnancy_dvt_treat = True
                    st.success("DVT dương tính: có thể điều trị kháng đông và không nhất thiết cần CTPA theo pregnancy-adapted YEARS. Không tự động gán phân nhóm PE AHA/ACC nếu chưa có bằng chứng PE trực tiếp.")
                elif cus == "chưa làm":
                    st.warning("Có triệu chứng DVT: nên hoàn tất siêu âm chèn ép trước khi đi tiếp trong pregnancy-adapted YEARS.")
            if not pregnancy_dvt_treat and (not dvt_sym or cus == "âm tính"):
                y2 = st.checkbox("Ho ra máu", key="preg_y2")
                y3 = st.checkbox("PE là chẩn đoán khả dĩ nhất", key="preg_y3")
                dd = st.number_input("D-dimer (ng/mL FEU)", min_value=0.0, value=500.0, key="preg_dd")
                preg_years_ok = st.checkbox("Đã xác nhận các tiêu chí YEARS và kết quả D-dimer của thai phụ; không dùng giá trị mặc định", key="preg_years_ok")
                if preg_years_ok:
                    pr = pregnancy_adapted_years_decision(
                        dvt_symptoms=dvt_sym, cus_result="negative" if cus == "âm tính" else "not_done",
                        hemoptysis=y2, pe_most_likely=y3, ddimer_feu_ng_ml=dd)
                    if "cutoff" in pr:
                        st.write(f"Ngưỡng YEARS: **{pr['cutoff']:g} ng/mL FEU**")
                    if pr["rule_out"]:
                        st.success(str(pr["message"]))
                    elif pr["status"] == "imaging":
                        st.warning(str(pr["message"]))
                        needs_imaging = True
                        cxr_normal = st.checkbox("X-quang ngực bình thường", key="preg_cxr")
                        if cxr_normal:
                            st.info("Thai kỳ + YEARS không loại trừ + X-quang ngực bình thường: CTPA liều bức xạ thấp là lựa chọn hợp lý hơn xạ hình tưới máu liều thấp theo hướng dẫn 2026.")
                else:
                    st.info("Chưa diễn giải pregnancy-adapted YEARS cho đến khi xác nhận dữ liệu.")
        else:
            strategy_label = st.radio("Chọn MỘT chiến lược D-dimer", ["Hiệu chỉnh theo tuổi", "YEARS"], key="dd_strategy")
            age = st.number_input("Tuổi", 18, 120, 55, key="dd_age")
            dd = st.number_input("D-dimer (ng/mL FEU)", min_value=0.0, value=500.0, key="dd_val")
            y1 = y2 = y3 = False
            if strategy_label == "YEARS":
                y1 = st.checkbox("Dấu hiệu lâm sàng DVT", key="y1")
                y2 = st.checkbox("Ho ra máu", key="y2")
                y3 = st.checkbox("PE là chẩn đoán khả dĩ nhất", key="y3")
            dd_inputs_ok = st.checkbox("Đã xác nhận tuổi, kết quả D-dimer và các tiêu chí của chiến lược đang chọn; không dùng giá trị mặc định", key="dd_inputs_ok")
            if dd_inputs_ok:
                if strategy_label == "Hiệu chỉnh theo tuổi":
                    r = ddimer_strategy_result(strategy="age_adjusted", age=age, ddimer_feu_ng_ml=dd, low_or_intermediate_pretest=nonhigh, therapeutic_anticoagulation_within_24h=False)
                else:
                    yc = sum(map(_bool, [y1, y2, y3]))
                    r = ddimer_strategy_result(strategy="years", age=age, ddimer_feu_ng_ml=dd, low_or_intermediate_pretest=nonhigh, therapeutic_anticoagulation_within_24h=False, years_count=yc)
                if r["usable"]:
                    st.write(f"Ngưỡng đang áp dụng: **{r['cutoff']:g} ng/mL FEU**")
                    if r["rule_out"]:
                        st.success("Dưới ngưỡng: có thể loại trừ PE, không cần hình ảnh theo chiến lược đã chọn.")
                    else:
                        st.warning("Không loại trừ PE bằng D-dimer; cần hình ảnh.")
                        needs_imaging = True
            else:
                st.info("Chưa diễn giải D-dimer cho đến khi xác nhận dữ liệu đầu vào.")

        if needs_imaging:
            cannot_ctpa = st.checkbox("Không thể thực hiện CTPA", key="dx_no_ctpa")
            if cannot_ctpa:
                st.info("Khi không thể CTPA, V/Q được ưu tiên hơn MRA; nếu có điều kiện, V/Q SPECT hợp lý hơn V/Q planar.")
            else:
                st.info("CTPA là phương tiện hình ảnh được ưu tiên để xác nhận PE.")

        st.subheader("Kết quả hình ảnh")
        img = st.selectbox("Kết quả xét nghiệm hình ảnh chuyên biệt", [
            "Chưa có/không xác định", "CTPA dương tính", "CTPA âm tính", "V/Q xác suất cao", "V/Q SPECT bình thường", "V/Q không chẩn đoán"
        ], key="img_result")
        mapping = {"CTPA dương tính":"positive_ctpa", "CTPA âm tính":"negative_ctpa", "V/Q xác suất cao":"high_probability_vq",
                   "V/Q SPECT bình thường":"normal_vq_spect", "V/Q không chẩn đoán":"nondiagnostic_vq", "Chưa có/không xác định":"other_indeterminate"}
        interp = diagnostic_imaging_interpretation(mapping[img])
        st.session_state["pe_confirmed"] = bool(interp["confirmed"])
        if interp["confirmed"]:
            st.success("PE đã được xác nhận. Có thể chuyển sang phân tầng AHA/ACC.")
            if img == "CTPA dương tính":
                st.info("Khi CTPA xác nhận PE: nên báo cáo tỷ số RV/LV bằng số để phân tầng; có thể mô tả các dấu hiệu mạn tính (web nội mạch, co kéo/giãn động mạch phổi, giãn động mạch phế quản, phì đại RV, dẹt vách liên thất) để nhận diện nguy cơ di chứng mạn.")
            dvt_reason = st.checkbox("Có dấu hiệu DVT hoặc kết quả siêu âm tĩnh mạch chi dưới sẽ thay đổi xử trí/tiên lượng", key="dx_duplex_reason")
            if dvt_reason:
                st.info("Sau khi PE đã xác nhận, siêu âm duplex tĩnh mạch chi dưới có thể hợp lý nếu nghi DVT hoặc kết quả sẽ thay đổi xử trí/tiên lượng.")
        elif interp["excluded"]:
            st.success("Kết quả hình ảnh chuyên biệt đủ để loại trừ PE trong bối cảnh phù hợp.")
        else:
            st.warning("Chưa có kết luận PE. Không tự động chuyển sang phác đồ điều trị PE xác định.")
        st.caption("Siêu âm tim không được dùng đơn độc để xác nhận hoặc loại trừ PE. Sau CTPA âm tính hoặc V/Q SPECT bình thường, siêu âm tĩnh mạch chi dưới không hữu ích chỉ để tiếp tục chẩn đoán PE.")
        st.caption("Nếu làm siêu âm tim để phân tầng RV, nên đánh giá/báo cáo đầy đủ theo khả năng: RV/LV cuối tâm trương, đường kính RV cuối tâm trương, TAPSE, áp lực tâm thu RV ước tính, dấu McConnell, vận tốc tâm thu vòng van ba lá, vận động nghịch thường vách liên thất và độ xẹp IVC theo hô hấp.")

        with st.expander("Kháng đông khi đang chờ hình ảnh"):
            suspected_c2_plus = st.checkbox("Lâm sàng nghi PE mức C2 trở lên", key="emp_c2")
            imaging_delayed = st.checkbox("Hình ảnh bị trì hoãn/không tiếp cận ngay", key="emp_delay")
            low_bleed = st.checkbox("Nguy cơ chảy máu thấp", key="emp_bleed")
            if suspected_c2_plus and imaging_delayed and low_bleed and not interp["confirmed"]:
                st.info("Có thể có lợi khi dùng kháng đông điều trị trong lúc chờ hình ảnh (COR 2a, LOE C-EO). Đây không phải xác nhận chẩn đoán PE và không mở phân nhóm AHA/ACC tự động.")

    with tab2:
        st.header("2. Phân tầng AHA/ACC 2026")
        confirmed = bool(st.session_state.get("pe_confirmed", False))
        if not confirmed:
            st.warning("Chưa xác nhận PE ở phần Chẩn đoán; hệ thống khóa khuyến cáo điều trị theo phân nhóm.")

        symptomatic = st.checkbox("PE có triệu chứng", value=True, key="cls_symp")
        incidental = st.checkbox("PE tình cờ phát hiện", value=False, key="cls_inc")
        location = st.selectbox("Vị trí huyết khối", ["chưa rõ", "dưới phân thùy", "phân thùy hoặc gần hơn"], key="cls_loc")
        locmap = {"chưa rõ":"unknown", "dưới phân thùy":"subsegmental", "phân thùy hoặc gần hơn":"segmental_or_proximal"}

        st.subheader("Dữ liệu lâm sàng và thang điểm")
        c1, c2, c3 = st.columns(3)
        with c1:
            age_r = st.number_input("Tuổi", 18, 120, 60, key="risk_age")
            male = st.checkbox("Giới tính nam", key="risk_male")
            cancer = st.checkbox("Ung thư", key="risk_ca")
            hf = st.checkbox("Tiền sử suy tim", key="risk_hf")
            lung = st.checkbox("Bệnh phổi mạn", key="risk_lung")
        with c2:
            hr_r = st.number_input("Nhịp tim (/phút)", 20, 250, 90, key="risk_hr")
            sbp_r = st.number_input("Huyết áp tâm thu hiện tại (mmHg)", 30.0, 250.0, 120.0, key="risk_sbp")
            rr_r = st.number_input("Nhịp thở (/phút)", 5, 80, 20, key="risk_rr")
            temp_r = st.number_input("Nhiệt độ (°C)", 30.0, 43.0, 37.0, key="risk_temp")
            spo2_r = st.number_input("SpO₂ (%)", 50.0, 100.0, 96.0, key="risk_spo2")
        with c3:
            ams_r = st.checkbox("Thay đổi tri giác", key="risk_ams")
            rv = st.selectbox("Kích thước/chức năng thất phải", ["chưa biết", "bình thường", "bất thường"], key="cls_rv")
            trop = st.selectbox("Troponin", ["chưa đo", "bình thường", "tăng"], key="risk_trop")
            bnp = st.selectbox("BNP/NT-proBNP", ["chưa đo", "bình thường", "tăng"], key="risk_bnp")
            saddle = st.checkbox("Huyết khối cưỡi ngựa", key="risk_saddle")
            concom_dvt = st.checkbox("Có DVT đồng thời", key="risk_dvt")

        pesi = pesi_score(age=int(age_r), male=male, cancer=cancer, heart_failure=hf, chronic_lung_disease=lung,
                          hr_ge_110=hr_r >= 110, sbp_lt_100=sbp_r < 100, rr_ge_30=rr_r >= 30,
                          temp_lt_36=temp_r < 36, altered_mental_status=ams_r, spo2_lt_90=spo2_r < 90)
        spesi = spesi_score(age_gt_80=age_r > 80, cancer=cancer, chronic_cardiopulmonary_disease=(hf or lung),
                            sbp_lt_100=sbp_r < 100, hr_ge_110=hr_r >= 110, spo2_lt_90=spo2_r < 90)
        rv_abn = rv == "bất thường"
        trop_abn = trop == "tăng"
        bova = bova_score(sbp_90_100=(90 <= sbp_r <= 100), troponin_elevated=trop_abn,
                          rv_dysfunction=rv_abn, hr_ge_110=hr_r >= 110)
        cpes = cpes_score(troponin_elevated=trop_abn, bnp_elevated=(bnp == "tăng"),
                          moderate_severe_rv_dysfunction=rv_abn, saddle_pe=saddle,
                          concomitant_dvt=concom_dvt, hr_ge_100=hr_r >= 100)

        with st.expander("Tiêu chí Hestia"):
            h_unstable = st.checkbox("Huyết động không ổn định", key="hes_unstable")
            h_reperf = st.checkbox("Cần tiêu sợi huyết hoặc lấy huyết khối", key="hes_reperf")
            h_bleed = st.checkbox("Đang chảy máu hoặc nguy cơ chảy máu cao", key="hes_bleed")
            h_o2 = st.checkbox("Cần oxy >24 giờ để duy trì SpO₂ >90%", key="hes_o2")
            h_onac = st.checkbox("PE được chẩn đoán trong khi đang điều trị kháng đông", key="hes_onac")
            h_pain = st.checkbox("Đau nặng cần giảm đau tĩnh mạch >24 giờ", key="hes_pain")
            h_social = st.checkbox("Lý do y khoa/xã hội cần nằm viện >24 giờ", key="hes_social")
            h_crcl = st.checkbox("CrCl <30 mL/phút", key="hes_crcl")
            h_liver = st.checkbox("Suy gan nặng", key="hes_liver")
            h_preg = st.checkbox("Mang thai", key="hes_preg")
            h_hit = st.checkbox("Tiền sử HIT đã xác nhận", key="hes_hit")
            h_reviewed = st.checkbox("Đã rà soát đầy đủ cả 11 tiêu chí Hestia", key="hes_reviewed")
        hestia = hestia_positive({
            "unstable":h_unstable,"reperfusion":h_reperf,"bleeding":h_bleed,"oxygen":h_o2,
            "on_anticoag":h_onac,"pain":h_pain,"medical_social":h_social,"crcl":h_crcl,
            "liver":h_liver,"pregnancy":h_preg,"hit":h_hit})

        st.write(f"**PESI:** {pesi} điểm — lớp {pesi_class(pesi)} | **sPESI:** {spesi} | **Bova:** {bova} — giai đoạn {bova_stage(bova)} | **CPES:** {cpes}/6 | **Hestia:** {'dương tính' if hestia else 'âm tính'}")
        st.caption("Ở bệnh nhân C–D huyết động ổn định, NEWS/NEWS2 có thể là lựa chọn thay thế cho thang điểm đặc hiệu PE để nhận diện nguy cơ diễn tiến xấu. Công cụ không tự tính NEWS/NEWS2 vì guideline PE này không cung cấp bảng chấm điểm chi tiết đầy đủ.")
        st.caption("Không dùng định lượng tổng gánh huyết khối trên chụp mạch để phân tầng nguy cơ ngắn hạn cho nhóm A–C. Huyết khối cưỡi ngựa chỉ được dùng ở đây như một thành phần của CPES, không phải thước đo gánh huyết khối độc lập.")
        primary = st.selectbox("Thang điểm dùng làm chỉ số mức độ lâm sàng chính cho phân nhóm", ["PESI", "sPESI", "Bova", "Hestia"], key="risk_primary")
        risk_inputs_confirmed = st.checkbox("Đã nhập và xác nhận đầy đủ dữ liệu của thang điểm mức độ đang chọn; không dùng các giá trị mặc định", key="risk_inputs_ok")
        if primary == "PESI":
            sev_low = pesi <= 85
            sev_known = risk_inputs_confirmed
        elif primary == "sPESI":
            sev_low = spesi == 0
            sev_known = risk_inputs_confirmed
        elif primary == "Bova":
            # Bova cần biết SBP/HR, troponin và tình trạng RV; không được mặc định dữ liệu chưa xác nhận = 0 điểm.
            sev_low = bova <= 4
            sev_known = risk_inputs_confirmed and trop != "chưa đo" and rv != "chưa biết"
            if not sev_known:
                st.warning("Chưa đủ dữ liệu để dùng Bova làm chỉ số mức độ chính: cần xác nhận sinh hiệu, troponin và đánh giá thất phải. Hệ thống sẽ không tự động phân B/C.")
        else:
            sev_low = not hestia
            sev_known = h_reviewed
            if not h_reviewed:
                st.warning("Chưa xác nhận đã rà soát đủ 11 tiêu chí Hestia; hệ thống sẽ không tự động dùng Hestia để phân B/C.")
            if hestia:
                st.warning("Hestia dương tính có thể do lý do y khoa/xã hội không phản ánh trực tiếp sinh lý PE; guideline cũng xem Hestia là công cụ chọn ngoại trú. Hãy diễn giải cùng toàn cảnh lâm sàng.")
        if primary in {"PESI", "sPESI", "Bova"} and not risk_inputs_confirmed:
            st.info("Điểm đang hiển thị chỉ là phép tính từ các ô hiện tại; chưa được dùng để phân nhóm cho đến khi xác nhận dữ liệu.")

        # Biomarker cho C1/C2/C3: guideline yêu cầu ít nhất 1 dấu ấn sinh học tim ở nhóm C.
        if trop == "tăng" or bnp == "tăng":
            bm_status = "abnormal"
        elif (trop == "bình thường" or bnp == "bình thường") and trop != "tăng" and bnp != "tăng":
            bm_status = "normal"
        else:
            bm_status = "unknown"
        rvmap = {"chưa biết":"unknown", "bình thường":"normal", "bất thường":"abnormal"}

        st.subheader("Huyết động và giảm tưới máu")
        h1, h2, h3 = st.columns(3)
        with h1:
            sbp_drop = st.number_input("Mức giảm SBP so với nền (mmHg)", min_value=0.0, max_value=150.0, value=0.0, key="hd_drop")
            hypotension_duration = st.number_input("Thời gian đợt tụt HA hiện tại (phút)", min_value=0.0, max_value=240.0, value=0.0, key="hd_duration")
            fluid_response = st.checkbox("Tụt HA đáp ứng với dịch tĩnh mạch", key="hd_fluid")
            recurrent = st.checkbox("Đã có các đợt tụt HA tái diễn đạt tiêu chuẩn SBP <90 mmHg hoặc giảm >40 mmHg so với nền VÀ các đợt này ngắn hoặc đáp ứng dịch", key="hd_recurrent")
        with h2:
            shock = st.checkbox("Có sốc tim", key="cls_shock")
            refractory = st.checkbox("Sốc tim kháng trị", key="cls_refract")
            arrest30 = st.checkbox("Ngừng tuần hoàn không ROSC sau ≥30 phút hồi sức", key="cls_arrest")
            arrest_rosc_early = st.checkbox("Đã ngừng tuần hoàn nhưng ROSC trước 30 phút", key="cls_arrest_rosc_early")
            aki = st.checkbox("Tổn thương thận cấp", key="cls_aki")
            ams = st.checkbox("Thay đổi tri giác do giảm tưới máu", key="cls_ams")
        with h3:
            lact_measured = st.checkbox("Đã đo lactate", key="hd_lact_m")
            lact_val = st.number_input("Lactate (mmol/L)", min_value=0.0, max_value=30.0, value=1.0, key="hd_lact") if lact_measured else None
            uo_measured = st.checkbox("Đã đánh giá nước tiểu mL/kg/giờ", key="hd_uo_m")
            uo_val = st.number_input("Nước tiểu (mL/kg/giờ)", min_value=0.0, max_value=10.0, value=1.0, key="hd_uo") if uo_measured else None
            ci_measured = st.checkbox("Đã đo chỉ số tim", key="hd_ci_m")
            ci_val = st.number_input("Chỉ số tim (L/phút/m²)", min_value=0.0, max_value=10.0, value=2.5, key="hd_ci") if ci_measured else None
            map_measured = st.checkbox("Đã đo MAP", key="hd_map_m")
            map_val = st.number_input("MAP (mmHg)", min_value=0.0, max_value=180.0, value=80.0, key="hd_map") if map_measured else None
            scai_increased = st.checkbox("SCAI SHOCK tăng (B/C) hoặc đánh giá tương đương", key="hd_scai")

        hypotension = derive_hypotension_flags(sbp_mm_hg=sbp_r, sbp_drop_from_baseline_mm_hg=sbp_drop,
                                               duration_min=hypotension_duration, responds_to_iv_fluids=fluid_response,
                                               recurrent=recurrent)
        hypoperfusion = derive_hypoperfusion_flags(lactate_mmol_l=lact_val, aki=aki,
                                                    urine_output_ml_kg_h=uo_val, mental_status_change=ams,
                                                    cardiac_index_l_min_m2=ci_val, map_mm_hg=map_val,
                                                    increased_shock_score_stage=(scai_increased or cpes == 6))

        st.subheader("Hô hấp liên quan PE hiện tại")
        r1, r2 = st.columns(2)
        with r1:
            supp = st.checkbox("Cần oxy bổ sung vì PE", key="cls_o2")
            flow = st.number_input("Lưu lượng oxy qua ống thông mũi (L/phút)", min_value=0.0, max_value=30.0, value=0.0, key="cls_flow")
            nrb = st.checkbox("Đang dùng mặt nạ không thở lại", key="cls_nrb")
        with r2:
            ppv = st.checkbox("Cần thông khí áp lực dương (NIV hoặc xâm lấn)", key="cls_ppv")
            st.caption("Ngưỡng C-R dùng SpO₂ <90%, nhịp thở ≥30 hoặc cần oxy; D-R dùng >6 L/phút ống thông mũi hoặc mặt nạ không thở lại; E-R dùng thông khí áp lực dương.")

        ci_obj = ClassificationInput(
            confirmed_pe=confirmed, symptomatic=symptomatic, incidental=incidental,
            clot_location=locmap[location], severity_known=sev_known, severity_low=sev_low,
            rv_status=rvmap[rv], biomarker_status=bm_status,
            transient_hypotension=hypotension["transient"], persistent_hypotension=hypotension["persistent"],
            recurrent_hypotension=hypotension["recurrent"], cardiogenic_shock=shock,
            refractory_cardiogenic_shock=refractory, cardiac_arrest_no_rosc_30min=arrest30, cardiac_arrest_with_rosc_before_30min=arrest_rosc_early,
            lactate_gt_2=hypoperfusion["lactate_gt_2"], acute_kidney_injury=hypoperfusion["acute_kidney_injury"],
            urine_output_lt_05_mlkg_h=hypoperfusion["urine_output_lt_05_mlkg_h"],
            mental_status_change=hypoperfusion["mental_status_change"],
            cardiac_index_lt_22=hypoperfusion["cardiac_index_lt_22"], map_lt_60=hypoperfusion["map_lt_60"],
            increased_shock_score_stage=hypoperfusion["increased_shock_score_stage"],
            spo2_lt_90=spo2_r < 90, rr_ge_30=rr_r >= 30, supplemental_oxygen_for_pe=supp,
            nasal_cannula_flow_l_min=flow, nonrebreather=nrb, positive_pressure_ventilation=ppv,
        )
        result = classify_pe(ci_obj)
        st.session_state["pe_category"] = result.category if result.complete else None
        st.session_state["cardiogenic_shock"] = shock
        st.session_state["reduced_preload_concern"] = st.checkbox("Có lo ngại giảm tiền tải cần cân nhắc bù dịch thận trọng", key="hd_preload")
        st.subheader(f"Kết quả phân nhóm: {result.category}")
        for x in result.rationale: st.write("• " + x)
        for w in result.warnings: st.warning(w)
        result_letter = _letter(result.category.replace("R", ""))
        if result.category.startswith("C") and result.category not in {"CR", "C?"}:
            st.info("Nhóm C: cần ít nhất 1 dấu ấn sinh học tim để hỗ trợ phân tầng ngắn hạn.")
        if result_letter in {"C", "D", "E"} and not lact_measured:
            st.warning("AHA/ACC 2026 khuyến cáo đo lactate ở PE nhóm C–E tại cơ sở cấp cứu để hỗ trợ phân tầng nguy cơ ngắn hạn.")
        if result_letter in {"C", "D"} and rv == "chưa biết":
            st.warning("Nhóm C–D: khuyến cáo đánh giá kích thước/chức năng thất phải; siêu âm tim được ưu tiên hơn CT cho phân tầng ngắn hạn khi phù hợp.")
        if result.category.replace("R", "") == "C3":
            st.info("C3: MAP <80 mmHg có thể giúp nhận diện bệnh nhân có thể cần tăng cường điều trị; 24–72 giờ đầu là giai đoạn cần theo dõi sát.")
        if result.category.replace("R", "") == "D2":
            st.info("D2: đánh giá sốc huyết áp còn bảo tồn (normotensive shock) và theo dõi sát nguy cơ diễn tiến xấu.")

    with tab3:
        st.header("3. Điều trị ban đầu")
        category = st.session_state.get("pe_category")
        if not category:
            st.warning("Chưa có phân nhóm AHA/ACC hoàn chỉnh. Không hiển thị phác đồ tự động.")
        else:
            st.success(f"Phân nhóm đang sử dụng: **{category}**")
            clean = category.replace("R", "")
            letter = _letter(clean)
            if letter in {"C", "D", "E"}:
                st.warning("Khuyến cáo đánh giá đa chuyên khoa PERT cho nhóm C–E.")
            elif clean in {"A", "B1", "B2"}:
                st.caption("Nhóm A/B có bệnh đồng mắc phức tạp vẫn có thể hưởng lợi từ đánh giá đa chuyên khoa PERT khi cần.")
            if clean in {"A", "B1", "B2"}:
                st.info("Không quyết định ngoại trú chỉ dựa vào nhãn A/B. AHA/ACC khuyến cáo dùng Hestia, PESI và/hoặc sPESI để xác nhận nguy cơ thấp, đồng thời bảo đảm thuốc kháng đông và theo dõi sau xuất viện.")
                with st.expander("Đánh giá phù hợp điều trị ngoại trú"):
                    out_tool = st.selectbox("Công cụ quyết định đã xác nhận nguy cơ thấp", [
                        "chưa xác nhận", "Hestia âm tính", "PESI lớp I–II", "sPESI = 0"
                    ], key="out_tool")
                    out_drug = st.checkbox("Có thể nhận thuốc kháng đông ngay khi xuất viện", key="out_drug")
                    out_follow = st.checkbox("Có kế hoạch theo dõi chuyên môn nhanh và tin cậy", key="out_follow")
                    out_goals = st.checkbox("Điều trị ngoại trú phù hợp mục tiêu/nguyện vọng người bệnh", key="out_goals")
                    out_assess = outpatient_management_assessment(
                        category=category,
                        low_risk_decision_tool_confirmed=(out_tool != "chưa xác nhận"),
                        immediate_anticoagulant_access=out_drug,
                        rapid_reliable_expert_followup=out_follow,
                        aligns_with_patient_goals=out_goals,
                    )
                    if out_assess["reasonable"]:
                        st.success("Đủ các điều kiện tối thiểu theo guideline để CÂN NHẮC điều trị ngoại trú; quyết định cuối vẫn dựa vào toàn cảnh lâm sàng và quyết định chung.")
                    else:
                        st.warning("Chưa đủ điều kiện để công cụ gợi ý ngoại trú: " + " ".join(out_assess["missing"]))
                if clean == "B1":
                    st.info("B1 (PE dưới phân thùy): vị trí huyết khối và DVT đồng thời có thể làm thay đổi quyết định ngoại trú/nhập viện và quyết định kháng đông; công cụ không tự động suy diễn chiến lược không kháng đông.")
            if clean in {"C3", "D1", "D2"}:
                st.info("Nếu huyết động ổn nhưng cần liệu pháp nâng cao không sẵn có tại chỗ, C3–D có thể cân nhắc chuyển trung tâm phù hợp.")
            if letter == "E":
                st.error("Nhóm E không nên chuyển viện khi chưa ổn định.")
            st.caption("Nếu dùng tiêu sợi huyết toàn thân hoặc tiêu sợi huyết qua catheter: nên theo dõi tại ICU hoặc đơn vị chăm sóc trung gian có khả năng giám sát sát. Sau lấy huyết khối cơ học, bệnh nhân ổn định có thể được theo dõi tại đơn vị có telemetry và nhân sự quen chăm sóc sau thủ thuật, tùy bối cảnh lâm sàng và nguồn lực.")

            st.subheader("Hỗ trợ huyết động và hô hấp")
            shock_now = bool(st.session_state.get("cardiogenic_shock", False))
            preload_concern = bool(st.session_state.get("reduced_preload_concern", False))
            if clean in {"D2", "E1", "E2"} and shock_now:
                st.info("Có sốc tim ở D2–E2: dùng vận mạch và/hoặc inotrope để duy trì tưới máu (mức khuyến cáo 1). Norepinephrin thường được xem là vận mạch lựa chọn; dobutamin có thể hỗ trợ khi cung lượng tim thấp.")
            if clean in {"D1", "D2"} and preload_concern:
                st.info("D1–D2 có giảm tiền tải: có thể cân nhắc bù dịch thận trọng; dữ liệu hỗ trợ liều dịch nhỏ, tránh bù dịch ồ ạt gây quá tải thất phải.")
            if clean in {"C2", "C3", "D1", "D2", "E1", "E2"}:
                st.info("C2–E: có thể cân nhắc thuốc giãn mạch phổi dạng hít để giảm hậu tải thất phải (COR 2b).")
            if letter in {"C", "D", "E"}:
                st.warning("Ở PE nhóm C–E, tránh an thần sâu và thông khí cơ học nếu không có chỉ định vì có thể gây sụp đổ huyết động. Nếu cần an thần để đặt nội khí quản, phải chuẩn bị sẵn hỗ trợ huyết động (vận mạch/inotrope và/hoặc VA-ECMO khi có nguồn lực).")
            if category.endswith("R") or category in {"CR", "DR", "ER"}:
                st.info("Khi thiếu oxy mức vừa–nặng, HFNC có thể hữu ích hơn ống thông mũi chuẩn để cải thiện oxy hóa.")
            if clean == "E2":
                st.info("Sốc tim kháng trị do PE: VA-ECMO là lựa chọn hợp lý nếu có nguồn lực. Khi đang VA-ECMO và không chảy máu, tiếp tục kháng đông đường tiêm; lợi ích thêm MT/CDL khi đã ECMO chưa được xác lập.")

            st.subheader("Tái tưới máu / can thiệp nâng cao")
            grp = advanced_group(category)
            if grp:
                for name, (cor, text) in ADVANCED_THERAPY_TABLE[grp].items():
                    st.write(f"**{name}:** {text}")
                if grp in {"C2", "C3", "D1-2"}:
                    st.caption("Khi đang cân nhắc can thiệp ở C2–D2 và không chống chỉ định tiêu sợi huyết, chưa rõ tiêu sợi huyết qua catheter hay lấy huyết khối cơ học tốt hơn về tử vong hoặc chảy máu nặng; lựa chọn phụ thuộc giải phẫu, độ khẩn, bệnh đồng mắc và kinh nghiệm trung tâm.")
                if grp in {"C2", "C3", "D1-2", "E1"}:
                    st.caption("Nếu đã quyết định tiêu sợi huyết qua catheter: hướng dẫn không khuyến cáo giảm alteplase xuống <5 mg cho mỗi động mạch phổi chỉ nhằm giảm chảy máu/diễn tiến xấu so với phác đồ 5–10 mg cho mỗi động mạch phổi; thời gian truyền và thiết bị theo quy trình chuyên môn.")
                if grp in {"C2", "C3", "D1-2", "E1", "E2"}:
                    st.caption("Nếu thực hiện tiêu sợi huyết qua catheter, kháng đông đồng thời bằng LMWH/UFH liều điều trị hoặc UFH dưới liều điều trị được khuyến cáo hơn là không kháng đông. Sau thủ thuật nội mạch hoặc tiêu sợi huyết, LMWH được ưu tiên hơn UFH cho kháng đông đường tiêm ban đầu khi phù hợp.")
                clot_in_transit = st.checkbox("Có huyết khối tự do trong nhĩ phải/thất phải (huyết khối tự do buồng tim phải)", key="tx_clot_transit")
                if clot_in_transit and grp in {"C3", "D1-2", "E1", "E2"}:
                    st.warning("C3–E2 có huyết khối tự do nhĩ phải/thất phải: điều trị nâng cao thay vì kháng đông đơn thuần là hợp lý (mức khuyến cáo 2a, mức chứng cứ C-LD).")
            else:
                st.warning("Phân nhóm hô hấp độc lập (CR/DR/ER) không được tự động ánh xạ sang Bảng 7; cần đánh giá PERT theo toàn cảnh lâm sàng.")

            st.subheader("Cá thể hóa kháng đông")
            col1, col2 = st.columns(2)
            with col1:
                pregnant = st.checkbox("Mang thai", key="tx_preg")
                breastfeeding = st.checkbox("Cho con bú", key="tx_bf")
                aps = st.checkbox("APS huyết khối đã xác lập", key="tx_aps")
                lowaps = st.checkbox("Chỉ một kháng thể anticardiolipin/β2-GPI nguy cơ thấp", key="tx_lowaps")
                brain_tumor = st.checkbox("U não nguyên phát hoặc di căn", key="tx_brain")
                hit = st.checkbox("Tiền sử HIT", key="tx_hit")
                abscontra = st.checkbox("Chống chỉ định tuyệt đối với kháng đông", key="tx_abscontra")
                high_bleed = st.checkbox("Nguy cơ chảy máu cao nhưng chưa phải chống chỉ định tuyệt đối", key="tx_highbleed")
            with col2:
                ckd = st.selectbox("Giai đoạn CKD", ["không/không rõ", "2", "3", "4", "5", "ESKD"], key="tx_ckd")
                cp = st.selectbox("Child-Pugh", ["không", "A", "B", "C"], key="tx_cp")
                bari = st.checkbox("Phẫu thuật giảm béo trong 4 tuần", key="tx_bari")
                interactions = st.checkbox("Đã rà soát tương tác thuốc theo nhãn sản phẩm", key="tx_interactions")
                interaction_present = st.checkbox("Có tương tác thuốc có thể cần tránh hoặc chỉnh liều DOAC", key="tx_interaction_present")
                age_tx = st.number_input("Tuổi", min_value=18, max_value=120, value=60, key="tx_age")
                female_tx = st.checkbox("Giới tính nữ", key="tx_female")
                weight = st.number_input("Cân nặng (kg)", min_value=20.0, max_value=300.0, value=70.0, key="tx_w")
                height = st.number_input("Chiều cao (cm)", min_value=100.0, max_value=230.0, value=165.0, key="tx_h")
                bmi = weight / ((height/100.0)**2)
                st.write(f"BMI = **{bmi:.1f} kg/m²**")
                creat_unit = st.radio("Đơn vị creatinine", ["µmol/L", "mg/dL"], key="tx_creat_unit")
                if creat_unit == "µmol/L":
                    creat_umol = st.number_input("Creatinine (µmol/L)", min_value=1.0, max_value=3000.0, value=88.4, key="tx_creat_umol")
                    creat_mg = creat_umol_to_mgdl(creat_umol)
                else:
                    creat_mg = st.number_input("Creatinine (mg/dL)", min_value=0.01, max_value=30.0, value=1.0, key="tx_creat_mg")
                crcl = cockcroft_gault(float(age_tx), float(weight), float(creat_mg), female_tx)
                st.write(f"CrCl Cockcroft–Gault = **{crcl:.1f} mL/phút**" if crcl is not None else "Không tính được CrCl.")
                if bmi >= 40 or bmi < 18.5:
                    st.warning("Hình thể cực đoan: CrCl phụ thuộc cách chọn cân nặng. Hãy kiểm tra lại với dược lâm sàng/quy trình bệnh viện trước khi dùng kết quả để kê thuốc.")
                dose_inputs_confirmed = st.checkbox("Đã nhập và xác nhận tuổi, giới, cân nặng, creatinine và tình trạng thận/gan của bệnh nhân; không dùng các giá trị mặc định", key="tx_dose_inputs_ok")

            ctx = MedicationContext(
                absolute_contraindication_to_anticoag=abscontra, high_bleeding_risk_nonabsolute=high_bleed,
                pregnant=pregnant, breastfeeding=breastfeeding, thrombotic_aps=aps,
                single_low_risk_aps_antibody_only=lowaps, brain_tumor=brain_tumor,
                ckd_stage={"không/không rõ":"none","2":"2","3":"3","4":"4","5":"5","ESKD":"eskd"}[ckd],
                crcl_ml_min=crcl, child_pugh={"không":"none","A":"A","B":"B","C":"C"}[cp],
                bariatric_surgery_within_4_weeks=bari, documented_hit=hit,
                bmi=bmi, weight_kg=weight, interaction_review_completed=interactions, relevant_drug_interaction_present=interaction_present, dose_inputs_confirmed=dose_inputs_confirmed)
            strat = anticoagulation_strategy(ctx, category)
            for x in strat["recommendations"]: st.write("• " + x)
            for x in strat["warnings"]: st.warning(x)
            if strat["exact_oral_dose_allowed"]:
                with st.expander("Liều DOAC theo nhãn sản phẩm"):
                    st.write("**Apixaban:**", apixaban_vte_dose(ctx))
                    st.write("**Rivaroxaban:**", rivaroxaban_vte_dose(ctx))
                    st.write("**Dabigatran:**", dabigatran_vte_dose(ctx))
                    st.write("**Edoxaban:**", edoxaban_vte_dose(ctx, relevant_pgp_inhibitor=False))
                    st.caption("Cổng này chỉ mở khi đã xác nhận KHÔNG có tương tác cần tránh/chỉnh liều. Nếu có tương tác (bao gồm P-gp/CYP liên quan), công cụ khóa liều cụ thể và yêu cầu đối chiếu nhãn/dược lâm sàng thay vì tự sửa liều.")
            st.markdown("### Kháng đông đường tiêm — trả đồng thời LMWH và UFH")
            p1, p2 = st.columns(2)
            with p1:
                st.markdown("**LMWH — enoxaparin**")
                st.write(enoxaparin_pe_dose(ctx))
                st.caption("Ở C1–E1, AHA/ACC 2026 ưu tiên LMWH hơn UFH khi cần kháng đông đường tiêm và không có chống chỉ định. BMI >40 hoặc cân nặng rất cao cần cá thể hóa; CrCl <30 cần chỉnh liều/giám sát phù hợp.")
            with p2:
                st.markdown("**UFH — lựa chọn thay thế khi phù hợp/khả dụng**")
                st.write(ufh_vte_initial_dose(ctx))
                st.caption("Liều UFH hiển thị là nomogram VTE cân nặng 80 đơn vị/kg bolus + 18 đơn vị/kg/giờ, không phải liều riêng của AHA/ACC 2026. Phải chỉnh theo aPTT/anti-Xa và nomogram của bệnh viện. Nếu đang/chuẩn bị dùng alteplase, không tự áp dụng bolus này: nhãn Activase yêu cầu khởi/khởi lại kháng đông đường tiêm gần cuối hoặc ngay sau truyền khi aPTT hoặc thrombin time ≤2 lần bình thường.")

            st.subheader("Lưới lọc tĩnh mạch chủ dưới")
            cannot_ac = st.checkbox("Hiện không thể dùng kháng đông", key="ivc_noac")
            therapeutic_ac = st.checkbox("Đang kháng đông điều trị hiệu quả", key="ivc_txac")
            recurrent_on_ac = st.checkbox("PE tái phát dù kháng đông tối ưu", key="ivc_recur")
            adv_proc = st.checkbox("Đang thực hiện liệu pháp nâng cao", key="ivc_adv")
            for x in ivc_filter_recommendation(cannot_anticoagulate=cannot_ac, therapeutic_anticoagulation=therapeutic_ac,
                                                recurrent_pe_despite_optimal_anticoag=recurrent_on_ac, category=category,
                                                undergoing_advanced_intervention=adv_proc):
                st.write("• " + x)

            if grp in {"C3", "D1-2", "E1", "E2"}:
                with st.expander("Tiêu sợi huyết toàn thân — kiểm tra chỉ định và an toàn"):
                    st.warning("Liều alteplase không được dùng như một tín hiệu 'nên tiêu sợi huyết'. Hệ thống chỉ mở liều sau khi phân nhóm cho phép cân nhắc/hợp lý, bác sĩ hoặc PERT đã chủ động chọn tiêu sợi huyết toàn thân, và cổng chảy máu đã đạt. Không tính liều tenecteplase cho PE vì tenecteplase chưa được FDA phê duyệt cho PE.")
                    selected_lysis = st.checkbox("Sau đánh giá bác sĩ/PERT, đã quyết định chọn tiêu sợi huyết toàn thân cho ca này", key="lyt_selected")
                    st.markdown("**Chống chỉ định theo nhãn Activase cho PE:**")
                    c_active = st.checkbox("Chảy máu nội đang hoạt động", key="lyt_c1")
                    c_stroke = st.checkbox("Tiền sử đột quỵ gần đây", key="lyt_c2")
                    c_surg = st.checkbox("Phẫu thuật nội sọ/nội tủy hoặc chấn thương đầu nặng trong 3 tháng", key="lyt_c3")
                    c_ic = st.checkbox("Tổn thương nội sọ làm tăng nguy cơ chảy máu", key="lyt_c4")
                    c_diath = st.checkbox("Cơ địa chảy máu", key="lyt_c5")
                    c_htn = st.checkbox("Tăng huyết áp nặng chưa kiểm soát", key="lyt_c6")
                    acceptable = st.checkbox("Sau đánh giá toàn diện, nguy cơ chảy máu được xem là chấp nhận được", key="lyt_ok")
                    contra = [name for name,flag in [
                        ("chảy máu nội đang hoạt động",c_active),("đột quỵ gần đây",c_stroke),
                        ("phẫu thuật nội sọ/nội tủy hoặc chấn thương đầu nặng gần đây",c_surg),
                        ("tổn thương nội sọ nguy cơ chảy máu",c_ic),("cơ địa chảy máu",c_diath),
                        ("tăng huyết áp nặng chưa kiểm soát",c_htn)] if flag]
                    lyt = systemic_thrombolysis_decision(category=category,
                                                         clinician_selected_systemic_lysis=selected_lysis,
                                                         contraindications=contra,
                                                         acceptable_bleeding_risk=acceptable)
                    st.caption(str(lyt["guideline_position"]))
                    if lyt["dose_visible"]:
                        if grp in {"E1", "E2"}:
                            st.success(str(lyt["dose"]) + ". " + str(lyt["note"]))
                        else:
                            st.info("Nếu quyết định tiêu sợi huyết đã được chốt: " + str(lyt["dose"]) + ". " + str(lyt["note"]))
                    else:
                        st.warning("Chưa mở liều alteplase: " + "; ".join(lyt["reason"]))



if __name__ == "__main__":
    run_app()
