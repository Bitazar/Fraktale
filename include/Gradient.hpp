#pragma once

#include <tuple>
#include <inttypes.h>

namespace fractal {

    class Gradient {
    public:
        typedef std::tuple<uint8_t, uint8_t, uint8_t>       Pixel;

        explicit Gradient(
            Pixel const& lowerLimit,
            Pixel const& upperLimit,
            bool inverted = false)
            : lowerLimit{lowerLimit}, upperLimit{upperLimit}, inverted{inverted} {}

        void invert(void) noexcept
            { inverted = !inverted; }

        Pixel operator() (uint8_t value) const;
    private:
        Pixel                                               lowerLimit;
        Pixel                                               upperLimit;
        bool                                                inverted;

        template <uint8_t Axis>
        uint8_t interpolate(uint8_t value) const {
            int16_t range = std::get<Axis>(upperLimit) - std::get<Axis>(lowerLimit);
            int16_t scaled = (int16_t) std::get<Axis>(lowerLimit) + range * value / 255;
            uint8_t result = scaled < 256 ? (
                scaled >= 0 ? static_cast<uint8_t>(scaled) : 0 ) : 255;
            return inverted ? 255 - result : result;
        }
    };

}
