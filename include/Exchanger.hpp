#pragma once

#include <map>
#include <atomic>
#include <type_traits>

namespace fractal {

    template <typename Tp>
    class Exchanger {
    public:
        explicit Exchanger(void) = default;

        Exchanger(Exchanger const&) = delete;
        Exchanger(Exchanger&&) = delete;

        Exchanger& operator=(Exchanger const&) = delete;
        Exchanger& operator=(Exchanger&&) = delete;

        uint32_t assign(Tp base);

        Tp get(uint32_t key)
            { return exchangeLib.at(key); }

        ~Exchanger(void)
    private:
        std::map<uint32_t, Tp>              exchangeLib;
        std::atomic<uint32_t>               addressQueue;
    };

}

#include "Exchanger.tpp"
