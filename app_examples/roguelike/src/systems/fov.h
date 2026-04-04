#pragma once

#include "../map/dungeon.h"
#include <vector>

namespace rl {

class FOV {
public:
    void compute(const Dungeon& dungeon, int origin_x, int origin_y, int radius);
    bool is_visible(int x, int y) const;
    bool is_explored(int x, int y) const;

private:
    void cast_light(const Dungeon& dungeon, int cx, int cy, int row,
                    float start_slope, float end_slope, int radius,
                    int xx, int xy, int yx, int yy);

    std::vector<std::vector<bool>> visible_;
    std::vector<std::vector<bool>> explored_;
    int radius_ = 0;
    int ox_ = 0, oy_ = 0;
};

}
