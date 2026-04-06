#pragma once

#include <string>
#include <vector>
#include "raylib.h"

namespace rl {

class MessageLog {
public:
    void add(const std::string& msg);
    void render() const;
    std::vector<std::string>& messages() { return messages_; }
    const std::vector<std::string>& messages() const { return messages_; }

private:
    std::vector<std::string> messages_;
    static constexpr int MAX_MESSAGES = 5;
};

}
