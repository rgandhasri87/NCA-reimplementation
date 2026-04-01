import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    from nca_utils import load_emoji

    emoji_input = mo.ui.text(
        value="🫏",
        label="Enter emoji to use as target",
        placeholder="🫏"
    )

    emoji_input
    return emoji_input, load_emoji


@app.cell
def _(emoji_input, load_emoji):
    target_np = load_emoji(emoji_input.value)
    target_np
    return (target_np,)


@app.cell
def _(target_np):
    import numpy as np
    assert np.any(target_np != np.zeros((40,40,4)))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
