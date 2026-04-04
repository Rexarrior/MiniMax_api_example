#pragma once

#include "raylib.h"
#include "../core/config.h"

namespace rl {

class GameCamera {
public:
    GameCamera();

    void follow(int target_x, int target_y);
    Camera2D camera() const { return camera_; }

private:
    Camera2D camera_{};
};

}
