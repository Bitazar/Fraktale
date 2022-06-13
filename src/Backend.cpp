#include "../include/Exchanger.hpp"
#include "../include/Mandelbrot.hpp"

fractal::Exchanger<fractal::Mandelbrot*>        mandelbrots;

extern "C" uint32_t create_mandelbrot(
    uint32_t maxIterations, double startReal, double startImag,
    double endReal, double endImag)
{
    return mandelbrots.assign(new fractal::Mandelbrot{
        maxIterations, {startReal, startImag}, {endReal, endImag}
    });
}

extern "C" void generate_mandelbrot(
    uint32_t ptr, uint8_t* memory, uint32_t width, uint32_t height)
{
    mandelbrots.get(ptr)->generate(memory, width, height);
}

extern "C" void generate_mandelbrot_parallel(
    uint32_t ptr, uint8_t* memory, uint32_t width, uint32_t height,
    int32_t threads)
{
    mandelbrots.get(ptr)->generateParallel(memory, width, height, threads);
}
