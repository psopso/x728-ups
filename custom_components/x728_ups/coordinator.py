    async def _async_update_data(self):
        data = {}

        # GPIO
        try:
            power_loss_val = self.power_loss_req.get_value(PIN_POWER_LOSS)
            data["power_loss"] = (power_loss_val == Value.INACTIVE)
        except Exception as err:
            _LOGGER.error("GPIO read failed: %s", err)
            data["power_loss"] = None

        # I2C
        try:
            raw_v = self.bus.read_word_data(I2C_ADDR, REG_VOLTAGE)
            raw_v = ((raw_v >> 8) | (raw_v << 8)) & 0xFFFF
            data["voltage"] = round(raw_v * 1.25 / 1000, 2)

            raw_c = self.bus.read_word_data(I2C_ADDR, REG_CAPACITY)
            raw_c = ((raw_c >> 8) | (raw_c << 8)) & 0xFFFF
            data["capacity"] = round(raw_c / 256, 1)

        except OSError as err:
            _LOGGER.warning("I2C read failed: %s", err)
            data["voltage"] = None
            data["capacity"] = None

        return data   # ← TOTO TAM CHYBĚLO
