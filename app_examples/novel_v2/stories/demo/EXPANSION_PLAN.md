# Demo Story Expansion Plan

## Current State
- Story: "The Mysterious Forest" (20 scenes)
- No video transitions yet
- Demo visual novel with branching paths

## Target
- 25-30 scenes total
- 3 video transition/cutscene scenes
- Expanded narrative with more depth

## Story Arc Expansion

### Act 1: Awakening (Existing + New)
- intro → explore_clearing/call_out/forest_path
- NEW: `video_transition_1` - Opening cinematic (forest_trail.mp4)
- NEW: `deeper_forest` - After forest_path, exploring deeper
- NEW: `ancient_ruins` - Discovering ruins

### Act 2: The Quest (New scenes)
- NEW: `spirit_encounter` - Meeting forest spirits
- NEW: `magic_pool` - Sacred pool with visions
- NEW: `video_transition_2` - Spirit guide cinematic (spirit_journey.mp4)
- NEW: `dragon_cave_entrance` - Dangerous territory
- NEW: `underground_river` - Through the caves
- NEW: `treasure_room` - The amulet's origin

### Act 3: Resolution (Existing + New)
- challenge_accepted path (existing)
- NEW: `forest_shrine` - Final shrine
- NEW: `final_trial` - Test of courage
- NEW: `video_transition_3` - Climax cinematic (final_confrontation.mp4)
- NEW: `ending_legend` - Legendary hero ending
- NEW: `ending_freedom` - True freedom ending

## New Scenes List (15 scenes)
1. `video_transition_1` - Opening cinematic
2. `deeper_forest` - Darker forest area
3. `ancient_ruins` - Mysterious ruins
4. `spirit_encounter` - Forest spirits
5. `magic_pool` - Sacred pool vision
6. `video_transition_2` - Spirit journey cinematic
7. `dragon_cave_entrance` - Cave entrance
8. `underground_river` - Cave river
9. `treasure_room` - Ancient treasure
10. `forest_shrine` - Sacred shrine
11. `final_trial` - Final challenge
12. `video_transition_3` - Climax cinematic
13. `ending_legend` - Legendary hero ending
14. `ending_freedom` - True freedom ending
15. `scene_mirror_world` - Mirror dimension

## Video Transitions
1. `video_transition_1`: Opening - forest_trail.mp4 (5-10 sec)
2. `video_transition_2`: Spirit journey - spirit_journey.mp4 (5-10 sec)
3. `video_transition_3`: Final confrontation - final_battle.mp4 (5-10 sec)

## Character Additions
- spirit_guardian - Forest spirit guide
- ancient_dragon - Guardian of treasure (optional)

## Image Assets (Existing + New backgrounds)
Existing backgrounds can be reused creatively with new scenes.

## Implementation Order
1. Create new scene files (15 .scn files)
2. Create placeholder video files (0 bytes, named correctly)
3. Update existing scenes to connect to new scenes
4. Ensure proper branching paths