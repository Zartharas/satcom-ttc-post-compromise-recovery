# Study E scaffold (development, NOT frozen)

Exact DP (`model.py`), an independent path simulator/enumerator/Monte Carlo (`sim.py`), shared rule file (`rules.py`), tests and a frozen-record guard.
No pre-registered grid has been run. See docs/ASSUMPTIONS.md for source status and open items.

    make test                 # python3 -I -W error::ResourceWarning ...
    make test-full            # larger exhaustive differential grid
    TTC_REPO_ROOT=/path/to/satcom-ttc-post-compromise-recovery make test   # enables the frozen-record guard
    docker compose run --rm test        # same, in a locked-down container (see docker-compose.yml)

Docker files were written but NOT build-tested by the author of this scaffold (no Docker in the dev VM).
