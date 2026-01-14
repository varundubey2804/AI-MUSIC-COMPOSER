# note_utils.py
import re
import music21

def sargam_to_western(token):
    """
    Converts Indian Sargam notation to Western keys (C Major base).
    Handles basic octaves attached to text (e.g., 'Sa4' -> 'C4').
    """
    # Mapping based on C Major (Bilawal Thaat) as a safe default
    map_rules = {
        'sa': 'C',
        're': 'D',
        'ga': 'E',
        'ma': 'F',
        'pa': 'G',
        'dha': 'A',
        'ni': 'B',
        'sa.': 'C' # Handle dotted notation if any
    }
    
    token_lower = token.lower()
    
    # Check if the token starts with a sargam syllable
    for sargam, western in map_rules.items():
        if token_lower.startswith(sargam):
            # Extract the octave number if present (e.g., '4' from 'Sa4')
            octave = re.findall(r'\d+', token)
            octave_suffix = octave[0] if octave else "4"
            
            # Return translated note
            return f"{western}{octave_suffix}"
            
    return token # Return original if no sargam match

def sanitize_notes(raw_llm_output):
    """
    Parses a messy string from LLM and extracts valid music21 note tokens.
    Handles commas, newlines, and converts Sargam to Western.
    """
    if not raw_llm_output:
        return []

    # 1. Clean basic delimiters
    clean_text = raw_llm_output.replace(',', ' ').replace('\n', ' ')
    
    # 2. Split by whitespace
    tokens = clean_text.split()
    
    valid_notes = []
    
    # 3. Regex for valid WESTERN note formats (e.g., C4, D#4, E-4, F)
    western_pattern = re.compile(r"^[A-G][#\-]?[0-9]?$")

    for token in tokens:
        clean_token = token.strip(".,;:\"'").replace("’", "")
        
        # Try converting Sargam first
        translated_token = sargam_to_western(clean_token)
        
        if western_pattern.match(translated_token):
            valid_notes.append(translated_token)
        else:
            # Only print warning if it's NOT a valid note
            pass 

    return valid_notes

def validate_stream_compatibility(note_list):
    """Final check to ensure music21 can actually parse the list."""
    playable_notes = []
    for n in note_list:
        try:
            # Test instantiation
            _ = music21.note.Note(n)
            playable_notes.append(n)
        except:
            continue
    return playable_notes