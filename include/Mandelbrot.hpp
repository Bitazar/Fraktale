#pragma once

#include "Exchanger.hpp"
#include "Gradient.hpp"

#include <complex.h>

namespace fractal {

    class Mandelbrot {
    public:
        typedef std::complex<double>                Complex;

        explicit Mandelbrot(uint32_t maxIterations, Complex start, Complex end)
            : maxIterations{maxIterations}, start{start}, end{end} {}

        int operator() (Complex const& step) const noexcept;

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

        void setMaxIterations(uint32_t maxIterations) noexcept
            { this->maxIterations = maxIterations; }

        void setStart(Complex const& start) noexcept
            { this->start = start; }

        void setEnd(Complex const& end) noexcept
            { this->end = end; }
    private:
        Complex                                     start;
        Complex                                     end;
        uint32_t                                    maxIterations;

        Complex getStep(uint32_t width, uint32_t height, uint32_t x, uint32_t y) const;

        void generateSegment(uint8_t* memory, uint32_t width, uint32_t height, Gradient* gradient,
            uint32_t segmentHeight, uint32_t segmentStart) const;
    };

}
