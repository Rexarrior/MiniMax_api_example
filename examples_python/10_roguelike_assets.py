#!/usr/bin/env python3
"""Generate pixel art assets for a 2D roguelike game using MiniMax image-01 API."""

from __future__ import annotations

import json
import os
import sys
import time
import httpx

import minimax_http as mh

ASPECT_RATIO = "1:1"
PIXEL_ART_STYLE = "16-bit SNES style pixel art"
OUTPUT_DIR = mh.out_dir() / "roguelike_assets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ASSETS = [
    (
        "champion_gladiator",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a Roman gladiator champion warrior, "
            "full body character with metal helmet, chainmail armor, short sword (gladius) and round shield. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, sword held at side, shield raised slightly. "
            "TOP-RIGHT panel (green background): walking pose, one leg forward, sword and shield in motion. "
            "BOTTOM-LEFT panel (red background): attacking pose, sword swung forward in a slashing motion, shield pushed ahead. "
            "BOTTOM-RIGHT panel (yellow background): defending pose, shield raised high blocking, sword held ready behind shield. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet, white background outside the colored panels."
        ),
    ),
    (
        "enemy_skeleton_warrior",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a skeleton warrior enemy, undead skeleton soldier wielding a rusty sword and cracked shield, "
            "glowing red eye sockets, bones with dark cracks. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, sword planted in ground. "
            "TOP-RIGHT panel (green background): walking pose, shambling forward with sword raised. "
            "BOTTOM-LEFT panel (red background): attacking pose, sword swung overhead in a downward strike. "
            "BOTTOM-RIGHT panel (purple background): dead pose, skeleton collapsed on the ground, bones scattered, sword dropped. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_goblin_thief",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a goblin thief enemy, small green-skinned humanoid with pointy ears, "
            "wearing ragged brown leather armor, carrying a curved dagger and a small pouch, sneaky expression with yellow eyes. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, crouching slightly, dagger in hand. "
            "TOP-RIGHT panel (green background): sneaking/walking pose, hunched forward, tiptoeing. "
            "BOTTOM-LEFT panel (red background): attacking pose, lunging forward with dagger thrust. "
            "BOTTOM-RIGHT panel (purple background): dead pose, goblin lying flat on back, dagger dropped, tongue out. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_orc_berserker",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of an orc berserker enemy, large muscular green-skinned humanoid with tusks protruding from lower jaw, "
            "wearing spiked leather armor and metal shoulder pads, wielding a massive two-handed battle axe, angry red eyes. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, axe resting on shoulder, roaring. "
            "TOP-RIGHT panel (green background): walking pose, stomping forward with axe held ready. "
            "BOTTOM-LEFT panel (red background): attacking pose, axe swung down in a powerful overhead chop. "
            "BOTTOM-RIGHT panel (purple background): dead pose, orc fallen face-down, axe beside him. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_giant_rat",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a giant rat enemy, oversized rat the size of a dog, "
            "dark brown fur, pink hairless tail, sharp yellow teeth, beady red eyes, long whiskers. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, on all fours, sniffing. "
            "TOP-RIGHT panel (green background): walking/scuttling pose, moving forward low to ground. "
            "BOTTOM-LEFT panel (red background): biting/attacking pose, leaping forward with jaws open wide, teeth bared. "
            "BOTTOM-RIGHT panel (purple background): dead pose, rat lying on its side, legs curled, tongue out. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_giant_spider",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a giant spider enemy, massive spider with eight long jointed legs, "
            "bulbous dark purple body with red hourglass marking on abdomen, multiple glowing yellow eyes, fangs dripping venom. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, legs spread, body lowered. "
            "TOP-RIGHT panel (green background): walking pose, legs in motion crawling forward. "
            "BOTTOM-LEFT panel (red background): attacking/biting pose, rearing up on hind legs, fangs forward, venom dripping. "
            "BOTTOM-RIGHT panel (purple background): dead pose, spider curled up on its back, legs limp. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_slime",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a slime monster enemy, translucent teal gelatinous blob creature, "
            "with two simple black dot eyes and a small mouth, small floating core crystal visible inside its body, "
            "slightly wobbly amorphous shape. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, round blob shape resting on ground. "
            "TOP-RIGHT panel (green background): moving pose, stretched forward as if hopping/sliding. "
            "BOTTOM-LEFT panel (red background): attacking pose, leaping forward with body stretched mid-air, mouth open. "
            "BOTTOM-RIGHT panel (purple background): dead pose, slime dissolved into a flat puddle on the ground, core crystal visible. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_fire_demon",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a fire demon enemy, humanoid monster made of dark obsidian rock "
            "with cracks of glowing orange lava running through its body, horns on head, flaming hands, "
            "burning eyes, small bat-like wings on back. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, arms at sides with flames flickering. "
            "TOP-RIGHT panel (green background): walking pose, striding forward with fire trailing behind. "
            "BOTTOM-LEFT panel (red background): attacking pose, both hands thrust forward shooting fireballs. "
            "BOTTOM-RIGHT panel (purple background): dead pose, demon crumbled into a pile of dark rocks, fire extinguished. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_ghost",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a ghost enemy, translucent pale blue-white spectral spirit, "
            "tattered flowing robe-like body with no legs, hollow dark eye sockets, gaping mouth, "
            "wispy ethereal trail below, faintly glowing aura. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): floating idle pose, hovering in place, arms dangling. "
            "TOP-RIGHT panel (green background): floating forward pose, drifting toward viewer, arms reaching. "
            "BOTTOM-LEFT panel (red background): attacking pose, mouth wide open in a shriek, arms lunging forward to grab. "
            "BOTTOM-RIGHT panel (purple background): dead pose, ghost fading away, becoming transparent and dissipating into mist. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_werewolf",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a werewolf enemy, bipedal wolf-humanoid hybrid, "
            "covered in thick dark grey fur, muscular build, sharp claws on hands and feet, "
            "wolf snout with fangs, pointed ears, glowing amber eyes, wearing torn pants. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, hunched, claws flexed, growling. "
            "TOP-RIGHT panel (green background): walking pose, prowling forward on digitigrade legs. "
            "BOTTOM-LEFT panel (red background): attacking pose, lunging forward with claws slashing, jaws open. "
            "BOTTOM-RIGHT panel (purple background): dead pose, werewolf lying on its side, fur matted, tongue out. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "enemy_dark_mage",
        (
            f"{PIXEL_ART_STYLE} game sprite sheet of a dark mage enemy, hooded human sorcerer in tattered dark purple robes, "
            "pale gaunt face visible under hood, glowing green eyes, holding a gnarled wooden staff "
            "with a purple crystal orb on top, dark magical energy swirling around hands. "
            "Four poses arranged in a 2x2 grid with clear separation, each pose in its own bright colored square panel: "
            "TOP-LEFT panel (blue background): standing idle pose, staff planted, hands clasped. "
            "TOP-RIGHT panel (green background): walking pose, gliding forward with staff in hand. "
            "BOTTOM-LEFT panel (red background): casting/attacking pose, staff raised high, green magic bolt shooting from orb. "
            "BOTTOM-RIGHT panel (purple background): dead pose, mage collapsed, staff fallen beside, robes deflated. "
            "Consistent character design across all panels, clean pixel art, no overlapping between panels, "
            "bold outlines, game-ready sprite sheet."
        ),
    ),
    (
        "background_dungeon_corridor",
        (
            f"{PIXEL_ART_STYLE} seamless game background scene of a dark dungeon corridor, "
            "stone walls with torches casting warm orange light, arched ceiling, "
            "stone floor with cracks and puddles, atmospheric shadows, "
            "side-view perspective for a 2D side-scrolling roguelike game. "
            "No characters, no UI, no text. Full scene background."
        ),
    ),
    (
        "background_forest",
        (
            f"{PIXEL_ART_STYLE} seamless game background scene of a dark enchanted forest, "
            "tall twisted trees with dense canopy, moss-covered rocks, "
            "purple and green foliage, misty atmosphere, moonlight filtering through branches, "
            "side-view perspective for a 2D side-scrolling roguelike game. "
            "No characters, no UI, no text. Full scene background."
        ),
    ),
    (
        "background_cave",
        (
            f"{PIXEL_ART_STYLE} seamless game background scene of a deep underground cave, "
            "stalactites and stalagmites, glowing blue crystals embedded in walls, "
            "underground pool of water, dark rocky ceiling with drips, "
            "side-view perspective for a 2D side-scrolling roguelike game. "
            "No characters, no UI, no text. Full scene background."
        ),
    ),
    (
        "background_menu",
        (
            f"{PIXEL_ART_STYLE} dark fantasy menu background for a roguelike game, "
            "dramatic composition with a dark stone arena floor, flickering torches on pillars, "
            "fog rolling across the ground, starry night sky visible through broken ceiling, "
            "epic moody atmosphere, dark color palette with orange and purple accents, "
            "leaves empty space in center for menu text and buttons. "
            "No characters, no UI, no text. Full scene background."
        ),
    ),
    (
        "props_healing_herbs_and_potions",
        (
            f"{PIXEL_ART_STYLE} game prop sprite sheet of healing items, "
            "arranged in a 2x2 grid with clear separation, each item in its own colored panel: "
            "TOP-LEFT panel (green background): a cluster of glowing green healing herbs with leaves. "
            "TOP-RIGHT panel (red background): a small glass potion bottle filled with red liquid, corked, with a cross label. "
            "BOTTOM-LEFT panel (blue background): a medium glass potion bottle filled with blue liquid, corked. "
            "BOTTOM-RIGHT panel (yellow background): a large glass potion bottle filled with golden liquid, corked, glowing. "
            "Clean pixel art, game-ready props, no overlapping between panels."
        ),
    ),
    (
        "props_mushrooms_and_fungi",
        (
            f"{PIXEL_ART_STYLE} game prop sprite sheet of dungeon mushrooms and fungi, "
            "arranged in a 2x2 grid with clear separation, each item in its own colored panel: "
            "TOP-LEFT panel (purple background): a cluster of glowing purple mushrooms with spotted caps. "
            "TOP-RIGHT panel (red background): a single large red mushroom with white spots, poisonous looking. "
            "BOTTOM-LEFT panel (blue background): a patch of glowing blue bioluminescent moss. "
            "BOTTOM-RIGHT panel (green background): a cluster of small brown edible mushrooms growing together. "
            "Clean pixel art, game-ready props, no overlapping between panels."
        ),
    ),
    (
        "chests_closed_and_open",
        (
            f"{PIXEL_ART_STYLE} game prop sprite sheet of treasure chests, "
            "arranged side by side in a 1x2 grid with clear separation, each in its own colored panel: "
            "LEFT panel (green background): a closed wooden treasure chest with iron bands, metal lock, "
            "rich brown wood with gold trim, sitting on stone floor. "
            "RIGHT panel (yellow background): an open wooden treasure chest with iron bands, lid thrown open, "
            "golden glow emanating from inside, gold coins and gems spilling out, sitting on stone floor. "
            "Clean pixel art, game-ready props, no overlapping between panels."
        ),
    ),
    (
        "portal_entry",
        (
            f"{PIXEL_ART_STYLE} game prop of a magical entry portal for dungeon level transition, "
            "a stone archway with swirling blue and white magical energy in the center, "
            "runic symbols carved into the stone frame glowing faintly, "
            "particles of light floating around the arch, standing on a stone floor platform, "
            "clean pixel art, game-ready prop, isolated on dark background."
        ),
    ),
    (
        "portal_exit",
        (
            f"{PIXEL_ART_STYLE} game prop of a magical exit portal for dungeon level transition, "
            "a stone archway with swirling green and gold magical energy in the center, "
            "runic symbols carved into the stone frame glowing brightly, "
            "particles of light and sparkles floating around the arch, standing on a stone floor platform, "
            "clean pixel art, game-ready prop, isolated on dark background."
        ),
    ),
    (
        "texture_wall_stone",
        (
            f"{PIXEL_ART_STYLE} seamless tileable wall texture of grey stone blocks, "
            "the texture MUST fill the ENTIRE image from edge to edge with NO background, NO border, NO frame. "
            "This is a repeating texture pattern - there should be absolutely no empty space or background color. "
            "Large rectangular grey stone blocks with mortar lines between them, "
            "subtle cracks and weathering on stones, dark grey and light grey variation, "
            "designed to tile seamlessly in all directions. The stone pattern must continue across all four edges."
        ),
    ),
    (
        "texture_wall_brick",
        (
            f"{PIXEL_ART_STYLE} seamless tileable wall texture of dark red dungeon bricks, "
            "the texture MUST fill the ENTIRE image from edge to edge with NO background, NO border, NO frame. "
            "This is a repeating texture pattern - there should be absolutely no empty space or background color. "
            "Dark red rectangular bricks in a running bond pattern with dark grey mortar, "
            "some bricks chipped or cracked, subtle darkening and moisture stains, "
            "designed to tile seamlessly in all directions. The brick pattern must continue across all four edges."
        ),
    ),
    (
        "texture_wall_cave",
        (
            f"{PIXEL_ART_STYLE} seamless tileable wall texture of natural cave rock, "
            "the texture MUST fill the ENTIRE image from edge to edge with NO background, NO border, NO frame. "
            "This is a repeating texture pattern - there should be absolutely no empty space or background color. "
            "Dark grey and brown rough natural rock surface with cracks, crevices, and small holes, "
            "patches of dark moss in crevices, uneven organic rock shapes, "
            "designed to tile seamlessly in all directions. The rock pattern must continue across all four edges."
        ),
    ),
    (
        "texture_floor_tile",
        (
            f"{PIXEL_ART_STYLE} seamless tileable floor texture of stone dungeon tiles, "
            "the texture MUST fill the ENTIRE image from edge to edge with NO background, NO border, NO frame. "
            "This is a repeating texture pattern - there should be absolutely no empty space or background color. "
            "Square grey stone floor tiles in a grid pattern with narrow gaps between tiles, "
            "some tiles cracked or stained, subtle wear marks, dark grey grout lines, "
            "designed to tile seamlessly in all directions. The tile pattern must continue across all four edges."
        ),
    ),
    (
        "texture_floor_dirt",
        (
            f"{PIXEL_ART_STYLE} seamless tileable floor texture of packed dirt and earth, "
            "the texture MUST fill the ENTIRE image from edge to edge with NO background, NO border, NO frame. "
            "This is a repeating texture pattern - there should be absolutely no empty space or background color. "
            "Brown packed dirt surface with small pebbles, cracks, and subtle footprints, "
            "variation in brown tones from light tan to dark brown, small scattered stones, "
            "designed to tile seamlessly in all directions. The dirt pattern must continue across all four edges."
        ),
    ),
    (
        "texture_ground_grass",
        (
            f"{PIXEL_ART_STYLE} seamless tileable ground texture of grass and dirt for outdoor areas, "
            "the texture MUST fill the ENTIRE image from edge to edge with NO background, NO border, NO frame. "
            "This is a repeating texture pattern - there should be absolutely no empty space or background color. "
            "Green grass patches mixed with brown dirt, individual grass blades visible, "
            "small weeds and clover scattered throughout, earth showing through in patches, "
            "designed to tile seamlessly in all directions. The grass and dirt pattern must continue across all four edges."
        ),
    ),
]


