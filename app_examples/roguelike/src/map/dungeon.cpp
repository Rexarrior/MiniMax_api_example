#include "dungeon.h"
#include "../core/config.h"
#include "../core/random.h"
#include <algorithm>

namespace rl {

Dungeon::Dungeon() {
    for (int y = 0; y < MAP_HEIGHT; ++y)
        for (int x = 0; x < MAP_WIDTH; ++x)
            tiles_[y][x] = TileType::Wall;
}

void Dungeon::generate_bsp(Biome biome) {
    biome_ = biome;
    rooms_.clear();

    for (int y = 0; y < MAP_HEIGHT; ++y)
        for (int x = 0; x < MAP_WIDTH; ++x)
            tiles_[y][x] = TileType::Wall;

    auto& rng = RNG::instance();

    for (int attempt = 0; attempt < 500 && static_cast<int>(rooms_.size()) < MAX_ROOMS; ++attempt) {
        int w = rng.range(MIN_ROOM_SIZE, MAX_ROOM_SIZE);
        int h = rng.range(MIN_ROOM_SIZE, MAX_ROOM_SIZE);
        int x = rng.range(1, MAP_WIDTH - w - 1);
        int y = rng.range(1, MAP_HEIGHT - h - 1);

        Room new_room{x, y, w, h};

        bool overlaps = false;
        for (const auto& existing : rooms_) {
            if (new_room.x - 1 < existing.x + existing.w &&
                new_room.x + new_room.w + 1 > existing.x &&
                new_room.y - 1 < existing.y + existing.h &&
                new_room.y + new_room.h + 1 > existing.y) {
                overlaps = true;
                break;
            }
        }

        if (!overlaps) {
            carve_room(new_room);
            if (!rooms_.empty()) {
                connect_rooms();
            }
            rooms_.push_back(new_room);
        }
    }
}

void Dungeon::generate_cellular(Biome biome) {
    biome_ = biome;
    auto& rng = RNG::instance();

    for (int y = 0; y < MAP_HEIGHT; ++y)
        for (int x = 0; x < MAP_WIDTH; ++x)
            tiles_[y][x] = rng.chance(45) ? TileType::Wall : TileType::Floor;

    smooth_cellular(5);

    rooms_.clear();
    bool visited[MAP_HEIGHT][MAP_WIDTH] = {};

    for (int y = 1; y < MAP_HEIGHT - 1; ++y) {
        for (int x = 1; x < MAP_WIDTH - 1; ++x) {
            if (tiles_[y][x] == TileType::Floor && !visited[y][x]) {
                Room r{x, y, 1, 1};
                std::vector<Position> flood;
                flood.push_back({x, y});
                visited[y][x] = true;

                size_t idx = 0;
                while (idx < flood.size()) {
                    auto p = flood[idx++];
                    const int dirs[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
                    for (auto& d : dirs) {
                        int nx = p.x + d[0], ny = p.y + d[1];
                        if (is_in_bounds(nx, ny) && tiles_[ny][nx] == TileType::Floor && !visited[ny][nx]) {
                            visited[ny][nx] = true;
                            flood.push_back({nx, ny});
                            r.x = std::min(r.x, nx);
                            r.y = std::min(r.y, ny);
                            r.w = std::max(r.w, nx - r.x + 1);
                            r.h = std::max(r.h, ny - r.y + 1);
                        }
                    }
                }

                if (r.w >= 3 && r.h >= 3) {
                    rooms_.push_back(r);
                }
            }
        }
    }

    if (rooms_.size() > 1) {
        for (size_t i = 1; i < rooms_.size(); ++i) {
            carve_corridor(rooms_[i-1].center_x(), rooms_[i-1].center_y(),
                          rooms_[i].center_x(), rooms_[i].center_y());
        }
    }
}

void Dungeon::smooth_cellular(int iterations) {
    for (int iter = 0; iter < iterations; ++iter) {
        auto next = tiles_;
        for (int y = 1; y < MAP_HEIGHT - 1; ++y) {
            for (int x = 1; x < MAP_WIDTH - 1; ++x) {
                int walls = 0;
                for (int dy = -1; dy <= 1; ++dy)
                    for (int dx = -1; dx <= 1; ++dx)
                        if (tiles_[y+dy][x+dx] == TileType::Wall) ++walls;

                next[y][x] = (walls >= 5) ? TileType::Wall : TileType::Floor;
            }
        }
        tiles_ = next;
    }
}

void Dungeon::carve_room(const Room& r) {
    for (int y = r.y; y < r.y + r.h; ++y)
        for (int x = r.x; x < r.x + r.w; ++x)
            if (is_in_bounds(x, y))
                tiles_[y][x] = TileType::Floor;
}

void Dungeon::carve_corridor(int x1, int y1, int x2, int y2) {
    int x = x1, y = y1;
    while (x != x2) {
        if (is_in_bounds(x, y)) tiles_[y][x] = TileType::Floor;
        x += (x2 > x) ? 1 : -1;
    }
    while (y != y2) {
        if (is_in_bounds(x, y)) tiles_[y][x] = TileType::Floor;
        y += (y2 > y) ? 1 : -1;
    }
}

void Dungeon::connect_rooms() {
    if (rooms_.size() < 2) return;
    const auto& a = rooms_[rooms_.size() - 2];
    const auto& b = rooms_.back();
    carve_corridor(a.center_x(), a.center_y(), b.center_x(), b.center_y());
}

TileType Dungeon::tile_at(int x, int y) const {
    if (!is_in_bounds(x, y)) return TileType::Wall;
    return tiles_[y][x];
}

void Dungeon::set_tile(int x, int y, TileType t) {
    if (is_in_bounds(x, y)) tiles_[y][x] = t;
}

bool Dungeon::is_walkable(int x, int y) const {
    if (!is_in_bounds(x, y)) return false;
    return tiles_[y][x] == TileType::Floor;
}

bool Dungeon::is_in_bounds(int x, int y) const {
    return x >= 0 && x < MAP_WIDTH && y >= 0 && y < MAP_HEIGHT;
}

}
