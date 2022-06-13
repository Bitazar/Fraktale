namespace fractal {

    template <typename Tp>
    uint32_t Exchanger<Tp>::assign(Tp base) {
        uint32_t key = addressQueue++;
        exchangeLib.insert({key, base});
        return key;
    }

    template <typename Tp>
    Exchanger<Tp>::~Exchanger(void) {
        if constexpr (std::is_pointer<Tp>::value) {
            for (auto const& [addr, ptr] : exchangeLib)
                delete ptr;
        }
    }

}
