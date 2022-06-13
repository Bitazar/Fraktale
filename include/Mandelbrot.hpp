#pragma once

#include "Exchanger.hpp"

#include <complex.h>

namespace fractal {

    class Mandelbrot {
    public:
        typedef std::complex<double>                Complex;

        explicit Mandelbrot(uint32_t maxIterations, Complex start, Complex end)
            : maxIterations{maxIterations}, start{start}, end{end} {}

        int operator() (Complex const& step) noexcept;

        void generate(uint8_t* memory, uint32_t width, uint32_t height);

        void generateParallel(uint8_t* memory, uint32_t width, uint32_t height, int32_t threads);
    private:
        Complex                                     start;
        Complex                                     end;
        uint32_t                                    maxIterations;

        Complex getStep(uint32_t width, uint32_t height, uint32_t x, uint32_t y);

        void generateSegment(uint8_t* memory, uint32_t width, uint32_t height,
            uint32_t segmentHeight, uint32_t segmentStart);
    };

}
