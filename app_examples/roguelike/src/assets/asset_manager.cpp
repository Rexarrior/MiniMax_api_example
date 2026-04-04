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

    load_tex("champion", "sprites/champion.png");
    load_tex("skeleton", "enemies/skeleton.png");
    load_tex("goblin", "enemies/goblin.png");
    load_tex("orc", "enemies/orc.png");
    load_tex("rat", "enemies/rat.png");
    load_tex("spider", "enemies/spider.png");
    load_tex("slime", "enemies/slime.png");
    load_tex("demon", "enemies/demon.png");
    load_tex("ghost", "enemies/ghost.png");
    load_tex("werewolf", "enemies/werewolf.png");
    load_tex("dark_mage", "enemies/dark_mage.png");

    load_tex("wall_stone", "tiles/wall_stone.png");
    load_tex("wall_brick", "tiles/wall_brick.png");
    load_tex("wall_cave", "tiles/wall_cave.png");
    load_tex("floor_tile", "tiles/floor_tile.png");
    load_tex("floor_dirt", "tiles/floor_dirt.png");
    load_tex("ground_grass", "tiles/ground_grass.png");

    load_tex("chest", "props/chest.png");
    load_tex("potions", "props/potions.png");
    load_tex("portal_entry", "props/portal_entry.png");
    load_tex("portal_exit", "props/portal_exit.png");
    load_tex("bg_menu", "backgrounds/menu.png");

    font_ = GetFontDefault();
}

Texture2D AssetManager::get_texture(const std::string& name) const {
    auto it = textures_.find(name);
    if (it != textures_.end()) return it->second;
    return Texture2D{};
}

}
