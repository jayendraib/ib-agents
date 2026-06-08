
import pandas as pd
from io import BytesIO
#import uvicorn
import httpx
import json

#app = FastAPI(title="PAN Matcher API")

"""app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)"""

# ─────────────────────────────────────────────
# External API Configuration
# ─────────────────────────────────────────────
QA_AUTH_URL    = "https://qa-kycapi.indiabonds.com/api/Authenticate/GenerateToken"
QA_RESET_URL   = "https://qa-kycapi.indiabonds.com/api/UCC/ResetUCCStatusToPending"
PROD_AUTH_URL  = "https://kycapi.indiabonds.com/api/Authenticate/GenerateToken"
PROD_RESET_URL = "https://kycapi.indiabonds.com/api/UCC/ResetUCCStatusToPending"

AUTH_PAYLOAD = {
    "userName": "KycIntegration",
    "password": "Kyc#$@#&2022"
}


'''def read_file(upload_file: UploadFile):
    """Robustly reads CSV or Excel into a DataFrame."""
    content = upload_file.file.read()
    filename = upload_file.filename.lower()

    if filename.endswith('.csv'):
        return pd.read_csv(
            BytesIO(content),
            on_bad_lines='skip',
            engine='python'
        )
    else:
        return pd.read_excel(BytesIO(content))'''

def read_file(file_input):
    """
    Reads a file path (str) or file-like object (BytesIO, UploadedFile) into DataFrame.
    """
    try:
        # Case 1: String file path
        if isinstance(file_input, str):
            if file_input.lower().endswith('.csv'):
                return pd.read_csv(file_input)
            return pd.read_excel(file_input)
        
        # Case 2: File-like object (Streamlit UploadedFile, BytesIO, etc.)
        # Reset pointer to beginning (critical!)
        if hasattr(file_input, 'seek'):
            file_input.seek(0)
        
        # Detect CSV vs Excel by name or content
        is_csv = False
        if hasattr(file_input, 'name'):
            is_csv = file_input.name.lower().endswith('.csv')
        elif hasattr(file_input, 'getvalue'):
            # Peek at first bytes for CSV detection
            content = file_input.getvalue()
            if hasattr(file_input, 'seek'):
                file_input.seek(0)
            # Simple heuristic: if it contains commas in first line, likely CSV
            try:
                first_line = content.split(b'\n')[0].decode('utf-8', errors='ignore')
                is_csv = ',' in first_line and not first_line.startswith('PK')
            except:
                pass
        
        if is_csv:
            return pd.read_csv(file_input)
        return pd.read_excel(file_input)
        
    except Exception as e:
        raise ValueError(f"Failed to read file: {e}")

def find_client_id_column(df: pd.DataFrame, requested_col: str) -> str:
    """
    Returns the actual column name to use for Client ID.
    Priority: 1) User's requested column if it exists
              2) Auto-detect common names: ClientID, Client ID, client_id, etc.
              3) Empty string if nothing found
    """
    if requested_col and requested_col.strip() and requested_col.strip() in df.columns:
        return requested_col.strip()

    # Auto-detect common Client ID column names
    candidates = ["ClientID", "Client ID", "client_id", "ClientId", "CLIENTID", "clientID"]
    for col in candidates:
        if col in df.columns:
            return col

    return ""


def fetch_auth_token(auth_url=None):
    """
    Get Bearer token from IndiaBonds auth API.
    SYNCHRONOUS version - uses httpx.Client instead of AsyncClient.
    """
    url = auth_url or QA_AUTH_URL
    with httpx.Client() as client:
        resp = client.post(url, json=AUTH_PAYLOAD, timeout=30.0)
        
        raw_text = resp.text
        
        if resp.status_code >= 400:
            raise Exception(f"Auth API returned {resp.status_code}: {raw_text[:500]}")
        
        # Try JSON first
        try:
            data = resp.json()
            if isinstance(data, dict):
                token = (
                    data.get("token")
                    or data.get("Token")
                    or data.get("accessToken")
                    or data.get("access_token")
                    or data.get("bearerToken")
                )
                if token:
                    return str(token).strip()
            if isinstance(data, str):
                return data.strip()
        except json.JSONDecodeError:
            pass
        
        # Fallback: raw text as token
        cleaned = raw_text.strip().strip('"').strip("'")
        if cleaned:
            return cleaned
        
        raise Exception("Auth API returned empty body or no token found")


