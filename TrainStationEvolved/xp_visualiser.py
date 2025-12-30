def xp_to_next_level(level: int) -> int:
    if level <= 5:
        return [20, 80, 231, 556, 1035][level - 1]
    
    elif level > 300:
        BASE_XP = 700000
        BLOCK_GROWTH = 10000

        block = (level - 1) // 5
        return BASE_XP + (block * BLOCK_GROWTH)


    A = 500
    B = 200
    C = 9

    xp = A + (B * level) + (C * (level ** 2))
    return int(xp)

# =========================
# VISUALIZAÇÃO NÍVEL A NÍVEL
# =========================

def visualize_levels(max_level):
    total_xp = 0

    print("-" * 50)
    print(f"{'LVL':>4} | {'XP → Próx':>8} | {'XP Total':>10}")
    print("-" * 50)

    for level in range(1, max_level + 1):

        xp_needed = xp_to_next_level(level)
        total_xp += xp_needed

        print(
            f"{level:>4} | "
            f"{xp_needed:>8} | "
            f"{total_xp:>10}"
        )

    print("-" * 50)


# =========================
# EXECUÇÃO
# =========================

#visualize_levels(1000)