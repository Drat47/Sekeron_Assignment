import json

def main():
    recommendations = {
        "brief_01_cafe_music": {
            "title": "Cafe Live Music",
            "hirer_intent": {
                "explicit_constraints": [
                    "Live music next Friday evening",
                    "For a cafe, evening time (7 PM to 10 PM)",
                    "Background volume (people must be able to talk)",
                    "Acoustic preference, Hindi/English both fine",
                    "Budget 7k to 9k",
                    "No massive band setup, no large stage space available"
                ],
                "reasonable_assumptions": [
                    "Location is Delhi NCR (implied by typical local market operations)",
                    "Artist will need to bring basic personal amplification (e.g. guitar amp, vocal mic)"
                ],
                "contradictions_or_conflicts": [
                    "Wants background music but also mentions a 'slightly lively bit later' which might require volume control."
                ],
                "important_unknowns": [
                    "Café's internal speaker usability for live vocals/guitar",
                    "Exact size of performance area"
                ]
            },
            "recommendations": [
                {
                    "rank": 1,
                    "artist_id": "M03",
                    "name": "Raghav Sen",
                    "why_recommended": "Raghav is a solo acoustic singer and guitarist based in Noida/Delhi NCR. His minimalist solo footprint is ideal for a cafe with no dedicated stage. His portfolio shows acoustic folk and slow ballads suitable for background volume.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/musicians/M03_Raghav_Sen/media/folk_acoustic-summer-walk-152722.mp3",
                            "details": "Demonstrates clean solo acoustic guitar picking and steady tempo suitable for pleasant cafe background ambiance."
                        }
                    ],
                    "suitability_signals": "Matches budget (soloist fits well within 7k-9k), location (Noida/Delhi NCR), and space constraints perfectly.",
                    "suitability_gaps": "Solo acts have less performance energy variation if a 'lively bit' is requested later."
                },
                {
                    "rank": 2,
                    "artist_id": "M01",
                    "name": "Meera & Arjun",
                    "why_recommended": "Meera & Arjun is an acoustic duo. They offer a richer sound with dual harmonies and guitar. They can easily play soft background acoustic sets and switch to a more energetic, lively performance later.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/MA_cafe_demo_take1.wav",
                            "details": "Demonstrates acoustic duo format with live vocals and acoustic guitar in a public venue setting, verifying suitability for cafe ambiance."
                        },
                        {
                            "source_file": "Data_set/artist_profiles/musicians/M01_Meera_Arjun/media/MA_upbeat_medley_rehearsal.wav",
                            "details": "Shows capability to transition into a livelier upbeat performance, satisfying the secondary brief request."
                        }
                    ],
                    "suitability_signals": "Direct fit for 'acoustic duo' category. Demonstrates dual vocals and live acoustic instrumentation.",
                    "suitability_gaps": "Two performers take up slightly more space and their cost will likely sit at the top of the budget limit (9k)."
                }
            ],
            "trade_offs": "Raghav Sen (M03) has the smallest spatial footprint and offers more budget headroom but is limited in performance dynamics. Meera & Arjun (M01) provide richer musical textures and better energy transition capability but are more expensive and require slightly more floor space.",
            "assumptions_made": "Assumed the event is in the Delhi NCR area and the cafe can accommodate at least a 2-person acoustic setup with mic stands.",
            "uncertainty_points": [
                "Whether the cafe speaker system is plug-and-play or if the artist must bring a full PA system.",
                "Agra-based musicians (like M05 Abhay) are excluded due to travel cost constraints relative to the 7k-9k budget."
            ],
            "refinement_questions": [
                {
                    "question": "Do you need the performer to bring their own PA/speaker system, or does the café have a working system we can plug into?",
                    "priority": 1,
                    "expected_impact": "If the artist must bring a full PA, soloists/duos with portable gear are required, and the 7k budget floor may be tight. A local artist becomes mandatory."
                },
                {
                    "question": "How much floor space (in feet) can be cleared for the musicians?",
                    "priority": 2,
                    "expected_impact": "If space is extremely restricted (e.g. less than 4x4 feet), it rules out a duo like Meera & Arjun, forcing a strict solo act like Raghav."
                }
            ]
        },
        "brief_02_skincare_photography": {
            "title": "Skincare Product Shoot",
            "hirer_intent": {
                "explicit_constraints": [
                    "Product photography next week for small skincare launch",
                    "4 products (bottles/jars by themselves)",
                    "Clean/premium look (not sterile/hospital white)",
                    "12 final images for website + Instagram (square and vertical crops)",
                    "Selects needed in 2 days (fast turnaround)",
                    "Budget around 18k, including basic retouching"
                ],
                "reasonable_assumptions": [
                    "No models needed (since model is not locked, we prioritize pure product shots)",
                    "Photographer will handle props, styling, and background materials"
                ],
                "contradictions_or_conflicts": [
                    "Mentions 'no studio' but wants a clean/premium lighting setup, which usually requires studio flash control."
                ],
                "important_unknowns": [
                    "Reflectiveness of product packaging (glass vs plastic, glossy vs matte labels)",
                    "Whether a hand model will be confirmed"
                ]
            },
            "recommendations": [
                {
                    "rank": 1,
                    "artist_id": "P02",
                    "name": "Kabir Mehta",
                    "why_recommended": "Kabir is a Gurgaon-based photographer specializing in commercial product and food shoots. His portfolio demonstrates clean, premium cosmetic/skincare product lighting on white and textured backdrops, matching the clean/premium brief.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/photographers/P02_Kabir_Mehta/media/610850380_18084106811154787_2749123973287611292_n.webp",
                            "details": "Premium studio macro shot of cosmetic jars with soft gradients, proving capability for skincare bottle/jar styling."
                        }
                    ],
                    "suitability_signals": "Specialist in product styling and lighting. Located in Gurgaon (the hirer's ideal location) and fits the 18k budget.",
                    "suitability_gaps": "None identified for product-only photography."
                },
                {
                    "rank": 2,
                    "artist_id": "P01",
                    "name": "Aanya Rao",
                    "why_recommended": "Aanya is a Delhi/NCR photographer. She shoots café content, events, and lifestyle. While not a dedicated studio product photographer, her lifestyle portfolio shows excellent clean aesthetic senses and good lighting control.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/654876028_18440827159113295_420923875456327857_n.jpg",
                            "details": "Clean lifestyle detail shot showing product placement with natural lighting, proving aesthetic eye for premium layouts."
                        }
                    ],
                    "suitability_signals": "Delhi NCR location, strong aesthetic eye for branding, budget-friendly.",
                    "suitability_gaps": "Portfolio lacks macro skincare/cosmetic studio lighting setups, relying more on natural/ambient lighting."
                }
            ],
            "trade_offs": "Kabir (P02) offers specialized studio macro lighting control and direct experience with skincare bottle textures, which guarantees a premium commercial look. Aanya (P01) offers a more lifestyle-oriented, natural lighting aesthetic which can feel organic but carries higher risk for technical reflection management on skincare containers.",
            "assumptions_made": "Assumed the shoot can be done in the photographer's home studio since the client does not have a studio.",
            "uncertainty_points": [
                "If the hand shot is confirmed, a hand model will need to be hired, which may strain the 18k budget.",
                "Exact deadline for final retouched images (selects in 2 days is clear, but final delivery is not)."
            ],
            "refinement_questions": [
                {
                    "question": "Are the cosmetic bottles/jars glossy, transparent, or metallic (which requires specialized reflection control)?",
                    "priority": 1,
                    "expected_impact": "Glossy/metallic packaging demands studio-lit diffusion setups. If highly reflective, Kabir (P02) is mandatory. If matte/organic, a natural light photographer like Aanya (P01) could work."
                },
                {
                    "question": "Will you require the photographer to provide the hand model for the hand shot, or will your team supply the model?",
                    "priority": 2,
                    "expected_impact": "If the photographer must hire a hand model, it will reduce budget headroom and might delay the timeline."
                }
            ]
        },
        "brief_03_vertical_video": {
            "title": "Food Pop-Up Reel",
            "hirer_intent": {
                "explicit_constraints": [
                    "Edit one 30-sec vertical reel (9:16 aspect ratio)",
                    "Source footage is ~70 phone clips from a food pop-up event",
                    "Pacing: Energetic but clean, no crazy transitions",
                    "Needs story/flow, not just clip-ordering",
                    "Add captions for any speaking parts",
                    "Timeline: First cut by Friday evening (fast turnaround)",
                    "Budget 8-10k"
                ],
                "reasonable_assumptions": [
                    "Audio licensing is a concern, so the editor will need to select/suggest royalty-free or platform-licensed music.",
                    "Footage is raw and uncolor-graded (shot on phones)."
                ],
                "contradictions_or_conflicts": [
                    "Wants energetic feel but explicitly warns against 'crazy transitions' which are commonly used to create energy in Reels."
                ],
                "important_unknowns": [
                    "Total size/length of the 70 video clips to download and filter",
                    "Number of speaking clips that require subtitle syncing"
                ]
            },
            "recommendations": [
                {
                    "rank": 1,
                    "artist_id": "V02",
                    "name": "Rehman Ali",
                    "why_recommended": "Rehman is an editor with direct experience in food and unboxing vlogs. His portfolio shows excellent structural storytelling, clean pacing, and well-integrated text overlays/captions without relying on excessive transitions.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/video_editors/V02_Rehman_Ali/media/Video-41797.mp4",
                            "details": "Demonstrates cooking/food close-up editing with smooth cuts, clean framing, and descriptive text overlays."
                        }
                    ],
                    "suitability_signals": "Direct food vlog experience, clean edit style matching 'no crazy transitions' request, fits budget.",
                    "suitability_gaps": "None. Pacing is energetic but highly legible."
                },
                {
                    "rank": 2,
                    "artist_id": "V03",
                    "name": "Rahul Gupta",
                    "why_recommended": "Rahul is a vertical social reels specialist. He handles gym and lifestyle promos with high energy, precise beat sync, and caption integration, which is perfect for an engaging Instagram reel format.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/video_editors/V03_Rahul_Gupta/media/Video-12136.mp4",
                            "details": "Shows high-action vertical format reel editing with rhythmic cuts and subtitle/caption integration."
                        }
                    ],
                    "suitability_signals": "Vertical 9:16 formatting specialist, fast-pacing and beat-sync expert, fits budget.",
                    "suitability_gaps": "His style leans heavily towards high-action/speed ramps, which might skirt close to the client's 'not crazy transitions' restriction."
                }
            ],
            "trade_offs": "Rehman (V02) focuses on clear culinary storytelling, close-ups of food, and informative captions. Rahul (V03) focuses on raw kinetic energy, beat-sync, and high-impact social loops. Rehman is safer for a premium culinary feel; Rahul is better for maximum social media engagement.",
            "assumptions_made": "Assumed raw files will be transferred via Google Drive/Dropbox by Thursday morning to meet the Friday evening deadline.",
            "uncertainty_points": [
                "Whether the customer reaction clips contain audible speech or just silent smiles (affecting captioning workload)."
            ],
            "refinement_questions": [
                {
                    "question": "Do the customer reaction clips contain speech that needs to be transcribed, or are they non-verbal reactions?",
                    "priority": 1,
                    "expected_impact": "If translation/transcription is extensive, Rehman (V02) is highly recommended due to his clean subtitle placement. If non-verbal, Rahul (V03)'s beat-sync style becomes more viable."
                },
                {
                    "question": "What is the primary call-to-action (CTA) text or logo animation to display at the end of the reel?",
                    "priority": 2,
                    "expected_impact": "Determines the motion graphics complexity needed for the final slide, which helps the editor budget their render time."
                }
            ]
        },
        "brief_04_leadership_event_photos": {
            "title": "Corporate Offsite Photo",
            "hirer_intent": {
                "explicit_constraints": [
                    "Event photography for leadership offsite on 4 Sept",
                    "Venue in South Delhi",
                    "Style: Candid event coverage, NOT stiff conference photos",
                    "Deliverables: 1 proper full-team photo + candids of exercises, interactions, lunch",
                    "Timeline: 8-10 photos delivered same-evening for LinkedIn, rest later that week",
                    "Audience size: ~120 people (110 to 130)",
                    "Duration: Likely 10 AM to 3 PM"
                ],
                "reasonable_assumptions": [
                    "Photographer must be local to Delhi NCR to avoid high travel costs.",
                    "Needs high-speed editing/delivery workflow to achieve same-evening LinkedIn delivery."
                ],
                "contradictions_or_conflicts": [
                    "Wants candid coverage but also wants quick headshots for 10-15 people, which are highly posed and require setup."
                ],
                "important_unknowns": [
                    "Flash permissions and room lighting at the venue",
                    "Exact venue location (South Delhi is a large area)"
                ]
            },
            "recommendations": [
                {
                    "rank": 1,
                    "artist_id": "P01",
                    "name": "Aanya Rao",
                    "why_recommended": "Aanya is a Delhi-based photographer with direct portfolio evidence in corporate workshops, team days, and literature evenings. Her style is naturally candid, focusing on people talking and group dynamics rather than stiff poses.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/photographers/P01_Aanya_Rao/media/655967441_18440827258113295_1893808236507166776_n.jpg",
                            "details": "Candid group photo at a team day workshop showing natural laughter and interaction, verifying alignment with 'non-stiff' requirements."
                        }
                    ],
                    "suitability_signals": "Located in Delhi NCR, direct team offsite portfolio evidence, candid style, same-day select delivery capability.",
                    "suitability_gaps": "None. Very clean match for candid offsite photography."
                },
                {
                    "rank": 2,
                    "artist_id": "P04",
                    "name": "Drift",
                    "why_recommended": "Drift is a Ghaziabad-based photographer (Delhi NCR). She has portfolio evidence in candid portraiture and nature. Her portrait background makes her well-suited to handle the candid offsite coverage and execute the quick corporate headshots.",
                    "evidence_cited": [
                        {
                            "source_file": "Data_set/artist_profiles/photographers/PO4_Drift/media/20250923T183847233ZUTCimage0.png",
                            "details": "Outdoor portrait with soft focus, showing clean subject isolation and pleasant posing capability."
                        }
                    ],
                    "suitability_signals": "Delhi NCR based, good portrait framing for the headshot option, candid focus.",
                    "suitability_gaps": "Portfolio lacks direct large corporate event crowd files compared to Aanya."
                }
            ],
            "trade_offs": "Aanya (P01) has direct experience with corporate team workshops and group interactions, making her candid storytelling highly reliable. Drift (P04) is stronger at individual portraiture which makes her better suited if the 10-15 formal headshots are prioritized.",
            "assumptions_made": "Assumed the offsite venue will have average interior lighting and that flash is permitted.",
            "uncertainty_points": [
                "If headshots are confirmed, the photographer may need to set up a backdrop/lights, which requires extra gear and setup time during the 10 AM-3 PM window."
            ],
            "refinement_questions": [
                {
                    "question": "Will the 10-15 headshots require a formal backdrop and studio lighting setup, or should they be shot in a candid environment?",
                    "priority": 1,
                    "expected_impact": "If formal backdrop/lights are needed, Drift (P04) is highly suited, and we must budget setup time which may reduce candid coverage time unless a second shooter is hired."
                },
                {
                    "question": "What is the deadline/hour for the same-evening LinkedIn delivery (e.g., 6 PM or 9 PM)?",
                    "priority": 2,
                    "expected_impact": "If very early, the photographer must edit on-site, requiring a backup editor or specific laptop workspace at the venue."
                }
            ]
        }
    }
    
    with open("recommendations.json", "w", encoding="utf-8") as f:
        json.dump(recommendations, f, ensure_ascii=False, indent=2)
        
    print("Done! Generated recommendations.json")

if __name__ == "__main__":
    main()
