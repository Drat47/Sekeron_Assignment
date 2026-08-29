import os
import subprocess
import sys

def run_step(script_name):
    print(f"\n>>> Running {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_name], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR executing {script_name}:")
        print(e.stderr)
        sys.exit(1)

def main():
    print("==================================================")
    print("      ARTIST INTELLIGENCE & RECOMMENDATION        ")
    print("==================================================")
    
    # Step 0: Ensure dataset is downloaded
    if not os.path.exists("Data_set"):
        print("Dataset directory not found. Running download_data.py...")
        run_step("download_data.py")
        
    # Step 1: Extract Artist Intelligence
    run_step("extract_intelligence.py")
    
    # Step 2: Generate Recommendations
    run_step("recommend.py")
    
    # Step 3: Generate Re-ranking Updates
    run_step("re_rank.py")
    
    print("==================================================")
    print("Pipeline Execution Completed Successfully!")
    print("Files Generated:")
    print("  - artist_intelligence.jsonl")
    print("  - recommendations.json")
    print("  - updated_recommendation.json")
    print("==================================================")

if __name__ == "__main__":
    main()
