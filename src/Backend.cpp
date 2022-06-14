#include "../include/Exchanger.hpp"
#include "../include/Mandelbrot.hpp"
#include "../include/Gradient.hpp"
#include "../include/Julia.hpp"
#include "../include/BarnsleyFern.hpp"

fractal::Exchanger<fractal::Mandelbrot*>        mandelbrots;
fractal::Exchanger<fractal::Gradient*>          gradients;
fractal::Exchanger<fractal::Julia*>             julias;
fractal::Exchanger<fractal::BarnsleyFern*>      ferns;

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
    uint8_t upper_red, uint8_t upper_green, uint8_t upper_blue,
    bool inverted)
{
    return gradients.assign(new fractal::Gradient{
        {lower_red, lower_green, lower_blue},
        {upper_red, upper_green, upper_blue}, inverted
    });
}

extern "C" void invert_gradient(uint32_t ptr) {
    gradients.get(ptr)->invert();
}

extern "C" void change_gradient_system(uint32_t ptr, uint8_t system) {
    gradients.get(ptr)->changeSystem(system);
}

extern "C" void gradient_change_lower_limit(uint32_t ptr,
    uint8_t lower_red, uint8_t lower_green, uint8_t lower_blue)
{
    gradients.get(ptr)->changeLowerLimit({lower_red, lower_green, lower_blue});
}

extern "C" void gradient_change_upper_limit(uint32_t ptr,
    uint8_t upper_red, uint8_t upper_green, uint8_t upper_blue)
{
    gradients.get(ptr)->changeLowerLimit({upper_red, upper_green, upper_blue});
}

extern "C" uint32_t create_julia(
    uint32_t maxIterations, double startReal, double startImag,
    double endReal, double endImag,
    double constReal, double constImag)
{
    return julias.assign(new fractal::Julia{
        maxIterations, {startReal, startImag}, {endReal, endImag},
        {constReal, constImag}
    });
}

extern "C" void generate_julia(
    uint32_t ptr, uint8_t* memory, uint32_t width, uint32_t height, uint32_t gradPtr)
{
    julias.get(ptr)->generate(memory, width, height, gradients.get(gradPtr));
}

extern "C" void generate_julia_parallel(
    uint32_t ptr, uint8_t* memory, uint32_t width, uint32_t height, uint32_t gradPtr,
    int32_t threads)
{
    julias.get(ptr)->generateParallel(memory, width, height, gradients.get(gradPtr), threads);
}

extern "C" uint32_t create_barnsley_fern(
    uint32_t points)
{
    return ferns.assign(new fractal::BarnsleyFern{points});
}

extern "C" void generate_barnsley_fern(
    uint32_t ptr, uint8_t* memory, uint32_t width, uint32_t height, uint32_t gradPtr)
{
    ferns.get(ptr)->generate(memory, width, height, gradients.get(gradPtr));
}

extern "C" void generate_barnsley_fern_parallel(
    uint32_t ptr, uint8_t* memory, uint32_t width, uint32_t height, uint32_t gradPtr,
    int32_t threads)
{
    ferns.get(ptr)->generateParallel(memory, width, height, gradients.get(gradPtr), threads);
}
