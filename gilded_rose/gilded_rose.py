# -*- coding: utf-8 -*-
""" Module containing classes used to manage items
from Gilded Rose shop."""


from loguru import logger


class GildedRose(object):
    """Main class used to manage items from the Gilded
    Rose shop."""

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """Updates quality and sell_in properties for items in the store."""

        for item in self.items:
            item.tick()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class StandardItem(Item):
    """Class definition for StandardItem."""

    def __init__(self, name, sell_in, quality):
        """Initializes StandardItem object.

        Args:
            name: Item name.
            sell_in: Days remaining until expiration date.
            quality: Indicates product quality.

        Returns:
            An object of class StandardItem.
        """

        logger.debug(f"Initializing StandardItem: {name}")

        self._max_quality = 50
        self._min_quality = 0
        self._quality_daily_change = 1

        super().__init__(name=name, sell_in=sell_in, quality=quality)

    def tick(self):
        """Function used to update items sell_in and quality properties."""

        self.update_quality()
        self.update_sell_in()

    def _get_updated_quality(self):

        quality_change = self._quality_daily_change
        if self.sell_in <= 0:
            quality_change = self._quality_daily_change * 2

        # "Clamp" quality between min and max value
        updated_quality = max(
            self._min_quality,
            min(self.quality - quality_change, self._max_quality)
        )

        return updated_quality

    def update_quality(self):
        """Updates quality for the item."""

        logger.debug("Update quality")
        updated_quality = self._get_updated_quality()
        self.quality = updated_quality

    def update_sell_in(self):
        """Updates item sell_in property."""

        logger.debug(f"Updating sell_in, current value: {self.sell_in}")
        self.sell_in -= 1


class AgedBrie(StandardItem):
    """Definition for AgedBrie class."""

    def __init__(self, name, sell_in, quality):

        super().__init__(name, sell_in, quality)
        # AgedBrie increases in quality over time
        self._quality_daily_change *= -1


class BackstagePass(StandardItem):
    """Definition for BackstagePass class."""

    def _get_updated_quality(self):

        logger.debug(f"Quality: {self.quality}, Max: {self._max_quality}")
        logger.debug(f"Sell In: {self.sell_in}")

        quality_increase = 0
        if (self.sell_in <= 0):
            return 0
        elif self.sell_in > 10:
            quality_increase = self._quality_daily_change
        elif 5 < self.sell_in <= 10:
            quality_increase = 2 * self._quality_daily_change
        elif 0 < self.sell_in <= 5:
            quality_increase = 3 * self._quality_daily_change

        target_quality = self.quality + quality_increase
        updated_quality = min(self._max_quality, target_quality)
        return updated_quality

    def update_quality(self):
        """Updates quality for BackstagePass item."""

        self.quality = self._get_updated_quality()


class Conjured(StandardItem):
    """Definition for Conjured class."""

    def __init__(self, name, sell_in, quality):
        """Initializes Conjured object.

        Args:
            name: Item name.
            sell_in: Days remaining until expiration date.
            quality: Indicates product quality.

        Returns:
            An object of class Conjured.
        """

        super().__init__(name=name, sell_in=sell_in, quality=quality)
        self._quality_daily_change = 2 * self._quality_daily_change
        logger.debug(
            f"Updated daily quality decrease: \
            {self._quality_daily_change}"
        )


class Sulfuras(StandardItem):
    """Initializes Sulfuras object.

        Args:
            name: Item name.
            sell_in: Days remaining until expiration date.
            quality: Indicates product quality (kept for compatibility
            purposes; always replaced by 80).

        Returns:
            An object of class Sulfuras.
        """

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality=80)

    def update_quality(self):
        pass

    def update_sell_in(self):
        pass
