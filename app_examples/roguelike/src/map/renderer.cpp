#include "renderer.h"
#include "../assets/asset_manager.h"
#include "../core/config.h"
#include <algorithm>

namespace rl {

void MapRenderer::set_biome(Biome biome) {
    biome_ = biome;
}

void MapRenderer::render(const Dungeon& dungeon, Camera2D camera) {
    int start_x = static_cast<int>(camera.target.x / TILE_SIZE) - VIEWPORT_TILES_X / 2 - 2;
    int start_y = static_cast<int>(camera.target.y / TILE_SIZE) - VIEWPORT_TILES_Y / 2 - 2;
    int end_x = start_x + VIEWPORT_TILES_X + 5;
    int end_y = start_y + VIEWPORT_TILES_Y + 5;

    start_x = std::max(0, start_x);
    start_y = std::max(0, start_y);
    end_x = std::min(MAP_WIDTH, end_x);
    end_y = std::min(MAP_HEIGHT, end_y);

    auto& assets = AssetManager::instance();

    for (int y = start_y; y < end_y; ++y) {
        for (int x = start_x; x < end_x; ++x) {
            TileType type = dungeon.tile_at(x, y);
            int sx = static_cast<int>(x * TILE_SIZE);
            int sy = static_cast<int>(y * TILE_SIZE);

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
                Vector2 wp = {static_cast<float>(sx), static_cast<float>(sy)};
                Vector2 sp = GetWorldToScreen2D(wp, camera);
                int ix = static_cast<int>(sp.x);
                int iy = static_cast<int>(sp.y);
                int ts = TILE_SIZE + 1;
                Rectangle dst = {static_cast<float>(ix), static_cast<float>(iy),
                                static_cast<float>(ts), static_cast<float>(ts)};
                DrawTexturePro(tex, src, dst, {0, 0}, 0, WHITE);
            } else {
                Color c = (type == TileType::Wall) ? DARKGRAY : GRAY;
                DrawRectangle(sx, sy, TILE_SIZE, TILE_SIZE, c);
            }

            Color grid_color = {50, 50, 50, 80};
            DrawRectangleLines(sx, sy, TILE_SIZE, TILE_SIZE, grid_color);
        }
    }
}

}