def generate_all() -> None:
    total = len(ASSETS)
    print(f"Starting generation of {total} assets...", file=sys.stderr)
    print(f"Output directory: {OUTPUT_DIR}", file=sys.stderr)
    print("", file=sys.stderr)

    for idx, (filename, prompt) in enumerate(ASSETS, start=1):
        print(f"[{idx}/{total}] Generating: {filename}", file=sys.stderr)

        body = {
            "model": "image-01",
            "prompt": prompt,
            "aspect_ratio": ASPECT_RATIO,
            "response_format": "url",
            "n": 1,
            "prompt_optimizer": False,
        }

        try:
            d = mh.api_request("POST", "/v1/image_generation", body)
            mh.require_base_ok(d)
            urls = (d.get("data") or {}).get("image_urls") or []

            if not urls:
                print(f"  WARNING: No image URLs in response for {filename}", file=sys.stderr)
                continue

            for i, u in enumerate(urls):
                dest = OUTPUT_DIR / f"{filename}.png"
                mh.download_url_to_file(str(u), dest)
                print(f"  Saved: {dest}", file=sys.stderr)

            if idx < total:
                time.sleep(2)

        except Exception as e:
            print(f"  ERROR generating {filename}: {e}", file=sys.stderr)
            continue

    print("", file=sys.stderr)
    print(f"Done! Generated assets saved to: {OUTPUT_DIR}", file=sys.stderr)


if __name__ == "__main__":
    generate_all()
