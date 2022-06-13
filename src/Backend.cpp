#include "../include/Exchanger.hpp"
#include "../include/Mandelbrot.hpp"
#include "../include/Gradient.hpp"

fractal::Exchanger<fractal::Mandelbrot*>        mandelbrots;
fractal::Exchanger<fractal::Gradient*>          gradients;

extern "C" uint32_t create_mandelbrot(
    uint32_t maxIterations, double startReal, double startImag,
    double endReal, double endImag)
{
    return mandelbrots.assign(new fractal::Mandelbrot{
        maxIterations, {startReal, startImag}, {endReal, endImag}
    });
}

extern "C" void generate_mandelbrot(
    uint32_t ptr, uint8_t* memory, uint32_t width, uint32_t height, uint32_t gradPtr)
{
    mandelbrots.get(ptr)->generate(memory, width, height, gradients.get(gradPtr));
}

extern "C" void generate_mandelbrot_parallel(
    uint32_t ptr, uint8_t* memory, uint32_t width, uint32_t height, uint32_t gradPtr,
    int32_t threads)
{
    mandelbrots.get(ptr)->generateParallel(memory, width, height, gradients.get(gradPtr), threads);
}

extern "C" uint32_t generate_gradient(
    uint8_t lower_red, uint8_t lower_green, uint8_t lower_blue,
    uint8_t upper_red, uint8_t upper_green, uint8_t upper_blue)
{
    return gradients.assign(new fractal::Gradient{
        {lower_red, lower_green, lower_blue},
        {upper_red, upper_green, upper_blue}
    });
}
