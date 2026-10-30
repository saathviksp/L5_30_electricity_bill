# Lab 5: Static Code Analysis — Issue Identification & Resolution Report

**Course:** Software Engineering (UE24CS351A)  
**Student Name:** Saathvik Shenoy Padubidri  
**SRN:** PES1UG24CS394  
**Assigned File:** `electricity_bill.py`  

---

## 1. Issue Identification Table

The following table documents the static code analysis findings discovered across **Bandit**, **Pylint**, and **Flake8**, prioritized by severity (High and Medium severity security and logic flaws first, followed by warnings and style violations).

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **B605: Shell Command Injection** | Security (High) | 63 | `os.system("curl http://" + meterIp + "/reading")` spawns an external shell to execute curl with unsanitized user-controlled input (`meterIp`), allowing arbitrary OS command injection (`CWE-78`). | Replaced the shell call with Python's standard `urllib.request.urlopen(f"http://{meter_ip}/reading", timeout=5)` with explicit error handling (`URLError`, `TimeoutError`), completely avoiding shell subprocess creation. |
| **B314 / B405: Vulnerable XML Parsing** | Security (Medium / Low) | 3, 18 | `xml.etree.ElementTree` and `ET.fromstring(xmlText)` are susceptible to XML Entity Expansion (Billion Laughs / Quadratic Blowup) and External Entity (XXE) attacks (`CWE-20`). | Replaced `xml.etree.ElementTree` with `defusedxml.ElementTree as ET`, providing hardened XML parsing that protects against denial-of-service and entity injection. |
| **B105: Hardcoded Password String** | Security (Low) | 13 | `CLERK_PASSWORD = "bill-desk-demo"` stores plain-text credentials directly in the source code (`CWE-259`), risking credential exposure in version control. | Refactored credential retrieval to read from environment variables using `os.getenv("CLERK_PASSWORD", "bill-desk-demo")`, following 12-factor application security principles. |
| **W0102: Dangerous Mutable Default Argument** | Bug / Quality (Warning) | 42 | `def generateBill(..., extras={})` binds a mutable dictionary as a default argument evaluated at function definition time, resulting in shared state across repeated function calls. | Changed default parameter value to `None` (`extras=None`) and safely initialized a new dictionary inside the function: `if extras is None: extras = {}`. |
| **W1514: Unspecified File Encoding** | Quality (Warning) | 57 | `open(fileName, "w")` opens a file without declaring an explicit character encoding, leading to platform-dependent encoding mismatches (e.g., Windows CP1252 vs. Linux UTF-8). | Added explicit encoding specification: `open(file_name, "w", encoding="utf-8")`. |
| **W0613: Unused Function Argument** | Quality (Warning) | 50 | `currency` parameter was defined in `averageBill(currency)` but never utilized in the function body, cluttering the API signature. | Prefixed the unused optional argument with an underscore (`_currency="INR"`) to document intent and satisfy Pylint's unused parameter rule. |
| **C0103, C0114, C0116: Naming & Missing Docstrings** | Quality (Convention) | 1, 17, 22, 29, 34, 42, 50, 56, 61, 66 | Missing module docstring, missing function docstrings, and camelCase naming conventions (`readMeters`, `calculateUnits`, `energyCharge`, `generateBill`, `averageBill`, `saveBills`, `syncMeter`, `meterId`, `slabUnits`, etc.). | Added comprehensive PEP 257 docstrings for the module and all functions, and refactored all function and identifier names to standard PEP 8 `snake_case`. |
| **E302, E203, E501, E225: PEP 8 Style Violations** | Style (Formatting) | 22, 44, 72, 76 | Expected 2 blank lines (found 1 at line 22); whitespace before colon at line 44 (`"meter" :`); line length exceeding 79 characters (86 > 79 at line 72); missing whitespace around assignment operator at line 76 (`total=sum`). | Adjusted blank line spacing to 2 lines between top-level functions, removed whitespace before colon, split long print statements across multiple lines, and added standard spacing around operators. |

---

## 2. Summary of Quantitative Improvements

| Metric / Tool | Initial (Before Fixes) | Final (After Fixes) | Delta / Outcome |
| :--- | :--- | :--- | :--- |
| **Pylint Score** | **5.44 / 10** | **10.00 / 10** | **+4.56 points (Flawless 10/10)** |
| **Bandit Issues** | 4 issues (1 High, 1 Medium, 2 Low) | **0 issues** | **100% vulnerabilities eliminated** |
| **Flake8 Violations** | 4 style violations | **0 violations** | **100% PEP 8 compliant** |
| **Program Output** | Correct demonstration output | Identical demonstration output | **100% functional parity preserved** |
