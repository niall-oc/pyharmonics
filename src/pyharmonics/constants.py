__author__ = 'github.com/niall-oc'

# Positions
STOP = 'stop'
BUY = 'buy'
SELL = 'sell'
LIMIT = 'limit'
LONG = 'long'
SHORT = 'short'
WAITING = 'waiting'  # Waiting to be traded
OPENED = 'opened'
STOPPED = 'stopped'
CLOSED = 'closed'
TARGET1 = 'target1'
TARGET2 = 'target2'
TARGET3 = 'target3'
TARGET4 = 'target4'
TARGET5 = 'target5'
TARGETS = [TARGET1, TARGET2, TARGET3, TARGET4, TARGET5]

DTS = 'dts'
CLOSE_TIME = 'close_time'
OPEN = 'open'
LOW = 'low'
HIGH = 'high'
CLOSE = 'close'
VOLUME = 'volume'
INDEX = 'index'
COLUMNS = [OPEN, HIGH, LOW, CLOSE, VOLUME, CLOSE_TIME, DTS]
TREND = 'trend'

MIN_1 = "1m"
MIN_3 = "3m"
MIN_5 = "5m"
MIN_10 = "10m"
MIN_15 = "15m"
MIN_30 = "30m"
MIN_45 = "45m"
HOUR_1 = "1h"
HOUR_2 = "2h"
HOUR_4 = "4h"
HOUR_8 = "8h"
DAY_1 = "1d"
DAY_3 = "3d"
DAY_5 = "5d"
WEEK_1 = "1w"
MONTH_1 = "1M"
MONTH_3 = "3M"
MONTH_6 = "6M"

BULLISH = True
BEARISH = False

FORMED = True
FORMING = False


# fib levels
RETRACE = 'retrace'
EXTENSION = 'extension'

R_382 = 0.382
R_5 = 0.5
R_618 = 0.618
R_707 = 0.707
R_786 = 0.786
R_886 = 0.886

E_113 = 1.13
E_1272 = 1.272
E_1414 = 1.414
E_1618 = 1.618
E_2 = 2
E_2227 = 2.227
E_224 = 2.24
E_2618 = 2.618
E_3 = 3
E_3618 = 3.618
E_4 = 4
E_4618 = 4.618

RETRACES = {R_382, R_5, R_618, R_707, R_786, R_886}
EXTENSIONS = {E_113, E_1272, E_1414, E_1618, E_2, E_2227, E_224, E_2618, E_3, E_3618, E_4, E_4618}
ABC_EXTENSIONS = {E_1414, E_1618, E_2, E_2227, E_224, E_2618, E_3, E_3618, E_4, E_4618}

# Divergences
DIVERGENCE = 'divergence'

# Harmonic patterns
HARMONIC = 'harmonic'
CYPHER = 'cypher'
SHARK = 'shark'
DEEP_SHARK = 'deep shark'
ABCD = 'ABCD'
XABCD = 'XABCD'
FIVE_0 = 'five_0'
CRAB = 'crab'
DEEP_CRAB = 'deep crab'
BUTTERFLY = 'butterfly'
DEEP_BUTTERFLY = 'deep butterfly'
BAT = 'bat'
ALT_BAT = 'alt bat'
GARTLEY = 'gartley'
BARTLEY = 'bartley'
OXA = 'OXA'
XAB = 'XAB'
ABC = 'ABC'
BCD = 'BCD'
XAC = 'XAC'
XAD = 'XAD'
XCD = 'XCD'
DOUBLE = 'double'
COMPLETION = 'completion'
MIN = 'min'
MAX = 'max'
ABCD_382_1 = f'{ABCD}-382-1'
ABCD_382_2 = f'{ABCD}-382-2'
ABCD_50 = f'{ABCD}-50'
ABCD_618 = f'{ABCD}-618'
ABCD_707 = f'{ABCD}-707'
ABCD_786 = f'{ABCD}-786'
ABCD_886 = f'{ABCD}-886'

