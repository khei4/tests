#ifndef GENERATOR_H
#define GENERATOR_H
#include <filesystem>
#include <optional>

using namespace std;

// FIXME: make
class Generator
{
private:
public:
  Generator(const Generator &) = delete;
  Generator &operator=(const Generator &) = delete;
  Generator() {}
  virtual optional<filesystem::path> generate() = 0;
};

#endif
