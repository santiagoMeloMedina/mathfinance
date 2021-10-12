def format_money(value: float, decimal: int = 3) -> str:
    expression = f":,.{decimal}f"
    return ("{" + expression + "}").format(value)
