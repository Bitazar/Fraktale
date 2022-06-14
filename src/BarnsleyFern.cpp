#include "../include/BarnsleyFern.hpp"

#include <random>
#include <thread>
#include <vector>
#include <functional>

namespace fractal {

    BarnsleyFern::Vector2f BarnsleyFern::firstTransform(
        Vector2f const& position) const noexcept
    {
        auto const& [x, y] = position;
        return {0., 0.16 * y};
    }

    BarnsleyFern::Vector2f BarnsleyFern::secondTransform(
        Vector2f const& position) const noexcept
    {
        auto const& [x, y] = position;
        return {0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6};
    }

    BarnsleyFern::Vector2f BarnsleyFern::thirdTransform(
        Vector2f const& position) const noexcept
    {
        auto const& [x, y] = position;
        return {0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6};
    }

    BarnsleyFern::Vector2f BarnsleyFern::fourthTransform(
        Vector2f const& position) const noexcept
    {
        auto const& [x, y] = position;
        return {-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44};
    }

    BarnsleyFern::Vector2f BarnsleyFern::remap(
        Vector2f const& position,
        uint32_t width,
        uint32_t height) const noexcept
    {
        auto const& [x, y] = position;
        auto rx = (x + 2.182) / 4.8378;
        auto ry = y / 9.9983;
        return {
            rx == 1. ? width - 1. : rx * width,
            ry == 1. ? height - 1. : ry * height
        };
    }

    void BarnsleyFern::generate(
        uint8_t* memory,
        uint32_t width,
        uint32_t height,
        Gradient* gradient) const
    {
        generatePart(memory, width, height, gradient, points);
    }

    void BarnsleyFern::generateParallel(
        uint8_t* memory,
        uint32_t width,
        uint32_t height,
        Gradient* gradient,
        int32_t threads) const
    {
        uint32_t elementPoints = points / threads;
        std::vector<std::thread> jthreads;
        for (uint32_t i = 0; i < threads; ++i)
            jthreads.emplace_back(std::function<void()>([&, ind=i]() -> void
               { this->generatePart(memory, width, height, gradient, elementPoints); }));
        for (auto& thread : jthreads)
            thread.join();
    }

    void BarnsleyFern::generatePart(
        uint8_t* memory,
        uint32_t width,
        uint32_t height,
        Gradient* gradient,
        uint32_t elements) const
    {
        std::uniform_real_distribution<> distributor{};
        std::mt19937 generator{};
        Vector2f pos{0., 0.};
        for (uint32_t iter = 0; iter < elements; ++iter) {
            auto random = distributor(generator);
            if (random < 0.01)
                pos = firstTransform(pos);
            else if (random < 0.86)
                pos = secondTransform(pos);
            else if (random < 0.93)
                pos = thirdTransform(pos);
            else
                pos = fourthTransform(pos);
            auto const& [x, y] = remap(pos, width, height);
            auto const& [rx, ry] = Vector2ui{x, height - 1. - y};
            auto pixel = gradient->operator()(x * y * 255. / (width * height));
            *(memory + width * 3 * ry + 3 * rx) = std::get<0>(pixel);
            *(memory + width * 3 * ry + 3 * rx + 1) = std::get<1>(pixel);
            *(memory + width * 3 * ry + 3 * rx + 2) = std::get<2>(pixel);
        }
    }

}
