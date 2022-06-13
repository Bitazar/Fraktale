#include "../include/Gradient.hpp"

namespace fractal {

    Gradient::Pixel Gradient::operator() (uint8_t value) const {
        switch (pallete) {
            case Palletes::RGB:
                return rgb(value);
            case Palletes::HSV:
                return hsv(value);
            case Palletes::YCbCr:
                return ycbcr(value);
        }
        return yuv(value);
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

    Gradient::Pixel Gradient::ycbcr(uint8_t value) const noexcept {
        uint8_t luminancy = interpolate<0>(value);
        uint8_t blue = interpolate<1>(value);
        uint8_t red = interpolate<2>(value);
        uint16_t green = 3 * luminancy - blue - red;
        return {red, static_cast<uint8_t>(green), blue};
    }

    Gradient::Pixel Gradient::yuv(uint8_t value) const noexcept {
        double y = interpolate<0>(value) - 16;
        double u = interpolate<1>(value) - 128;
        double v = interpolate<2>(value) - 128;
        return {
            1.164 * y + 1.596 * v,
            1.164 * y - 0.392 * u - 0.813 * v,
            1.164 * y + 2.017 * u
        };
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
