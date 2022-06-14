#pragma once

#include "Gradient.hpp"

namespace fractal {

    class BarnsleyFern {
    public:
        explicit BarnsleyFern(uint32_t points)
            : points{points} {}

        void generate(
            uint8_t* memory,
            uint32_t width,
            uint32_t height,
            Gradient* gradient) const;

        void generateParallel(
            uint8_t* memory,
            uint32_t width,
            uint32_t height,
            Gradient* gradient,
            int32_t threads) const;

        void setPoints(uint32_t points) noexcept
            { this->points = points; }

    private:
        uint32_t                                    points;

        typedef std::pair<double, double>       Vector2f;
        typedef std::pair<uint32_t, uint32_t>   Vector2ui;

        Vector2f firstTransform(Vector2f const& position) const noexcept;
        Vector2f secondTransform(Vector2f const& position) const noexcept;
        Vector2f thirdTransform(Vector2f const& position) const noexcept;
        Vector2f fourthTransform(Vector2f const& position) const noexcept;

        Vector2f remap(Vector2f const& position, uint32_t width, uint32_t height) const noexcept;

        void generatePart(
            uint8_t* memory,
            uint32_t width,
            uint32_t height,
            Gradient* gradient,
            uint32_t elements) const;
    };

}
