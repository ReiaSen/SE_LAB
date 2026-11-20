import pytest
from marathon_registration import entry_fee, start_wave, finisher_status

#Example test cases:
def test_10k_standard():
    assert entry_fee("10k", 30, False, False) == 800

def test_first_timer_wave():
    assert start_wave(None, "full") == "D"

#Write the rest of the test cases so that the code is 90- 100% covered.


@pytest.mark.parametrize(
    "race,age,message",
    [
        ("ultra", 30, "unknown race"),
        ("5k", 11, "too young"),
        ("half", 17, "too young for this distance"),
        ("full", 17, "too young for this distance"),
    ],
)
def test_entry_fee_rejects_ineligible_registration(race, age, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        entry_fee(race, age, False, False)


@pytest.mark.parametrize(
    "race,age,early_bird,tshirt,expected",
    [
        ("5k", 12, False, False, 500),
        ("half", 18, False, False, 1200),
        ("full", 18, False, False, 1800),
        ("10k", 64, False, False, 800),
        ("10k", 65, False, False, 400),
        ("half", 30, True, False, 900),
        ("5k", 30, False, True, 800),
        ("5k", 65, True, True, 487),
    ],
)
def test_entry_fee_prices_and_adjustments(race, age, early_bird, tshirt, expected):
    assert entry_fee(race, age, early_bird, tshirt) == expected


@pytest.mark.parametrize(
    "race,minutes,expected",
    [
        ("full", 180, "A"),
        ("full", 181, "B"),
        ("full", 240, "B"),
        ("full", 241, "C"),
        ("half", 90, "A"),
        ("half", 91, "B"),
        ("half", 120, "B"),
        ("half", 121, "C"),
    ],
)
def test_start_wave_boundaries(race, minutes, expected):
    assert start_wave(minutes, race) == expected


@pytest.mark.parametrize(
    "race,minutes,expected",
    [
        ("full", 360, "finisher"),
        ("full", 361, "DNF"),
        ("half", 180, "finisher"),
        ("half", 181, "DNF"),
        ("10k", 90, "finisher"),
        ("10k", 91, "DNF"),
    ],
)
def test_finisher_status_time_limits(race, minutes, expected):
    assert finisher_status(minutes, race, 0) == expected


def test_missed_checkpoint_overrides_valid_finishing_time():
    assert finisher_status(89, "10k", 1) == "DSQ"
