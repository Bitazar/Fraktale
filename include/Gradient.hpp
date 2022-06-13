#include <tuple>
#include <inttypes.h>

namespace fractal {

    class Gradient {
    public:
        typedef std::tuple<uint8_t, uint8_t, uint8_t>       Pixel;

        explicit Gradient(Pixel const& lowerLimit, Pixel const& upperLimit)
            : lowerLimit{lowerLimit}, upperLimit{upperLimit} {}

        Pixel operator() (uint8_t value);
    private:
        Pixel                                               lowerLimit;
        Pixel                                               upperLimit;

        template <uint8_t Axis>
        uint8_t interpolate(uint8_t value) {
            int16_t range = std::get<Axis>(upperLimit) - std::get<Axis>(lowerLimit);
            int16_t scaled = (int16_t) std::get<Axis>(lowerLimit) + range * value / 255;
            return scaled < 256 ? (
                scaled >= 0 ? static_cast<uint8_t>(scaled) : 0 ) : 255;
        }
    };

}
