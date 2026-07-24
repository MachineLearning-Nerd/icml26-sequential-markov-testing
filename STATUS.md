# Status

- Paper: arXiv 2602.17587; source SHA-256
  `2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8`.
- Live judge: 5/12 at Hugging Face revision
  `66d5e67b5426622768e4d797656e409526f3a299`, judged
  `2026-07-23T16:36:19+00:00`.
- Scientific winner: `orx/corrected-paper-scale-application-evidence`,
  commit `69eb2f484b32ab603f856fd0fcdee1fd960fb4ba`, run
  `0a874377-72e3-48af-9134-d75c4d509b10`.
- Local result: six source-pinned claim contracts VERIFIED; this is not a
  predicted judge score.
- Compute: local Apple M2 CPU, 18m12s accepted wall time, $0 paid cost.
- Diagnosis: the published Space contained the faithful raw outputs but omitted
  the Python that generated them, so the judge relied on archived SPRT snippets.
- Repair publication: final Hugging Face revision
  `a3b49a603d3777270e8e1cd11eb312f4e92efbe2`, containing 109 files and
  preserving all 99 paths from the 5/12 revision. The Space-root verifier
  independently returns VERIFIED for C1–C6.
- Publication state: `PUBLISHED_AWAITING_JUDGE`. The last live score remains
  5/12 until a new verdict is produced.
