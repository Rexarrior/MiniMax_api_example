# Fix Plan - Test Issues

## Date: 2026-03-28
## Phase: Architecture Fix Planning (Step 9)

---

## Issues to Fix

### Issue 1: `characters.yaml` Wrong Format

**Current format (wrong):**
```yaml
id: hermit
name: "Old Hermit"
default_mood: neutral
description: "A mysterious old man living in the forest"
```

**Correct format (per architecture):**
```yaml
hermit:
  name: "Old Hermit"
  default_mood: neutral
  description: "A mysterious old man living in the forest"
```

**Fix:** Restructure YAML to nested format with character id as top-level key.

---

### Issue 2: Narrator Text Not Parsed

**Current code in `scene.py`:**
```python
elif "narrator" in d:
    speaker = "narrator"
    text = d.get("text", "")  # Gets ""
```

**Scene format per architecture:**
```yaml
- narrator: "You wake up in a strange place..."
```

The text IS the value of the `narrator` key, not a nested `text` key.

**Fix:** For narrator, get text directly from the `narrator` value:
```python
elif "narrator" in d:
    speaker = "narrator"
    text = d.get("narrator", "") or ""
```

---

## Files to Modify

1. `app_examples/novel/stories/demo/assets/characters.yaml`
2. `app_examples/novel/engine/scene.py`

---

## Implementation

Apply fixes in step 10 (Code mode).
