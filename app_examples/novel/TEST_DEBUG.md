# Test Debug Report - Mini-Visual Novel

## Date: 2026-03-28
## Phase: Test Execution (Step 8)

---

## Test Results Summary

**Total: 15 tests**
- **Passed: 12**
- **Failed: 3**

---

## Failed Tests Analysis

### 1. `test_story_characters` - Wrong data structure

**Error:**
```
AssertionError: assert 'hermit' in {'default_mood': 'neutral', 'description': '...', 'id': 'hermit', 'name': 'Old Hermit'}
```

**Root Cause:** The `characters.yaml` format doesn't match the architecture specification.

- **Architecture expects:**
  ```yaml
  hermit:
    name: "Old Hermit"
    default_mood: neutral
    description: "A mysterious old man living in the forest"
  ```
  Which should parse to `{"hermit": {"name": "...", ...}}`

- **Current YAML format:**
  ```yaml
  id: hermit
  name: "Old Hermit"
  default_mood: neutral
  description: "A mysterious old man living in the forest"
  ```
  Which parses to flat `{"id": "hermit", "name": "...", ...}`

**Fix Required:** Update `stories/demo/assets/characters.yaml` to use proper nested format per architecture.

---

### 2. `test_parse_scene_basic` - Narrator text not parsed correctly

**Error:**
```
AssertionError: assert '' == 'Test narration'
  - Test narration
```

**Root Cause:** Scene parser doesn't handle narrator format correctly.

- **Architecture scene format:**
  ```yaml
  - narrator: "You wake up in a strange place..."
  ```
  Here the text IS the value of `narrator` key.

- **Current parser code in `scene.py`:**
  ```python
  elif "narrator" in d:
      speaker = "narrator"
      text = d.get("text", "")  # WRONG: Gets "" instead of the narrator value
  ```

**Fix Required:** Update `engine/scene.py` to get text from the narrator value itself, not from a `text` key.

---

### 3. `test_get_next_scene_no_choices` - Test expectation issue

**Error:**
```
AssertionError: assert 'fallback_scene' is None
```

**Analysis:** This is a test expectation issue, not a code bug.

The current `get_next_scene()` logic:
- If `choice_index` is valid (0 <= idx < len(choices)), return choices[idx].next_scene
- Otherwise, return `scene.next_scene` as fallback

When choices=[], next_scene="fallback_scene", and idx=0:
- 0 is NOT < 0 (empty list), so first condition fails
- Returns `scene.next_scene` = "fallback_scene"

The test expects `None` when passing an index to an empty choices list.

**Note:** This behavior is arguably correct (fallback to next_scene) but the test has a different expectation.

---

## Action Required

Per workflow step 9: Create architect task to plan fixes.

Issues to fix:
1. `stories/demo/assets/characters.yaml` - restructure to nested format
2. `engine/scene.py` - fix narrator text extraction
3. (Optional) `engine/choices.py` - clarify behavior for invalid indices
