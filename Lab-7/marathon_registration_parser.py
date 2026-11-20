def format_bib_name(name):
    """Return an uppercase bib name of at most 12 characters, or an empty string."""
    if not isinstance(name, str):
        return ""
    return name.strip().upper()[:12]


def parse_finish_time(text):
    """Convert H:MM:SS to seconds, or return None for invalid input."""
    if not isinstance(text, str):
        return None

    parts = text.strip().split(":")
    if len(parts) != 3:
        return None
    try:
        hours, minutes, seconds = map(int, parts)
    except ValueError:
        return None
    if hours < 0 or not (0 <= minutes < 60 and 0 <= seconds < 60):
        return None
    return hours * 3600 + minutes * 60 + seconds


def average_split(text):
    """Average positive whole-minute splits, or return None for invalid input."""
    if not isinstance(text, str):
        return None

    try:
        splits = [int(part) for part in text.split()]
        if not splits or any(split <= 0 for split in splits):
            return None
        return sum(splits) / len(splits)
    except (ValueError, OverflowError):
        return None


def main():
    print("==== Running format_bib_name ====")
    value = input("Enter the name to print on the bib: ")
    print("Bib name:", format_bib_name(value))

    print("\n==== Running parse_finish_time ====")
    value = input("Enter a finish time as H:MM:SS (e.g. 3:45:10): ")
    finish_time = parse_finish_time(value)
    if finish_time is None:
        print("Invalid finish time. Enter hours, minutes and seconds as H:MM:SS.")
    else:
        print("Finish time in seconds:", finish_time)

    print("\n==== Running average_split ====")
    value = input("Enter your 5 km split times in minutes separated by spaces (e.g. 25 26 24): ")
    average = average_split(value)
    if average is None:
        print("Invalid split times. Enter one or more positive whole minutes.")
    else:
        print("Average split (minutes):", average)

if __name__ == "__main__":
    main()
