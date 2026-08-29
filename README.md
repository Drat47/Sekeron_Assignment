# Artist Intelligence & Recommendation System

**Author**: Dharmesh Singhal

This repository contains a lightweight, evidence-led intelligence and recommendation system built to parse artist profiles/portfolio media and generate matching recommendations for hirer briefs.

## 1. Environment Setup & Requirements
The system is built on Python 3.13 and uses standard libraries along with a few common utility packages.

### Prerequisites
- **Python**: version 3.10+ (tested on 3.13)
- **FFmpeg**: `ffprobe` must be installed on the system and available in the system's `PATH` variable to extract audio/video metadata details.

### Installation
Install the pinned dependencies using pip:
```bash
pip install requests pillow pypdf ffmpeg-python
```

## 2. Documented Run Command
To run the entire pipeline (download data if missing, extract capabilities, run matching recommendation engine, and process follow-up re-rankings), execute the following orchestrator command from the project root:
```bash
python run_pipeline.py
```
> [!NOTE]
> The orchestrator will automatically detect if the `Data_set/` folder is present, and if missing, it will execute `download_data.py` to pull the dataset files from Google Drive.
> 
> You can also manually download the dataset at any time by running:
> ```bash
> python download_data.py
> ```

This command runs:
1. `extract_intelligence.py` -> Generates `artist_intelligence.jsonl`
2. `recommend.py` -> Generates `recommendations.json`
3. `re_rank.py` -> Generates `updated_recommendation.json`

## 3. Core Approach & Media Selection Rationale
Instead of processing raw pixels or audio samples blindly (which is slow, expensive, and resource-heavy), the system implements a **Metadata-Led Technical Verification** strategy:
- **Profiles**: Profile text is parsed from `.txt` or `.docx` formats (by unzipping and parsing the raw XML `word/document.xml` structure to avoid heavy external word processor dependencies).
- **Images**: Pillow reads image size, format, and aspect ratios (e.g., vertical vs. square vs. horizontal).
- **Audio & Videos**: The system executes `ffprobe` to query codecs, sample rates, channels, duration, and video resolution.
- **Evidence Verification**: Claims in the profile (e.g., "Acoustic duo") are verified against technical media signals:
  - For M01 (duo), audio properties are scanned for stereo/mono layers, and track durations are measured.
  - For photographers, image aspect ratios and genre labels are checked.
  - For video editors, aspect ratios (9:16 vertical reels vs 16:9 horizontal) and editing formats are verified.

## 4. Implemented Choices & Rationale
- **Graceful Degradation for Damaged Cases**: 
  - **M03 (Raghav Sen)**: One of his portfolio files (`letting-go-342368.mp3`) is only 1.6 seconds long. The system flags this as a damaged/incomplete upload, decreases the confidence score to `Medium`, and lists it as an unknown.
  - **VO4 (Shivam)**: The profile folder has a corrupted/empty `media` folder, but work samples are placed in a subfolder named `Work`. The system correctly detects this fallback folder, parses the files, and flags the directory structure anomaly while keeping the confidence at `Medium`.
- **Match Scoring**:
  - The matching engine parses briefs into constraints and maps them to artist profiles. It ranks matching candidates using category tags, location limits, budget bounds, and verified media proof.
- **Re-ranking Trigger**:
  - In the follow-up for Brief 1, the budget increases to 15k and the requirement shifts to a high-impact 45-min "headline performance" for 80 guests. Quiet soloists (M03) are down-ranked, and a full live acoustic cover band (**KillRush - M04**) is promoted to #1 because the budget now permits a 5-piece live act.

## 5. Evaluation and Limitations
- **Strengths**: High execution speed (<2 seconds total pipeline execution), robust file error handling (BOM detection, fallback folders, XML unzipping), zero-cost API dependencies, and clear separation of claims vs. demonstrated evidence.
- **Limitations**: Since it does not use a massive multimodal neural network, the system does not analyze semantic aesthetics (e.g. the specific colors of a photo or the emotional tone of vocals) beyond technical file properties.