# ========== RESET API ==========
def reset_ucc_to_pending(token, clients, reset_url=None):
    """
    Calls ResetUCCStatusToPending API.
    Payload wrapped in {"clients": [...]} because the API expects an object.
    """
    url = reset_url or QA_RESET_URL
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {"clients": clients}

    with httpx.Client() as client:
        resp = client.post(url, json=payload, headers=headers, timeout=60.0)
        
        try:
            resp_data = resp.json()
            if not isinstance(resp_data, dict):
                resp_data = {"response": resp_data}
        except:
            resp_data = {"raw": resp.text}
        
        return resp.status_code, resp_data, resp.text


# ========== MAIN COMPARE FUNCTION ==========
# CHANGED: Removed all external API logic from this function.
# It now ONLY compares PANs and returns missing records.
def compare_pans(
    ib_file,
    ucc_file,
    ib_column="PAN",
    ucc_column="PAN No.",
    ib_client_id_column="Client ID"
):
    """
    Synchronous version of compare_pans.
    Accepts file paths (str) or file-like objects (Streamlit UploadedFile, BytesIO).
    """
    try:
        # ─── Read files ───
        df_ib = read_file(ib_file)
        df_ucc = read_file(ucc_file)

        # Create PAN column from RegistrationCode
        if 'RegistrationCode' not in df_ib.columns:
            return {
                "success": False,
                "error": "RegistrationCode column not found in IB file"
            }

        df_ib['PAN'] = df_ib['RegistrationCode'].astype(str).str.strip().str[:-2]

        # ─── Normalize PANs ───
        df_ib['__PAN_NORM__'] = df_ib[ib_column].astype(str).str.strip().str.upper()
        ucc_pans = set(df_ucc[ucc_column].dropna().astype(str).str.strip().str.upper())

        # ─── Auto-detect ClientID column ───
        effective_client_id_col = find_client_id_column(df_ib, ib_client_id_column)

        # ─── Build PAN -> ClientID mapping ───
        pan_to_client_id = {}
        if effective_client_id_col:
            for _, row in df_ib.iterrows():
                pan = str(row['__PAN_NORM__']).strip()
                if pan and pan not in ('NAN', 'NONE', ''):
                    raw_cid = row[effective_client_id_col]
                    client_id = str(raw_cid).strip() if pd.notna(raw_cid) else ""
                    if pan not in pan_to_client_id:
                        pan_to_client_id[pan] = client_id

        # ─── Find missing PANs ───
        seen = set()
        missing_records = []

        for pan in df_ib['__PAN_NORM__']:
            clean_pan = str(pan).strip()
            if clean_pan and clean_pan not in ('NAN', 'NONE', '') and clean_pan not in ucc_pans and clean_pan not in seen:
                seen.add(clean_pan)
                missing_records.append({
                    "PAN": clean_pan,
                    "ClientID": pan_to_client_id.get(clean_pan, "")
                })

        all_ib_pans = {p for p in df_ib['__PAN_NORM__'].dropna().astype(str).str.strip() if p and p not in ('NAN', 'NONE', '')}
        total_missing = len(missing_records)
        total_found = len(all_ib_pans) - total_missing

        return {
            "success": True,
            "stats": {
                "total_checked": len(all_ib_pans),
                "total_found": total_found,
                "total_missing": total_missing
            },
            "data": missing_records,
            "debug": {
                "ib_client_id_column_requested": ib_client_id_column,
                "ib_client_id_column_used": effective_client_id_col,
                "ib_columns": list(df_ib.columns),
                "sample_mapping": {k: pan_to_client_id[k] for k in list(pan_to_client_id.keys())[:5]}
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ========== NEW FUNCTION: Separate API Reset ==========
# ADDED: This is called independently by the second button in the frontend.
def reset_ucc_for_missing(missing_records, auth_url=None, reset_url=None):
    """
    Takes the missing_records list from compare_pans() and calls:
      1. Auth API to get token
      2. ResetUCCStatusToPending API
    """
    try:
        if not missing_records:
            return {
                "success": False,
                "error": "No missing records provided"
            }

        clients = []
        for rec in missing_records:
            cid = rec.get("ClientID", "")
            pan = rec.get("PAN", "")
            if cid and pan:
                clients.append({
                    "clientID": cid,
                    "pan": pan
                })

        if not clients:
            return {
                "success": False,
                "error": "No valid clientID+PAN pairs to send. Check that ClientID values are not empty."
            }

        token = fetch_auth_token(auth_url=auth_url)
        status_code, reset_resp, raw_text = reset_ucc_to_pending(token, clients, reset_url=reset_url)
        
        return {
            "success": 200 <= status_code < 300,
            "resetApiStatusCode": status_code,
            "resetApiResponse": reset_resp,
            "rawResponse": raw_text[:1000],
            "clientsProcessed": len(clients)
        }

    except Exception as api_err:
        return {
            "success": False,
            "error": str(api_err),
            "hint": "Check if auth API returns plain text token or if URL is reachable"
        }


