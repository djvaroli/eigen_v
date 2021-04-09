

def row_column_permutations(n_rows, n_cols, start=1):
    permutations = []
    for r in range(start, n_rows + start):
        for c in range(start, n_cols + start):
            permutations.append((r, c))
    return permutations
