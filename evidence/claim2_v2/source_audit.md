# Source audit

Primary anchors are `body.tex:lem:control_solution_poisson` and `appendix.tex:sec:subsection_controlling`, with Paulin's pseudo-spectral-gap definition and total-variation inequality. The cited inequality is stated for `n>=1`, although the source applies it to a sum beginning at `n=0`. This audit repairs that proof gap explicitly: the zeroth row has norm `2(1-pi_x)`, which is no larger than the source envelope, and Paulin is then summed only from one. The repair does not change the proposition or its constant.
