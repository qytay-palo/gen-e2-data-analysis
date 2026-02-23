"""Visualization functions for workforce and capacity data.

This module provides standardized plotting functions for temporal trends, sector
comparisons, composition changes, and workforce-capacity relationships.

Author: Generated from User Story 3 Implementation Plan
Date: 2026-02-23
"""

import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Optional, List, Tuple
from loguru import logger


def plot_temporal_trends(
    df: pl.DataFrame,
    time_col: str = 'year',
    value_col: str = 'count',
    group_col: str = 'sector',
    title: str = 'Temporal Trends',
    ylabel: str = 'Count',
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    dpi: int = 300
) -> plt.Figure:
    """
    Create line plot showing temporal trends grouped by category.
    
    Args:
        df: Input DataFrame
        time_col: Column containing time dimension
        value_col: Column containing values to plot
        group_col: Column containing group categories
        title: Plot title
        ylabel: Y-axis label
        output_path: If provided, save figure to this path
        figsize: Figure size (width, height)
        dpi: Resolution for saved figure
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_temporal_trends(
        ...     workforce_df,
        ...     group_col='profession',
        ...     title='Workforce Trends by Profession',
        ...     output_path='reports/figures/workforce_trends.png'
        ... )
    """
    logger.info(f"Creating temporal trends plot grouped by {group_col}")
    
    # Convert to pandas for plotting
    plot_df = df.to_pandas()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot lines for each group
    for group in plot_df[group_col].unique():
        group_data = plot_df[plot_df[group_col] == group].sort_values(time_col)
        ax.plot(
            group_data[time_col],
            group_data[value_col],
            marker='o',
            label=group,
            linewidth=2,
            markersize=6
        )
    
    # Formatting
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(time_col.capitalize(), fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend(title=group_col.capitalize(), fontsize=10, title_fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add data source annotation
    ax.text(
        0.99, 0.01, 'Source: MOH Singapore via Kaggle',
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='bottom',
        style='italic',
        color='gray'
    )
    
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig


def plot_sector_comparison(
    df: pl.DataFrame,
    sector_col: str = 'sector',
    value_col: str = 'count',
    category_col: Optional[str] = None,
    title: str = 'Sector Comparison',
    ylabel: str = 'Count',
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6),
    dpi: int = 300
) -> plt.Figure:
    """
    Create grouped bar chart comparing sectors.
    
    Args:
        df: Input DataFrame
        sector_col: Column containing sector categories
        value_col: Column containing values to plot
        category_col: Optional column for grouping within sectors
        title: Plot title
        ylabel: Y-axis label
        output_path: If provided, save figure to this path
        figsize: Figure size
        dpi: Resolution
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_sector_comparison(
        ...     workforce_df,
        ...     category_col='profession',
        ...     title='Workforce by Sector and Profession (2019)',
        ...     output_path='reports/figures/sector_comparison.png'
        ... )
    """
    logger.info(f"Creating sector comparison bar chart")
    
    # Convert to pandas
    plot_df = df.to_pandas()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    if category_col:
        # Grouped bar chart
        sectors = sorted(plot_df[sector_col].unique())
        categories = sorted(plot_df[category_col].unique())
        
        x = np.arange(len(sectors))
        width = 0.8 / len(categories)
        
        for i, category in enumerate(categories):
            category_data = plot_df[plot_df[category_col] == category]
            values = [
                category_data[category_data[sector_col] == sector][value_col].sum()
                for sector in sectors
            ]
            ax.bar(
                x + i * width,
                values,
                width,
                label=category
            )
        
        ax.set_xticks(x + width * (len(categories) - 1) / 2)
        ax.set_xticklabels(sectors)
        ax.legend(title=category_col.capitalize())
    else:
        # Simple bar chart
        sector_data = plot_df.groupby(sector_col)[value_col].sum().reset_index()
        ax.bar(sector_data[sector_col], sector_data[value_col])
    
    # Formatting
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(sector_col.capitalize(), fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    
    # Add data source
    ax.text(
        0.99, 0.01, 'Source: MOH Singapore via Kaggle',
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='bottom',
        style='italic',
        color='gray'
    )
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig


def plot_composition_stacked(
    df: pl.DataFrame,
    time_col: str = 'year',
    category_col: str = 'profession',
    value_col: str = 'percentage',
    group_col: str = 'sector',
    title: str = 'Composition Over Time',
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 6),
    dpi: int = 300
) -> plt.Figure:
    """
    Create stacked area chart showing composition changes over time.
    
    Args:
        df: Input DataFrame with composition percentages
        time_col: Column containing time dimension
        category_col: Column containing composition categories
        value_col: Column containing percentage values
        group_col: Column to facet by (creates subplots)
        title: Plot title
        output_path: If provided, save figure to this path
        figsize: Figure size
        dpi: Resolution
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_composition_stacked(
        ...     composition_df,
        ...     category_col='profession',
        ...     group_col='sector',
        ...     title='Workforce Composition by Sector',
        ...     output_path='reports/figures/composition_trends.png'
        ... )
    """
    logger.info(f"Creating stacked composition chart")
    
    # Convert to pandas and pivot
    plot_df = df.to_pandas()
    groups = sorted(plot_df[group_col].unique())
    
    # Create subplots
    fig, axes = plt.subplots(1, len(groups), figsize=figsize, sharey=True)
    if len(groups) == 1:
        axes = [axes]
    
    categories = sorted(plot_df[category_col].unique())
    colors = sns.color_palette('Set2', n_colors=len(categories))
    
    for ax, group in zip(axes, groups):
        group_data = plot_df[plot_df[group_col] == group]
        
        # Pivot for stacked area
        pivot_data = group_data.pivot(
            index=time_col,
            columns=category_col,
            values=value_col
        ).fillna(0)
        
        # Plot stacked area
        ax.stackplot(
            pivot_data.index,
            *[pivot_data[cat] for cat in categories],
            labels=categories,
            colors=colors,
            alpha=0.8
        )
        
        ax.set_title(f'{group}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Year', fontsize=10)
        if ax == axes[0]:
            ax.set_ylabel('Percentage (%)', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(0, 100)
    
    # Add legend to last subplot
    axes[-1].legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)
    
    fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig


def plot_workforce_capacity_scatter(
    df: pl.DataFrame,
    workforce_col: str = 'total_workforce',
    capacity_col: str = 'total_beds',
    group_col: str = 'sector',
    title: str = 'Workforce vs. Capacity',
    output_path: Optional[str] = None,
    add_regression: bool = True,
    figsize: Tuple[int, int] = (10, 8),
    dpi: int = 300
) -> plt.Figure:
    """
    Create scatter plot of workforce vs. capacity with optional regression line.
    
    Args:
        df: Input DataFrame
        workforce_col: Column containing workforce values
        capacity_col: Column containing capacity values
        group_col: Column for color grouping
        title: Plot title
        output_path: If provided, save figure to this path
        add_regression: Whether to add regression line
        figsize: Figure size
        dpi: Resolution
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_workforce_capacity_scatter(
        ...     ratio_df,
        ...     add_regression=True,
        ...     output_path='reports/figures/workforce_capacity_scatter.png'
        ... )
    """
    logger.info(f"Creating workforce-capacity scatter plot")
    
    # Convert to pandas
    plot_df = df.to_pandas()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Scatter plot with groups
    groups = sorted(plot_df[group_col].unique())
    colors = sns.color_palette('Set1', n_colors=len(groups))
    
    for group, color in zip(groups, colors):
        group_data = plot_df[plot_df[group_col] == group]
        ax.scatter(
            group_data[capacity_col],
            group_data[workforce_col],
            label=group,
            alpha=0.7,
            s=100,
            color=color,
            edgecolors='black',
            linewidth=0.5
        )
    
    # Add regression line
    if add_regression:
        from scipy.stats import linregress
        x = plot_df[capacity_col]
        y = plot_df[workforce_col]
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept
        
        ax.plot(
            x_line,
            y_line,
            'k--',
            linewidth=2,
            label=f'Regression (R²={r_value**2:.3f})'
        )
    
    # Formatting
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(capacity_col.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel(workforce_col.replace('_', ' ').title(), fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add data source
    ax.text(
        0.99, 0.01, 'Source: MOH Singapore via Kaggle',
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='bottom',
        style='italic',
        color='gray'
    )
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig


def plot_growth_rate_comparison(
    df: pl.DataFrame,
    category_col: str = 'sector',
    growth_col: str = 'growth_rate',
    title: str = 'Average Growth Rates by Category',
    ylabel: str = 'Average Growth Rate (%)',
    output_path: Optional[str] = None,
    add_error_bars: bool = True,
    figsize: Tuple[int, int] = (10, 6),
    dpi: int = 300
) -> plt.Figure:
    """
    Create bar chart comparing average growth rates with error bars.
    
    Args:
        df: Input DataFrame with growth rates
        category_col: Column containing categories to compare
        growth_col: Column containing growth rate values
        title: Plot title
        ylabel: Y-axis label
        output_path: If provided, save figure to this path
        add_error_bars: Whether to add standard error bars
        figsize: Figure size
        dpi: Resolution
        
    Returns:
        Matplotlib Figure object
        
    Example:
        >>> fig = plot_growth_rate_comparison(
        ...     growth_df,
        ...     category_col='profession',
        ...     title='Average Growth Rates by Profession',
        ...     output_path='reports/figures/growth_comparison.png'
        ... )
    """
    logger.info(f"Creating growth rate comparison bar chart")
    
    # Convert to pandas
    plot_df = df.filter(pl.col(growth_col).is_not_null()).to_pandas()
    
    # Calculate means and std errors
    stats_df = plot_df.groupby(category_col)[growth_col].agg(['mean', 'sem']).reset_index()
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Bar chart
    x = np.arange(len(stats_df))
    bars = ax.bar(
        x,
        stats_df['mean'],
        yerr=stats_df['sem'] if add_error_bars else None,
        capsize=5,
        alpha=0.8,
        edgecolor='black',
        linewidth=1.5
    )
    
    # Color positive bars green, negative bars red
    for bar, mean_val in zip(bars, stats_df['mean']):
        if mean_val >= 0:
            bar.set_color('forestgreen')
        else:
            bar.set_color('firebrick')
    
    # Formatting
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(category_col.capitalize(), fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(stats_df[category_col])
    ax.axhline(0, color='black', linewidth=0.8)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (bar, mean_val, sem_val) in enumerate(zip(bars, stats_df['mean'], stats_df['sem'])):
        height = bar.get_height()
        label_y = height + sem_val + 0.2 if height >= 0 else height - sem_val - 0.5
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            label_y,
            f'{mean_val:.1f}%',
            ha='center',
            va='bottom' if height >= 0 else 'top',
            fontsize=9,
            fontweight='bold'
        )
    
    # Add data source
    ax.text(
        0.99, 0.01, 'Source: MOH Singapore via Kaggle',
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='bottom',
        style='italic',
        color='gray'
    )
    
    plt.tight_layout()
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
        logger.success(f"Figure saved to {output_path}")
    
    return fig
