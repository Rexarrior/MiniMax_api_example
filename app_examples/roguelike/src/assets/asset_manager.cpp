#include "asset_manager.h"
#include <iostream>
#include <filesystem>

namespace rl {

AssetManager& AssetManager::instance() {
    static AssetManager inst;
    return inst;
}

void AssetManager::load_all(const std::string& base_path) {
    base_path_ = base_path;
    namespace fs = std::filesystem;

    auto load_tex = [this](const std::string& name, const std::string& file) {
        std::string path = base_path_ + "/" + file;
        if (fs::exists(path)) {
            textures_[name] = LoadTexture(path.c_str());
        } else {
            std::cerr << "[AssetManager] Missing: " << path << std::endl;
        }
    };

    // Champion sprites (gladiator)
    load_tex("gladiator_idle",   "sprites/champion_gladiator_idle.png");
    load_tex("gladiator_walk",   "sprites/champion_gladiator_walk.png");
    load_tex("gladiator_attack", "sprites/champion_gladiator_attack.png");
    load_tex("gladiator_dead",   "sprites/champion_gladiator_dead.png");

    // Enemy sprites - 11 types x 4 states
    // skeleton_warrior
    load_tex("skeleton_warrior_idle",   "enemies/enemy_skeleton_warrior_idle.png");
    load_tex("skeleton_warrior_walk",   "enemies/enemy_skeleton_warrior_walk.png");
    load_tex("skeleton_warrior_attack", "enemies/enemy_skeleton_warrior_attack.png");
    load_tex("skeleton_warrior_dead",   "enemies/enemy_skeleton_warrior_dead.png");
    // goblin_thief
    load_tex("goblin_thief_idle",   "enemies/enemy_goblin_thief_idle.png");
    load_tex("goblin_thief_walk",   "enemies/enemy_goblin_thief_walk.png");
    load_tex("goblin_thief_attack", "enemies/enemy_goblin_thief_attack.png");
    load_tex("goblin_thief_dead",   "enemies/enemy_goblin_thief_dead.png");
    // orc_berserker
    load_tex("orc_berserker_idle",   "enemies/enemy_orc_berserker_idle.png");
    load_tex("orc_berserker_walk",   "enemies/enemy_orc_berserker_walk.png");
    load_tex("orc_berserker_attack", "enemies/enemy_orc_berserker_attack.png");
    load_tex("orc_berserker_dead",   "enemies/enemy_orc_berserker_dead.png");
    // giant_rat
    load_tex("giant_rat_idle",   "enemies/enemy_giant_rat_idle.png");
    load_tex("giant_rat_walk",   "enemies/enemy_giant_rat_walk.png");
    load_tex("giant_rat_attack", "enemies/enemy_giant_rat_attack.png");
    load_tex("giant_rat_dead",   "enemies/enemy_giant_rat_dead.png");
    // giant_spider
    load_tex("giant_spider_idle",   "enemies/enemy_giant_spider_idle.png");
    load_tex("giant_spider_walk",   "enemies/enemy_giant_spider_walk.png");
    load_tex("giant_spider_attack", "enemies/enemy_giant_spider_attack.png");
    load_tex("giant_spider_dead",   "enemies/enemy_giant_spider_dead.png");
    // slime
    load_tex("slime_idle",   "enemies/enemy_slime_idle.png");
    load_tex("slime_walk",   "enemies/enemy_slime_walk.png");
    load_tex("slime_attack", "enemies/enemy_slime_attack.png");
    load_tex("slime_dead",   "enemies/enemy_slime_dead.png");
    // fire_demon
    load_tex("fire_demon_idle",   "enemies/enemy_fire_demon_idle.png");
    load_tex("fire_demon_walk",   "enemies/enemy_fire_demon_walk.png");
    load_tex("fire_demon_attack", "enemies/enemy_fire_demon_attack.png");
    load_tex("fire_demon_dead",   "enemies/enemy_fire_demon_dead.png");
    // ghost
    load_tex("ghost_idle",   "enemies/enemy_ghost_idle.png");
    load_tex("ghost_walk",   "enemies/enemy_ghost_walk.png");
    load_tex("ghost_attack", "enemies/enemy_ghost_attack.png");
    load_tex("ghost_dead",   "enemies/enemy_ghost_dead.png");
    // werewolf
    load_tex("werewolf_idle",   "enemies/enemy_werewolf_idle.png");
    load_tex("werewolf_walk",   "enemies/enemy_werewolf_walk.png");
    load_tex("werewolf_attack", "enemies/enemy_werewolf_attack.png");
    load_tex("werewolf_dead",   "enemies/enemy_werewolf_dead.png");
    // dark_mage
    load_tex("dark_mage_idle",   "enemies/enemy_dark_mage_idle.png");
    load_tex("dark_mage_walk",   "enemies/enemy_dark_mage_walk.png");
    load_tex("dark_mage_attack", "enemies/enemy_dark_mage_attack.png");
    load_tex("dark_mage_dead",   "enemies/enemy_dark_mage_dead.png");

    // Props
    load_tex("healing_herbs_and_potions_idle",   "props/props_healing_herbs_and_potions_idle.png");
    load_tex("healing_herbs_and_potions_walk",   "props/props_healing_herbs_and_potions_walk.png");
    load_tex("healing_herbs_and_potions_attack", "props/props_healing_herbs_and_potions_attack.png");
    load_tex("healing_herbs_and_potions_dead",   "props/props_healing_herbs_and_potions_dead.png");
    load_tex("mushrooms_and_fungi_idle",   "props/props_mushrooms_and_fungi_idle.png");
    load_tex("mushrooms_and_fungi_walk",   "props/props_mushrooms_and_fungi_walk.png");
    load_tex("mushrooms_and_fungi_attack", "props/props_mushrooms_and_fungi_attack.png");
    load_tex("mushrooms_and_fungi_dead",   "props/props_mushrooms_and_fungi_dead.png");

    // Legacy sprites (keep for backward compatibility with existing code)
    load_tex("chest",        "props/chest.png");
    load_tex("potions",      "props/potions.png");
    load_tex("portal_entry", "props/portal_entry.png");
    load_tex("portal_exit",  "props/portal_exit.png");

    // Tile textures
    load_tex("wall_stone",   "tiles/wall_stone.png");
    load_tex("wall_brick",   "tiles/wall_brick.png");
    load_tex("wall_cave",    "tiles/wall_cave.png");
    load_tex("floor_tile",   "tiles/floor_tile.png");
    load_tex("floor_dirt",   "tiles/floor_dirt.png");
    load_tex("ground_grass", "tiles/ground_grass.png");

    // Backgrounds
    load_tex("bg_menu",      "backgrounds/menu.png");

    font_ = GetFontDefault();
}

Texture2D AssetManager::get_texture(const std::string& name) const {
    auto it = textures_.find(name);
    if (it != textures_.end()) return it->second;
    return Texture2D{};
}

}
