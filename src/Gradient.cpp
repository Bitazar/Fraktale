#include "../include/Gradient.hpp"

namespace fractal {

    Gradient::Pixel Gradient::operator() (uint8_t value) const {
        switch (pallete) {
            case Palletes::RGB:
                return rgb(value);
            case Palletes::HSV:
                return hsv(value);
        }

    }

    Gradient::Pixel Gradient::rgb(uint8_t value) const noexcept {
        return {
            interpolate<0>(value),
            interpolate<1>(value),
            interpolate<2>(value)
        };
    }

    Gradient::Pixel Gradient::hsv(uint8_t ivalue) const noexcept {
        uint8_t hue = interpolate<0>(ivalue);
        uint8_t saturation = interpolate<1>(ivalue);
        uint8_t value = interpolate<2>(ivalue);
        value = value == std::get<2>(upperLimit) ? 255 - value : value;
        if (saturation <= 0)
            return {value, value, value};
        double fhue = hue, ff;
        if (fhue > 360.)
            fhue = 360.;
        fhue /= 60.;
        ff = fhue - long(fhue);
        double p = value * (1. - saturation);
        double q = value * (1. - saturation * ff);
        double t = value * (1. - saturation * (1. - ff));
        switch (long(fhue)) {
            case 0:
                return {value, t, p};
            case 1:
                return {q, value, p};
            case 2:
                return {p, value, t};
            case 3:
                return {p, q, value};
            case 4:
                return {t, p, value};
        }
        return {value, p, q};
    }

    void Gradient::changeSystem(uint8_t system) {
        switch (system) {
            case 0x01:
                pallete = Palletes::RGB;
                break;;
            case 0x02:
                pallete = Palletes::HSV;
                break;
            case 0x04:
                pallete = Palletes::YCbCr;
                break;
            case 0x08:
                pallete = Palletes::YUV;
                return;
        }
    }

}
