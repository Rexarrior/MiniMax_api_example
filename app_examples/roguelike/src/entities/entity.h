#pragma once

#include "../core/types.h"
#include "../assets/sprite_sheet.h"
#include <string>

namespace rl {

enum class ActionState { Idle, Walk, Attack, Dead };

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

    ActionState action_state() const { return action_state_; }
    void set_action_state(ActionState s) { action_state_ = s; }

    void set_attack_timer(float duration) {
        attack_timer_ = duration;
        action_state_ = ActionState::Attack;
    }

    void set_moving(bool moving) {
        is_moving_ = moving;
        if (moving && action_state_ != ActionState::Dead) {
            action_state_ = ActionState::Walk;
        }
    }

    void update_timers(float dt) {
        if (attack_timer_ > 0) {
            attack_timer_ -= dt;
            if (attack_timer_ <= 0) {
                attack_timer_ = 0;
                if (action_state_ == ActionState::Attack) {
                    action_state_ = ActionState::Idle;
                }
            }
        }
    }

    std::string full_sprite_name() const {
        return sprite_name_ + action_to_string(action_state_);
    }

    static const char* action_to_string(ActionState s) {
        switch (s) {
            case ActionState::Idle:   return "_idle";
            case ActionState::Walk:   return "_walk";
            case ActionState::Attack: return "_attack";
            case ActionState::Dead:   return "_dead";
        }
        return "_idle";
    }

protected:
    Position pos_{};
    EntityType type_ = EntityType::Item;
    std::string sprite_name_;
    bool alive_ = true;
    Stats stats_{};
    int anim_row_ = 0;
    int anim_frame_ = 0;
    ActionState action_state_ = ActionState::Idle;
    float attack_timer_ = 0.0f;
    bool is_moving_ = false;
};

}
