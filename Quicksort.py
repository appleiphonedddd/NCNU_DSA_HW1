def normalize(card: str) -> str:
    card = card.strip()
    if not card:
        return card
    s = card[0].upper()
    r = card[1:]
    if r.isalpha():
        r = r.upper()
    return s + r

SUIT_PRI = {"C": 1, "D": 2, "S": 3, "H": 4}
RANK_PRI = {"J": 11, "Q": 12, "K": 13, "A": 14}

def parse_key(card_norm: str):

    s = card_norm[0]
    r = card_norm[1:]
    suit_w = SUIT_PRI.get(s, 0)
    if r in RANK_PRI:
        rank_w = RANK_PRI[r]
    else:
        
        try:
            rank_w = int(r)
        except ValueError:
            
            rank_w = -1
    return (suit_w, rank_w)

def quicksort(arr):

    a = [normalize(x) for x in arr]

    def swap(i, j):
        if i != j:
            a[i], a[j] = a[j], a[i]
            print(",".join(a))

    def partition(lo, hi):
        pivot = a[hi]
        pivot_key = parse_key(pivot)
        i = lo
        for j in range(lo, hi):
            if parse_key(a[j]) < pivot_key:
                swap(i, j)
                i += 1
        swap(i, hi)
        return i

    def qs(lo, hi):
        if lo < hi:
            p = partition(lo, hi)
            qs(lo, p - 1)
            qs(p + 1, hi)

    qs(0, len(a) - 1)

if __name__ == "__main__":
    array = input("").strip()
    print(array)

    parts = [x.strip() for x in array.split(",") if x.strip()]
    quicksort(parts)

