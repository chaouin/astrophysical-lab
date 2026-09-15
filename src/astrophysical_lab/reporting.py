import json
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from astrophysical_lab.models import ExperimentResult


def save_result_json(
    result: ExperimentResult,
    output_dir: str | Path = "outputs",
) -> Path:
    """Save the structured experiment result as JSON."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "results.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            asdict(result),
            file,
            indent=2,
            ensure_ascii=False,
        )

    return output_path


def plot_metallicity_distributions(
    short_period_hosts: pd.DataFrame,
    comparison_hosts: pd.DataFrame,
    output_dir: str | Path = "outputs",
) -> Path:
    """Plot stellar metallicity distributions for both host populations."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "metallicity_distribution.png"

    plt.figure(figsize=(8, 5))

    plt.hist(
        short_period_hosts["st_met"],
        bins=30,
        alpha=0.6,
        density=True,
        label="Hosts with short-period giants",
        color="lightgreen",
    )

    plt.hist(
        comparison_hosts["st_met"],
        bins=30,
        alpha=0.6,
        density=True,
        label="Other giant-planet hosts",
        color="pink",
    )

    plt.xlabel("Stellar metallicity [Fe/H]")
    plt.ylabel("Density")
    plt.title("Stellar Metallicity of Giant-Planet Host Populations")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    return output_path
