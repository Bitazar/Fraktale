#include "../include/Gradient.hpp"

namespace fractal {

    Gradient::Pixel Gradient::operator() (uint8_t value) const {
        return {
            interpolate<0>(value),
            interpolate<1>(value),
            interpolate<2>(value)
        };
    }

}
