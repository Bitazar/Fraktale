#include "../include/Mandelbrot.hpp"

#include <thread>
#include <vector>
#include <functional>

namespace fractal {

    Mandelbrot::Complex Mandelbrot::getStep(
        uint32_t width, uint32_t height, uint32_t x, uint32_t y)
    {
        double real = start.real() + ((double) x / width) * (end.real() - start.real());
        double imag = start.imag() + ((double) y / height) * (end.imag() - start.imag());
        return {real, imag};
    }

    int Mandelbrot::operator() (Complex const& step) noexcept {
        Complex z = 0;
        uint32_t iter = 0;
        for (;std::abs(z) <= 2 && iter < maxIterations; z = z * z + step, ++iter);
        return iter;
    }

    void Mandelbrot::generate(uint8_t* memory, uint32_t width, uint32_t height) {
        for (uint32_t x = 0; x != width; ++x) {
            for (uint32_t y = 0; y != height; ++y) {
                auto value = (*this)(getStep(width, height, x, y));
                for (uint32_t z = 0; z < 3; ++z)
                    *(memory + width * 3 * y + 3 * x + z) = 255 - value * 255 / maxIterations;
            }
        }
    }

    void Mandelbrot::generateSegment(uint8_t* memory, uint32_t width, uint32_t height,
        uint32_t segmentHeight, uint32_t segmentStart)
    {
        for (uint32_t x = 0; x != width; ++x) {
            for (uint32_t y = segmentStart; y != segmentStart + segmentHeight; ++y) {
                auto value = (*this)(getStep(width, height, x, y));
                for (uint32_t z = 0; z < 3; ++z)
                    *(memory + width * 3 * y + 3 * x + z) = 255 - value * 255 / maxIterations;
            }
        }
    }

    void Mandelbrot::generateParallel(
        uint8_t* memory, uint32_t width, uint32_t height,
        int32_t threads)
    {
        uint32_t rowsPerThread = height / threads;
        std::vector<std::thread> jthreads;
        for (uint32_t i = 0; i < threads - 1; ++i)
            jthreads.emplace_back(std::function<void()>([&, ind=i]() -> void
               { this->generateSegment(memory, width, height, rowsPerThread, ind * rowsPerThread); }));
        jthreads.emplace_back(std::function<void()>([&]() -> void {
            this->generateSegment(memory, width, height,
            height - rowsPerThread * (threads - 1),
            rowsPerThread * (threads - 1));
        }));
        for (auto& thread : jthreads)
            thread.join();
    }

}
