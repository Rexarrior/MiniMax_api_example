#pragma once

#include "../core/types.h"
#include "../core/config.h"
#include <vector>
#include <array>

namespace rl {

struct Room {
    int x, y, w, h;
    int center_x() const { return x + w / 2; }
    int center_y() const { return y + h / 2; }
    Position center() const { return {center_x(), center_y()}; }
};

class Dungeon {
public:
    Dungeon();

    void generate_bsp(Biome biome = Biome::Dungeon);
    void generate_cellular(Biome biome = Biome::Cave);

    TileType tile_at(int x, int y) const;
    void set_tile(int x, int y, TileType t);

    bool is_walkable(int x, int y) const;
    bool is_in_bounds(int x, int y) const;

    const std::vector<Room>& rooms() const { return rooms_; }
    Biome biome() const { return biome_; }

    void smooth_cellular(int iterations);

private:
    void carve_room(const Room& r);
    void carve_corridor(int x1, int y1, int x2, int y2);
    void connect_rooms();

    std::array<std::array<TileType, MAP_WIDTH>, MAP_HEIGHT> tiles_{};
    std::vector<Room> rooms_;
    Biome biome_ = Biome::Dungeon;
};

}
