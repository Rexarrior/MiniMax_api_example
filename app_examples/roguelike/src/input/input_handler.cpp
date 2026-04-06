#include "input_handler.h"
#include "raylib.h"

namespace rl {

Direction InputHandler::get_movement_input() const {
    if (IsKeyPressed(KEY_W) || IsKeyPressed(KEY_UP))    return Direction::Up;
    if (IsKeyPressed(KEY_S) || IsKeyPressed(KEY_DOWN))  return Direction::Down;
    if (IsKeyPressed(KEY_A) || IsKeyPressed(KEY_LEFT))  return Direction::Left;
    if (IsKeyPressed(KEY_D) || IsKeyPressed(KEY_RIGHT)) return Direction::Right;
    return Direction::None;
}

bool InputHandler::is_interact_pressed() const {
    return IsKeyPressed(KEY_E);
}

bool InputHandler::is_use_potion_pressed() const {
    return IsKeyPressed(KEY_Q) && !IsKeyDown(KEY_LEFT_CONTROL);
}

bool InputHandler::is_pause_pressed() const {
    return IsKeyPressed(KEY_ESCAPE);
}

bool InputHandler::is_enter_pressed() const {
    return IsKeyPressed(KEY_ENTER) || IsKeyPressed(KEY_KP_ENTER);
}

bool InputHandler::is_escape_pressed() const {
    return IsKeyPressed(KEY_ESCAPE);
}

bool InputHandler::is_quit_requested() const {
    return WindowShouldClose();
}

}
