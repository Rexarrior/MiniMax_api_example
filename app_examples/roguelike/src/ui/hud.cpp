#include "hud.h"
#include "../core/config.h"
#include <string>

namespace rl {

void HUD::draw_bar(int x, int y, int w, int h, float current, float max, Color color) {
    DrawRectangle(x, y, w, h, DARKGRAY);
    int fill_w = static_cast<int>(w * (current / max));
    DrawRectangle(x, y, fill_w, h, color);
    DrawRectangleLines(x, y, w, h, BLACK);
}

void HUD::render(const Champion& champion, int floor, int enemies_remaining) {
    int bar_y = SCREEN_HEIGHT - 32;

    DrawRectangle(0, bar_y, SCREEN_WIDTH, 32, Color{30, 30, 30, 220});

    const auto& stats = champion.stats();

    DrawText("HP:", 10, bar_y + 8, 14, WHITE);
    draw_bar(40, bar_y + 6, 150, 18, static_cast<float>(stats.hp), static_cast<float>(stats.max_hp), RED);
    std::string hp_text = std::to_string(stats.hp) + "/" + std::to_string(stats.max_hp);
    DrawText(hp_text.c_str(), 70, bar_y + 8, 12, WHITE);

    DrawText("ATK:", 210, bar_y + 8, 14, WHITE);
    DrawText(std::to_string(stats.attack).c_str(), 245, bar_y + 8, 12, WHITE);

    DrawText("DEF:", 280, bar_y + 8, 14, WHITE);
    DrawText(std::to_string(stats.defense).c_str(), 315, bar_y + 8, 12, WHITE);

    DrawText("LVL:", 360, bar_y + 8, 14, WHITE);
    DrawText(std::to_string(champion.level()).c_str(), 395, bar_y + 8, 12, YELLOW);

    DrawText("Floor:", 440, bar_y + 8, 14, WHITE);
    DrawText(std::to_string(floor).c_str(), 490, bar_y + 8, 12, WHITE);

    DrawText("Potions:", 540, bar_y + 8, 14, WHITE);
    DrawText(std::to_string(champion.potions()).c_str(), 610, bar_y + 8, 12, GREEN);

    DrawText("Enemies:", 660, bar_y + 8, 14, WHITE);
    DrawText(std::to_string(enemies_remaining).c_str(), 730, bar_y + 8, 12, ORANGE);
}

}
