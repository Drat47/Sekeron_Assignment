# Decision Note: Artist Intelligence & Recommendation System

**Author**: Dharmesh Singhal

## 1. Decisions Supported
The system is built to support two primary decisions in a creative marketplace:
1. **Capability Assessment Decision**: Determining the actual capabilities of an artist based on empirical portfolio evidence, distinguishing proven skills from self-claimed profile assertions.
2. **Talent Matching & Recommendation Decision**: Selecting and ranking the top two matching artists for incomplete hirer briefs, and determining the most impactful follow-up questions to resolve match uncertainty.

## 2. First-Version Scope and Non-Goals
### Scope
- **Evidence Extraction**: Parsing and extracting claimed vs. demonstrated capabilities from 15 profiles and their portfolio media (audio, video, images).
- **Media-backed Verification**: Matching profile claims to specific media files, timestamps, or visual/audio features.
- **Intent Interpretation**: Parsing 4 sparse hirer conversations into explicit constraints, assumptions, and key unknowns.
- **Ranking Engine**: Implementing a contextual matching scoring mechanism to produce a ranked shortlist of two artists per brief.
- **Feedback Loop**: Providing refinement questions and re-ranking recommendations based on a follow-up conversation update.

### Non-Goals
- **No Frontend/UI**: The system operates purely as a CLI-driven backend processor.
- **No Web Scraping**: Using only the provided dataset folders.
- **No Custom Model Training**: Utilizing only rules, heuristics, metadata, and existing pre-trained API or local models.
- **No Trust Signal Inferences**: The system explicitly does *not* evaluate punctuality, popularity, character, or professionalism.

## 3. Capability Dimensions by Category

| Category | Key Capability Dimensions | Observable Media Evidence Signals |
| :--- | :--- | :--- |
| **Photographers** | Genre/Setting, Subject Focus, Lighting Type, Composition Style, Gear/Medium | Subject matter (faces/products), exposure levels, indoor/outdoor metadata, depth of field |
| **Musicians** | Genre, Mood/Energy, Performance Format, Vocal Presence, Sound Type | Tempo (BPM), instruments heard, vocal presence (male/female/instrumental), track duration |
| **Video Editors** | Video Format, Cut Rhythm/Style, Narrative Flow, Audio-Video Sync | Aspect ratio (vertical/horizontal), cuts per minute, motion graphics, audio track integration |

## 4. Main Assumptions and Risks
- **Assumption 1**: The portfolio media provided is representative of the artist's current standard of work.
- **Assumption 2**: Hirer conversations, though incomplete, contain enough thematic context to infer a category (photo, audio, video).
- **Risk 1 (Damaged/Incomplete Data)**: One profile is damaged/incomplete, which could lead to low confidence scores; the system must gracefully degrade and flag this.
- **Risk 2 (Ambiguity)**: Multi-genre or multi-disciplinary artists might receive diluted match scores unless category-specific weights are applied.
- **Risk 3 (Uncertainty representation)**: A brief may be too sparse to differentiate between two high-ranking candidates, making high-priority clarification questions critical.
