"""CDSS thuyên tắc phổi cấp theo AHA/ACC 2026.

Bản FINAL cho tiếp cận ban đầu tại cấp cứu. Phần lõi không phụ thuộc Streamlit để có thể kiểm thử tự động.
Phạm vi: người lớn >=18 tuổi, từ nghi ngờ PE -> xác nhận -> phân nhóm AHA/ACC A-E + R -> điều trị ban đầu. Không thay thế đánh giá lâm sàng/PERT/quy trình bệnh viện.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Literal

GUIDELINE = "2026 AHA/ACC/ACCP/ACEP/CHEST/SCAI/SHM/SIR/SVM/SVN Guideline for Acute Pulmonary Embolism"
GUIDELINE_DOI = "10.1161/CIR.0000000000001415"
RELEASE_CANDIDATE = "FINAL-WIZARD-2026.08.22"

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
# ---------- HỖ TRỢ WIZARD / LIỀU TIÊU SỢI HUYẾT ----------
def severity_is_low(score_name: str, value: float | int | bool) -> bool:
    """Ngưỡng dùng trong Figure 2 / phần mô tả phân nhóm AHA/ACC 2026."""
    if score_name == "PESI":
        return float(value) <= 85
    if score_name == "sPESI":
        return int(value) == 0
    if score_name == "Bova":
        return int(value) <= 4
    if score_name == "Hestia":
        return not bool(value)  # False = Hestia âm tính
    raise ValueError("Thang điểm không hỗ trợ")


def urokinase_label_pe_dose(weight_kg: float) -> Dict[str, object]:
    """Kinlytic/urokinase label: 4,400 IU/kg over 10 min, then 4,400 IU/kg/h for 12 h."""
    if weight_kg <= 0:
        return {"eligible": False, "reason": ["Cân nặng không hợp lệ."]}
    load = 4400 * weight_kg
    hourly = 4400 * weight_kg
    total_12h = load + hourly * 12
    return {
        "eligible": True,
        "dose": f"Urokinase {load:,.0f} IU IV trong 10 phút, sau đó {hourly:,.0f} IU/giờ trong 12 giờ",
        "loading_iu": load,
        "hourly_iu": hourly,
        "total_12h_iu": total_12h,
        "note": "Liều theo nhãn Kinlytic cho PE cấp massive/không ổn định huyết động; kiểm tra nhãn sản phẩm sẵn có tại cơ sở và chống chỉ định trước dùng.",
    }


def streptokinase_reference_pe_dose() -> Dict[str, object]:
    """Phác đồ PE kinh điển từ product monograph/ESC; không phải liều riêng do AHA/ACC 2026 ban hành."""
    return {
        "eligible": True,
        "dose": "Streptokinase 250.000 IU IV trong 30 phút, sau đó 100.000 IU/giờ trong 24 giờ",
        "note": "Phác đồ tham khảo từ nhãn/product monograph và hướng dẫn PE trước đây; AHA/ACC 2026 ghi nhận streptokinase là thuốc tiêu sợi huyết đã được phê duyệt nhưng ít dùng hiện nay. Phải đối chiếu đúng chế phẩm tại cơ sở.",
    }


def run_app() -> None:
    import streamlit as st

    st.set_page_config(page_title="PE AHA/ACC 2026 — tiếp cận cấp cứu", layout="centered")

    if "wizard_step" not in st.session_state:
        st.session_state["wizard_step"] = 1
    if "pe_confirmed" not in st.session_state:
        st.session_state["pe_confirmed"] = False
    if "final_category" not in st.session_state:
        st.session_state["final_category"] = None
    if "base_category" not in st.session_state:
        st.session_state["base_category"] = None

    def reset_from(step: int) -> None:
        if step <= 1:
            st.session_state["pe_confirmed"] = False
        if step <= 2:
            st.session_state["final_category"] = None
            st.session_state["base_category"] = None
            st.session_state.pop("tx_dose_ready", None)
        st.session_state["wizard_step"] = step
        st.rerun()

    def next_step(step: int) -> None:
        st.session_state["wizard_step"] = step
        st.rerun()

    def perfusion_panel(prefix: str) -> tuple[Dict[str, bool], bool]:
        """Chỉ mở khi cần phân D1/D2 hoặc loại trừ normotensive shock trước khi chốt C."""
        perf_state = st.radio(
            "Có bằng chứng giảm tưới máu / rối loạn chức năng cơ quan do PE?",
            ["Không", "Có", "Chưa đánh giá đầy đủ"],
            horizontal=True,
            key=f"{prefix}_perf_state",
        )
        flags = {
            "lactate_gt_2": False,
            "acute_kidney_injury": False,
            "urine_output_lt_05_mlkg_h": False,
            "mental_status_change": False,
            "cardiac_index_lt_22": False,
            "map_lt_60": False,
            "increased_shock_score_stage": False,
        }
        complete = perf_state != "Chưa đánh giá đầy đủ"
        if perf_state in {"Có", "Chưa đánh giá đầy đủ"}:
            direct = st.multiselect(
                "Chọn dấu hiệu đang có",
                [
                    "Lactate >2 mmol/L",
                    "AKI",
                    "Nước tiểu <0,5 mL/kg/giờ",
                    "Thay đổi tri giác",
                    "Cardiac index <2,2 L/phút/m²",
                    "MAP <60 mmHg",
                ],
                key=f"{prefix}_direct",
            )
            flags["lactate_gt_2"] = "Lactate >2 mmol/L" in direct
            flags["acute_kidney_injury"] = "AKI" in direct
            flags["urine_output_lt_05_mlkg_h"] = "Nước tiểu <0,5 mL/kg/giờ" in direct
            flags["mental_status_change"] = "Thay đổi tri giác" in direct
            flags["cardiac_index_lt_22"] = "Cardiac index <2,2 L/phút/m²" in direct
            flags["map_lt_60"] = "MAP <60 mmHg" in direct

            shock_tool = st.selectbox(
                "Nếu cần, dùng thêm công cụ đánh giá shock",
                ["Không dùng", "CPES", "SCAI SHOCK"],
                key=f"{prefix}_shock_tool",
            )
            if shock_tool == "CPES":
                st.caption("CPES được dùng ở đây để hỗ trợ nhận diện nguy cơ normotensive shock; không thay thế các marker giảm tưới máu trực tiếp.")
                c_trop = st.checkbox("Troponin tăng", key=f"{prefix}_cp_trop")
                c_bnp = st.checkbox("BNP/NT-proBNP tăng", key=f"{prefix}_cp_bnp")
                c_rv = st.checkbox("RV dysfunction mức vừa/nặng", key=f"{prefix}_cp_rv")
                c_saddle = st.checkbox("Saddle PE", key=f"{prefix}_cp_saddle")
                c_dvt = st.checkbox("Có DVT đồng thời", key=f"{prefix}_cp_dvt")
                c_hr = st.checkbox("HR ≥100/phút", key=f"{prefix}_cp_hr")
                cp = cpes_score(
                    troponin_elevated=c_trop,
                    bnp_elevated=c_bnp,
                    moderate_severe_rv_dysfunction=c_rv,
                    saddle_pe=c_saddle,
                    concomitant_dvt=c_dvt,
                    hr_ge_100=c_hr,
                )
                st.write(f"CPES = **{cp}/6**")
                if cp == 6:
                    flags["increased_shock_score_stage"] = True
                    st.warning("CPES 6/6: nguy cơ cao normotensive shock — được tính là shock score tăng trong Figure 2.")
            elif shock_tool == "SCAI SHOCK":
                scai = st.selectbox("SCAI SHOCK stage", ["A", "B", "C", "D", "E"], key=f"{prefix}_scai")
                if scai in {"B", "C"}:
                    flags["increased_shock_score_stage"] = True
                elif scai in {"D", "E"}:
                    st.error("SCAI D–E gợi ý shock nặng hơn: hãy quay lại bước huyết động để đánh giá E1/E2 thay vì chỉ dùng như marker D2.")
                    complete = False

            if perf_state == "Có" and not any(flags.values()):
                st.warning("Bạn chọn 'Có' nhưng chưa chọn marker giảm tưới máu hoặc shock score tăng.")
                complete = False
            if perf_state == "Chưa đánh giá đầy đủ":
                st.info("Chưa đủ dữ liệu để chốt D1/C hay D2. Hãy bổ sung đánh giá tưới máu; ở nhóm C–E tại cơ sở cấp cứu, guideline khuyến cáo đo lactate.")
        return flags, complete

    st.title("🫁 THUYÊN TẮC PHỔI CẤP — AHA/ACC 2026")
    st.caption("Công cụ hỗ trợ tiếp cận ban đầu tại cấp cứu: nghi ngờ PE → xác nhận → phân loại A–E + R → điều trị ban đầu.")

    p1, p2, p3 = st.columns(3)
    p1.metric("Bước 1", "Chẩn đoán", "✓" if st.session_state["wizard_step"] > 1 else "đang làm")
    p2.metric("Bước 2", "Phân loại", "✓" if st.session_state["wizard_step"] > 2 else ("đang làm" if st.session_state["wizard_step"] == 2 else "chờ"))
    p3.metric("Bước 3", "Điều trị", "đang làm" if st.session_state["wizard_step"] == 3 else "chờ")

    # ==================== BƯỚC 1 ====================
    if st.session_state["wizard_step"] == 1:
        st.header("BƯỚC 1 — NGHI NGỜ / XÁC NHẬN PE")
        pregnant = st.checkbox("Đang mang thai", key="wz_dx_preg")
        on_ac = st.checkbox("Đã dùng kháng đông liều điều trị trong 24 giờ trước", key="wz_dx_ac")

        st.subheader("1. Xác suất tiền nghiệm")
        method = st.selectbox("Chọn cách đánh giá", ["— Chọn phương pháp —", "Wells", "Geneva giản lược", "Đánh giá lâm sàng"], key="wz_dx_method")
        high = False
        nonhigh = False
        very_low = False
        uncertain = False
        pretest_ready = method != "— Chọn phương pháp —"

        if method == "Wells":
            c1, c2 = st.columns(2)
            with c1:
                w_dvt = st.checkbox("Dấu hiệu DVT", key="wz_w_dvt")
                w_pe = st.checkbox("PE khả dĩ hơn chẩn đoán khác", key="wz_w_pe")
                w_hr = st.checkbox("HR >100/phút", key="wz_w_hr")
                w_imm = st.checkbox("Bất động ≥3 ngày / phẫu thuật 4 tuần", key="wz_w_imm")
            with c2:
                w_prev = st.checkbox("Tiền sử DVT/PE", key="wz_w_prev")
                w_hemo = st.checkbox("Ho ra máu", key="wz_w_hemo")
                w_ca = st.checkbox("Ung thư", key="wz_w_ca")
            ws = wells_score(dvt_signs=w_dvt, pe_most_likely=w_pe, hr_gt_100=w_hr,
                             immobilization_or_surgery=w_imm, prior_dvt_pe=w_prev,
                             hemoptysis=w_hemo, cancer=w_ca)
            st.write(f"**Wells {ws:g} điểm — {wells_category(ws)}**")
            high = ws > 6
            nonhigh = not high
            very_low = ws < 2
        elif method == "Geneva giản lược":
            c1, c2 = st.columns(2)
            with c1:
                g_age = st.checkbox("Tuổi >65", key="wz_g_age")
                g_prev = st.checkbox("Tiền sử DVT/PE", key="wz_g_prev")
                g_surg = st.checkbox("Phẫu thuật gây mê/gãy chi dưới trong 1 tháng", key="wz_g_surg")
                g_ca = st.checkbox("Ung thư hoạt động", key="wz_g_ca")
            with c2:
                g_leg = st.checkbox("Đau một bên chi dưới", key="wz_g_leg")
                g_hemo = st.checkbox("Ho ra máu", key="wz_g_hemo")
                g_hr = st.selectbox("Nhịp tim", ["<75", "75–94", "≥95"], key="wz_g_hr")
                g_dvt = st.checkbox("Đau TM sâu + phù một bên", key="wz_g_dvt")
            gs = simplified_geneva_score(age_gt_65=g_age, prior_dvt_pe=g_prev,
                                         surgery_or_lower_limb_fracture=g_surg, active_cancer=g_ca,
                                         unilateral_leg_pain=g_leg, hemoptysis=g_hemo,
                                         hr_75_94=g_hr == "75–94", hr_ge_95=g_hr == "≥95",
                                         deep_vein_tenderness_and_unilateral_edema=g_dvt)
            st.write(f"**Geneva giản lược {gs} điểm — {simplified_geneva_category(gs)}**")
            high = gs >= 5
            nonhigh = not high
            if not pregnant and not high:
                very_low = st.checkbox("Đánh giá lâm sàng cho rằng xác suất thực sự <15% để có thể dùng PERC", key="wz_g_perc")
        else:
            gestalt = st.radio("Xác suất lâm sàng", ["<15%", "15–<50%", ">50%", "Không chắc/quanh 50%"], horizontal=True, key="wz_gestalt")
            very_low = gestalt == "<15%"
            high = gestalt == ">50%"
            nonhigh = gestalt in {"<15%", "15–<50%"}
            uncertain = gestalt == "Không chắc/quanh 50%"

        diagnostic_state = "pending"
        imaging_needed = False

        if not pretest_ready:
            st.info("Chọn một phương pháp đánh giá xác suất tiền nghiệm để bắt đầu.")
        elif high or uncertain:
            st.warning("→ Cần hình ảnh để xác nhận/loại trừ PE; không dùng D-dimer để trì hoãn hình ảnh ở xác suất cao.")
            imaging_needed = True
        elif on_ac:
            st.warning("→ Đã dùng kháng đông điều trị trong 24 giờ: không dùng chiến lược D-dimer để tự động loại trừ PE; cân nhắc hình ảnh theo xác suất lâm sàng.")
            imaging_needed = True
        elif pregnant:
            st.subheader("2. Pregnancy-adapted YEARS")
            dvt_sym = st.checkbox("Có triệu chứng chi dưới gợi ý DVT", key="wz_p_dvt")
            cus = "không cần"
            if dvt_sym:
                cus = st.selectbox("CUS chi dưới", ["Chưa làm", "Âm tính", "Dương tính"], key="wz_p_cus")
                if cus == "Chưa làm":
                    st.info("→ Làm CUS trước.")
                elif cus == "Dương tính":
                    st.success("DVT dương tính: có thể điều trị VTE mà không nhất thiết cần CTPA. Nếu cần phân loại PE AHA/ACC, cần bằng chứng PE trực tiếp.")
            if not dvt_sym or cus == "Âm tính":
                y_hemo = st.checkbox("Ho ra máu", key="wz_p_hemo")
                y_likely = st.checkbox("PE là chẩn đoán khả dĩ nhất", key="wz_p_likely")
                dd = st.number_input("D-dimer (ng/mL FEU)", min_value=0.0, value=0.0, step=10.0, key="wz_p_dd")
                pr = pregnancy_adapted_years_decision(
                    dvt_symptoms=dvt_sym,
                    cus_result="negative" if cus == "Âm tính" else "not_done",
                    hemoptysis=y_hemo,
                    pe_most_likely=y_likely,
                    ddimer_feu_ng_ml=dd,
                )
                if dd > 0:
                    st.write(f"Ngưỡng YEARS: **{pr.get('cutoff', '—')} ng/mL FEU**")
                    if pr.get("rule_out"):
                        st.success("→ Loại trừ PE theo pregnancy-adapted YEARS.")
                        diagnostic_state = "excluded"
                    elif pr.get("needs_chest_imaging"):
                        st.warning("→ Cần hình ảnh ngực.")
                        imaging_needed = True
        else:
            perc_negative = False
            if very_low and not pregnant:
                use_perc = st.radio("Bệnh nhân rất thấp nguy cơ — bước tiếp theo", ["— Chọn —", "Dùng PERC", "Bỏ PERC, đi tiếp D-dimer"], horizontal=True, key="wz_use_perc")
                if use_perc == "Dùng PERC":
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        pa = st.number_input("Tuổi", 18, 120, 40, key="wz_pa")
                        phr = st.number_input("HR", 20, 250, 80, key="wz_phr")
                        pspo = st.number_input("SpO₂", 50, 100, 98, key="wz_pspo")
                    with c2:
                        phemo = st.checkbox("Ho ra máu", key="wz_phemo")
                        pest = st.checkbox("Dùng estrogen", key="wz_pest")
                        pprev = st.checkbox("Tiền sử DVT/PE", key="wz_pprev")
                    with c3:
                        pleg = st.checkbox("Sưng chân một bên", key="wz_pleg")
                        psurg = st.checkbox("PT/chấn thương cần nhập viện <4 tuần", key="wz_psurg")
                    pr = perc_result(gestalt_lt_15=True, age=pa, hr=phr, spo2=pspo,
                                     hemoptysis=phemo, estrogen_use=pest, prior_dvt_pe=pprev,
                                     unilateral_leg_swelling=pleg,
                                     recent_surgery_trauma_hospitalized=psurg)
                    if pr["negative"]:
                        st.success("→ PERC âm tính: không cần D-dimer/hình ảnh vì PE.")
                        perc_negative = True
                        diagnostic_state = "excluded"
                    else:
                        st.warning("→ PERC dương tính: đi tiếp D-dimer.")

            perc_pending = very_low and not pregnant and use_perc == "— Chọn —" if very_low and not pregnant else False
            if perc_pending:
                st.info("Chọn PERC hoặc đi thẳng D-dimer.")
            if not perc_negative and not perc_pending:
                st.subheader("2. D-dimer")
                strategy = st.radio("Chọn chiến lược", ["Hiệu chỉnh theo tuổi", "YEARS"], horizontal=True, key="wz_dd_strategy")
                age_dd = st.number_input("Tuổi dùng cho D-dimer", 18, 120, 55, key="wz_dd_age")
                dd = st.number_input("D-dimer (ng/mL FEU)", min_value=0.0, value=0.0, step=10.0, key="wz_dd")
                yc = 0
                if strategy == "YEARS":
                    y1 = st.checkbox("Dấu hiệu DVT", key="wz_y1")
                    y2 = st.checkbox("Ho ra máu", key="wz_y2")
                    y3 = st.checkbox("PE khả dĩ nhất", key="wz_y3")
                    yc = sum([y1, y2, y3])
                if dd > 0:
                    if strategy == "Hiệu chỉnh theo tuổi":
                        dr = ddimer_strategy_result(strategy="age_adjusted", age=age_dd,
                                                    ddimer_feu_ng_ml=dd, low_or_intermediate_pretest=nonhigh,
                                                    therapeutic_anticoagulation_within_24h=False)
                    else:
                        dr = ddimer_strategy_result(strategy="years", age=age_dd,
                                                    ddimer_feu_ng_ml=dd, low_or_intermediate_pretest=nonhigh,
                                                    therapeutic_anticoagulation_within_24h=False, years_count=yc)
                    st.write(f"Ngưỡng: **{dr.get('cutoff', '—')} ng/mL FEU**")
                    if dr.get("rule_out"):
                        st.success("→ D-dimer dưới ngưỡng: loại trừ PE, không cần hình ảnh vì PE.")
                        diagnostic_state = "excluded"
                    else:
                        st.warning("→ D-dimer không loại trừ PE: cần hình ảnh.")
                        imaging_needed = True

        st.subheader("3. Hình ảnh xác nhận")
        have_imaging = st.checkbox("Đã có kết quả hình ảnh PE", value=imaging_needed, key="wz_have_img")
        if have_imaging:
            img = st.selectbox(
                "Kết quả",
                ["Chưa có kết quả", "CTPA dương tính", "V/Q xác suất cao", "CTPA âm tính", "V/Q SPECT bình thường", "V/Q không chẩn đoán"],
                key="wz_img",
            )
            mapping = {
                "CTPA dương tính": "positive_ctpa",
                "V/Q xác suất cao": "high_probability_vq",
                "CTPA âm tính": "negative_ctpa",
                "V/Q SPECT bình thường": "normal_vq_spect",
                "V/Q không chẩn đoán": "nondiagnostic_vq",
            }
            if img in mapping:
                ir = diagnostic_imaging_interpretation(mapping[img])
                if ir["confirmed"]:
                    diagnostic_state = "confirmed"
                    st.success("PE ĐÃ XÁC NHẬN")
                elif ir["excluded"]:
                    diagnostic_state = "excluded"
                    st.success("PE đã được loại trừ bằng hình ảnh.")
                else:
                    st.warning("Kết quả chưa chẩn đoán: cần chiến lược hình ảnh/đánh giá tiếp theo.")

        if diagnostic_state == "confirmed":
            if st.button("Tiếp tục → PHÂN LOẠI AHA/ACC", type="primary", use_container_width=True):
                st.session_state["pe_confirmed"] = True
                st.session_state["wizard_step"] = 2
                st.rerun()
        elif diagnostic_state == "excluded":
            st.info("Dừng pathway PE cấp tại đây, trừ khi xuất hiện dữ kiện lâm sàng mới làm thay đổi xác suất.")

    # ==================== BƯỚC 2 ====================
    elif st.session_state["wizard_step"] == 2:
        if not st.session_state["pe_confirmed"]:
            reset_from(1)

        st.success("✓ BƯỚC 1 — PE đã xác nhận")
        if st.button("← Sửa bước chẩn đoán", key="edit_dx"):
            reset_from(1)

        st.header("BƯỚC 2 — PHÂN LOẠI AHA/ACC")
        st.subheader("1. Huyết động trước")
        arrest = st.radio(
            "Ngừng tuần hoàn liên quan đợt hiện tại?",
            ["— Chọn —", "Không", "Không ROSC sau ≥30 phút", "Đã ROSC trước 30 phút"],
            horizontal=True, key="wz_arrest"
        )
        if arrest == "Đã ROSC trước 30 phút":
            st.info("Sau ROSC, guideline cho phép category thay đổi theo tái đánh giá. Phân loại tiếp theo dựa trên trạng thái hiện tại; không tự động gán E2.")

        kwargs = dict(confirmed_pe=True, symptomatic=True, incidental=False)
        base_ready = arrest != "— Chọn —"
        stable_branch = False

        if arrest == "— Chọn —":
            st.info("Bắt đầu bằng đánh giá ngừng tuần hoàn/huyết động.")
        elif arrest == "Không ROSC sau ≥30 phút":
            kwargs["cardiac_arrest_no_rosc_30min"] = True
        else:
            refractory = st.checkbox("Sốc tim kháng trị", key="wz_refractory")
            if refractory:
                kwargs["refractory_cardiogenic_shock"] = True
            else:
                cardiogenic = st.checkbox("Có sốc tim do PE", key="wz_cardiogenic")
                st.caption("Nhập dữ kiện huyết áp để hệ thống tự nhận D1/E1 thay vì yêu cầu bác sĩ tự nhớ ngưỡng.")
                c1, c2 = st.columns(2)
                with c1:
                    sbp_now = st.number_input("SBP hiện tại/thấp nhất (mmHg)", 30.0, 250.0, 120.0, step=1.0, key="wz_hemo_sbp")
                    sbp_drop = st.number_input("Mức giảm SBP so với nền (mmHg)", 0.0, 150.0, 0.0, step=1.0, key="wz_hemo_drop")
                    duration = st.number_input("Thời gian tụt HA (phút)", 0.0, 1440.0, 0.0, step=1.0, key="wz_hemo_dur")
                with c2:
                    responds = st.checkbox("Tụt HA đáp ứng truyền dịch", key="wz_hemo_fluid")
                    recurrent = st.checkbox("Có các đợt tụt HA tái diễn đạt tiêu chuẩn", key="wz_hemo_recur")

                hf = derive_hypotension_flags(
                    sbp_mm_hg=float(sbp_now),
                    sbp_drop_from_baseline_mm_hg=float(sbp_drop),
                    duration_min=float(duration),
                    responds_to_iv_fluids=responds,
                    recurrent=recurrent,
                )

                if (hf["persistent"] or hf["recurrent"]) and cardiogenic:
                    kwargs["persistent_hypotension"] = bool(hf["persistent"])
                    kwargs["recurrent_hypotension"] = bool(hf["recurrent"])
                    kwargs["cardiogenic_shock"] = True
                elif hf["persistent"] and not cardiogenic:
                    kwargs["persistent_hypotension"] = True
                    base_ready = False
                    st.warning("Có tụt huyết áp kéo dài nhưng chưa xác nhận sốc tim do PE: chưa đủ để tự gán E1. Cần đánh giá nguyên nhân shock/tưới máu trước khi tiếp tục.")
                elif cardiogenic:
                    # Sốc tim khi chưa có tụt HA kéo dài phù hợp trạng thái normotensive shock / D2.
                    kwargs["cardiogenic_shock"] = True
                elif hf["transient"] or hf["recurrent"]:
                    kwargs["transient_hypotension"] = bool(hf["transient"] or hf["recurrent"])
                    kwargs["recurrent_hypotension"] = bool(hf["recurrent"])
                    st.subheader("2. D1 hay D2?")
                    hp, perf_complete = perfusion_panel("wz_dbranch")
                    kwargs.update(hp)
                    base_ready = perf_complete
                else:
                    stable_branch = True

        if stable_branch:
            st.subheader("2. Có phải PE tình cờ, hoàn toàn không triệu chứng?")
            incidental = st.selectbox("", ["— Chọn —", "Không — bệnh nhân có triệu chứng", "Có — phát hiện tình cờ và không triệu chứng"], key="wz_incidental", label_visibility="collapsed")
            if incidental == "— Chọn —":
                base_ready = False
                st.info("Xác định PE có hoàn toàn không triệu chứng/phát hiện tình cờ hay không.")
            elif incidental.startswith("Có"):
                kwargs["symptomatic"] = False
                kwargs["incidental"] = True
            else:
                st.subheader("3. Chọn thang điểm mức độ lâm sàng")
                score_name = st.selectbox("Thang điểm", ["— Chọn thang điểm —", "PESI", "sPESI", "Bova", "Hestia"], key="wz_score")
                if score_name == "— Chọn thang điểm —":
                    base_ready = False
                    st.info("Chọn một thang điểm được guideline cho phép cho tình huống này.")
                    score_value = 0
                    bova_rv_status = None
                    bova_biomarker_status = None
                else:
                    score_value: float | int | bool
                    bova_rv_status: Optional[str] = None
                    bova_biomarker_status: Optional[str] = None

                    if score_name == "PESI":
                        age = st.number_input("Tuổi", 18, 120, 60, key="wz_pesi_age")
                        c1, c2 = st.columns(2)
                        with c1:
                            male = st.checkbox("Nam", key="wz_pesi_male")
                            cancer = st.checkbox("Ung thư", key="wz_pesi_ca")
                            hf = st.checkbox("Suy tim", key="wz_pesi_hf")
                            lung = st.checkbox("Bệnh phổi mạn", key="wz_pesi_lung")
                            ams = st.checkbox("Thay đổi tri giác", key="wz_pesi_ams")
                        with c2:
                            hr = st.number_input("HR (/phút)", 20, 250, 90, key="wz_pesi_hr")
                            sbp = st.number_input("SBP (mmHg)", 40, 250, 120, key="wz_pesi_sbp")
                            rr = st.number_input("RR (/phút)", 5, 80, 20, key="wz_pesi_rr")
                            temp = st.number_input("Nhiệt độ (°C)", 30.0, 43.0, 37.0, step=0.1, key="wz_pesi_temp")
                            spo = st.number_input("SpO₂ (%)", 50, 100, 96, key="wz_pesi_spo")
                        score_value = pesi_score(age=int(age), male=male, cancer=cancer, heart_failure=hf,
                                                 chronic_lung_disease=lung, hr_ge_110=hr >= 110, sbp_lt_100=sbp < 100,
                                                 rr_ge_30=rr >= 30, temp_lt_36=temp < 36, altered_mental_status=ams,
                                                 spo2_lt_90=spo < 90)
                        st.write(f"PESI = **{score_value} điểm — lớp {pesi_class(int(score_value))}**")
                    elif score_name == "sPESI":
                        c1, c2 = st.columns(2)
                        with c1:
                            age80 = st.checkbox("Tuổi >80", key="wz_sp_age")
                            cancer = st.checkbox("Ung thư", key="wz_sp_ca")
                            cardio = st.checkbox("Bệnh tim-phổi mạn", key="wz_sp_cp")
                        with c2:
                            sbp = st.number_input("SBP (mmHg)", 40, 250, 120, key="wz_sp_sbp")
                            hr = st.number_input("HR (/phút)", 20, 250, 90, key="wz_sp_hr")
                            spo = st.number_input("SpO₂ (%)", 50, 100, 96, key="wz_sp_spo")
                        score_value = spesi_score(age_gt_80=age80, cancer=cancer,
                                                  chronic_cardiopulmonary_disease=cardio,
                                                  sbp_lt_100=sbp < 100, hr_ge_110=hr >= 110, spo2_lt_90=spo < 90)
                        st.write(f"sPESI = **{score_value}**")
                    elif score_name == "Bova":
                        sbp = st.number_input("SBP (mmHg)", 40, 250, 120, key="wz_bova_sbp")
                        hr = st.number_input("HR (/phút)", 20, 250, 90, key="wz_bova_hr")
                        trop = st.radio("Troponin", ["Bình thường", "Tăng"], horizontal=True, key="wz_bova_trop")
                        rv = st.radio("RV trên echo/CT", ["Bình thường", "Bất thường"], horizontal=True, key="wz_bova_rv")
                        score_value = bova_score(sbp_90_100=90 <= sbp <= 100, troponin_elevated=trop == "Tăng",
                                                 rv_dysfunction=rv == "Bất thường", hr_ge_110=hr >= 110)
                        bova_rv_status = "abnormal" if rv == "Bất thường" else "normal"
                        bova_biomarker_status = "abnormal" if trop == "Tăng" else "normal"
                        st.write(f"Bova = **{score_value} điểm — stage {bova_stage(int(score_value))}**")
                    else:
                        st.caption("Huyết động đã được sàng lọc ở bước trước; tiêu chí Hestia 'hemodynamically unstable' được xem là Không trong nhánh này.")
                        h = {}
                        h["thrombolysis_or_embolectomy"] = st.checkbox("Cần thrombolysis/embolectomy", key="wz_h1")
                        h["active_or_high_bleeding_risk"] = st.checkbox("Đang chảy máu / nguy cơ chảy máu cao", key="wz_h2")
                        h["oxygen_gt_24h"] = st.checkbox("Cần O₂ >24 giờ để duy trì SpO₂ >90%", key="wz_h3")
                        h["pe_on_anticoag"] = st.checkbox("PE xảy ra khi đang kháng đông", key="wz_h4")
                        h["iv_analgesia_gt_24h"] = st.checkbox("Cần giảm đau IV >24 giờ", key="wz_h5")
                        h["medical_social_admission"] = st.checkbox("Lý do y khoa/xã hội cần nằm viện >24 giờ", key="wz_h6")
                        h["crcl_lt_30"] = st.checkbox("CrCl <30 mL/phút", key="wz_h7")
                        h["severe_liver"] = st.checkbox("Suy gan nặng", key="wz_h8")
                        h["pregnancy"] = st.checkbox("Mang thai", key="wz_h9")
                        h["hit"] = st.checkbox("Tiền sử HIT được ghi nhận", key="wz_h10")
                        score_value = hestia_positive(h)
                        st.write("Hestia = **DƯƠNG TÍNH**" if score_value else "Hestia = **ÂM TÍNH**")
    
                    low = severity_is_low(score_name, score_value)
                    kwargs["severity_known"] = True
                    kwargs["severity_low"] = low
    
                    if low:
                        st.success("Mức độ lâm sàng thấp — trước khi chốt B, chỉ cần kiểm tra có dấu hiệu bất thường tưới máu rõ ràng làm vượt lên D2 hay không.")
                        low_hp_gate = st.radio(
                            "Có dấu hiệu gợi ý giảm tưới máu / normotensive shock?",
                            ["Không", "Có hoặc đang nghi"], horizontal=True, key="wz_low_hp_gate"
                        )
                        low_hp = {}
                        if low_hp_gate == "Có hoặc đang nghi":
                            low_hp, perf_complete = perfusion_panel("wz_lowbranch")
                            kwargs.update(low_hp)
                            base_ready = perf_complete
                        if base_ready and not any(low_hp.values()):
                            loc = st.radio("Vị trí PE", ["Dưới phân thùy (subsegmental)", "Phân thùy hoặc gần hơn"], horizontal=True, key="wz_loc")
                            kwargs["clot_location"] = "subsegmental" if loc.startswith("Dưới") else "segmental_or_proximal"
                    else:
                        st.warning("Mức độ lâm sàng tăng → trước khi chốt C, đánh giá normotensive shock/D2.")
                        hp, perf_complete = perfusion_panel("wz_cbranch")
                        kwargs.update(hp)
                        base_ready = perf_complete
                        if perf_complete and not any(hp.values()):
                            st.subheader("4. RV và cardiac biomarker → C1/C2/C3")
                            if score_name == "Bova":
                                rv_status = bova_rv_status or "unknown"
                                biomarker_status = bova_biomarker_status or "unknown"
                                st.caption("Dùng lại troponin và RV vừa nhập trong Bova.")
                            else:
                                rv = st.radio("RV trên echo/CT", ["Bình thường", "Bất thường"], horizontal=True, key="wz_c_rv")
                                rv_status = "abnormal" if rv == "Bất thường" else "normal"
                                bm_method = st.selectbox("Cardiac biomarker sử dụng", ["Troponin", "BNP/NT-proBNP", "Cả hai"], key="wz_c_bm_method")
                                if bm_method == "Troponin":
                                    t = st.radio("Troponin", ["Bình thường", "Tăng"], horizontal=True, key="wz_c_t")
                                    biomarker_status = "abnormal" if t == "Tăng" else "normal"
                                elif bm_method == "BNP/NT-proBNP":
                                    b = st.radio("BNP/NT-proBNP", ["Bình thường", "Tăng"], horizontal=True, key="wz_c_b")
                                    biomarker_status = "abnormal" if b == "Tăng" else "normal"
                                else:
                                    t = st.radio("Troponin", ["Bình thường", "Tăng"], horizontal=True, key="wz_c_t2")
                                    b = st.radio("BNP/NT-proBNP", ["Bình thường", "Tăng"], horizontal=True, key="wz_c_b2")
                                    biomarker_status = "abnormal" if (t == "Tăng" or b == "Tăng") else "normal"
                            kwargs["rv_status"] = rv_status
                            kwargs["biomarker_status"] = biomarker_status
        base_result = classify_pe(ClassificationInput(**kwargs)) if base_ready else None

        if base_result and base_result.complete:
            st.divider()
            st.subheader("R — chỉ đánh giá sau khi đã có phân loại nền")
            st.write(f"Phân loại nền: **{base_result.category}**")
            base_letter = _letter(base_result.category)
            if base_letter == "E":
                rlevel = st.radio("Hô hấp do PE", ["— Chọn —", "Không cần NIV/IMV", "Cần NIV hoặc thở máy xâm lấn"], key="wz_r_e")
            elif base_letter == "D":
                rlevel = st.radio("Mức hỗ trợ hô hấp do PE", ["— Chọn —", "Không đạt D-R/E-R", ">6 L/phút qua nasal cannula hoặc non-rebreather", "NIV hoặc thở máy xâm lấn"], key="wz_r_d")
            else:
                rlevel = st.radio("Mức bất thường hô hấp do PE", ["— Chọn —", "Không có tiêu chí R", "SpO₂ <90% hoặc RR ≥30 hoặc cần O₂ bổ sung", ">6 L/phút qua nasal cannula hoặc non-rebreather", "NIV hoặc thở máy xâm lấn"], key="wz_r_abc")

            if rlevel == "— Chọn —":
                st.info("Đánh giá R là bước cuối trước khi chốt category.")
                final_result = None
            else:
                final_kwargs = dict(kwargs)
                if "NIV" in rlevel:
                    final_kwargs["positive_pressure_ventilation"] = True
                elif ">6 L" in rlevel:
                    final_kwargs["nasal_cannula_flow_l_min"] = 7.0
                elif "SpO₂" in rlevel:
                    final_kwargs["supplemental_oxygen_for_pe"] = True

                final_result = classify_pe(ClassificationInput(**final_kwargs))
            if final_result is not None and final_result.complete:
                st.success(f"PHÂN LOẠI HOÀN TẤT: **{final_result.category}**")
                if st.button("Tiếp tục → ĐIỀU TRỊ BAN ĐẦU", type="primary", use_container_width=True):
                    st.session_state["base_category"] = final_result.base_category
                    st.session_state["final_category"] = final_result.category
                    st.session_state.pop("tx_dose_ready", None)
                    st.session_state["wizard_step"] = 3
                    st.rerun()
            else:
                st.warning("Chưa đủ dữ liệu để hoàn tất phân loại.")
        elif not base_ready:
            st.warning("Chưa đủ dữ liệu để chốt phân loại nền.")
        elif base_result:
            for w in base_result.warnings:
                st.warning(w)

    # ==================== BƯỚC 3 ====================
    else:
        category = st.session_state["final_category"]
        if not category:
            reset_from(2)

        st.success(f"✓ BƯỚC 2 — AHA/ACC: {category}")
        if st.button("← Sửa phân loại", key="edit_risk"):
            reset_from(2)

        st.header("BƯỚC 3 — ĐIỀU TRỊ BAN ĐẦU")

        clean = str(category).replace("R", "")
        letter = _letter(clean)
        grp = advanced_group(str(category))

        st.subheader("1. Nơi điều trị / đội ngũ")
        if letter in {"C", "D", "E"}:
            st.write("• **PERT:** khuyến cáo đánh giá đa chuyên khoa nếu có.")
        if clean in {"A", "B1", "B2"}:
            st.write("• Có thể cân nhắc ngoại trú ở bệnh nhân chọn lọc sau khi dùng Hestia/PESI/sPESI, bảo đảm có thuốc kháng đông ngay và follow-up nhanh, tin cậy.")
        elif letter == "C":
            st.write("• Nhập viện/quan sát phù hợp mức nguy cơ và diễn tiến; C3 cần theo dõi sát nguy cơ xấu đi.")
        elif letter == "D":
            st.write("• Theo dõi mức độ cao/ICU tùy tình trạng và khả năng cần điều trị nâng cao.")
        elif letter == "E":
            st.write("• Hồi sức/ICU; ổn định trước khi chuyển viện.")

        if clean in {"A", "B1", "B2"}:
            if st.checkbox("Đánh giá khả năng điều trị ngoại trú", key="wz_outpatient"):
                out_tool = st.selectbox("Công cụ", ["Hestia", "PESI", "sPESI"], key="wz_out_tool")
                st.info(f"Dùng **{out_tool}** để xác nhận nguy cơ thấp; nếu không đạt nguy cơ thấp hoặc không bảo đảm thuốc/follow-up, không chọn ngoại trú.")

        st.subheader("2. Nhập thông tin bệnh nhân → chọn thuốc và tính liều")
        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input("Tuổi", 18, 120, 60, key="wz_tx_age")
            sex = st.radio("Giới", ["Nam", "Nữ"], horizontal=True, key="wz_tx_sex")
            weight = st.number_input("Cân nặng (kg)", 20.0, 300.0, 70.0, step=0.5, key="wz_tx_w")
            height = st.number_input("Chiều cao (cm)", 100.0, 230.0, 165.0, step=0.5, key="wz_tx_h")
            creat_unit = st.radio("Creatinine", ["µmol/L", "mg/dL"], horizontal=True, key="wz_tx_unit")
            if creat_unit == "µmol/L":
                creat_umol = st.number_input("Creatinine (µmol/L)", 1.0, 3000.0, 88.4, step=1.0, key="wz_tx_cru")
                creat_mg = creat_umol_to_mgdl(creat_umol) or 0.0
            else:
                creat_mg = st.number_input("Creatinine (mg/dL)", 0.01, 30.0, 1.0, step=0.1, key="wz_tx_crm")
        with c2:
            ckd = st.selectbox("CKD", ["Không/không rõ", "GĐ 2", "GĐ 3", "GĐ 4", "GĐ 5", "ESKD"], key="wz_tx_ckd")
            cp = st.selectbox("Bệnh gan / Child-Pugh", ["Không", "A", "B", "C"], key="wz_tx_cp")
            special = st.multiselect(
                "Tình huống đặc biệt",
                [
                    "Mang thai", "Cho con bú", "APS huyết khối", "Chỉ 1 aCL/β2-GPI nguy cơ thấp",
                    "U não", "HIT", "Phẫu thuật giảm béo <4 tuần", "Chống chỉ định tuyệt đối kháng đông",
                    "Nguy cơ chảy máu cao",
                ],
                key="wz_tx_special",
            )
            interaction = st.selectbox("Tương tác thuốc DOAC", ["Chưa rà soát", "Không có tương tác đáng kể", "Có tương tác cần tránh/chỉnh liều"], key="wz_tx_interaction")

        bmi = weight / ((height / 100.0) ** 2)
        crcl = cockcroft_gault(float(age), float(weight), float(creat_mg), sex == "Nữ")
        st.write(f"**BMI {bmi:.1f} kg/m² | CrCl Cockcroft–Gault {crcl:.1f} mL/phút**")
        if bmi >= 40 or bmi < 18.5:
            st.warning("Hình thể cực đoan: cần kiểm tra cách chọn cân nặng cho Cockcroft–Gault theo quy trình dược của cơ sở.")

        if st.button("Tính liều / cập nhật lựa chọn thuốc theo bệnh nhân", type="primary", key="wz_tx_calc"):
            st.session_state["tx_dose_ready"] = True
        dose_ready = bool(st.session_state.get("tx_dose_ready", False))

        ctx = MedicationContext(
            absolute_contraindication_to_anticoag="Chống chỉ định tuyệt đối kháng đông" in special,
            high_bleeding_risk_nonabsolute="Nguy cơ chảy máu cao" in special,
            pregnant="Mang thai" in special,
            breastfeeding="Cho con bú" in special,
            thrombotic_aps="APS huyết khối" in special,
            single_low_risk_aps_antibody_only="Chỉ 1 aCL/β2-GPI nguy cơ thấp" in special,
            brain_tumor="U não" in special,
            ckd_stage={"Không/không rõ":"none", "GĐ 2":"2", "GĐ 3":"3", "GĐ 4":"4", "GĐ 5":"5", "ESKD":"eskd"}[ckd],
            crcl_ml_min=crcl,
            child_pugh={"Không":"none", "A":"A", "B":"B", "C":"C"}[cp],
            bariatric_surgery_within_4_weeks="Phẫu thuật giảm béo <4 tuần" in special,
            documented_hit="HIT" in special,
            bmi=bmi,
            weight_kg=weight,
            interaction_review_completed=interaction != "Chưa rà soát",
            relevant_drug_interaction_present=interaction == "Có tương tác cần tránh/chỉnh liều",
            dose_inputs_confirmed=True,
        )

        if not dose_ready:
            st.info("Nhập thông tin bệnh nhân rồi bấm **Tính liều / cập nhật lựa chọn thuốc** để mở phần thuốc.")
        strat = anticoagulation_strategy(ctx, str(category)) if dose_ready else {"recommendations": [], "warnings": [], "exact_oral_dose_allowed": False}
        for r in strat["recommendations"]:
            st.write("• " + str(r))
        for w in strat["warnings"]:
            st.warning(str(w))

        if dose_ready and not ctx.absolute_contraindication_to_anticoag:
            if letter in {"C", "D", "E"}:
                options = ["Enoxaparin (LMWH)", "UFH"]
            else:
                options = ["Apixaban", "Rivaroxaban", "Dabigatran", "Edoxaban", "Enoxaparin (LMWH)", "UFH"]
            chosen = st.multiselect("Thuốc hiện có tại cơ sở / muốn xem liều", options, default=options[:2], key="wz_tx_drugs")

            for drug in chosen:
                if drug == "Enoxaparin (LMWH)":
                    st.markdown("**Enoxaparin**")
                    st.write(enoxaparin_pe_dose(ctx))
                elif drug == "UFH":
                    st.markdown("**UFH**")
                    st.write(ufh_vte_initial_dose(ctx))
                elif not strat["exact_oral_dose_allowed"]:
                    st.warning(f"{drug}: chưa mở liều cụ thể vì điều kiện an toàn/đủ điều kiện DOAC chưa đạt.")
                elif drug == "Apixaban":
                    st.markdown("**Apixaban**")
                    st.write(apixaban_vte_dose(ctx))
                elif drug == "Rivaroxaban":
                    st.markdown("**Rivaroxaban**")
                    st.write(rivaroxaban_vte_dose(ctx))
                elif drug == "Dabigatran":
                    st.markdown("**Dabigatran**")
                    st.write(dabigatran_vte_dose(ctx))
                elif drug == "Edoxaban":
                    pgp = st.checkbox("Có P-gp inhibitor liên quan edoxaban", key="wz_tx_ed_pgp")
                    st.markdown("**Edoxaban**")
                    st.write(edoxaban_vte_dose(ctx, relevant_pgp_inhibitor=pgp))
        elif dose_ready and ctx.absolute_contraindication_to_anticoag:
            st.error("Không tự động kê kháng đông khi có chống chỉ định tuyệt đối.")
            st.write("• Nếu cần lưới lọc, ưu tiên loại có thể thu hồi và lấy ra sớm khi có thể dùng lại kháng đông.")

        st.subheader("3. Hỗ trợ hô hấp / huyết động")
        if "R" in str(category):
            if str(category).startswith("ER") or str(category).startswith("E1R") or str(category).startswith("E2R"):
                st.write("• Suy hô hấp cần NIV/IMV: chuẩn bị hỗ trợ huyết động trước/đồng thời vì an thần và thông khí áp lực dương có thể gây sụp huyết động.")
            elif str(category).startswith("DR") or str(category).startswith("D1R") or str(category).startswith("D2R"):
                st.write("• Nhu cầu O₂ mức D-R: theo dõi sát; HFNC có thể hữu ích nếu thiếu oxy mức vừa–nặng.")
            else:
                st.write("• Có R mức C: cung cấp O₂ phù hợp; HFNC có thể hữu ích nếu thiếu oxy mức vừa–nặng.")
        if clean in {"D1", "D2"}:
            st.write("• Nếu nghi giảm preload: có thể cân nhắc bù dịch thận trọng; tránh truyền dịch quá mức gây quá tải RV.")
        if clean in {"D2", "E1", "E2"}:
            st.write("• Nếu có sốc tim do PE: vasopressor/inotrope được khuyến cáo; norepinephrine thường là lựa chọn vận mạch đầu tay, có thể thêm dobutamine khi cung lượng thấp.")
        if clean == "E2":
            st.write("• Sốc tim kháng trị: VA-ECMO là lựa chọn hợp lý nếu có nguồn lực; tiếp tục kháng đông đường tiêm nếu không chảy máu.")

        st.subheader("4. Reperfusion / điều trị nâng cao")
        if grp is None:
            st.warning("Phân nhóm R độc lập không ánh xạ trực tiếp sang Table 7. Cần PERT đánh giá toàn cảnh trước khi chọn advanced therapy.")
        else:
            table = ADVANCED_THERAPY_TABLE[grp]
            adv = st.selectbox(
                "Phương án hiện có hoặc đang cân nhắc",
                ["Không chọn advanced therapy", "Tiêu sợi huyết toàn thân", "Tiêu sợi huyết qua catheter", "Lấy huyết khối cơ học", "Phẫu thuật lấy huyết khối"],
                key="wz_adv",
            )
            if adv != "Không chọn advanced therapy":
                pos, desc = table[adv]
                st.write(f"**{pos} — {desc}**")

                prohibited = ("Có hại" in pos) or ("Không lợi ích" in pos) or pos == "N/A"
                if prohibited:
                    st.error("Không mở hướng dẫn liều/thực hiện cho lựa chọn này ở category hiện tại.")
                elif adv == "Tiêu sợi huyết toàn thân":
                    agent = st.selectbox("Thuốc tiêu sợi huyết có tại cơ sở", ["Alteplase", "Urokinase", "Streptokinase"], key="wz_lyt_agent")
                    st.caption("Chỉ dùng sau khi đã cân nhắc nguy cơ chảy máu và quyết định reperfusion. Tenecteplase không được tự động đưa liều cho PE vì chưa được FDA phê duyệt cho PE.")
                    if agent == "Alteplase":
                        contra_options = [
                            "Chảy máu nội đang hoạt động",
                            "Đột quỵ gần đây",
                            "Phẫu thuật nội sọ/nội tủy hoặc chấn thương đầu nặng trong 3 tháng",
                            "Tổn thương nội sọ làm tăng nguy cơ chảy máu",
                            "Cơ địa chảy máu",
                            "Tăng huyết áp nặng chưa kiểm soát",
                        ]
                    elif agent == "Urokinase":
                        contra_options = [
                            "Chảy máu nội đang hoạt động",
                            "Tai biến mạch não gần đây",
                            "Phẫu thuật nội sọ/nội tủy gần đây",
                            "Chấn thương gần đây, kể cả CPR",
                            "U nội sọ/AVM/phình mạch nội sọ",
                            "Cơ địa chảy máu",
                            "Tăng huyết áp động mạch nặng chưa kiểm soát",
                            "Quá mẫn với chế phẩm urokinase",
                        ]
                    else:
                        contra_options = [
                            "Chảy máu đang hoạt động",
                            "Tiền sử/biến cố nội sọ nguy cơ cao",
                            "Phẫu thuật/chấn thương lớn gần đây",
                            "Cơ địa chảy máu",
                            "Tăng huyết áp nặng chưa kiểm soát",
                            "Quá mẫn hoặc đã dùng streptokinase gần đây theo chống chỉ định của chế phẩm",
                        ]
                    common_contra = st.multiselect(
                        "Chống chỉ định quan trọng của thuốc đang chọn",
                        contra_options,
                        key="wz_lyt_contra",
                    )
                    bleeding = st.radio("Nguy cơ chảy máu sau đánh giá toàn diện", ["Chưa đánh giá", "Chấp nhận được", "Không chấp nhận được"], horizontal=True, key="wz_lyt_bleed")
                    if common_contra:
                        st.error("Có chống chỉ định quan trọng → không tự động hiển thị liều.")
                    elif bleeding != "Chấp nhận được":
                        st.warning("Chỉ hiển thị liều khi nguy cơ chảy máu được đánh giá là chấp nhận được.")
                    else:
                        if agent == "Alteplase":
                            dose_mode = st.radio("Phác đồ", ["Liều chuẩn theo nhãn", "Muốn cân nhắc liều giảm"], horizontal=True, key="wz_alt_mode")
                            if dose_mode == "Liều chuẩn theo nhãn":
                                st.success("**Alteplase 100 mg IV truyền trong 2 giờ.**")
                                st.caption("Khởi/khởi lại kháng đông đường tiêm gần cuối hoặc ngay sau truyền khi aPTT/thrombin time ≤2 lần bình thường theo nhãn Activase.")
                            else:
                                st.warning("AHA/ACC 2026 cho phép cân nhắc lower-dose systemic thrombolysis nhưng không quy định một công thức giảm liều duy nhất; công cụ không tự sáng tạo phác đồ.")
                        elif agent == "Urokinase":
                            ud = urokinase_label_pe_dose(weight)
                            st.success("**" + str(ud["dose"]) + "**")
                            st.caption(str(ud["note"]))
                        else:
                            sd = streptokinase_reference_pe_dose()
                            st.success("**" + str(sd["dose"]) + "**")
                            st.caption(str(sd["note"]))
                elif adv == "Tiêu sợi huyết qua catheter":
                    st.write("• Nếu dùng alteplase qua catheter: guideline không ủng hộ giảm xuống **<5 mg mỗi động mạch phổi** chỉ để giảm chảy máu so với mức **5–10 mg mỗi động mạch phổi**.")
                    st.write("• Liều tổng, thời gian truyền và thiết bị phụ thuộc protocol/device; công cụ không tự suy diễn một regimen duy nhất.")
                elif adv in {"Lấy huyết khối cơ học", "Phẫu thuật lấy huyết khối"}:
                    st.write("• Chọn theo nguồn lực, giải phẫu, nguy cơ chảy máu và đánh giá PERT; không có liều thuốc thủ thuật cố định để công cụ tự kê.")

        if st.button("Bắt đầu ca mới", use_container_width=True):
            reset_from(1)


if __name__ == "__main__":
    run_app()
