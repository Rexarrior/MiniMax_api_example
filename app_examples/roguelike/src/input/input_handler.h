#pragma once

#include "../core/types.h"

namespace rl {

class InputHandler {
public:
    Direction get_movement_input() const;
    bool is_interact_pressed() const;
    bool is_use_potion_pressed() const;
    bool is_pause_pressed() const;
    bool is_enter_pressed() const;
    bool is_escape_pressed() const;
    bool is_quit_requested() const;
};

}
