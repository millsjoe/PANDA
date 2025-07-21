from src.utils.checksum import calculate_checksum


class TestChecksum:
    def test_calculate_checksum_success(self):
        """calculate_checksum returns True"""
        assert calculate_checksum("0021403597")  # valid NHS number

    def test_calculate_checksum_failure(self):
        """calculate_checksum returns False"""
        assert not calculate_checksum("12345678901")
