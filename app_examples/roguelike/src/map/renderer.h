#pragma once

#include "raylib.h"
#include "../map/dungeon.h"
#include "../entities/champion.h"
#include "../entities/enemy.h"
#include "../entities/item.h"
#include "../entities/portal.h"
#include <vector>
#include <memory>

namespace rl {

class MapRenderer {
public:
    void render(const Dungeon& dungeon, Camera2D camera);
    void set_biome(Biome biome);

private:
    void draw_tile(int x, int y, TileType type, Camera2D camera);
    Biome biome_ = Biome::Dungeon;
};

}