ABCD_382_1_113 = f'{ABCD_382_1}-{E_113}'
ABCD_382_2_113 = f'{ABCD_382_2}-{E_113}'
ABCD_50_113 = f'{ABCD_50}-{E_113}'
ABCD_618_113 = f'{ABCD_618}-{E_113}'
ABCD_707_113 = f'{ABCD_707}-{E_113}'
ABCD_786_113 = f'{ABCD_786}-{E_113}'
ABCD_886_113 = f'{ABCD_886}-{E_113}'

ABCD_382_1_1272 = f'{ABCD_382_1}-{E_1272}'
ABCD_382_2_1272 = f'{ABCD_382_2}-{E_1272}'
ABCD_50_1272 = f'{ABCD_50}-{E_1272}'
ABCD_618_1272 = f'{ABCD_618}-{E_1272}'
ABCD_707_1272 = f'{ABCD_707}-{E_1272}'
ABCD_786_1272 = f'{ABCD_786}-{E_1272}'
ABCD_886_1272 = f'{ABCD_886}-{E_1272}'

ABCD_382_1_1414 = f'{ABCD_382_1}-{E_1414}'
ABCD_382_2_1414 = f'{ABCD_382_2}-{E_1414}'
ABCD_50_1414 = f'{ABCD_50}-{E_1414}'
ABCD_618_1414 = f'{ABCD_618}-{E_1414}'
ABCD_707_1414 = f'{ABCD_707}-{E_1414}'
ABCD_786_1414 = f'{ABCD_786}-{E_1414}'
ABCD_886_1414 = f'{ABCD_886}-{E_1414}'

ABCD_382_1_1618 = f'{ABCD_382_1}-{E_1618}'
ABCD_382_2_1618 = f'{ABCD_382_2}-{E_1618}'
ABCD_50_1618 = f'{ABCD_50}-{E_1618}'
ABCD_618_1618 = f'{ABCD_618}-{E_1618}'
ABCD_707_1618 = f'{ABCD_707}-{E_1618}'
ABCD_786_1618 = f'{ABCD_786}-{E_1618}'
ABCD_886_1618 = f'{ABCD_886}-{E_1618}'

ABCDS = {
    ABCD_382_1, ABCD_382_2, ABCD_50, ABCD_618, ABCD_707, ABCD_786, ABCD_886,
    ABCD_382_1_1272, ABCD_382_2_1272, ABCD_50_1272, ABCD_618_1272, ABCD_707_1272, ABCD_786_1272, ABCD_886_1272,
    ABCD_382_1_1618, ABCD_382_2_1618, ABCD_50_1618, ABCD_618_1618, ABCD_707_1618, ABCD_786_1618, ABCD_886_1618
}

HARMONICS = {
    BAT,
    ALT_BAT,
    CRAB,
    SHARK,
    DEEP_SHARK,
    DEEP_CRAB,
    DEEP_BUTTERFLY,
    GARTLEY,
    BUTTERFLY,
    CYPHER
}

XABCDS = HARMONICS

