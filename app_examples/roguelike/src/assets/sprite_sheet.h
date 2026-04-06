#pragma once

#include "raylib.h"

namespace rl {

struct SpriteFrame {
    Rectangle src_rect{};
    float duration = 0.15f;
};

class SpriteSheet {
public:
    SpriteSheet() = default;
    SpriteSheet(Texture2D tex, int frame_width, int frame_height, int frames_per_row);

    void set_texture(Texture2D tex, int frame_width, int frame_height, int frames_per_row);

    const SpriteFrame& get_frame(int row, int col) const;
    int frame_count(int row) const { return frames_per_row_; }
    Texture2D texture() const { return texture_; }

private:
    Texture2D texture_{};
    int frame_width_ = 0;
    int frame_height_ = 0;
    int frames_per_row_ = 0;
};

}
