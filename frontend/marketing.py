"""
OBPP Compliance Agent — evaluates marketing scripts against the SEBI rulebook.
Rulebook is a constant; only the script changes per evaluation.
"""
import os
import json
import time
import re
from dataclasses import dataclass
from typing import List, Optional, Union
from enum import Enum
from pathlib import Path

RULEBOOK_PATH = os.getenv(
    "OBPP_RULEBOOK_PATH",
    str(Path(__file__).parent / "Advertisement Code - AI.docx"),
)

# ==================== CONFIG ====================
class Config:
    LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "")
    LITELLM_API_KEY  = os.getenv("LITELLM_API_KEY",  "")
    MODEL       = "gpt-4.1"
    TEMPERATURE = 0.0
    MAX_TOKENS  = 10000
    TIMEOUT     = 200.0
    CHUNK_SIZE  = 1500

# ==================== DATA MODELS ====================
class Verdict(Enum):
    COMPLIANT     = "Compliant — Requires Exchange Approval before Release"
    NON_COMPLIANT = "Non-Compliant — Changes Required"
    EXEMPT        = "Approval Exempt — Educational"

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH     = "HIGH"
    MEDIUM   = "MEDIUM"
    LOW      = "LOW"

@dataclass
class Violation:
    rule_id:    str
    rule_name:  str
    severity:   Severity
    message:    str
    found_text: str
    suggestion: str

@dataclass
class ComplianceReport:
    verdict:          Verdict
    score:            float
    violations:       List[Violation]
    passed:           List[str]
    corrected_script: Optional[str]
    summary:          str

# ==================== FILE READER ====================
SUPPORTED_EXTENSIONS = [".txt", ".md", ".docx", ".pdf"]

def read_script_file(file_path: Union[str, Path]) -> str:
    path = Path(file_path)
    ext  = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}. Allowed: {SUPPORTED_EXTENSIONS}")
    if ext in (".txt", ".md"):
        return path.read_text(encoding="utf-8")
    if ext == ".docx":
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    if ext == ".pdf":
        import fitz
        doc  = fitz.open(path)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text
    return ""

# ==================== KNOWLEDGE BASE ====================
class KnowledgeBase:
    def __init__(self):
        self.rules_text: str       = ""
        self.is_loaded:  bool      = False
        self._chunks:    List[str] = []

    def load(self, file_path: Union[str, Path]):
        self.rules_text = read_script_file(file_path)
        self._build_chunks()
        self.is_loaded = True

    def _build_chunks(self):
        paragraphs    = [p.strip() for p in self.rules_text.split("\n\n") if p.strip()]
        self._chunks  = []
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 > Config.CHUNK_SIZE and current_chunk:
                self._chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk += ("\n\n" + para) if current_chunk else para
        if current_chunk:
            self._chunks.append(current_chunk.strip())

    def get_chunks(self) -> List[str]:
        if not self.is_loaded:
            raise RuntimeError("Rulebook not loaded.")
        return self._chunks

