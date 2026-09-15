from astrophysical_lab.cli import build_parser


def test_investigate_command_defaults():
    parser = build_parser()

    args = parser.parse_args(["investigate"])

    assert args.command == "investigate"
    assert args.max_papers > 0
    assert args.top_k > 0
    assert args.json is False


def test_investigate_command_accepts_options():
    parser = build_parser()

    args = parser.parse_args(
        [
            "investigate",
            "--max-papers",
            "10",
            "--top-k",
            "3",
            "--json",
        ]
    )

    assert args.max_papers == 10
    assert args.top_k == 3
    assert args.json is True