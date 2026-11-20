import pytest
from hypothesis import given, strategies as st

from marathon_registration_parser import average_split, format_bib_name, parse_finish_time


unexpected_types = st.one_of(st.none(), st.integers(), st.binary())


@given(st.text() | unexpected_types)
def test_format_bib_name_no_crash(name):
    try:
        result = format_bib_name(name)
    except Exception as exc:
        pytest.fail(f"format_bib_name raised {exc!r} for {name!r}")

    expected = name.strip().upper()[:12] if isinstance(name, str) else ""
    assert result == expected
    assert isinstance(result, str)
    assert len(result) <= 12


@given(
    st.data(),
    st.integers(min_value=0, max_value=10000),
    st.integers(min_value=0, max_value=59),
    st.integers(min_value=0, max_value=59),
)
def test_parse_finish_time_no_crash(data, hours, minutes, seconds):
    valid = f"{hours}:{minutes:02d}:{seconds:02d}"
    invalid = st.one_of(
        unexpected_types,
        st.text(alphabet=" abc012+-"),
        st.sampled_from(("1::03", "1:02:03:04", "1:60:00", "1:00:60", "-1:00:00")),
    )
    text, expected = data.draw(
        st.one_of(
            invalid.map(lambda value: (value, None)),
            st.just((valid, hours * 3600 + minutes * 60 + seconds)),
        )
    )
    try:
        result = parse_finish_time(text)
    except Exception as exc:
        pytest.fail(f"parse_finish_time raised {exc!r} for {text!r}")

    assert result == expected
    if expected is not None:
        assert type(result) is int


@given(st.data(), st.lists(st.integers(min_value=1, max_value=1000), min_size=1))
def test_average_split_no_crash(data, splits):
    valid = "  ".join(map(str, splits))
    invalid = st.one_of(
        unexpected_types,
        st.text(alphabet=" \t\n"),
        st.sampled_from(("25 x 24", "25 24.5", "25 -1", "25 0")),
    )
    text, expected = data.draw(
        st.one_of(
            invalid.map(lambda value: (value, None)),
            st.just((valid, sum(splits) / len(splits))),
        )
    )
    try:
        result = average_split(text)
    except Exception as exc:
        pytest.fail(f"average_split raised {exc!r} for {text!r}")

    if expected is None:
        assert result is None
    else:
        assert isinstance(result, float)
        assert result == pytest.approx(expected)
        assert min(splits) <= result <= max(splits)
