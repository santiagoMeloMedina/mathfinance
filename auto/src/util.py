def format_money(value: float, decimal: int) -> str:
    expression = f":,.{decimal}f"
    return ("{" + expression + "}").format(value)
