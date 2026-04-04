#include "fov.h"
#include "../core/config.h"
#include <cmath>

namespace rl {

FOV::FOV() {
    visible_.resize(MAP_HEIGHT, std::vector<bool>(MAP_WIDTH, false));
    explored_.resize(MAP_HEIGHT, std::vector<bool>(MAP_WIDTH, false));
}

void FOV::compute(const Dungeon& dungeon, int origin_x, int origin_y, int radius) {
    ox_ = origin_x;
    oy_ = origin_y;
    radius_ = radius;

    for (int y = 0; y < MAP_HEIGHT; ++y)
        for (int x = 0; x < MAP_WIDTH; ++x)
            visible_[y][x] = false;

    visible_[origin_y][origin_x] = true;
    explored_[origin_y][origin_x] = true;

    cast_light(dungeon, origin_x, origin_y, 1, 1.0f, 0.0f, radius, 1, 0, 0, -1);
    cast_light(dungeon, origin_x, origin_y, 1, 1.0f, 0.0f, radius, -1, 0, 0, 1);
    cast_light(dungeon, origin_x, origin_y, 1, 1.0f, 0.0f, radius, 0, 1, -1, 0);
    cast_light(dungeon, origin_x, origin_y, 1, 1.0f, 0.0f, radius, 0, -1, 1, 0);
    cast_light(dungeon, origin_x, origin_y, 1, 1.0f, 0.0f, radius, 1, 0, 0, 1);
    cast_light(dungeon, origin_x, origin_y, 1, 1.0f, 0.0f, radius, -1, 0, 0, -1);
    cast_light(dungeon, origin_x, origin_y, 1, 1.0f, 0.0f, radius, 0, 1, 1, 0);
    cast_light(dungeon, origin_x, origin_y, 1, 1.0f, 0.0f, radius, 0, -1, -1, 0);
}

void FOV::cast_light(const Dungeon& dungeon, int cx, int cy, int row,
                      float start_slope, float end_slope, int radius,
                      int xx, int xy, int yx, int yy) {
    if (start_slope < end_slope) return;

    float new_start = start_slope;
    bool blocked = false;

    for (int distance = row; distance <= radius && !blocked; ++distance) {
        int dy = -distance;
        for (int dx = -distance; dx <= 0; ++dx) {
            int current_x = cx + dx * xx + dy * xy;
            int current_y = cy + dx * yx + dy * yy;
            float left_slope = (dx - 0.5f) / (dy + 0.5f);
            float right_slope = (dx + 0.5f) / (dy - 0.5f);

            if (!(current_x >= 0 && current_x < MAP_WIDTH && current_y >= 0 && current_y < MAP_HEIGHT)) continue;
            if (start_slope < right_slope) continue;
            if (end_slope > left_slope) break;

            if (dx * dx + dy * dy < radius * radius) {
                if (!dungeon.is_walkable(current_x, current_y)) {
                    blocked = true;
                    new_start = right_slope;
                } else {
                    visible_[current_y][current_x] = true;
                    explored_[current_y][current_x] = true;
                }
            }

            if (blocked) {
                if (!dungeon.is_walkable(current_x, current_y)) {
                    cast_light(dungeon, cx, cy, distance + 1, new_start, left_slope,
                              radius, xx, xy, yx, yy);
                    new_start = right_slope;
                }
            }
        }
    }
}

bool FOV::is_visible(int x, int y) const {
    if (x < 0 || x >= MAP_WIDTH || y < 0 || y >= MAP_HEIGHT) return false;
    return visible_[y][x];
}

bool FOV::is_explored(int x, int y) const {
    if (x < 0 || x >= MAP_WIDTH || y < 0 || y >= MAP_HEIGHT) return false;
    return explored_[y][x];
}

}
