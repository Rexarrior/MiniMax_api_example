#pragma once

#include "raylib.h"
#include "../core/types.h"

namespace rl {

class Menu {
public:
    void render_main_menu() const;
    void render_paused() const;
    void render_game_over(bool victory, int floor, int level) const;

private:
    void draw_centered_text(const char* text, int y, int size, Color color) const;
};

}