HARMONIC_PATTERNS = {
    XABCD: {
        CRAB: {
            XAB: {MIN: R_382, MAX: R_618},
            ABC: {MIN: R_382, MAX: R_886},
            BCD: {MIN: E_2618, MAX: E_3618},
            XABCD: {MIN: E_1618, MAX: E_1618}
        },
        DEEP_CRAB: {
            XAB: {MIN: R_886, MAX: R_886},
            ABC: {MIN: R_382, MAX: R_886},
            BCD: {MIN: E_2227, MAX: E_3618},
            XABCD: {MIN: E_1618, MAX: E_1618}
        },
        DEEP_BUTTERFLY: {
            XAB: {MIN: R_786, MAX: R_786},
            ABC: {MIN: R_382, MAX: R_886},
            BCD: {MIN: E_1618, MAX: E_2618},
            XABCD: {MIN: E_1414, MAX: E_1618}
        },
        BUTTERFLY: {
            XAB: {MIN: R_786, MAX: R_786},
            ABC: {MIN: R_382, MAX: R_886},
            BCD: {MIN: E_1618, MAX: E_2618},
            XABCD: {MIN: E_1272, MAX: E_1414}
        },
        BAT: {
            XAB: {MIN: R_382, MAX: R_5},
            ABC: {MIN: R_382, MAX: R_886},
            BCD: {MIN: E_1618, MAX: E_2618},
            COMPLETION: {MIN: R_886, MAX: R_886}
        },
        ALT_BAT: {
            XAB: {MIN: R_382, MAX: R_382},
            ABC: {MIN: R_382, MAX: R_886},
            BCD: {MIN: E_2, MAX: E_3618},
            XABCD: {MIN: E_113, MAX: E_113}
        },
        GARTLEY: {
            XAB: {MIN: R_618, MAX: R_618},
            ABC: {MIN: R_382, MAX: R_886},
            BCD: {MIN: E_1272, MAX: E_1618},
            XABCD: {MIN: R_786, MAX: R_786}
        },
        BARTLEY: {
            XAB: {MIN: R_618, MAX: R_618},
            ABC: {MIN: R_382, MAX: R_886},
            BCD: {MIN: E_1272, MAX: E_2618},
            XABCD: {MIN: R_886, MAX: R_886}
        },
        CYPHER: {
            XAB: {MIN: R_382, MAX: R_618},
            XAC: {MIN: E_113, MAX: E_1414},
            BCD: {MIN: E_1272, MAX: E_2},
            XABCD: {MIN: R_786, MAX: R_786}
        },
        SHARK: {
            XAB: {MIN: R_382, MAX: R_618},
            ABC: {MIN: E_113, MAX: E_1618},
            BCD: {MIN: E_1618, MAX: E_224},
            XABCD: {MIN: R_886, MAX: R_886}
        },
        DEEP_SHARK: {
            XAB: {MIN: R_618, MAX: R_618},
            ABC: {MIN: E_113, MAX: E_1618},
            BCD: {MIN: E_1618, MAX: E_224},
            XABCD: {MIN: E_113, MAX: E_113}
        }
    },
    ABCD: {
        ABCD_382_1: {
            ABC: {MIN: R_382, MAX: R_382},
            BCD: {MIN: E_224, MAX: E_224},
            ABCD: {MIN: E_224, MAX: E_224},
        },
        ABCD_382_2: {
            ABC: {MIN: R_382, MAX: R_382},
            BCD: {MIN: E_2618, MAX: E_2618},
            ABCD: {MIN: E_2618, MAX: E_2618}
        },
        ABCD_50: {
            ABC: {MIN: R_5, MAX: R_5},
            BCD: {MIN: E_2, MAX: E_2},
            ABCD: {MIN: E_2, MAX: E_2},
        },
        ABCD_618: {
            ABC: {MIN: R_618, MAX: R_618},
            BCD: {MIN: E_1618, MAX: E_1618},
            ABCD: {MIN: E_1618, MAX: E_1618},
        },
        ABCD_707: {
            ABC: {MIN: R_707, MAX: R_707},
            BCD: {MIN: E_1414, MAX: E_1414},
            ABCD: {MIN: E_1414, MAX: E_1414},
        },
        ABCD_786: {
            ABC: {MIN: R_786, MAX: R_786},
            BCD: {MIN: E_1272, MAX: E_1272},
            ABCD: {MIN: E_1272, MAX: E_1272},
        },
        ABCD_886: {
            ABC: {MIN: R_886, MAX: R_886},
            BCD: {MIN: E_113, MAX: E_113},
            ABCD: {MIN: E_113, MAX: E_113},
        },
        # 1272 extensions
        ABCD_382_1_1272: {
            ABC: {MIN: R_382, MAX: R_382},
            BCD: {MIN: E_224 * E_1272, MAX: E_224 * E_1272},
            ABCD: {MIN: E_224 * E_1272, MAX: E_224 * E_1272},
        },
        ABCD_382_2_1272: {
            ABC: {MIN: R_382, MAX: R_382},
            BCD: {MIN: E_2618 * E_1272, MAX: E_2618 * E_1272},
            ABCD: {MIN: E_2618 * E_1272, MAX: E_2618 * E_1272},
        },
        ABCD_50_1272: {
            ABC: {MIN: R_5, MAX: R_5},
            BCD: {MIN: E_2 * E_1272, MAX: E_2 * E_1272},
            ABCD: {MIN: E_2 * E_1272, MAX: E_2 * E_1272},
        },
        ABCD_618_1272: {
            ABC: {MIN: R_618, MAX: R_618},
            BCD: {MIN: E_1618 * E_1272, MAX: E_1618 * E_1272},
            ABCD: {MIN: E_1618 * E_1272, MAX: E_1618 * E_1272},
        },
        ABCD_707_1272: {
            ABC: {MIN: R_707, MAX: R_707},
            BCD: {MIN: E_1414 * E_1272, MAX: E_1414 * E_1272},
            ABCD: {MIN: E_1414 * E_1272, MAX: E_1414 * E_1272},
        },
        ABCD_786_1272: {
            ABC: {MIN: R_786, MAX: R_786},
            BCD: {MIN: E_1272 * E_1272, MAX: E_1272 * E_1272},
            ABCD: {MIN: E_1272 * E_1272, MAX: E_1272 * E_1272},
        },
        ABCD_886_1272: {
            ABC: {MIN: R_886, MAX: R_886},
            BCD: {MIN: E_113 * E_1272, MAX: E_113 * E_1272},
            ABCD: {MIN: E_113 * E_1272, MAX: E_113 * E_1272},
        },
        # 1618 extensions
        ABCD_382_1_1618: {
            ABC: {MIN: R_382, MAX: R_382},
            BCD: {MIN: E_224 * E_1618, MAX: E_224 * E_1618},
            ABCD: {MIN: E_224 * E_1618, MAX: E_224 * E_1618},
        },
        ABCD_382_2_1618: {
            ABC: {MIN: R_382, MAX: R_382},
            BCD: {MIN: E_2618 * E_1618, MAX: E_2618 * E_1618},
            ABCD: {MIN: E_2618 * E_1618, MAX: E_2618 * E_1618},
        },
        ABCD_50_1618: {
            ABC: {MIN: R_5, MAX: R_5},
            BCD: {MIN: E_2 * E_1618, MAX: E_2 * E_1618},
            ABCD: {MIN: E_2 * E_1618, MAX: E_2 * E_1618},
        },
        ABCD_618_1618: {
            ABC: {MIN: R_618, MAX: R_618},
            BCD: {MIN: E_1618 * E_1618, MAX: E_1618 * E_1618},
            ABCD: {MIN: E_1618 * E_1618, MAX: E_1618 * E_1618},
        },
        ABCD_707_1618: {
            ABC: {MIN: R_707, MAX: R_707},
            BCD: {MIN: E_1414 * E_1618, MAX: E_1414 * E_1618},
            ABCD: {MIN: E_1414 * E_1618, MAX: E_1414 * E_1618},
        },
        ABCD_786_1618: {
            ABC: {MIN: R_786, MAX: R_786},
            BCD: {MIN: E_1272 * E_1618, MAX: E_1272 * E_1618},
            ABCD: {MIN: E_1272 * E_1618, MAX: E_1272 * E_1618},
        },
        ABCD_886_1618: {
            ABC: {MIN: R_886, MAX: R_886},
            BCD: {MIN: E_113 * E_1618, MAX: E_113 * E_1618},
            ABCD: {MIN: E_113 * E_1618, MAX: E_113 * E_1618}
        }
    },
    ABC: {
        R_382: {ABC: {MIN: R_382, MAX: R_382}},
        R_5: {ABC: {MIN: R_5, MAX: R_5}},
        R_618: {ABC: {MIN: R_618, MAX: R_618}},
        R_707: {ABC: {MIN: R_707, MAX: R_707}},
        R_786: {ABC: {MIN: R_786, MAX: R_786}},
        R_886: {ABC: {MIN: R_886, MAX: R_886}},
        E_113: {ABC: {MIN: E_113, MAX: E_113}},
        E_1272: {ABC: {MIN: E_1272, MAX: E_1272}},
        E_1414: {ABC: {MIN: E_1414, MAX: E_1414}},
        E_1618: {ABC: {MIN: E_1618, MAX: E_1618}},
        E_2: {ABC: {MIN: E_2, MAX: E_2}},
        E_2618: {ABC: {MIN: E_2618, MAX: E_2618}}
    }
}

