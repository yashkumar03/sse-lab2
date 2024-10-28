from app import process_query


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == (
        "Dinosaurs ruled the Earth 200 million years ago"
    )


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_addition():
    assert process_query("What is 44 plus 87?") == "131"


def test_substraction():
    assert process_query("What is 87 minus 44?") == "43"


def test_multiplication():
    assert process_query("What is 2 multiplied by 10?") == "20"


def test_largest_number():
    assert (
        process_query(
            "Which of the following numbers is the largest: \
    9, 46, 72?"
        )
        == "72"
    )


def test_primes():
    assert (
        process_query(
            "Which of the following numbers are primes: \
    87, 73, 43, 29, 77?"
        )
        == "73, 43, 29"
    )


def test_squares_and_cubes():
    assert (
        process_query(
            "Which of the following numbers is both \
    a square and a cube: 4239, 1521, 1, 3969, 2744, 2788, 4297?"
        )
        == "1"
    )
