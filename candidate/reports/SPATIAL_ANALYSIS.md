# Geographic robustness

At 200 shots/class, saved audits use a 10-lattice-key buffer and 10 episodes in each of four directions. All methods share direction/trial support and query sets. [Matched gains](../tables/spatial_matched_control.md) use those keys. The random-pixel control has the same budget and development exclusion, but a different query geography; it is not an exact matched spatial control.

Coordinate_RF: x-half 0.682326, y-half 0.706106, worst direction 0.644816, four-direction mean 0.694216. ASTRA: 0.687017, 0.706326, 0.658183, 0.696672 respectively. Coordinate_RF loses about 0.028670 on high-x → low-x. Random-pixel gains therefore coexist with worse geographic extrapolation. Coordinates can exploit local structure without guaranteeing transfer beyond observed support regions. No model selection or changes followed this audit. New cities and geographically blocked organizer tests remain necessary.
