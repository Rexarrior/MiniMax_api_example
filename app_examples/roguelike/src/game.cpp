#include "game.h"
#include "assets/asset_manager.h"
#include "core/config.h"
#include <algorithm>

namespace rl {

Game::Game() {
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Dungeon of Champions");
    SetTargetFPS(TARGET_FPS);

    std::string asset_path = "out/roguelike_assets";
    AssetManager::instance().load_all(asset_path);

    map_renderer_.set_biome(Biome::Dungeon);
}

void Game::init_level(int floor) {
    floor_ = floor;

    Biome biome = (floor % 3 == 0) ? Biome::Cave : (floor % 3 == 1) ? Biome::Dungeon : Biome::Forest;
    dungeon_ = std::make_unique<Dungeon>(DungeonGenerator::generate(biome));
    map_renderer_.set_biome(biome);

    const auto& rooms = dungeon_->rooms();
    if (rooms.empty()) return;

    auto start_room = rooms.front();
    auto end_room = rooms.back();

    champion_ = std::make_unique<Champion>(start_room.center());
    champion_->set_floor(floor);

    entry_portal_ = {start_room.center(), PortalType::Entry, true};
    exit_portal_ = {end_room.center(), PortalType::Exit, true};

    enemies_.clear();
    items_.clear();

    int enemy_count = 5 + floor * 2;
    for (int i = 0; i < enemy_count && i < static_cast<int>(rooms.size()) - 1; ++i) {
        const auto& room = rooms[1 + i % (rooms.size() - 1)];
        Position pos{RNG::instance().range(room.x + 1, room.x + room.w - 2),
                     RNG::instance().range(room.y + 1, room.y + room.h - 2)};
        if (dungeon_->is_walkable(pos.x, pos.y)) {
            auto type = EnemyRegistry::random_for_floor(floor);
            enemies_.emplace_back(pos, type);
        }
    }

    for (size_t i = 1; i < rooms.size(); ++i) {
        const auto& room = rooms[i];
        if (RNG::instance().chance(50)) {
            Position pos{RNG::instance().range(room.x + 1, room.x + room.w - 2),
                         RNG::instance().range(room.y + 1, room.y + room.h - 2)};
            if (dungeon_->is_walkable(pos.x, pos.y)) {
                items_.push_back(Item::make_potion(pos));
            }
        }
    }

    camera_.follow(champion_->pos().x, champion_->pos().y);
    fov_.compute(*dungeon_, champion_->pos().x, champion_->pos().y, FOV_RADIUS);

    message_log_.add("You descend to floor " + std::to_string(floor) + "...");
}

void Game::update() {
    if (state_ == GameState::Menu) {
        if (input_.is_enter_pressed()) {
            state_ = GameState::Playing;
            floor_ = 1;
            champion_ = nullptr;
            init_level(1);
        }
        if (input_.is_escape_pressed()) {
            CloseWindow();
        }
        return;
    }

    if (state_ == GameState::Paused) {
        if (input_.is_pause_pressed()) {
            state_ = GameState::Playing;
        }
        return;
    }

    if (state_ == GameState::GameOver || state_ == GameState::Victory) {
        if (input_.is_enter_pressed()) {
            state_ = GameState::Menu;
        }
        return;
    }

    if (state_ != GameState::Playing) return;

    auto dir = input_.get_movement_input();

    if (dir != Direction::None) {
        turn_manager_.process_player_turn(dir, *champion_, enemies_, *dungeon_, message_log_);

        if (champion_->stats().hp <= 0) {
            state_ = GameState::GameOver;
            return;
        }

        turn_manager_.process_enemy_turn(enemies_, *champion_, *dungeon_, message_log_);

        if (champion_->stats().hp <= 0) {
            state_ = GameState::GameOver;
            return;
        }

        auto pos = champion_->pos();
        fov_.compute(*dungeon_, pos.x, pos.y, FOV_RADIUS);

        if (pos == exit_portal_.pos) {
            if (floor_ >= 5) {
                state_ = GameState::Victory;
            } else {
                init_level(floor_ + 1);
            }
        }

        for (auto& item : items_) {
            if (!item.picked_up && item.pos == pos) {
                item.picked_up = true;
                if (item.type == ItemType::HealthPotion) {
                    champion_->add_potion();
                    message_log_.add("Picked up a Health Potion!");
                }
            }
        }

        enemies_.erase(
            std::remove_if(enemies_.begin(), enemies_.end(),
                           [](const Enemy& e) { return !e.alive(); }),
            enemies_.end());
    }

    if (input_.is_use_potion_pressed() && champion_->has_potions()) {
        champion_->use_potion();
        message_log_.add("Used a health potion. HP: " + std::to_string(champion_->stats().hp));
    }

    if (input_.is_pause_pressed()) {
        state_ = GameState::Paused;
    }

    camera_.follow(champion_->pos().x, champion_->pos().y);
    particles_.update(GetFrameTime());
}

void Game::render() {
    BeginDrawing();
    ClearBackground(BLACK);

    if (state_ == GameState::Menu) {
        menu_.render_main_menu();
        EndDrawing();
        return;
    }

    if (state_ == GameState::GameOver || state_ == GameState::Victory) {
        menu_.render_game_over(state_ == GameState::Victory, floor_,
                               champion_ ? champion_->level() : 1);
        EndDrawing();
        return;
    }

    if (state_ == GameState::Paused) {
        map_renderer_.render(*dungeon_, camera_.camera());
        menu_.render_paused();
        EndDrawing();
        return;
    }

    map_renderer_.render(*dungeon_, camera_.camera());

    auto cam = camera_.camera();

    for (const auto& item : items_) {
        if (item.picked_up) continue;
        if (!fov_.is_visible(item.pos.x, item.pos.y)) continue;
        Vector2 wp = {static_cast<float>(item.pos.x * TILE_SIZE),
                      static_cast<float>(item.pos.y * TILE_SIZE)};
        Vector2 sp = GetWorldToScreen2D(wp, cam);
        DrawRectangle(static_cast<int>(sp.x), static_cast<int>(sp.y),
                     TILE_SIZE, TILE_SIZE, GREEN);
    }

    Vector2 ep = {static_cast<float>(entry_portal_.pos.x * TILE_SIZE),
                  static_cast<float>(entry_portal_.pos.y * TILE_SIZE)};
    Vector2 esp = GetWorldToScreen2D(ep, cam);
    DrawRectangle(static_cast<int>(esp.x), static_cast<int>(esp.y),
                 TILE_SIZE, TILE_SIZE, SKYBLUE);

    Vector2 xp = {static_cast<float>(exit_portal_.pos.x * TILE_SIZE),
                  static_cast<float>(exit_portal_.pos.y * TILE_SIZE)};
    Vector2 xsp = GetWorldToScreen2D(xp, cam);
    DrawRectangle(static_cast<int>(xsp.x), static_cast<int>(xsp.y),
                 TILE_SIZE, TILE_SIZE, GOLD);

    for (const auto& enemy : enemies_) {
        if (!enemy.alive()) continue;
        if (!fov_.is_visible(enemy.pos().x, enemy.pos().y)) continue;
        Vector2 wp = {static_cast<float>(enemy.pos().x * TILE_SIZE),
                      static_cast<float>(enemy.pos().y * TILE_SIZE)};
        Vector2 sp = GetWorldToScreen2D(wp, cam);
        DrawRectangle(static_cast<int>(sp.x), static_cast<int>(sp.y),
                     TILE_SIZE, TILE_SIZE, RED);
    }

    if (champion_) {
        Vector2 cp = {static_cast<float>(champion_->pos().x * TILE_SIZE),
                      static_cast<float>(champion_->pos().y * TILE_SIZE)};
        Vector2 csp = GetWorldToScreen2D(cp, cam);
        DrawRectangle(static_cast<int>(csp.x), static_cast<int>(csp.y),
                     TILE_SIZE, TILE_SIZE, BLUE);
    }

    particles_.render();
    hud_.render(*champion_, floor_, static_cast<int>(enemies_.size()));
    message_log_.render();

    EndDrawing();
}

void Game::run() {
    while (!WindowShouldClose()) {
        update();
        render();
    }
    CloseWindow();
}

}
