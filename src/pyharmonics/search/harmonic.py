__author__ = 'github.com/niall-oc'

from pyharmonics import utils
from pyharmonics import constants
from pyharmonics.patterns import ABCDPattern, ABCPattern, XABCDPattern

class HarmonicSearch:
    """
    HarmonicSearch is a class for searching for harmonic patterns in technical data.
    """
    XABCD = 'XABCD'
    ABCD = 'ABCD'
    ABC = 'ABC'
    PEAK = -1

    def __init__(self, technicals, patterns=None, fib_tolerance=0.03, check_anchor=True):
        """
        Constructor for HarmonicSearch.

        >>> h = HarmonicSearch(technicals)
        >>> h = HarmonicSearch(technicals, patterns=constants.MATRIX_PATTERNS, fib_tolerance=0.03, check_anchor=True)

        :param pyharmonics.technicals.OHLCTechnicals technicals: An instance of OHLCTechnicals.
        :param dict patterns: The patterns to search for.
        :param float fib_tolerance: The tolerance for fibonacci retraces.
        :param bool check_anchor: Check for false anchors.
            False anchors are peaks that aren't the maximum or minimum in a trend.
        """
        self._formed = {self.XABCD: [], self.ABCD: [], self.ABC: []}
        self._forming = {self.XABCD: [], self.ABCD: [], self.ABC: []}
        self.PATTERNS = utils.get_pattern_definition(fib_tolerance, patterns or constants.MATRIX_PATTERNS)
        self.td = technicals
        self.check_anchor = check_anchor
        self._build_fib_matrix()

    def get_patterns(self, family=None, formed=True):
        """
        Return the formed or forming patterns.

        >>> h.get_patterns()
        >>> h.get_patterns(family=h.XABCD)
        >>> h.get_patterns(family=h.ABCD, formed=False)

        :param str family: The family of patterns to return.
        :param bool formed: True if the formed patterns are to be returned.
        :return: The formed or forming patterns.
        """
        group = self._formed
        if not formed:
            group = self._forming

        if family:
            group = {family: group[family]}
        return group

    def _build_fib_matrix(self):
        """
        Builds a matrix of retraces from the peak data.

        Iterate over each peak or dip in the data.
        From that peak or dip calculate all retraces that occur going forward.
        """
        MAX = len(self.td.peak_type)
        matrix = [[None] * MAX for i in range(MAX)]
        for i in range(MAX):
            # For each peak point as a starting point.
            if self.td.peak_type[i] == 0:  # for a bull pattern a dip is a starting point
                # Build from low
                self._build_from_low(matrix, i)
            else:
                # Build from high
                self._build_from_high(matrix, i)
        self.fib_matrix = matrix
        self.MATRIX_LEN = len(self.fib_matrix)

    def _build_from_low(self, matrix, index):
        """
        From a low point ( price low ) calculate all retraces going forward.
        """
        MAX_LEN = len(self.td.peak_data)
        row = matrix[index]
        _, start_price, _ = self.td.peak_data[index]
        max_price = 0.0
        move = 0.00000000001
        min_price = 1000000000
        no_retraces_remain = False
        for i in range(index + 1, MAX_LEN):
            _, this_price, is_high = self.td.peak_data[i]
            max_price = max(max_price, this_price)
            min_price = min(min_price, this_price)
            row[i] = False
            if no_retraces_remain or this_price == max_price and min_price < start_price:
                # no more retraces
                no_retraces_remain = True
            elif this_price == max_price and is_high and min_price > start_price:
                # This is the new highest price
                row[i] = self.PEAK
                min_price = this_price
                move = abs(max_price - start_price)
            elif this_price == min_price and not is_high:
                # this_price is the the min_price after the move peak.
                # retraces from a low must be another low is_high must be false.
                retrace = (max_price - this_price) / move
                if retrace >= constants.R_382:
                    row[i] = retrace
            else:
                pass
        return matrix

    def _build_from_high(self, matrix, index):
        """
        From a high point ( price high ) calculate all retraces going forward.
        """
        MAX = len(self.td.peak_data)
        row = matrix[index]
        _, start_price, _ = self.td.peak_data[index]
        max_price = 0.0
        move = 0.00000000001
        min_price = 100000000
        no_retraces_remain = False
        for i in range(index + 1, MAX):
            _, this_price, is_high = self.td.peak_data[i]
            min_price = min(min_price, this_price)
            max_price = max(max_price, this_price)
            row[i] = False
            if no_retraces_remain or this_price == min_price and max_price > start_price:
                # no more retraces
                no_retraces_remain = True
            elif this_price == min_price and not is_high and max_price < start_price:
                # This is the new lowest price
                row[i] = self.PEAK
                max_price = this_price
                move = start_price - min_price
            elif this_price == max_price and is_high:
                # this_price is the the max_price after the move dip.
                # retraces from a peak must be another peak is_high must be true.
                retrace = abs((this_price - min_price) / move)
                if retrace >= constants.R_382:
                    row[i] = retrace
            else:
                pass
        return matrix

    def _search_retraces(self, retrace, stage):
        """
        Search for patterns that fit a retrace.

        >>> self.search_retraces(0.618, constants.ABC)
        >>> {'crab', 'gartley', 'shark', 'deep-shark'}
        Because that retrace on an ABC supports those patterns.

        :param float retrace: The retrace to search for.
        :param str stage: The stage of the pattern.
        :return: The patterns that fit the retrace.
        """
        return set([
            pattern
            for pattern, retraces in self.PATTERNS[stage].items()
            if retrace >= retraces[constants.MIN] and ((retrace == constants.ABCD or retrace == constants.XABCD) or retrace <= retraces[constants.MAX])
        ])

    def _search_candle(self, candle_idx, stage, filter_by=None):
        """
        Consider the current candle to be the D point at the end of a pattern.
        Look back at the previous candles to see which start points could be the X, A, B or C points of a pattern.

        >>> self._search_candle(100, constants.XCD)

        :param int candle_idx: The index of the candle to search.
        :param str stage: The stage of the pattern to search for.
        :param set filter_by: The patterns to filter by.
        :return: The patterns that fit the retrace.
        """
        harmonics = {}
        filter_by = filter_by or set()
        # Extract every retrace that lands on this candle, don't go past None.
        candle = self._get_candle_retraces(candle_idx)
        for idx in range(len(candle)):
            # For each row index in this candle
            # If the retrace is above the minimum 382 or False
            if candle[idx] >= constants.R_382:

                # Mark the peak from None to this retrace
                leg = self.fib_matrix[idx]
                peak_idx = candle_idx - 1
                while peak_idx > idx and leg[peak_idx] > self.PEAK:
                    peak_idx -= 1

                # Search fro any patterns that fit with this retrace
                patterns = self._search_retraces(candle[idx], stage)
                # If we are trying to match these patterns to other forming patterns
                if filter_by:
                    patterns = patterns & filter_by
                # Add this formation to the set.
                if stage == constants.ABCD or stage == constants.XABCD:
                    patterns = {
                        p for p in patterns
                        if max(leg[peak_idx + 1:candle_idx] + [0]) < constants.MATRIX_PATTERNS[stage][p][constants.MAX]
                    }
                if patterns:
                    harmonics[(idx, peak_idx, candle_idx,)] = patterns
        return harmonics

    def _get_candle_retraces(self, candle_idx):
        """
        Extract all retraces that land on this candle.
        """
        return [r[candle_idx] for r in self.fib_matrix if r[candle_idx] is not None]

    def _merge_patterns(self, patterns):
        """
        Merge all patterns into a single set.
        """
        results = set()
        for p in patterns.values():
            results = results | p
        return results

    def search(self, limit_to=-1):
        """
        Search for harmonic patterns in the technical data. These are fully formed patterns.

        >>> h = HarmonicSearch(t)

        Search all peaks for patterns
        >>> h.search()

        Search for patterns that complete within the most recent 3 peaks
        >>> h.search(limit_to=3)

        :param int limit_to: Limit to patterns that completed in the last n candles. ( This speeds up the search )
            Should be a positive integer.  Negative values search teh entire space.
        """
        self._formed = {constants.XABCD: [], constants.ABCD: [], constants.ABC: []}
        if limit_to > -1:
            limit_to = max(2, self.MATRIX_LEN - limit_to) - 1

        # First locate all retraces that could be completion points for A Harmonic/ABCD pattern
        for D_idx in range(self.MATRIX_LEN - 1, limit_to, -1):
            # Gather all valid cells ( upper right triangle of matrix)
            # Search for BCD patterns that also complete on this candle.
            # this gives both the X to d, and the bcd within that x to d
            self._formed[self.XABCD] += self._find_xabcd(D_idx)
            self._formed[self.ABCD] += self._find_abcd(D_idx)
            self._formed[self.ABC] += self._find_abc(D_idx)

    def _find_abc(self, C_idx):
        """
        From this candles perspective. What ABC retraces complete here.

        >>> self._find_abc(100)

        :param int C_idx: The index of the candle to search.
        :return: The patterns that fit the retrace.
        """
        found = []
        abcs = self._search_candle(C_idx, constants.SCALPS)

        for pattern_indexes, patterns in abcs.items():
            A, B, C = pattern_indexes
            for p in patterns:
                if self._is_anchor_valid(A, B):
                    found.append(
                        self._create_abc_pattern(A, B, C, p)
                    )
        return found

    def _find_abcd(self, D_idx):
        """
        Given the set of BCD retraces that complete at this candle, is the following possible
        1. Using the C point of each retrace, is there an ABC retrace that fits
        2. Does the over all ABCD fit?

        >>> self._find_abcd(100)

        :param int D_idx: The index of the candle to search.
        :return: The patterns that fit the retrace.
        """
        found = []
        abcds = self._search_candle(D_idx, constants.ABCD)

        for b_key, abcd_patterns in abcds.items():
            # Locate C point
            B_idx, C_idx, _ = b_key
            # From the point of C how many ABC retraces fit
            abcs = self._search_candle(C_idx, constants.ABC, filter_by=abcd_patterns & constants.ABCDS)
            for a_key, abc_patterns in abcs.items():
                # Extract the A point and potential b point
                A_idx, b_idx, _ = a_key
                # If the b points intersect
                if b_idx == B_idx:
                    # Confirmation ---
                    # THere exists a BCD retrace where
                    # A valid ABC intersects with B and C
                    # The intersection of the ABC and BCD candidates is a valid ABCD pattern
                    patterns = abc_patterns & abcd_patterns
                    for p in patterns:
                        if self._is_anchor_valid(A_idx, B_idx):
                            found.append(self._create_abcd_pattern(A_idx, B_idx, C_idx, D_idx, p))
        return found

    def _find_xabcd(self, D_idx):
        """
        Given the set of BCD retraces that complete at this candle, is the following possible
        1. Scan the same candle for X, A or C, D retraces that are consistent with harmonic patterns.
        2. Scan for XAB retraces, the first component of a pattern
        3. for every B in the BCD set, is there an XAB where the B component of both are the same.
        4. Is there an ABC retrace present and all together does this make a pattern?

        >>> self._find_xabcd(100)

        :param int D_idx: The index of the candle to search.
        :return: The patterns that fit the retrace.
        """
        found = []

        # From D find all X, ??, D retraces that are harmonic XABCD pattern candidates
        xds = self._search_candle(D_idx, constants.XABCD)

        # For all candidates
        for x_key, xd_patterns in xds.items():
            # Capture the X and peak point
            X_idx, peak_idx, _ = x_key
            # Consider all of the BCD candidates
            bcds = self._search_candle(D_idx, constants.BCD)
            for b_key, bcd_patterns in bcds.items():
                # Capture the B and C points
                B_idx, C_idx, _ = b_key
                # Finally find all ABC candidates that intersect with point C
                abcs = self._search_candle(C_idx, constants.ABC, filter_by=bcd_patterns)
                # Iterate over the ABC cancidates
                for a_key, abc_patterns in abcs.items():
                    # Capture the A index and the potential B index
                    A_idx, b_idx, _ = a_key
                    # If the ABC retrace shares the same B point as the BCD retrace we have a valid ABCD retrace.
                    # In addition if the A or C point are a match with the peak_index we potentially have a Harmonic pattern
                    if b_idx == B_idx and (peak_idx == C_idx or peak_idx == A_idx):
                        # Finally look for XAB retraces that land on our confirmed B point
                        xabs = self._search_candle(B_idx, constants.XAB, filter_by=bcd_patterns)
                        # iterate through all candidates
                        for xa_key, xab_patterns in xabs.items():
                            # Extract out potential x and a points.
                            x_idx, a_idx, _ = xa_key

                            # If the XAB x point matchs with the X?D retrace x point,
                            # AND the a point matches the ABC retrace A point
                            if X_idx == x_idx and A_idx == a_idx:  # pattern potential
                                # Confirmation---
                                # There exists an X?D retrace where
                                # there is a valid BCD that intersects with D
                                # there is a valid ABC that intersects with B and C
                                # Either A or C matches with the peak index, the ? in X?D
                                # there is a valid XAB that intersects with X, A and B
                                # Therefore the pattern common between all retraces is a harmonic
                                patterns = xab_patterns & abc_patterns & bcd_patterns & xd_patterns
                                for p in patterns:
                                    if self._is_anchor_valid(X_idx, A_idx):
                                        found.append(self._create_xabcd_pattern(X_idx, A_idx, B_idx, C_idx, D_idx, p))
        return found

    def forming(self, limit_to=-1, percent_c_to_d=0.8):
        """
        Search for forming harmonic patterns in the technical data.
        These are different from completed patterns in that they are still forming and may not complete.

        >>> h = HarmonicSearch(t)
        >>> h.forming()
        >>> h.get_patterns(formed=False)

        :param int limit_to: Limits to patterns that whos CD leg is projected to form in the last n candles.
        :param float percent_c_to_d: The percentage of the pattern that must be
            complete from C to D. .8 means patterns that are 80% formed. .95 would produce
            fewer results as teh patterns would have to reach 95% completion.
        """
        self._forming = {constants.XABCD: [], constants.ABCD: [], constants.ABC: []}
        if limit_to > -1:
            limit_to = max(2, self.MATRIX_LEN - limit_to)

        # First locate all retraces that could be completion points for A Harmonic/ABCD pattern
        for D_idx in range(self.MATRIX_LEN - 1, limit_to - 1, -1):
            # Gather all valid cells ( upper right triangle of matrix)
            # Find X to D retraces that fit harmonic patterns.
            baams = self._bat_action_magnet_move(D_idx)
            for points, bcd_patterns in baams.items():
                B_idx, C_idx, D_idx = points
                # Locate ABC patterns who share this B and C point
                abcs = self._search_candle(C_idx, constants.ABC)
                for a_key, abc_patterns in abcs.items():
                    # A point
                    A_idx, b_idx, _ = a_key
                    abcd_patterns = abc_patterns & constants.ABCDS
                    if abcd_patterns and b_idx == B_idx:  # Is it a pattern and is it sharing the B point
                        for ap in abcd_patterns:
                            if self.fib_matrix[B_idx][D_idx] >= self.PATTERNS[constants.ABCD][ap][constants.MIN] * percent_c_to_d and \
                               self.fib_matrix[B_idx][D_idx] <= self.PATTERNS[constants.ABCD][ap][constants.MIN]:
                                if self._is_anchor_valid(A_idx, B_idx):
                                    self._forming[constants.ABCD].append(self._create_abcd_pattern(A_idx, B_idx, C_idx, D_idx, ap, formed=False))

                        xabs = self._search_candle(B_idx, constants.XAB)
                        for x_key, xab_patterns in xabs.items():
                            # If the XAB retraces X index is the same x index in the xd retrace that the bcd retrace intersects with
                            # then we have a pattern and need to finally locate the a and c points.
                            X_idx, A_idx, b_idx = x_key
                            xabcd_patterns = xab_patterns & abc_patterns & constants.XABCDS
                            for xp in xabcd_patterns:
                                # the pattern cannot have over shot the min completion zone
                                if self.fib_matrix[X_idx][D_idx] >= self.PATTERNS[constants.XABCD][xp][constants.MIN] * percent_c_to_d and\
                                   self.fib_matrix[X_idx][D_idx] <= self.PATTERNS[constants.XABCD][xp][constants.MIN]:
                                    if self._is_anchor_valid(X_idx, A_idx):
                                        self._forming[constants.XABCD].append(self._create_xabcd_pattern(X_idx, A_idx, B_idx, C_idx, D_idx, xp, formed=False))

    def _is_anchor_valid(self, anchor_idx, peak_idx, retrace_limit=constants.R_382):
        """
        Check if the anchor is a false anchor. A false anchor is a peak that is not the maximum or minimum in a trend.

        >>> self._false_anchor(100, 200)

        :param int anchor_idx: The index of the anchor.
        :param int peak_idx: The index of the peak.
        :param float retrace_limit: If a retrace greater than this limit is detected around the anchor it is valid.
        :return: True if the anchor is a valid anchor.
        """
        if not self.check_anchor:
            return True
        _, start_price, start_is_high = self.td.peak_data[anchor_idx]
        _, peak_price, _ = self.td.peak_data[peak_idx]
        move = abs(peak_price - start_price)

        for idx in range(anchor_idx - 1, -1, -1):
            _, this_price, this_is_high = self.td.peak_data[idx]
            # If this point type is the opposite of the anchor point type
            # ie. the anchor is a high and this is a low or vice versa
            if start_is_high != this_is_high:
                retrace_move = abs(start_price - this_price)
                if retrace_move:  # a zero here would indicate a double top.
                    retrace = retrace_move / move
                    if retrace >= retrace_limit:
                        # This is a valid anchor and valid pattern
                        return True
            elif (start_is_high and this_price > start_price) or\
                 (not start_is_high and this_price < start_price):
                # the previous peak is the true anchor and not this anchor.
                return False
        # In the absence of a retrace this is still the lowest anchor point.
        return True

    def _create_abc_pattern(self, A_idx, B_idx, C_idx, pattern):
        """
        """
        x, y = self.td.get_pattern_x_y([A_idx, B_idx, C_idx])
        x = self.td.get_index_x(x)
        p = ABCPattern(
            self.td.symbol,
            self.td.interval,
            x=x, y=y,
            name=pattern,
            retraces={constants.ABC: self.fib_matrix[A_idx][C_idx]},
            formed=True,
            bullish=bool(y[-2] > y[-1])
        )
        return p

    def _create_abcd_pattern(self, A_idx, B_idx, C_idx, D_idx, pattern, formed=True):
        """
        """
        pattern_indxes = [A_idx, B_idx, C_idx, D_idx]
        retraces = {
            constants.ABC: self.fib_matrix[A_idx][C_idx],
            constants.BCD: self.fib_matrix[B_idx][D_idx],
            constants.ABCD: self.fib_matrix[B_idx][D_idx]
        }
        x, y = self.td.get_pattern_x_y(pattern_indxes)
        x = self.td.get_index_x(x)
        # print(f'pattern {pattern}, type {type(pattern)}')
        p = ABCDPattern(
            self.td.symbol,
            self.td.interval,
            x=x, y=y,
            name=pattern,
            retraces=retraces,
            formed=formed,
            bullish=bool(y[-2] > y[-1])
        )
        return p

    def _create_xabcd_pattern(self, X_idx, A_idx, B_idx, C_idx, D_idx, pattern, formed=True):
        """
        """
        # Save the pattern
        pattern_indxes = [X_idx, A_idx, B_idx, C_idx, D_idx]
        retraces = {
            constants.XAB: self.fib_matrix[X_idx][B_idx],
            constants.ABC: self.fib_matrix[A_idx][C_idx],
            constants.BCD: self.fib_matrix[B_idx][D_idx],
            constants.XABCD: self.fib_matrix[X_idx][D_idx]
        }
        x, y = self.td.get_pattern_x_y(pattern_indxes)
        x = self.td.get_index_x(x)
        p = XABCDPattern(
            self.td.symbol,
            self.td.interval,
            x=x, y=y,
            name=pattern,
            retraces=retraces,
            formed=formed,
            bullish=bool(y[-2] > y[-1])
        )
        return p

    def _bat_action_magnet_move(self, candle_idx):
        """
        An ABCD or XABCD pattern is likely to complete when
            - the ABC component has completed and a reaction has occured
            - The reaction has passed the b point
        """
        harmonics = {}
        # Considering this candle as the present any retrace greater than 1.0
        # is a Bat action magnet move. Ie a reaction at C that will go past B and complete at D
        candle = self._get_candle_retraces(candle_idx)
        # Looking through every retrace that has occured at this point
        for idx in range(len(candle)):
            if candle[idx] >= constants.E_113:  # consider only retraces deeper than 113
                # look at all ABC retraces that latch on to this b point.
                leg = self.fib_matrix[idx]
                b_idx = candle_idx - 1
                while b_idx > idx and leg[b_idx] > self.PEAK:
                    b_idx -= 1
                harmonics[(idx, b_idx, candle_idx,)] = constants.XABCDS | constants.ABCDS
        return harmonics

if __name__ == '__main__':
    from pyharmonics.marketdata import BinanceCandleData
    from pyharmonics.search import DivergenceSearch
    from pyharmonics import OHLCTechnicals
    from pyharmonics.plotter import HarmonicPlotter
    import datetime

    present = int(datetime.datetime.now().timestamp() * 1000)

    b = BinanceCandleData()
    b.get_candles('BTCUSDT', b.HOUR_1, 1000)
    t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=10)
    h = HarmonicSearch(t, fib_tolerance=0.03, strict=True)
    h.search()
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search()
    p.add_peaks()
    p.add_harmonic_plots(h.get_patterns(family=h.XABCD))
    p.add_divergence_plots(d.get_patterns())
    p.show()
