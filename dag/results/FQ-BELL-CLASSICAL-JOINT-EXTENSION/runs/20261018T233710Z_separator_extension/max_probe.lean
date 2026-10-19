import BellOperad
example (a b c : Int) (h : a ≤ c) (h2 : b ≤ c) : max a b ≤ c := by omega
example (a b : Int) : max 0 a + max 0 b = max 0 (max (a+b) (max a b)) := by omega
