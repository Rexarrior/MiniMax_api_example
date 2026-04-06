#include "sprite_sheet.h"

namespace rl {

SpriteSheet::SpriteSheet(Texture2D tex, int frame_width, int frame_height, int frames_per_row) {
    set_texture(tex, frame_width, frame_height, frames_per_row);
}

void SpriteSheet::set_texture(Texture2D tex, int frame_width, int frame_height, int frames_per_row) {
    texture_ = tex;
    frame_width_ = frame_width;
    frame_height_ = frame_height;
    frames_per_row_ = frames_per_row;
}

const SpriteFrame& SpriteSheet::get_frame(int row, int col) const {
    static SpriteFrame fallback{};
    if (!texture_.id || col < 0 || col >= frames_per_row_) return fallback;
    static SpriteFrame frame;
    frame.src_rect = {
        static_cast<float>(col * frame_width_),
        static_cast<float>(row * frame_height_),
        static_cast<float>(frame_width_),
        static_cast<float>(frame_height_),
    };
    return frame;
}

}