MAX_RETRACE = {
    XAB: R_886,
    ABC: E_1618,
    BCD: E_3618
}
SCALPS = 'SCALPS'
MATRIX_PATTERNS = {
    SCALPS: {
        R_382: {MIN: R_382, MAX: R_382},
        R_5: {MIN: R_5, MAX: R_5},
        R_618: {MIN: R_618, MAX: R_618},
        R_707: {MIN: R_707, MAX: R_707},
        R_786: {MIN: R_786, MAX: R_786},
        R_886: {MIN: R_886, MAX: R_886},
        E_113: {MIN: E_113, MAX: E_113},
        E_1272: {MIN: E_1272, MAX: E_1272},
        E_1414: {MIN: E_1414, MAX: E_1414},
        E_1618: {MIN: E_1618, MAX: E_1618},
        E_2: {MIN: E_2, MAX: E_2},
        E_2618: {MIN: E_2618, MAX: E_2618}
    },
    XAB: {
        BAT: {MIN: R_382, MAX: R_5},
        ALT_BAT: {MIN: R_382, MAX: R_382},
        CRAB: {MIN: R_382, MAX: R_618},
        SHARK: {MIN: R_382, MAX: R_618},
        DEEP_SHARK: {MIN: R_382, MAX: R_618},
        DEEP_CRAB: {MIN: R_886, MAX: R_886},
        DEEP_BUTTERFLY: {MIN: R_886, MAX: R_886},
        GARTLEY: {MIN: R_618, MAX: R_618},
        BUTTERFLY: {MIN: R_786, MAX: R_786},
        CYPHER: {MIN: R_786, MAX: R_786},
    },
    DOUBLE: {1: {MIN: 1, MAX: 1}},
    ABC: {
        ABCD_382_1: {MIN: R_382, MAX: R_382},
        ABCD_382_2: {MIN: R_382, MAX: R_382},
        ABCD_50: {MIN: R_5, MAX: R_5},
        ABCD_618: {MIN: R_618, MAX: R_618},
        ABCD_707: {MIN: R_707, MAX: R_707},
        ABCD_786: {MIN: R_786, MAX: R_786},
        ABCD_886: {MIN: R_886, MAX: R_886},
        ABCD_382_1_1272: {MIN: R_382, MAX: R_382},
        ABCD_382_2_1272: {MIN: R_382, MAX: R_382},
        ABCD_50_1272: {MIN: R_5, MAX: R_5},
        ABCD_618_1272: {MIN: R_618, MAX: R_618},
        ABCD_707_1272: {MIN: R_707, MAX: R_707},
        ABCD_786_1272: {MIN: R_786, MAX: R_786},
        ABCD_886_1272: {MIN: R_886, MAX: R_886},
        ABCD_382_1_1618: {MIN: R_382, MAX: R_382},
        ABCD_382_2_1618: {MIN: R_382, MAX: R_382},
        ABCD_50_1618: {MIN: R_5, MAX: R_5},
        ABCD_618_1618: {MIN: R_618, MAX: R_618},
        ABCD_707_1618: {MIN: R_707, MAX: R_707},
        ABCD_786_1618: {MIN: R_786, MAX: R_786},
        ABCD_886_1618: {MIN: R_886, MAX: R_886},
        BAT: {MIN: R_382, MAX: R_886},
        ALT_BAT: {MIN: R_382, MAX: R_886},
        CRAB: {MIN: R_382, MAX: R_886},
        DEEP_CRAB: {MIN: R_382, MAX: R_886},
        DEEP_BUTTERFLY: {MIN: R_786, MAX: R_786},
        GARTLEY: {MIN: R_382, MAX: R_886},
        BUTTERFLY: {MIN: R_382, MAX: R_886},
        CYPHER: {MIN: E_1272, MAX: E_1414},
        DEEP_SHARK: {MIN: E_113, MAX: E_1618},
        SHARK: {MIN: E_113, MAX: E_1618},
    },
    BCD: {
        CRAB: {MIN: E_2618, MAX: E_3618},
        DEEP_CRAB: {MIN: E_2227, MAX: E_3618},
        DEEP_BUTTERFLY: {MIN: E_1618, MAX: E_2618},
        BUTTERFLY: {MIN: E_1618, MAX: E_2618},
        BAT: {MIN: E_1618, MAX: E_2618},
        ALT_BAT: {MIN: E_2, MAX: E_3618},
        GARTLEY: {MIN: E_1272, MAX: E_1618},
        BARTLEY: {MIN: E_1272, MAX: E_2618},
        CYPHER: {MIN: E_1272, MAX: E_2},
        SHARK: {MIN: E_1618, MAX: E_224},
        DEEP_SHARK: {MIN: E_1618, MAX: E_224},
    },
    ABCD: {
        # ABCD straight
        ABCD_382_1: {MIN: E_224, MAX: E_224},
        ABCD_382_2: {MIN: E_2618, MAX: E_2618},
        ABCD_50: {MIN: E_2, MAX: E_2},
        ABCD_618: {MIN: E_1618, MAX: E_1618},
        ABCD_707: {MIN: E_1414, MAX: E_1414},
        ABCD_786: {MIN: E_1272, MAX: E_1272},
        ABCD_886: {MIN: E_113, MAX: E_113},
        # ABCD 1272 extension
        ABCD_382_1_1272: {MIN: E_224 * E_1272, MAX: E_224 * E_1272},
        ABCD_382_2_1272: {MIN: E_2618 * E_1272, MAX: E_2618 * E_1272},
        ABCD_50_1272: {MIN: E_2 * E_1272, MAX: E_2 * E_1272},
        ABCD_618_1272: {MIN: E_1618 * E_1272, MAX: E_1618 * E_1272},
        ABCD_707_1272: {MIN: E_1414 * E_1272, MAX: E_1414 * E_1272},
        ABCD_786_1272: {MIN: E_1272 * E_1272, MAX: E_1272 * E_1272},
        ABCD_886_1272: {MIN: E_113 * E_1272, MAX: E_113 * E_1272},
        # ABCD 1618 extension
        ABCD_382_1_1618: {MIN: E_224 * E_1618, MAX: E_224 * E_1618},
        ABCD_382_2_1618: {MIN: E_2618 * E_1618, MAX: E_2618 * E_1618},
        ABCD_50_1618: {MIN: E_2 * E_1618, MAX: E_2 * E_1618},
        ABCD_618_1618: {MIN: E_1618 * E_1618, MAX: E_1618 * E_1618},
        ABCD_707_1618: {MIN: E_1414 * E_1618, MAX: E_1414 * E_1618},
        ABCD_786_1618: {MIN: E_1272 * E_1618, MAX: E_1272 * E_1618},
        ABCD_886_1618: {MIN: E_113 * E_1618, MAX: E_113 * E_1618},
    },
    XABCD: {
        CRAB: {MIN: E_1618, MAX: E_1618},
        DEEP_CRAB: {MIN: E_1618, MAX: E_1618},
        DEEP_BUTTERFLY: {MIN: E_1414, MAX: E_1618},
        BUTTERFLY: {MIN: E_1272, MAX: E_1414},
        BAT: {MIN: R_886, MAX: R_886},
        ALT_BAT: {MIN: E_113, MAX: E_113},
        GARTLEY: {MIN: R_786, MAX: R_786},
        BARTLEY: {MIN: R_886, MAX: R_886},
        CYPHER: {MIN: R_786, MAX: R_786},
        SHARK: {MIN: R_886, MAX: R_886},
        DEEP_SHARK: {MIN: E_113, MAX: E_113},
    }
}
