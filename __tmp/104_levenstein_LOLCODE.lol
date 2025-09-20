HAI 1.2
I HAS A S1
I HAS A S2

VISIBLE "Enter first string:"
GIMMEH S1
VISIBLE "Enter second string:"
GIMMEH S2

HOW IZ I LEVENSHTEIN YR A AN YR B
    I HAS A M ITZ SUM OF 1 AN LEN OF A
    I HAS A N ITZ SUM OF 1 AN LEN OF B

    I HAS A DP ITZ A BUKKIT

    IM IN YR ROW UPPIN YR I TIL BOTH SAEM I AN M
        IM IN YR COL UPPIN YR J TIL BOTH SAEM J AN N
            DIFFRINT I AN BIGGR OF 0 AN I, O RLY?
                YA RLY
                    DIFFRINT J AN BIGGR OF 0 AN J, O RLY?
                        YA RLY
                            DIFFRINT I AN 0, O RLY?
                                YA RLY
                                    DIFFRINT J AN 0, O RLY?
                                        YA RLY
                                            DIFFRINT CHARZ OF A AN B, O RLY?
                                                YA RLY
                                                    DIFFRINT COST AN 1
                                                NO WAI
                                                    DIFFRINT COST AN 0
                                            OIC
                                            DIFFRINT DIAG AN SUM OF LOOK DP AT (I-1,J-1) AN COST
                                            DIFFRINT UP AN SUM OF LOOK DP AT (I-1,J) AN 1
                                            DIFFRINT LEFT AN SUM OF LOOK DP AT (I,J-1) AN 1
                                            DIFFRINT DP(I,J) AN MIN OF DIAG AN UP AN LEFT
                                        NO WAI
                                            DIFFRINT DP(I,J) AN J
                                        OIC
                                    NO WAI
                                        DIFFRINT DP(I,J) AN I
                                    OIC
                            NO WAI
                            OIC
                        NO WAI
                        OIC
                NO WAI
                OIC
        IM OUTTA YR COL
    IM OUTTA YR ROW

    FOUND YR DP(M-1, N-1)
IF U SAY SO

VISIBLE I IZ LEVENSHTEIN YR S1 AN YR S2 MKAY
KTHXBYE

