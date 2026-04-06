#include "menu.h"
#include "../core/config.h"
#include <cstring>

namespace rl {

void Menu::draw_centered_text(const char* text, int y, int size, Color color) const {
    int w = MeasureText(text, size);
    DrawText(text, (SCREEN_WIDTH - w) / 2, y, size, color);
}

void Menu::render_main_menu() const {
    DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK);

    draw_centered_text("DUNGEON OF CHAMPIONS", 150, 40, GOLD);
    draw_centered_text("A Roguelike Adventure", 210, 20, GRAY);

    draw_centered_text("Press ENTER to Start", 350, 24, WHITE);
    draw_centered_text("WASD / Arrows - Move & Attack", 420, 16, GRAY);
    draw_centered_text("Space - Wait", 450, 16, GRAY);
    draw_centered_text("E - Interact", 480, 16, GRAY);
    draw_centered_text("ESC - Quit", 510, 16, GRAY);
}

void Menu::render_paused() const {
    DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color{0, 0, 0, 180});
    draw_centered_text("PAUSED", 250, 40, WHITE);
    draw_centered_text("Press ESC to Resume", 310, 20, GRAY);
    draw_centered_text("Press Q to Quit", 350, 20, GRAY);
}

void Menu::render_game_over(bool victory, int floor, int level) const {
    DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK);

    if (victory) {
        draw_centered_text("VICTORY!", 200, 48, GOLD);
        draw_centered_text("You conquered the dungeon!", 270, 24, WHITE);
    } else {
        draw_centered_text("YOU DIED", 200, 48, RED);
        draw_centered_text("The dungeon claims another soul...", 270, 24, GRAY);
    }

    char info[128];
    std::snprintf(info, sizeof(info), "Floor Reached: %d  |  Level: %d", floor, level);
    draw_centered_text(info, 340, 20, WHITE);

    draw_centered_text("Press ENTER to Play Again", 420, 24, WHITE);
    draw_centered_text("Press ESC to Quit", 460, 20, GRAY);
}

}
