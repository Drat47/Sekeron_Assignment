# AI Usage Log

**Author**: Dharmesh Singhal

This document details the assistance provided by AI tools in building this system, the code generated, and the human verification performed.

## 1. AI Tools Utilized
- **Assistant**: ChatGPT (GPT-4o) & GitHub Copilot
- **Role**: Pair-programming partner for scripting, parsing structure design, formatting JSON schemas, and writing documentation templates.

## 2. AI-Generated Code & Assets
- **Download Script (`download_data.py`)**: Mapped file folders to GDrive IDs and set up request downloads.
- **DOCX Parser Helper**: Suggested unzipping docx files and querying `word/document.xml` paragraphs to read Word document files without needing a bulky Word library.
- **ffprobe JSON Parsing**: Provided the subprocess arguments to fetch media details in JSON format.
- **Pipeline Orchestrator (`run_pipeline.py`)**: Structured the sequential subprocess runner.

## 3. Human Verification and Changes Made
The following modifications, corrections, and logical verifications were performed on the AI suggestions:
1. **Network Error Handling**: Added a request retry loop with exponential backoff and connection-timeout settings to the GDrive downloader to handle remote abort issues.
2. **Download Skip Logic**: Implemented file-existence checks in the download script so it skips downloading files that are already completed, saving time and preventing duplicates on network resumes.
3. **Encoding Issues on Windows**: Identified cp1252 print errors on the Windows PowerShell terminal when outputting BOM unicode strings. Fixed this by redirecting profile data outputs into a UTF-8 text file (`gathered_profiles.txt`).
4. **Incorrect Path Creation**: Fixed a Windows `os.makedirs` crash in the downloader when downloading root files (empty dirname) by adding path existence guards.
5. **Re-ranking Logic Validation**: Verified the client requirements and updated weights manually to ensure that `KillRush (M04)` was correctly promoted for the headline slot due to the new budget and format constraints.
6. **Damaged Folder Fallback**: Verified that VO4 Shivam's work folder structure anomaly was handled correctly without throwing directory exceptions.
