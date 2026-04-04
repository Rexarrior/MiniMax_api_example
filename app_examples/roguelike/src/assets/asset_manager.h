#pragma once

#include <string>
#include <unordered_map>
#include "raylib.h"

namespace rl {

class AssetManager {
public:
    static AssetManager& instance();

    void load_all(const std::string& base_path);

    Texture2D get_texture(const std::string& name) const;
    Font get_font() const { return font_; }

private:
    std::unordered_map<std::string, Texture2D> textures_;
    Font font_{};
    std::string base_path_;
};

}
