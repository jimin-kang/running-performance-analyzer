from dataclasses import dataclass
import pandas as pd
from matplotlib.figure import Figure

@dataclass
class WorkbookSheetConfig:
    """
    Dataclass for an excel worksheet.
    Each worksheet requires the name, the data to write, and the figure that visualizes that data (if applicable).
    """
    name: str
    data: pd.DataFrame
    fig: Figure | None = None
    
@dataclass
class PdfConfig:
    """
    Dataclass for a PDF report.
    Contains all the figures to include in the report, where each figure is written to a separate page.
    """
    figs: list[Figure]