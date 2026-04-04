#include "camera.h"

namespace rl {

GameCamera::GameCamera() {
    camera_.target = {0, 0};
    camera_.offset = {SCREEN_WIDTH / 2.0f, (SCREEN_HEIGHT - 64) / 2.0f};
    camera_.rotation = 0;
    camera_.zoom = 3.0f;
}

void GameCamera::follow(int target_x, int target_y) {
    float tx = static_cast<float>(target_x * TILE_SIZE + TILE_SIZE / 2);
    float ty = static_cast<float>(target_y * TILE_SIZE + TILE_SIZE / 2);
    camera_.target.x += (tx - camera_.target.x) * 0.15f;
    camera_.target.y += (ty - camera_.target.y) * 0.15f;
}

}
