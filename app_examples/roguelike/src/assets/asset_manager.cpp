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
            std::cerr << "[AssetManager] Loaded: " << path << std::endl;
        } else {
            std::cerr << "[AssetManager] Missing: " << path << std::endl;
        }
    };

    load_tex("champion", "champion_gladiator.png");
    load_tex("skeleton", "enemy_skeleton_warrior.png");
    load_tex("goblin", "enemy_goblin_thief.png");
    load_tex("orc", "enemy_orc_berserker.png");
    load_tex("rat", "enemy_giant_rat.png");
    load_tex("spider", "enemy_giant_spider.png");
    load_tex("slime", "enemy_slime.png");
    load_tex("demon", "enemy_fire_demon.png");
    load_tex("ghost", "enemy_ghost.png");
    load_tex("werewolf", "enemy_werewolf.png");
    load_tex("dark_mage", "enemy_dark_mage.png");

    load_tex("wall_stone", "texture_wall_stone.png");
    load_tex("wall_brick", "texture_wall_brick.png");
    load_tex("wall_cave", "texture_wall_cave.png");
    load_tex("floor_tile", "texture_floor_tile.png");
    load_tex("floor_dirt", "texture_floor_dirt.png");
    load_tex("ground_grass", "texture_ground_grass.png");

    load_tex("chest", "chests_closed_and_open.png");
    load_tex("potions", "props_healing_herbs_and_potions.png");
    load_tex("portal_entry", "portal_entry.png");
    load_tex("portal_exit", "portal_exit.png");
    load_tex("bg_menu", "background_menu.png");

    font_ = GetFontDefault();
}

Texture2D AssetManager::get_texture(const std::string& name) const {
    auto it = textures_.find(name);
    if (it != textures_.end()) return it->second;
    return Texture2D{};
}

}
