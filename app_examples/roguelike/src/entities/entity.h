#pragma once

#include "../core/types.h"
#include "../assets/sprite_sheet.h"
#include <string>

namespace rl {

class Entity {
public:
    Entity() = default;
    Entity(Position pos, EntityType type, const std::string& sprite_name);

    Position pos() const { return pos_; }
    void set_pos(Position p) { pos_ = p; }
    EntityType type() const { return type_; }
    const std::string& sprite_name() const { return sprite_name_; }

    bool alive() const { return alive_; }
    void kill() { alive_ = false; }

    const Stats& stats() const { return stats_; }
    Stats& stats() { return stats_; }

    int anim_row() const { return anim_row_; }
    int anim_frame() const { return anim_frame_; }
    void set_anim(int row, int frame) { anim_row_ = row; anim_frame_ = frame; }

protected:
    Position pos_{};
    EntityType type_ = EntityType::Item;
    std::string sprite_name_;
    bool alive_ = true;
    Stats stats_{};
    int anim_row_ = 0;
    int anim_frame_ = 0;
};

}
