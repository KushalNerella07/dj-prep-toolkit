"""Local extension: read cue, beat-grid and phrase data without screenshots."""
from typing import Any


def inspect_track_analysis(database: Any, track_id: str) -> dict:
    content = database.get_content(ID=str(track_id))
    if content is None or getattr(content, "rb_local_deleted", 0):
        raise ValueError(f"Active track {track_id} not found")
    result = {
        "track_id": str(content.ID),
        "title": content.Title,
        "bpm": content.BPM / 100.0,
        "length_seconds": content.Length,
        "analysis_directory": str(database.get_anlz_dir(content)),
        "cues": [
            {column.name: getattr(cue, column.name) for column in cue.__table__.columns
             if column.name not in {"created_at", "updated_at"}}
            for cue in database.get_cue(ContentID=str(content.ID))
        ],
        "cue_cache": [
            {"Cues": row.Cues, "rb_cue_count": row.rb_cue_count}
            for row in database.get_content_cue(ContentID=str(content.ID))
        ],
        "files": {},
        "beats": [],
        "phrases": [],
    }
    files = database.read_anlz_files(content)
    for path, parsed in files.items():
        result["files"][str(path)] = parsed.tag_types
        if "PQTZ" in parsed and not result["beats"]:
            beats, bpms, times = parsed.get("PQTZ")
            result["beats"] = [
                {"index": i + 1, "beat_in_bar": int(b), "time_seconds": float(t)}
                for i, (b, t) in enumerate(zip(beats, times))
            ]
        if "PSSI" in parsed:
            structure = parsed.get_tag("PSSI").content
            result["phrase_mood"] = int(structure.mood)
            result["phrase_end_beat"] = int(structure.end_beat)
            result["phrases"] = [
                {k: int(v) for k, v in entry.items() if not k.startswith("_")}
                for entry in structure.entries
            ]
    return result
