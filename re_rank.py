import json

def main():
    updated = {
        "brief_01_cafe_music_update": {
            "title": "Cafe Launch Night headline Performance",
            "follow_up_context": {
                "new_messages": [
                    "Change of plan: management made it a launch night.",
                    "Expect around 80 guests.",
                    "Needs a proper 45-minute headline set, NOT background music for 3 hours.",
                    "Budget increased up to 15k (from 7-9k).",
                    "Acoustic is still fine but must feel like a 'performance/moment'.",
                    "Small cleared area available. Speaker situation still pending."
                ]
            },
            "original_ranking": [
                {
                    "rank": 1,
                    "artist_id": "M03",
                    "name": "Raghav Sen",
                    "reason": "Solo acoustic suited for low-profile 3-hour background music within a 7-9k budget."
                },
                {
                    "rank": 2,
                    "artist_id": "M01",
                    "name": "Meera & Arjun",
                    "reason": "Acoustic duo offering richer background sounds and some energy within a 9k max limit."
                }
            ],
            "revised_ranking": [
                {
                    "rank": 1,
                    "artist_id": "M04",
                    "name": "KillRush",
                    "why_recommended": "KillRush is a live acoustic band based in Noida/Delhi NCR. Their portfolio shows high-energy acoustic live sets in front of active audiences. A 5-piece live band setup is perfect for a 45-minute headline performance that creates a 'moment' for 80 guests on a launch night. The increased budget of 15k makes a full live band affordable.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/musicians/M04_KillRush/media/VID_20260820_214956_321.mp4",
                            "details": "Live video showing full band coordination, stage presence, and energetic vocal performance, proving capacity to hold a headline slot."
                        },
                        {
                            "source_file": "Data_set/artist_profiles/musicians/M04_KillRush/media/VID_20260820_215633_211.mp4",
                            "details": "Live performance snippet showing crowd engagement and upbeat tempos, matching the launch-night performance expectations."
                        }
                    ],
                    "suitability_signals": "Live acoustic band format, energetic Bollywood/Rock covers, Delhi NCR based, fits the updated 15k budget.",
                    "suitability_gaps": "Requires more floor space than a soloist or duo, and requires a dedicated sound system (PA)."
                },
                {
                    "rank": 2,
                    "artist_id": "M01",
                    "name": "Meera & Arjun",
                    "why_recommended": "Meera & Arjun remains in the top two, moving up to #2. As an acoustic duo, they can deliver a tight, harmonized 45-minute headline set. They have a smaller footprint than the full band KillRush, making them a safer choice if the venue's cleared performance area is very small, while still delivering a 'performance moment' within the 15k budget.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/MA_upbeat_medley_rehearsal.wav",
                            "details": "Upbeat medley rehearsal track demonstrating dual vocal harmonies and dynamic energy suitable for a performance set."
                        }
                    ],
                    "suitability_signals": "Acoustic duo format, easily fits the 15k budget, small footprint, Delhi NCR based.",
                    "suitability_gaps": "Smaller sound projection compared to a 5-piece band, which may feel less like a massive 'launch moment' in a room of 80 guests."
                }
            ],
            "rationale_for_change": {
                "what_changed": "The brief changed from 3 hours of quiet background music to a high-impact 45-minute headline performance set for a launch event with 80 guests, with a budget increase to 15k.",
                "why_rankings_shifted": "1. Raghav Sen (M03), the original #1, was downgraded because a quiet solo background singer is not suited for a headline 'moment' for 80 launch-night guests. 2. KillRush (M04), previously excluded due to their high budget and loud band format, was upgraded to #1 because the budget increase to 15k makes them viable, and their live acoustic band format is perfect for a headline performance. 3. Meera & Arjun (M01) moved to #2 as they offer a balanced compromise of headline performance capability and small footprint if the space is too small for a full band."
            },
            "unresolved_risks": [
                "The speaker/PA situation remains pending. KillRush (M04) requires a solid PA system, whereas Meera & Arjun (M01) can perform with a smaller portable amplifier."
            ]
        }
    }
    
    with open("updated_recommendation.json", "w", encoding="utf-8") as f:
        json.dump(updated, f, ensure_ascii=False, indent=2)
        
    print("Done! Generated updated_recommendation.json")

if __name__ == "__main__":
    main()
