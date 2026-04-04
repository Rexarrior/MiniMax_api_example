#include "message_log.h"

namespace rl {

void MessageLog::add(const std::string& msg) {
    messages_.push_back(msg);
    if (messages_.size() > MAX_MESSAGES * 3) {
        messages_.erase(messages_.begin(), messages_.begin() + static_cast<long>(messages_.size()) - MAX_MESSAGES * 3);
    }
}

void MessageLog::render() const {
    int start = static_cast<int>(messages_.size()) - MAX_MESSAGES;
    if (start < 0) start = 0;

    int y = 10;
    for (size_t i = static_cast<size_t>(start); i < messages_.size(); ++i) {
        float alpha = 1.0f - static_cast<float>(messages_.size() - 1 - i) * 0.15f;
        if (alpha < 0.3f) alpha = 0.3f;
        Color c = {255, 255, 255, static_cast<unsigned char>(alpha * 255)};
        DrawText(messages_[i].c_str(), 10, y, 14, c);
        y += 18;
    }
}

}
