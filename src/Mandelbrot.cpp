#include "../include/Mandelbrot.hpp"

#include <thread>
#include <vector>
#include <functional>

namespace fractal {

    Mandelbrot::Complex Mandelbrot::getStep(
        uint32_t width, uint32_t height, uint32_t x, uint32_t y) const
    {
        double real = start.real() + ((double) x / width) * (end.real() - start.real());
        double imag = start.imag() + ((double) y / height) * (end.imag() - start.imag());
        return {real, imag};
    }

    int Mandelbrot::operator() (Complex const& step) const noexcept {
        Complex z = 0;
        uint32_t iter = 0;
        for (;std::abs(z) <= 2 && iter < maxIterations; z = z * z + step, ++iter);
        return iter;
    }

    void Mandelbrot::generate(uint8_t* memory, uint32_t width, uint32_t height, Gradient* gradient) const {
        for (uint32_t x = 0; x != width; ++x) {
            for (uint32_t y = 0; y != height; ++y) {
                auto value = (*this)(getStep(width, height, x, y));
                auto pixel = gradient->operator()(value * 255 / maxIterations);
                *(memory + width * 3 * y + 3 * x) = std::get<0>(pixel);
                *(memory + width * 3 * y + 3 * x + 1) = std::get<1>(pixel);
                *(memory + width * 3 * y + 3 * x + 2) = std::get<2>(pixel);
            }
        }
    }

    void Mandelbrot::generateSegment(uint8_t* memory, uint32_t width, uint32_t height, Gradient* gradient,
        uint32_t segmentHeight, uint32_t segmentStart) const
    {
        for (uint32_t x = 0; x != width; ++x) {
            for (uint32_t y = segmentStart; y != segmentStart + segmentHeight; ++y) {
                auto value = (*this)(getStep(width, height, x, y));
                auto pixel = gradient->operator()(value * 255 / maxIterations);
                *(memory + width * 3 * y + 3 * x) = std::get<0>(pixel);
                *(memory + width * 3 * y + 3 * x + 1) = std::get<1>(pixel);
                *(memory + width * 3 * y + 3 * x + 2) = std::get<2>(pixel);
            }
        }
    }

    void Mandelbrot::generateParallel(
        uint8_t* memory, uint32_t width, uint32_t height, Gradient* gradient,
        int32_t threads) const
    {
        uint32_t rowsPerThread = height / threads;
        std::vector<std::thread> jthreads;
        for (uint32_t i = 0; i < threads - 1; ++i)
            jthreads.emplace_back(std::function<void()>([&, ind=i]() -> void
               { this->generateSegment(memory, width, height, gradient, rowsPerThread, ind * rowsPerThread); }));
        jthreads.emplace_back(std::function<void()>([&]() -> void {
            this->generateSegment(memory, width, height, gradient,
            height - rowsPerThread * (threads - 1),
            rowsPerThread * (threads - 1));
        }));
        for (auto& thread : jthreads)
            thread.join();
    }

}
