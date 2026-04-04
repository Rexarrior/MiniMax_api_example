#pragma once

#include "core/types.h"
#include "core/random.h"
#include "entities/champion.h"
#include "entities/enemy.h"
#include "entities/item.h"
#include "entities/portal.h"
#include "entities/enemy_registry.h"
#include "map/dungeon.h"
#include "map/generator.h"
#include "map/renderer.h"
#include "camera/camera.h"
#include "ui/hud.h"
#include "ui/message_log.h"
#include "ui/menu.h"
#include "systems/turn_manager.h"
#include "systems/fov.h"
#include "systems/particle.h"
#include "input/input_handler.h"
#include <vector>
#include <memory>
#include <string>

namespace rl {

class Game {
public:
    Game();
    void run();

private:
    void init_level(int floor);
    void update();
    void render();
    void draw_entity_texture(const std::string& name, Position pos, Camera2D cam, Color tint);

    GameState state_ = GameState::Menu;
    std::unique_ptr<Dungeon> dungeon_;
    std::unique_ptr<Champion> champion_;
    std::vector<Enemy> enemies_;
    std::vector<Item> items_;
    Portal entry_portal_{};
    Portal exit_portal_{};

    MapRenderer map_renderer_;
    GameCamera camera_;
    HUD hud_;
    MessageLog message_log_;
    Menu menu_;
    TurnManager turn_manager_;
    FOV fov_;
    ParticleSystem particles_;
    InputHandler input_;

    int floor_ = 1;
    float anim_timer_ = 0;
};

}
