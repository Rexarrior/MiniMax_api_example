#pragma once

#include "raylib.h"
#include "../entities/champion.h"

namespace rl {

class HUD {
public:
    void render(const Champion& champion, int floor, int enemies_remaining);

private:
    void draw_bar(int x, int y, int w, int h, float current, float max, Color color);
};

}
