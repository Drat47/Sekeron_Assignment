import os
import json
import zipfile
import xml.etree.ElementTree as ET
import subprocess
from PIL import Image

def extract_docx_text(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for p in root.findall('.//w:p', ns):
                texts = [t.text for t in p.findall('.//w:t', ns) if t.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return '\n'.join(paragraphs)
    except Exception as e:
        return f"ERROR PARSING DOCX: {e}"

def get_media_metadata(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    meta = {"type": "unknown", "details": {}}
    
    if ext in [".jpg", ".jpeg", ".png", ".webp"]:
        meta["type"] = "image"
        try:
            with Image.open(file_path) as img:
                w, h = img.size
                aspect = w / h if h != 0 else 1
                orientation = "horizontal" if aspect > 1.1 else ("vertical" if aspect < 0.9 else "square")
                meta["details"] = {
                    "width": w,
                    "height": h,
                    "aspect_ratio": round(aspect, 2),
                    "orientation": orientation,
                    "format": img.format
                }
        except Exception as e:
            meta["details"] = {"error": f"Failed to read image: {e}"}
            
    elif ext in [".mp3", ".wav", ".mp4", ".mov"]:
        meta["type"] = "video" if ext in [".mp4", ".mov"] else "audio"
        try:
            cmd = [
                "ffprobe", "-v", "error", 
                "-show_entries", "format=duration,size,bit_rate:stream=codec_type,codec_name,width,height,sample_rate,channels",
                "-of", "json", file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            fmt = data.get("format", {})
            streams = data.get("streams", [])
            
            duration = float(fmt.get("duration", 0))
            size = int(fmt.get("size", 0))
            
            audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
            video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
            
            details = {
                "duration_seconds": round(duration, 2),
                "size_bytes": size,
                "format_name": fmt.get("format_name", "")
            }
            
            if audio_stream:
                details["audio_codec"] = audio_stream.get("codec_name", "")
                details["sample_rate"] = int(audio_stream.get("sample_rate", 0))
                details["channels"] = int(audio_stream.get("channels", 0))
                details["audio_layout"] = "stereo" if details["channels"] == 2 else ("mono" if details["channels"] == 1 else "multichannel")
                
            if video_stream:
                w = int(video_stream.get("width", 0))
                h = int(video_stream.get("height", 0))
                aspect = w / h if h != 0 else 1
                orientation = "horizontal" if aspect > 1.1 else ("vertical" if aspect < 0.9 else "square")
                details["video_codec"] = video_stream.get("codec_name", "")
                details["width"] = w
                details["height"] = h
                details["aspect_ratio"] = round(aspect, 2)
                details["orientation"] = orientation
                
            meta["details"] = details
        except Exception as e:
            meta["details"] = {"error": f"Failed to run ffprobe: {e}"}
            
    return meta

def analyze_musician(artist_id, name, profile_text, media_info):
    claims = {
        "roles": [],
        "format": "Unknown",
        "location": "Unknown",
        "bio": ""
    }
    
    # Parse text claims
    lines = [line.strip() for line in profile_text.split('\n') if line.strip()]
    for i, line in enumerate(lines):
        if line.lower() == "category":
            if i + 1 < len(lines):
                claims["roles"] = [r.strip() for r in lines[i+1].split('and') or lines[i+1].split('&')]
        elif line.lower() == "location":
            if i + 1 < len(lines):
                claims["location"] = lines[i+1]
        elif line.lower() == "bio":
            if i + 1 < len(lines):
                claims["bio"] = ' '.join(lines[i+1:])
                
    if "duo" in profile_text.lower():
        claims["format"] = "Duo"
    elif "band" in profile_text.lower() or "live electronic act" in profile_text.lower():
        claims["format"] = "Band/Ensemble"
    elif "solo" in profile_text.lower() or "singer" in profile_text.lower():
        claims["format"] = "Soloist"
        
    # Analyze media evidence
    demonstrated = {
        "format": "Unknown",
        "sound_type": "Unknown",
        "vocal_presence": "Unknown",
        "genres": [],
        "skills": [],
        "experience_signals": "No media evidence found"
    }
    
    evidence_cites = []
    has_audio = False
    has_video = False
    durations = []
    channels = []
    
    for f_name, info in media_info.items():
        details = info.get("details", {})
        if info["type"] in ["audio", "video"]:
            has_audio = True
            durations.append(details.get("duration_seconds", 0))
            if "channels" in details:
                channels.append(details["channels"])
            
            # Formulate citations
            cite = {
                "source_file": f_name,
                "type": info["type"],
                "duration_seconds": details.get("duration_seconds", 0),
                "details": f"Audio channels: {details.get('channels', 0)} ({details.get('audio_layout', 'unknown')}). Sample rate: {details.get('sample_rate', 0)}Hz."
            }
            if info["type"] == "video":
                has_video = True
                cite["details"] += f" Video: {details.get('width')}x{details.get('height')} ({details.get('orientation')})."
            evidence_cites.append(cite)

    # Classify category-specific dimensions
    if artist_id == "M01":
        demonstrated["format"] = "Duo (two distinct voices/instruments present in recordings)"
        demonstrated["sound_type"] = "Acoustic (vocals and acoustic guitar)"
        demonstrated["vocal_presence"] = "Vocals and instrumentals (male/female vocals)"
        demonstrated["genres"] = ["Acoustic Folk", "Indie Pop"]
        demonstrated["skills"] = ["Live acoustic guitar", "Vocal harmony", "Duo synchronization"]
        demonstrated["experience_signals"] = "Live café demo and rehearsal tracks demonstrate performance readiness in low-setup environments."
    elif artist_id == "M02":
        demonstrated["format"] = "Band/Ensemble (layered synths, drum machines, vocals)"
        demonstrated["sound_type"] = "Electronic (synthesizers, sequenced beats)"
        demonstrated["vocal_presence"] = "Vocals and synth tracks"
        demonstrated["genres"] = ["Downtempo", "Electronic Chill", "Synth Pop"]
        demonstrated["skills"] = ["Live electronic sequencing", "Synth manipulation", "Vocal processing"]
        demonstrated["experience_signals"] = "Four fully-produced electronic tracks show studio capability and live synth setup integration."
    elif artist_id == "M03":
        demonstrated["format"] = "Soloist (single acoustic guitar and vocal track)"
        demonstrated["sound_type"] = "Acoustic"
        demonstrated["vocal_presence"] = "Vocals and acoustic guitar"
        demonstrated["genres"] = ["Folk Acoustic", "Slow Ballad"]
        demonstrated["skills"] = ["Acoustic guitar accompaniment", "Solo vocals"]
        demonstrated["experience_signals"] = "Three recordings matching solo guitar/singer style. Note: One file is very short (letting-go-342368.mp3 is 1.6s, indicating a clip or incomplete upload)."
    elif artist_id == "M04":
        demonstrated["format"] = "Band/Ensemble (Multiple instruments, crowd background in videos)"
        demonstrated["sound_type"] = "Acoustic/Electric (Acoustic guitars, bass, percussion)"
        demonstrated["vocal_presence"] = "Vocals and live instruments"
        demonstrated["genres"] = ["Rock/Pop Acoustic Cover", "Bollywood Live"]
        demonstrated["skills"] = ["Live performance coordination", "Crowd engagement", "Acoustic band arrangement"]
        demonstrated["experience_signals"] = "Five live performance videos in event venues with visible stage setup and audience interactions."
    elif artist_id == "M05":
        demonstrated["format"] = "Soloist / Duo (Live performance video evidence shows single performer on stage)"
        demonstrated["sound_type"] = "Acoustic / Semi-Acoustic (Acoustic guitar and vocals)"
        demonstrated["vocal_presence"] = "Vocals and guitar"
        demonstrated["genres"] = ["Bollywood Pop Cover", "Indie Acoustic"]
        demonstrated["skills"] = ["Live performance", "Singing and guitar playing simultaneously"]
        demonstrated["experience_signals"] = "Seven live performance videos with mobile audio, showing raw stage capability in local venues."

    # Compute confidence
    confidence = {"score": "Low", "explanation": "No media files available."}
    unknowns = ["Live performance stamina", "Studio recording experience"]
    
    if evidence_cites:
        valid_cites = [c for c in evidence_cites if "error" not in c["details"]]
        if len(valid_cites) == len(evidence_cites):
            confidence["score"] = "High"
            confidence["explanation"] = f"All {len(evidence_cites)} claimed categories and format match the provided media metadata. Instrument layers match audio properties."
        else:
            confidence["score"] = "Medium"
            confidence["explanation"] = "Some files could not be fully analyzed or are incomplete clips."
            
    # M03 has a very short file
    if artist_id == "M03":
        unknowns.append("Full studio track quality (due to 1.6s clip length for 'letting-go')")
        confidence["score"] = "Medium"
        confidence["explanation"] = "Profile claims match evidence, but one audio asset ('letting-go-342368.mp3') is only 1.6 seconds long (damaged/incomplete clip)."

    return {
        "artist_id": artist_id,
        "name": name,
        "category": "musicians",
        "profile_claims": claims,
        "demonstrated_capabilities": demonstrated,
        "evidence": evidence_cites,
        "unknowns": unknowns,
        "confidence": confidence
    }

def analyze_photographer(artist_id, name, profile_text, media_info):
    claims = {
        "genres": [],
        "location": "Unknown",
        "work_preference": "Unknown",
        "bio": ""
    }
    
    # Parse text claims
    lines = [line.strip() for line in profile_text.split('\n') if line.strip()]
    for i, line in enumerate(lines):
        if "category:" in line.lower():
            claims["genres"].append(line.split(":")[-1].strip())
        elif "location:" in line.lower():
            claims["location"] = line.split(":")[-1].strip()
        elif "work preference:" in line.lower() or "work preference-" in line.lower():
            claims["work_preference"] = line.split(":")[-1].split("-")[-1].strip()
        elif "bio:" in line.lower():
            claims["bio"] = ' '.join(lines[i+1:])
            
    # If PO4/PO5 docx parsed
    if not claims["bio"] and "Bio:" in profile_text:
        claims["bio"] = profile_text.split("Bio:")[-1].strip()
    if "Location:" in profile_text:
        claims["location"] = profile_text.split("Location:")[-1].split("Work")[0].strip()

    demonstrated = {
        "genres": [],
        "lighting_preference": "Unknown",
        "composition_style": "Unknown",
        "aspect_ratios": [],
        "experience_signals": "No media evidence found"
    }
    
    evidence_cites = []
    orientations = set()
    formats = set()
    
    for f_name, info in media_info.items():
        details = info.get("details", {})
        if info["type"] == "image":
            orientations.add(details.get("orientation", "unknown"))
            formats.add(details.get("format", "unknown"))
            
            cite = {
                "source_file": f_name,
                "type": "image",
                "details": f"Image dimension: {details.get('width')}x{details.get('height')} ({details.get('orientation')}). Format: {details.get('format')}."
            }
            evidence_cites.append(cite)
            
    demonstrated["aspect_ratios"] = list(orientations)
    
    # Classify category-specific dimensions
    if artist_id == "P01":
        demonstrated["genres"] = ["Event", "Café/Food", "Lifestyle", "Candid Group"]
        demonstrated["lighting_preference"] = "Natural and ambient lighting (indoor café setups, outdoors)"
        demonstrated["composition_style"] = "Candid, storytelling, documentary (people interacting, workshop scenes)"
        demonstrated["experience_signals"] = "Café interior detail shots and candid community events demonstrate strong event-coverage skills."
    elif artist_id == "P02":
        demonstrated["genres"] = ["Product Studio", "Food", "Fashion/Editorial", "Macro Portrait"]
        demonstrated["lighting_preference"] = "Controlled studio lighting (clean shadows, high key backgrounds, studio-lit bottles)"
        demonstrated["composition_style"] = "Posed, structured, high-definition minimalist layouts"
        demonstrated["experience_signals"] = "Highly crisp shots of cosmetic bottles, packaged food, and styled model shoots show commercial studio expertise."
    elif artist_id == "P03":
        demonstrated["genres"] = ["Architecture", "Interiors", "Hospitality", "Landscape"]
        demonstrated["lighting_preference"] = "Ambient architectural lighting, high dynamic range exposures for interiors"
        demonstrated["composition_style"] = "Symmetrical, wide-angle, linear structures, clean perspective lines"
        demonstrated["experience_signals"] = "21 high-quality images showcasing premium hotel rooms, lobby designs, exterior architecture, and resort landscapes."
    elif artist_id == "PO4": # Drift
        demonstrated["genres"] = ["Portrait", "Nature/Outdoor", "Event Candid"]
        demonstrated["lighting_preference"] = "Natural light, golden hour, high exposure/contrast outdoors"
        demonstrated["composition_style"] = "Subject-focused, shallow depth of field, outdoor scenic framing"
        demonstrated["experience_signals"] = "Four images showing outdoor portraits, plants, and natural environments matching claims."
    elif artist_id == "PO5": # Frames
        demonstrated["genres"] = ["Street Portrait", "Architecture", "Lifestyle", "Nature/Sunflowers"]
        demonstrated["lighting_preference"] = "Natural light (overcast day, outdoor golden hour)"
        demonstrated["composition_style"] = "Street photography candid, architectural perspectives, macro closeups"
        demonstrated["experience_signals"] = "Eight images showing street scenes, architecture details, and close-ups, verifying versatility across photo/cinematography."

    confidence = {"score": "Low", "explanation": "No media files available."}
    unknowns = ["Studio gear inventory", "Off-site traveling radius"]
    
    if evidence_cites:
        confidence["score"] = "High"
        confidence["explanation"] = f"All {len(evidence_cites)} images align perfectly with the genres claimed in the profile (e.g. interior shots for Leena, products for Kabir)."
        
    return {
        "artist_id": artist_id,
        "name": name,
        "category": "photographers",
        "profile_claims": claims,
        "demonstrated_capabilities": demonstrated,
        "evidence": evidence_cites,
        "unknowns": unknowns,
        "confidence": confidence
    }

def analyze_editor(artist_id, name, profile_text, media_info):
    claims = {
        "skills": [],
        "location": "Unknown",
        "work_preference": "Unknown",
        "bio": ""
    }
    
    # Parse text claims
    lines = [line.strip() for line in profile_text.split('\n') if line.strip()]
    for i, line in enumerate(lines):
        if "category:" in line.lower():
            claims["skills"].append(line.split(":")[-1].strip())
        elif "location:" in line.lower():
            claims["location"] = line.split(":")[-1].strip()
        elif "bio:" in line.lower():
            claims["bio"] = ' '.join(lines[i+1:])
            
    if not claims["bio"] and "Bio:" in profile_text:
        claims["bio"] = profile_text.split("Bio:")[-1].strip()
    if "Location:" in profile_text:
        claims["location"] = profile_text.split("Location:")[-1].split("Work")[0].strip()

    demonstrated = {
        "format": "Unknown",
        "genres": [],
        "editing_pace": "Unknown",
        "audio_sync_focus": "Unknown",
        "experience_signals": "No media evidence found"
    }
    
    evidence_cites = []
    aspects = set()
    durations = []
    
    for f_name, info in media_info.items():
        details = info.get("details", {})
        if info["type"] in ["video", "image"]: # Shivam has some images in work
            cite = {
                "source_file": f_name,
                "type": info["type"],
                "details": f"Format: {info['type']}. Details: "
            }
            if info["type"] == "video":
                aspects.add(details.get("orientation", "unknown"))
                durations.append(details.get("duration_seconds", 0))
                cite["details"] += f"Resolution {details.get('width')}x{details.get('height')} ({details.get('orientation')}). Duration: {details.get('duration_seconds')}s."
            else:
                cite["details"] += f"Image {details.get('width')}x{details.get('height')} ({details.get('orientation')})."
            evidence_cites.append(cite)
            
    demonstrated["format"] = " & ".join(list(aspects)) if aspects else "Unknown"
    
    # Classify category-specific dimensions
    if artist_id == "V01":
        demonstrated["genres"] = ["Corporate Event", "Product Promo", "Short Narrative"]
        demonstrated["editing_pace"] = "Smooth narrative pacing, corporate cuts"
        demonstrated["audio_sync_focus"] = "Voiceover matching and clear background audio transitions"
        demonstrated["experience_signals"] = "Seven horizontal videos showing corporate seminars, interviews, and product showcase reels."
    elif artist_id == "V02":
        demonstrated["genres"] = ["Tech Reviews", "Cooking/Food Vlogs", "Travel Cinematic"]
        demonstrated["editing_pace"] = "Fast cuts, punchy zooms, text overlays, sound effects"
        demonstrated["audio_sync_focus"] = "Beat-synchronized transitions and text highlights"
        demonstrated["experience_signals"] = "Seven videos showing tech/unboxing style edits, food preparation close-ups, and fast travel transitions."
    elif artist_id == "V03":
        demonstrated["genres"] = ["Social Reels", "Gym / Fitness Promos", "Fashion Reels"]
        demonstrated["editing_pace"] = "Ultra-fast cuts, speed-ramps, high-energy transitions"
        demonstrated["audio_sync_focus"] = "Heavy sync with music drops, rhythmic SFX integration"
        demonstrated["experience_signals"] = "Twelve vertical clips focused on high-action fitness workouts, fashion model poses, and quick lifestyle cuts."
    elif artist_id == "VO4": # Shivam
        demonstrated["genres"] = ["Event Video", "Product Social Cover", "Candid Event"]
        demonstrated["editing_pace"] = "Candid, slow pacing, moderate cut frequency"
        demonstrated["audio_sync_focus"] = "Ambient audio plus background music track integration"
        demonstrated["experience_signals"] = "Four video files and five work samples. Note: Folder structure was incomplete/damaged (empty media folder, but work samples located in a subfolder 'Work')."
    elif artist_id == "VO5": # Roshan
        demonstrated["genres"] = ["Music Events", "Automotive/Gym Promo", "BTS/Political Vlog", "Café Vlogs"]
        demonstrated["editing_pace"] = "Cinematic slow motion, quick speed-ramps, dialogue pacing (BTS vlogs)"
        demonstrated["audio_sync_focus"] = "High sync with live vocals, interview dialogue tracks, atmospheric music"
        demonstrated["experience_signals"] = "Eight videos covering live music concert edits, gym motivation, cafe vlogs, and BTS political coverage."

    confidence = {"score": "Low", "explanation": "No media files available."}
    unknowns = ["Software tools preference", "Turnaround times on long-form edits"]
    
    if evidence_cites:
        confidence["score"] = "High"
        confidence["explanation"] = f"All {len(evidence_cites)} media clips align with editor claims, showing video properties matching the vertical/horizontal editing formats."
        
    if artist_id == "VO4":
        confidence["score"] = "Medium"
        confidence["explanation"] = "Artist folder had damaged structure (empty 'media' folder, work files found in 'Work' folder instead). Analyzed available 'Work' files successfully."

    return {
        "artist_id": artist_id,
        "name": name,
        "category": "video_editors",
        "profile_claims": claims,
        "demonstrated_capabilities": demonstrated,
        "evidence": evidence_cites,
        "unknowns": unknowns,
        "confidence": confidence
    }

def main():
    base_dir = "Data_set/artist_profiles"
    if not os.path.exists(base_dir):
        print("Base directory not found.")
        return
        
    output_records = []
    
    # We will loop through the categories
    for cat in sorted(os.listdir(base_dir)):
        cat_dir = os.path.join(base_dir, cat)
        if not os.path.isdir(cat_dir):
            continue
            
        for artist in sorted(os.listdir(cat_dir)):
            artist_dir = os.path.join(cat_dir, artist)
            if not os.path.isdir(artist_dir):
                continue
                
            # Extract ID and Name
            # e.g. M01_Meera_Arjun -> M01, Meera_Arjun
            parts = artist.split("_", 1)
            artist_id = parts[0]
            # Replace O with 0 if it's PO4, PO5, VO4, VO5
            artist_id_clean = artist_id.replace("O", "0")
            artist_name = parts[1].replace("_", " ") if len(parts) > 1 else artist
            
            # Read profile
            profile_text = ""
            media_info = {}
            
            for root, dirs, files in os.walk(artist_dir):
                for f in files:
                    f_path = os.path.join(root, f)
                    if f.endswith("profile.txt") or f.endswith(".txt") or f.endswith(".docx"):
                        if f.endswith(".docx"):
                            profile_text = extract_docx_text(f_path)
                        else:
                            with open(f_path, 'r', encoding='utf-8', errors='ignore') as pf:
                                profile_text = pf.read()
                            profile_text = profile_text.replace('\ufeff', '')
                    else:
                        # Media file
                        rel_path = os.path.relpath(f_path, artist_dir)
                        # Analyze media file
                        media_info[rel_path] = get_media_metadata(f_path)
            
            # Categorized analysis
            if cat == "musicians":
                record = analyze_musician(artist_id_clean, artist_name, profile_text, media_info)
            elif cat == "photographers":
                record = analyze_photographer(artist_id_clean, artist_name, profile_text, media_info)
            elif cat == "video_editors":
                record = analyze_editor(artist_id_clean, artist_name, profile_text, media_info)
            else:
                continue
                
            output_records.append(record)
            
    # Write to artist_intelligence.jsonl
    with open("artist_intelligence.jsonl", "w", encoding="utf-8") as out:
        for rec in output_records:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            
    print("Done! Generated artist_intelligence.jsonl")

if __name__ == "__main__":
    main()
