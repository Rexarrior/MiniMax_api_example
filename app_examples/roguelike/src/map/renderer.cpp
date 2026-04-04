#include "renderer.h"
#include "../assets/asset_manager.h"
#include "../core/config.h"

namespace rl {

void MapRenderer::set_biome(Biome biome) {
    biome_ = biome;
}

void MapRenderer::render(const Dungeon& dungeon, Camera2D camera) {
    int start_x = static_cast<int>(camera.target.x / TILE_SIZE) - VIEWPORT_TILES_X / 2 - 1;
    int start_y = static_cast<int>(camera.target.y / TILE_SIZE) - VIEWPORT_TILES_Y / 2 - 1;
    int end_x = start_x + VIEWPORT_TILES_X + 3;
    int end_y = start_y + VIEWPORT_TILES_Y + 3;

    start_x = std::max(0, start_x);
    start_y = std::max(0, start_y);
    end_x = std::min(MAP_WIDTH, end_x);
    end_y = std::min(MAP_HEIGHT, end_y);

    for (int y = start_y; y < end_y; ++y) {
        for (int x = start_x; x < end_x; ++x) {
            draw_tile(x, y, dungeon.tile_at(x, y), camera);
        }
    }
}

void MapRenderer::draw_tile(int x, int y, TileType type, Camera2D camera) {
    Vector2 world_pos = {static_cast<float>(x * TILE_SIZE), static_cast<float>(y * TILE_SIZE)};
    Vector2 screen_pos = GetWorldToScreen2D(world_pos, camera);

    auto& assets = AssetManager::instance();
    std::string tex_name;

    switch (type) {
        case TileType::Wall:
            if (biome_ == Biome::Cave) tex_name = "wall_cave";
            else if (biome_ == Biome::Forest) tex_name = "wall_stone";
            else tex_name = "wall_brick";
            break;
        case TileType::Floor:
            if (biome_ == Biome::Forest) tex_name = "ground_grass";
            else if (biome_ == Biome::Cave) tex_name = "floor_dirt";
            else tex_name = "floor_tile";
            break;
        case TileType::Door:
            tex_name = "floor_dirt";
            break;
        case TileType::Wall_Torch:
            tex_name = "wall_brick";
            break;
        case TileType::Floor_Water:
            tex_name = "floor_dirt";
            break;
    }

    Texture2D tex = assets.get_texture(tex_name);
    if (tex.id) {
        Rectangle src = {0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height)};
        Rectangle dst = {screen_pos.x, screen_pos.y,
                        static_cast<float>(TILE_SIZE), static_cast<float>(TILE_SIZE)};
        DrawTexturePro(tex, src, dst, {0, 0}, 0, WHITE);
    } else {
        Color c = (type == TileType::Wall) ? DARKGRAY : GRAY;
        DrawRectangle(static_cast<int>(screen_pos.x), static_cast<int>(screen_pos.y),
                     TILE_SIZE, TILE_SIZE, c);
    }
}

}
