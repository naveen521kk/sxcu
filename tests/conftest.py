def pytest_addoption(parser):
    parser.addoption(
        "--skip_slow",
        action="store_true",
        default=False,
        help="Will skip all the slow marked tests. Slow tests are arbitrarily marked as such.",
    )
