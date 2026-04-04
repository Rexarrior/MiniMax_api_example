#pragma once

#include <string>
#include <vector>
#include "raylib.h"

namespace rl {

class MessageLog {
public:
    void add(const std::string& msg);
    void render() const;

private:
    std::vector<std::string> messages_;
    static constexpr int MAX_MESSAGES = 5;
};

}