# ==================== LLM CLIENT ====================
class LLMClient:
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            import openai
            self._client = openai.OpenAI(
                base_url   = Config.LITELLM_BASE_URL,
                api_key    = Config.LITELLM_API_KEY,
                timeout    = Config.TIMEOUT,
                max_retries= 0,
            )
        return self._client

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        response = self._get_client().chat.completions.create(
            model       = Config.MODEL,
            messages    = [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature = Config.TEMPERATURE,
            max_tokens  = Config.MAX_TOKENS,
            timeout     = Config.TIMEOUT,
        )
        return response.choices[0].message.content

# ==================== COMPLIANCE AGENT ====================
class ComplianceAgent:
    _SEV_DEDUCTIONS = {"CRITICAL": 25, "HIGH": 15, "MEDIUM": 10, "LOW": 5}

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb  = knowledge_base
        self.llm = LLMClient()

    def _chunk_system_prompt(self, chunk: str) -> str:
        return (
            "You are a SEBI OBPP Compliance Officer. Evaluate the script against ONLY these rules:\n"
            f"{chunk}\n\n"
            'Return JSON only: {"violations":[{"rule_id":"","rule_name":"","severity":"CRITICAL|HIGH|MEDIUM|LOW",'
            '"message":"","found_text":"","suggestion":""}],"passed":["rule names satisfied in this chunk"]}\n'
            "If no violations, return an empty violations array."
        )

    def _evaluate_chunk(self, chunk: str, script: str, meta: str) -> tuple:
        """Returns (result_dict, error_str_or_None)."""
        user_prompt = f"META:{meta}\n\nSCRIPT:\n{script}\n\nReturn JSON only."
        last_error = None
        for attempt in range(2):
            try:
                raw = self.llm.complete(self._chunk_system_prompt(chunk), user_prompt)
                try:
                    return json.loads(raw), None
                except json.JSONDecodeError:
                    m = re.search(r'\{.*\}', raw, re.DOTALL)
                    if m:
                        return json.loads(m.group()), None
                    last_error = f"JSON parse failed. Raw response: {raw[:200]}"
                    return {"violations": [], "passed": []}, last_error
            except Exception as e:
                last_error = f"{type(e).__name__}: {e}"
                if attempt == 0:
                    time.sleep(1)
        return {"violations": [], "passed": []}, last_error

    def _merge(self, chunk_results: List[dict], meta: str) -> ComplianceReport:
        all_violations: list = []
        all_passed:     list = []
        for r in chunk_results:
            all_violations.extend(r.get("violations", []))
            all_passed.extend(r.get("passed", []))

        seen, unique = set(), []
        for v in all_violations:
            key = v.get("rule_id", "") + v.get("found_text", "")
            if key and key not in seen:
                seen.add(key)
                unique.append(v)

        score = max(0, 100 - sum(
            self._SEV_DEDUCTIONS.get(v.get("severity", "MEDIUM"), 10) for v in unique
        ))

        has_critical = any(v.get("severity") == "CRITICAL" for v in unique)
        if has_critical or score < 80:
            verdict = Verdict.NON_COMPLIANT
        elif "Edu" in meta:
            verdict = Verdict.EXEMPT
        else:
            verdict = Verdict.COMPLIANT

        sev_map = {s.value: s for s in Severity}
        violation_objs = [
            Violation(
                rule_id    = v.get("rule_id", ""),
                rule_name  = v.get("rule_name", ""),
                severity   = sev_map.get(v.get("severity", "MEDIUM"), Severity.MEDIUM),
                message    = v.get("message", ""),
                found_text = v.get("found_text", ""),
                suggestion = v.get("suggestion", ""),
            )
            for v in unique
        ]

        if not unique:
            summary = f"Score {score}/100. No violations detected."
        else:
            critical_n = sum(1 for v in unique if v.get("severity") == "CRITICAL")
            high_n     = sum(1 for v in unique if v.get("severity") == "HIGH")
            parts = [f"Score {score}/100. {len(unique)} violation(s) found."]
            if critical_n:
                parts.append(f"{critical_n} CRITICAL issue(s) require immediate attention.")
            if high_n:
                parts.append(f"{high_n} HIGH severity issue(s) found.")
            parts.append(f"Key issues: {', '.join(v.get('rule_name','') for v in unique[:3])}.")
            summary = " ".join(parts)

        return ComplianceReport(
            verdict          = verdict,
            score            = score,
            violations       = violation_objs,
            passed           = list(set(all_passed)),
            corrected_script = None,
            summary          = summary,
        )

    def evaluate(
        self,
        script:             str,
        channel:            str  = "video",
        language:           str  = "English",
        is_educational:     bool = False,
        visual_description: str  = "",
        log_callback=None,
    ) -> ComplianceReport:
        if not self.kb.is_loaded:
            raise RuntimeError("Rulebook not loaded.")
        meta   = f"{channel}|{language}|{'Edu' if is_educational else 'Promo'}|{visual_description[:50]}"
        chunks = self.kb.get_chunks()
        if log_callback:
            log_callback(f"Rulebook split into {len(chunks)} chunk(s). Script length: {len(script)} chars.")
        chunk_results = []
        for i, c in enumerate(chunks):
            if log_callback:
                log_callback(f"Evaluating chunk {i+1}/{len(chunks)}...")
            result, err = self._evaluate_chunk(c, script, meta)
            if err and log_callback:
                log_callback(f"  ⚠️  Chunk {i+1} error: {err}")
            elif log_callback:
                n_v = len(result.get("violations", []))
                log_callback(f"  ✓  Chunk {i+1} done — {n_v} violation(s) found.")
            chunk_results.append(result)
        return self._merge(chunk_results, meta)

# ==================== REPORT HELPERS ====================
def report_to_json(report: ComplianceReport) -> str:
    return json.dumps({
        "verdict":   report.verdict.value,
        "score":     report.score,
        "summary":   report.summary,
        "violations": [
            {
                "rule_id":    v.rule_id,
                "rule_name":  v.rule_name,
                "severity":   v.severity.value,
                "message":    v.message,
                "found_text": v.found_text,
                "suggestion": v.suggestion,
            }
            for v in report.violations
        ],
        "passed": report.passed,
    }, indent=2, ensure_ascii=False)

# ==================== PUBLIC API ====================
_kb: Optional[KnowledgeBase] = None

def _get_kb() -> KnowledgeBase:
    global _kb
    if _kb is None:
        _kb = KnowledgeBase()
        _kb.load(RULEBOOK_PATH)
    return _kb

def evaluate_script(
    script_text:        str,
    channel:            str  = "video",
    language:           str  = "English",
    is_educational:     bool = False,
    visual_description: str  = "",
    log_callback=None,
) -> ComplianceReport:
    return ComplianceAgent(_get_kb()).evaluate(
        script             = script_text,
        channel            = channel,
        language           = language,
        is_educational     = is_educational,
        visual_description = visual_description,
        log_callback       = log_callback,
    )
