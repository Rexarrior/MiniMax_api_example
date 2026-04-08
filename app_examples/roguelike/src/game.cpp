#include "game.h"
#include "assets/asset_manager.h"
#include "core/config.h"
#include <algorithm>
#include <iostream>

namespace rl {

Game::Game() {
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Dungeon of Champions");
    SetTargetFPS(TARGET_FPS);

    std::string asset_path = "../../assets";
    AssetManager::instance().load_all(asset_path);

    std::cerr << "[Game] Checking loaded textures:" << std::endl;
    auto& am = AssetManager::instance();
    std::vector<std::string> check = {"gladiator_idle", "skeleton_warrior_idle", "wall_brick", "floor_tile", "bg_menu"};
    for (auto& n : check) {
        auto t = am.get_texture(n);
        std::cerr << "  " << n << ": " << (t.id ? "OK" : "NULL") << " (" << t.width << "x" << t.height << ")" << std::endl;
    }

    map_renderer_.set_biome(Biome::Dungeon);
}

void Game::init_level(int floor) {
    floor_ = floor;

    Biome biome = (floor % 3 == 0) ? Biome::Cave : (floor % 3 == 1) ? Biome::Dungeon : Biome::Forest;
    dungeon_ = std::make_unique<Dungeon>(DungeonGenerator::generate(biome));
    map_renderer_.set_biome(biome);

    const auto& rooms = dungeon_->rooms();
    std::cerr << "[Game] Floor " << floor << ": generated " << rooms.size() << " rooms, biome=" << static_cast<int>(biome) << std::endl;
    if (rooms.empty()) {
        std::cerr << "[Game] ERROR: No rooms generated!" << std::endl;
        return;
    }

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
        // Spawn props (herbs and mushrooms)
        if (RNG::instance().chance(30)) {
            Position pos{RNG::instance().range(room.x + 1, room.x + room.w - 2),
                         RNG::instance().range(room.y + 1, room.y + room.h - 2)};
            if (dungeon_->is_walkable(pos.x, pos.y)) {
                if (RNG::instance().chance(50)) {
                    items_.push_back(Item::make_prop_healing_herbs(pos));
                } else {
                    items_.push_back(Item::make_prop_mushrooms(pos));
                }
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
    if (!champion_ || !dungeon_) return;

    auto dir = input_.get_movement_input();

    if (dir != Direction::None) {
        turn_manager_.process_player_turn(dir, *champion_, enemies_, *dungeon_, message_log_);

        if (champion_->stats().hp <= 0) {
            champion_->set_action_state(ActionState::Dead);
            state_ = GameState::GameOver;
            return;
        }

        turn_manager_.process_enemy_turn(enemies_, *champion_, *dungeon_, message_log_);

        if (champion_->stats().hp <= 0) {
            champion_->set_action_state(ActionState::Dead);
            state_ = GameState::GameOver;
            return;
        }

        // Update champion action state based on outcome
        if (champion_->action_state() != ActionState::Dead) {
            champion_->set_action_state(ActionState::Idle);
        }

        // Update enemy action states - set dead ones to Dead, others to Idle
        for (auto& enemy : enemies_) {
            if (!enemy.alive()) {
                enemy.set_action_state(ActionState::Dead);
            } else if (enemy.action_state() == ActionState::Dead) {
                enemy.set_action_state(ActionState::Idle);
            }
        }
    }

    // Update animation timers
    champion_->update_timers(GetFrameTime());
    for (auto& enemy : enemies_) {
        enemy.update_timers(GetFrameTime());
    }

    camera_.follow(champion_->pos().x, champion_->pos().y);
    particles_.update(GetFrameTime());
}

void Game::draw_entity_texture(const std::string& name, Position pos, Camera2D cam, Color tint, int frame_row, int frame_col) {
    auto& assets = AssetManager::instance();
    Texture2D tex = assets.get_texture(name);
    if (!tex.id) return;

    float fx = static_cast<float>(pos.x * TILE_SIZE);
    float fy = static_cast<float>(pos.y * TILE_SIZE);

    // Scale entire sprite to TILE_SIZE (16x16)
    Rectangle src = {0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height)};
    Rectangle dst = {fx, fy, static_cast<float>(TILE_SIZE), static_cast<float>(TILE_SIZE)};
    DrawTexturePro(tex, src, dst, {0, 0}, 0, tint);
}

void Game::render() {
    BeginDrawing();
    ClearBackground(BLACK);

    if (state_ == GameState::Menu) {
        auto& assets = AssetManager::instance();
        Texture2D bg = assets.get_texture("bg_menu");
        if (bg.id) {
            Rectangle src = {0, 0, static_cast<float>(bg.width), static_cast<float>(bg.height)};
            Rectangle dst = {0, 0, static_cast<float>(SCREEN_WIDTH), static_cast<float>(SCREEN_HEIGHT)};
            DrawTexturePro(bg, src, dst, {0, 0}, 0, WHITE);
        } else {
            DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK);
        }
        menu_.render_main_menu();
        EndDrawing();
        return;
    }

    // Debug: check if champion texture exists
    if (champion_ && champion_->action_state() != ActionState::Dead) {
        std::string fullName = champion_->full_sprite_name();
        Texture2D tex = AssetManager::instance().get_texture(fullName);
        if (!tex.id) {
            std::cerr << "[RENDER] Missing champion texture: " << fullName << std::endl;
        }
    }

    if (state_ == GameState::GameOver || state_ == GameState::Victory) {
        BeginMode2D(camera_.camera());
        map_renderer_.render(*dungeon_, camera_.camera());
        if (champion_) {
            draw_entity_texture(champion_->full_sprite_name(), champion_->pos(), camera_.camera(), WHITE);
        }
        for (const auto& enemy : enemies_) {
            if (!enemy.alive()) continue;
            if (!fov_.is_visible(enemy.pos().x, enemy.pos().y)) continue;
            draw_entity_texture(enemy.full_sprite_name(), enemy.pos(), camera_.camera(), WHITE);
        }
        EndMode2D();
        menu_.render_game_over(state_ == GameState::Victory, floor_,
                               champion_ ? champion_->level() : 1);
        EndDrawing();
        return;
    }

    if (state_ == GameState::Paused) {
        BeginMode2D(camera_.camera());
        map_renderer_.render(*dungeon_, camera_.camera());
        EndMode2D();
        menu_.render_paused();
        EndDrawing();
        return;
    }

    BeginMode2D(camera_.camera());
    map_renderer_.render(*dungeon_, camera_.camera());

    for (const auto& item : items_) {
        if (item.picked_up) continue;
        if (!fov_.is_visible(item.pos.x, item.pos.y)) continue;
        if (!item.sprite_name.empty()) {
            draw_entity_texture(item.full_sprite_name(), item.pos, camera_.camera(), WHITE);
        } else {
            draw_entity_texture("potions", item.pos, camera_.camera(), WHITE);
        }
    }

    if (fov_.is_visible(entry_portal_.pos.x, entry_portal_.pos.y)) {
        draw_entity_texture("portal_entry", entry_portal_.pos, camera_.camera(), WHITE);
    }
    if (fov_.is_visible(exit_portal_.pos.x, exit_portal_.pos.y)) {
        draw_entity_texture("portal_exit", exit_portal_.pos, camera_.camera(), WHITE);
    }

    for (const auto& enemy : enemies_) {
        if (!enemy.alive()) continue;
        if (!fov_.is_visible(enemy.pos().x, enemy.pos().y)) continue;
        draw_entity_texture(enemy.full_sprite_name(), enemy.pos(), camera_.camera(), WHITE);
    }

    if (champion_) {
        draw_entity_texture(champion_->full_sprite_name(), champion_->pos(), camera_.camera(), WHITE);
    }
    EndMode2D();

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
